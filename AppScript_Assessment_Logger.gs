// KeyPlayers VA Academy — Assessment Results Logger
// Spreadsheet: https://docs.google.com/spreadsheets/d/1Tl7HU4eKpLf3sTyIndUx9lLAM-vhJxwVo3advwKBw7M
//
// DEPLOY INSTRUCTIONS:
// 1. Open the spreadsheet → Extensions → Apps Script
// 2. Delete any existing code, paste this entire file
// 3. Project Settings (gear) → Script properties, add:
//      ASSESSMENT_ALERT_WEBHOOK_URL = (the Slack Incoming Webhook URL for #<channel C0B5X7MS6UA>)
// 4. Click Deploy → New deployment → Web app
//    - Execute as: Me
//    - Who has access: Anyone
// 5. Copy the deployment URL and paste it into Day10_Assessment.html → CONFIG.SHEET_URL
//
// FAILSAFE (added 2026-07-19): if the sheet write can't complete — lock contention,
// a malformed payload, anything — this posts the student's name, PASS/FAIL, full
// score breakdown, and the raw answers JSON straight to Slack, so a result is never
// silently lost even if the row never lands in the sheet.

var SHEET_ID = '1Tl7HU4eKpLf3sTyIndUx9lLAM-vhJxwVo3advwKBw7M';
var SHEET_NAME = 'Results';
var LOCK_WAIT_MS = 20000;

var HEADERS = [
  'Timestamp',
  'Name',
  'Score %',
  'Pass / Fail',
  'Section A — MCQ (/22)',
  'Section B — Situational (/10)',
  'Section C — Sequencing (/5)',
  'Total (/37)',
  'Answers (JSON)'
];

function doPost(e) {
  var raw = e.postData ? e.postData.contents : '{}';
  var data;
  try {
    data = JSON.parse(raw);
  } catch (err) {
    slackAssessmentAlert_(null, err, raw);
    return json_({ ok: false, error: String(err) });
  }

  var lock = LockService.getScriptLock();
  var gotLock = false;
  try {
    gotLock = lock.tryLock(LOCK_WAIT_MS);
    if (!gotLock) {
      slackAssessmentAlert_(data, 'Could not acquire sheet lock within ' + (LOCK_WAIT_MS / 1000) + 's — write skipped', raw);
      return json_({ ok: false, error: 'lock timeout' });
    }

    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
    }

    // Write headers if the sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.getRange(1, 1, 1, HEADERS.length)
        .setFontWeight('bold')
        .setBackground('#0d3321')
        .setFontColor('#ffffff');
      sheet.setFrozenRows(1);
    }

    var row = [
      new Date(data.ts || new Date()),
      data.name   || '(unknown)',
      data.pct    || 0,
      data.pass   ? 'PASS' : 'FAIL',
      data.mcq    || 0,
      data.sit    || 0,
      data.seq    || 0,
      data.total  || 0,
      JSON.stringify(data.answers || {})
    ];

    sheet.appendRow(row);

    // Colour the row green (pass) or red (fail)
    var lastRow = sheet.getLastRow();
    var color = data.pass ? '#d4edda' : '#f8d7da';
    sheet.getRange(lastRow, 1, 1, HEADERS.length).setBackground(color);

    return json_({ ok: true });

  } catch (err) {
    slackAssessmentAlert_(data, err, raw);
    return json_({ ok: false, error: String(err) });
  } finally {
    if (gotLock) lock.releaseLock();
  }
}

// Posts a failure alert to Slack with everything needed to manually recover the
// result: name, pass/fail, score breakdown, the reason it failed, and the raw
// payload. `data` may be null if the payload didn't even parse as JSON.
function slackAssessmentAlert_(data, reason, rawBody) {
  var url = PropertiesService.getScriptProperties().getProperty('ASSESSMENT_ALERT_WEBHOOK_URL');
  if (!url) return; // nothing we can do if no webhook is configured

  var resultLine = data && typeof data.pass !== 'undefined'
    ? (data.pass ? '✅ PASSED' : '❌ FAILED')
    : '(result unknown — payload may be malformed)';

  var lines = [
    '🚨 *[Assessment Logger] Sheet write failed*',
    '*Name:* ' + (data && data.name ? data.name : '(unknown)'),
    '*Result:* ' + resultLine
  ];

  if (data) {
    lines.push('*Score:* ' + (data.pct || 0) + '%  (Total ' + (data.total || 0) + '/37 — MCQ ' +
      (data.mcq || 0) + '/22, Situational ' + (data.sit || 0) + '/10, Sequencing ' + (data.seq || 0) + '/5)');
  }

  lines.push('*Reason:* ' + String(reason));
  lines.push('*Raw payload:*\n```' + String(rawBody).slice(0, 2500) + '```');

  try {
    UrlFetchApp.fetch(url, {
      method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      payload: JSON.stringify({ text: lines.join('\n') })
    });
  } catch (e) { /* last resort: cannot report a failure of the failure reporter */ }
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// Optional: test by running this manually in Apps Script
function testPost() {
  var fake = {
    postData: {
      contents: JSON.stringify({
        name: 'Test VA',
        pct: 87,
        pass: true,
        mcq: 20,
        sit: 4,
        seq: 4,
        total: 28,
        ts: new Date().toISOString(),
        answers: { '1': 1, '2': 0, '3': 2 }
      })
    }
  };
  var result = doPost(fake);
  Logger.log(result.getContent());
}

// Optional: test the failure-alert path manually (does NOT touch the sheet).
// Run this, then check Slack channel C0B5X7MS6UA for the test message.
function testAssessmentAlert() {
  slackAssessmentAlert_(
    { name: 'Test VA (alert check)', pct: 42, pass: false, mcq: 8, sit: 2, seq: 1, total: 11, answers: { '1': 0 } },
    'Manual test of the failure alert — safe to ignore',
    '{"name":"Test VA (alert check)"}'
  );
}

// DIAGNOSTIC — run this manually, then View > Logs (or the "Execution log" button)
// to see exactly why the Slack post is/isn't landing: whether the script property
// was saved, and what Slack's own API said back (HTTP status + response body).
function kpDiagnoseAssessment() {
  var url = PropertiesService.getScriptProperties().getProperty('ASSESSMENT_ALERT_WEBHOOK_URL');
  Logger.log('ASSESSMENT_ALERT_WEBHOOK_URL found: ' + (url ? 'YES (' + url.slice(0, 40) + '...)' : 'MISSING'));
  if (!url) return;
  try {
    var res = UrlFetchApp.fetch(url, {
      method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      payload: JSON.stringify({ text: 'kpDiagnoseAssessment test ping — ' + new Date() })
    });
    Logger.log('HTTP status: ' + res.getResponseCode());
    Logger.log('Response body: ' + res.getContentText());
  } catch (err) {
    Logger.log('UrlFetchApp threw: ' + err);
  }
}

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

OUTPUT = r'C:\Users\jervi\OneDrive\Documents\Claude\Projects\KP AI TRAINING\github-push\Presenter-Guide-Make-ActivePieces.pdf'

doc = SimpleDocTemplate(
    OUTPUT, pagesize=letter,
    rightMargin=0.8*inch, leftMargin=0.8*inch,
    topMargin=0.85*inch, bottomMargin=0.85*inch
)

DARK_GREEN  = colors.HexColor('#1A4A2A')
MID_GREEN   = colors.HexColor('#2A6636')
ACCENT      = colors.HexColor('#4A9B5A')
LIGHT_GREEN = colors.HexColor('#E8F5EA')
GOLD_BG     = colors.HexColor('#FDF8ED')
GOLD_BORDER = colors.HexColor('#C9A84C')
GRAY_TEXT   = colors.HexColor('#333333')
MED_GRAY    = colors.HexColor('#666666')
LIGHT_GRAY  = colors.HexColor('#F5F5F5')
SCREEN_BG   = colors.HexColor('#0D1B12')
SCREEN_TXT  = colors.HexColor('#6DB87A')
MAKE_BG     = colors.HexColor('#1A3A4A')
AP_BG       = colors.HexColor('#3A1A4A')
WARN_BG     = colors.HexColor('#FDF0F0')
WARN_BDR    = colors.HexColor('#C0392B')

def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=10, textColor=GRAY_TEXT, leading=16, spaceAfter=4)
    d.update(kw)
    return ParagraphStyle(name, **d)

title_s    = S('T',  fontName='Helvetica-Bold', fontSize=22, textColor=DARK_GREEN, alignment=TA_CENTER, leading=28, spaceAfter=4)
sub_s      = S('Su', fontSize=11, textColor=MED_GRAY, alignment=TA_CENTER, spaceAfter=2)
disc_s     = S('D',  fontName='Helvetica-Oblique', fontSize=8.5, textColor=colors.HexColor('#999999'), alignment=TA_CENTER)
seg_hd_s   = S('SH', fontName='Helvetica-Bold', fontSize=13, textColor=colors.white, leading=18)
seg_sub_s  = S('SS', fontSize=8.5, textColor=colors.HexColor('#CCCCCC'), leading=13)
say_label  = S('SL', fontName='Helvetica-Bold', fontSize=8, textColor=MID_GREEN, leading=11, spaceAfter=3, letterSpacing=1.2)
say_s      = S('SA', fontSize=11, textColor=GRAY_TEXT, leading=18, spaceAfter=6, leftIndent=4)
screen_lbl = S('SCL',fontName='Helvetica-Bold', fontSize=8, textColor=SCREEN_TXT, leading=11, spaceAfter=3, letterSpacing=1.2)
screen_s   = S('SC', fontName='Helvetica', fontSize=9.5, textColor=colors.HexColor('#AADDAA'), leading=15, leftIndent=4)
tip_s      = S('TP', fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#5C4000'), leading=14)
warn_s     = S('W',  fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#8B0000'), leading=14)
time_s     = S('TM', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#AAAAAA'), alignment=TA_RIGHT, leading=11)
footer_s   = S('F',  fontSize=8, textColor=colors.HexColor('#AAAAAA'), alignment=TA_CENTER)
bullet_s   = S('BU', fontSize=11, textColor=GRAY_TEXT, leading=18, leftIndent=14, spaceAfter=5)
emph_s     = S('EM', fontName='Helvetica-Bold', fontSize=11, textColor=DARK_GREEN, leading=18, leftIndent=4, spaceAfter=5)


def segment_header(bg_hex, title, subtitle='', time_est=''):
    bg = colors.HexColor(bg_hex) if isinstance(bg_hex, str) else bg_hex
    rows = [[Paragraph(title, seg_hd_s)]]
    if subtitle:
        rows.append([Paragraph(subtitle, seg_sub_s)])
    tbl = Table(rows, colWidths=[6.4*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,0),  13),
        ('TOPPADDING',    (0,1),(-1,1),  2),
        ('BOTTOMPADDING', (0,-1),(-1,-1),11),
        ('LEFTPADDING',   (0,0),(-1,-1), 18),
        ('RIGHTPADDING',  (0,0),(-1,-1), 18),
    ]))
    if time_est:
        time_lbl = Table([[Paragraph(time_est, time_s)]], colWidths=[6.4*inch])
        time_lbl.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), colors.HexColor('#1A1A1A')),
            ('TOPPADDING',   (0,0),(-1,-1), 4),
            ('BOTTOMPADDING',(0,0),(-1,-1), 4),
            ('LEFTPADDING',  (0,0),(-1,-1), 18),
            ('RIGHTPADDING', (0,0),(-1,-1), 18),
        ]))
        return [tbl, time_lbl]
    return [tbl]


def say_block(points):
    out = []
    out.append(Paragraph('WHAT TO SAY', say_label))
    for p in points:
        out.append(Paragraph('•  ' + p, bullet_s))
    return out


def screen_block(points):
    tbl = Table([[
        Paragraph('SHOW ON SCREEN', screen_lbl),
    ]], colWidths=[6.4*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), SCREEN_BG),
        ('TOPPADDING', (0,0),(-1,-1),8),
        ('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LEFTPADDING', (0,0),(-1,-1),14),
        ('RIGHTPADDING',(0,0),(-1,-1),14),
    ]))
    rows = [[tbl]]
    for p in points:
        item = Table([[Paragraph('▶  ' + p, screen_s)]], colWidths=[6.4*inch])
        item.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), SCREEN_BG),
            ('TOPPADDING', (0,0),(-1,-1),3),
            ('BOTTOMPADDING',(0,0),(-1,-1),3),
            ('LEFTPADDING', (0,0),(-1,-1),14),
            ('RIGHTPADDING',(0,0),(-1,-1),14),
        ]))
        rows.append([item])
    close = Table([[Paragraph('', S('x'))]], colWidths=[6.4*inch])
    close.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), SCREEN_BG),
        ('TOPPADDING', (0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING', (0,0),(-1,-1),14),
        ('RIGHTPADDING',(0,0),(-1,-1),14),
    ]))
    rows.append([close])
    outer = Table(rows, colWidths=[6.4*inch])
    outer.setStyle(TableStyle([
        ('TOPPADDING',   (0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING',  (0,0),(-1,-1),0),
        ('RIGHTPADDING', (0,0),(-1,-1),0),
    ]))
    return outer


def note_box(label, text, bg_hex, border_hex, text_color_hex):
    s = S('NB', fontSize=9.5, textColor=colors.HexColor(text_color_hex), leading=15)
    tbl = Table([[Paragraph('<b>' + label + '</b>  ' + text, s)]], colWidths=[6.4*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), colors.HexColor(bg_hex)),
        ('LINEBEFORE',  (0,0),(0,-1),  3, colors.HexColor(border_hex)),
        ('TOPPADDING',    (0,0),(-1,-1),10),
        ('BOTTOMPADDING', (0,0),(-1,-1),10),
        ('LEFTPADDING',   (0,0),(-1,-1),14),
        ('RIGHTPADDING',  (0,0),(-1,-1),14),
    ]))
    return tbl

tip     = lambda t: note_box('Presenter tip:', t, '#E8F5EA', '#2A6636', '#1A4A2A')
remember = lambda t: note_box('Remember:', t, '#FDF8ED', '#C9A84C', '#5C4000')
skip    = lambda t: note_box('You can skip:', t, '#F5F5F5', '#888888', '#555555')


def divider():
    return [Spacer(1, 14), HRFlowable(width='100%', thickness=0.5,
        color=colors.HexColor('#CCCCCC'), spaceAfter=14)]


# ─────────────────────────────────────────────────────────────────────────────
story = []

# COVER
story.append(Spacer(1, 0.05*inch))
story.append(Paragraph('Presenter Guide', title_s))
story.append(Paragraph('Make &amp; ActivePieces — VA Tutorial Video', sub_s))
story.append(Spacer(1, 4))
story.append(Paragraph('Your talking points and screen cues for recording. Not for sharing with VAs.', disc_s))
story.append(Spacer(1, 8))
story.append(HRFlowable(width='100%', thickness=1.5, color=MID_GREEN, spaceAfter=14))

# HOW TO USE THIS GUIDE
story.append(Paragraph('How to Use This Guide', S('HU', fontName='Helvetica-Bold', fontSize=11,
    textColor=DARK_GREEN, spaceBefore=4, spaceAfter=8, leading=15)))
story.append(Paragraph(
    'Each section has two parts: <b>WHAT TO SAY</b> (your talking points - read these loosely, '
    'not word for word) and <b>SHOW ON SCREEN</b> (what to have open or click at that moment). '
    'Work through them in order. Rough total recording time: <b>15-20 minutes</b>.', S('HUB', fontSize=10, textColor=GRAY_TEXT, leading=16)))
story.append(Spacer(1, 10))

# BEFORE YOU RECORD
before = [
    'Have make.com open and logged in (free account)',
    'Have activepieces.com open in a second tab (free account)',
    'Have a Google Sheet open with a few rows of test data (Name | Status | Date columns)',
    'Close any other browser tabs - keep the screen clean',
    'Test your mic and check your recording software before starting',
]
bfr_tbl = Table([[Paragraph('✔  ' + b, S('BF', fontSize=10, textColor=GRAY_TEXT, leading=16, spaceAfter=3))] for b in before],
    colWidths=[6.4*inch])
bfr_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), LIGHT_GREEN),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING',   (0,0),(-1,-1), 14),
    ('RIGHTPADDING',  (0,0),(-1,-1), 14),
    ('LINEBEFORE',    (0,0),(0,-1),  3, MID_GREEN),
]))
story.append(Paragraph('Before You Hit Record', S('PR', fontName='Helvetica-Bold', fontSize=10,
    textColor=MID_GREEN, spaceAfter=6, leading=14)))
story.append(bfr_tbl)
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))


# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT 1 — INTRO
# ═══════════════════════════════════════════════════════════════════════════
story += segment_header('#1A4A2A', 'Segment 1 — Intro', time_est='Approx. 1-2 min')
story.append(Spacer(1, 12))

story += say_block([
    'Hey everyone - in this video I\'m going to show you two free automation tools: Make and ActivePieces.',
    'These connect your Google apps together so they can take actions automatically without you clicking anything.',
    'Both are free to start. Both work with Gmail, Google Sheets, Google Forms, all of it.',
    'The big thing both of them do is if/else logic - which just means: if this condition is true, do this. Otherwise, do something different.',
    'I\'ll show you Make first, then ActivePieces. At the end I\'ll tell you which one to start with.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Show your desktop or a blank browser - nothing specific needed for the intro',
    'Optional: show the quick comparison card from the VA tutorial PDF on screen',
]))
story.append(Spacer(1, 10))
story.append(tip('Keep the intro under 90 seconds. Don\'t over-explain before they\'ve seen anything. Get to the demo fast.'))

story += divider()


# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT 2 — MAKE OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
story += segment_header(MAKE_BG, 'Segment 2 — Make.com Overview', time_est='Approx. 2 min')
story.append(Spacer(1, 12))

story += say_block([
    'Make is a visual tool - you\'ll see a canvas, like a blank page, and you drag things called modules onto it.',
    'Each module is one app action. So "Watch Emails" is one module. "Send an Email" is another.',
    'When data moves through your modules, Make counts it as an operation. The free plan gives you 1,000 per month.',
    'Free plan also gives you 2 active scenarios. A scenario is just one complete automation.',
    'If/else in Make is called a Router - and it\'s free on every plan.',
    'There is an AI assistant that helps you build scenarios, but only on paid plans. I\'ll show you where it lives.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Show the Make dashboard (your scenario list)',
    'Point out the "Create a new scenario" button',
    'Open an existing scenario if you have one, or click Create to show the blank canvas',
    'Point to the + button in the center of the canvas',
]))
story.append(Spacer(1, 10))
story.append(remember('Free = 2 active scenarios, 1,000 ops/month. Core = $9/month, unlimited scenarios, 1-min intervals.'))

story += divider()


# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT 3 — MAKE DEMO
# ═══════════════════════════════════════════════════════════════════════════
story += segment_header(MAKE_BG, 'Segment 3 — Make Live Demo', time_est='Approx. 5-6 min')
story.append(Spacer(1, 12))

story += say_block([
    'Let me build one live so you can see exactly how it works.',
    'I\'ll use Google Sheets as the trigger - when a new row appears, something happens.',
    'Then I\'ll add a Router to show you the if/else.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Click "Create a new scenario"',
    'Click the + on the canvas - search Google Sheets - select "Watch Rows"',
    'Connect Google account (or select existing connection)',
    'Select your test spreadsheet and sheet tab - set max results to 5 - click OK',
]))
story.append(Spacer(1, 8))

story += say_block([
    'So that\'s my trigger. Every time a new row appears, this scenario wakes up.',
    'Now I\'ll add a Router right after - this is the if/else.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Click + after the Google Sheets module - search Router - select it',
    'Show the two route boxes that appear',
    'Click the wrench icon on Route 1 - show the filter panel',
    'Set condition: Status column | Equal to | Qualified - click OK',
]))
story.append(Spacer(1, 8))

story += say_block([
    'Route 1 runs only when Status equals Qualified. I\'ll add a Gmail action here.',
    'Route 2 gets no filter - that means it catches everything else. The "else" branch.',
    'Let me add a different Gmail action on Route 2 so you can see both paths.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Click + at end of Route 1 - Gmail - Send an Email - fill in To/Subject/Body - click OK',
    'Click + at end of Route 2 - Gmail - Send an Email - fill in different Subject - click OK',
    'Click "Run once" at the bottom left',
    'Show the execution result - point to which route ran and why',
    'Toggle the scenario ON at the bottom',
]))
story.append(Spacer(1, 10))
story.append(tip('If the test run shows an error, the most common cause is the Google connection. '
    'Just click the module, reconnect Google, and run once again. Don\'t panic on camera - '
    'troubleshooting live is actually good content.'))

story += divider()


# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT 4 — MAKE AI
# ═══════════════════════════════════════════════════════════════════════════
story += segment_header(MAKE_BG, 'Segment 4 — Make Native AI Feature', time_est='Approx. 1 min')
story.append(Spacer(1, 12))

story += say_block([
    'Make has a built-in AI assistant that can suggest modules based on what you describe.',
    'It\'s only on paid plans - Core is $9 a month.',
    'On the free plan you just search for modules manually, which is fine for learning.',
    'There\'s also a separate thing: you can add OpenAI or Anthropic as a module step inside any scenario to process text. But that uses your own API key - that\'s not part of Make\'s subscription.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'If you have a Core+ account: click + to add a module - show the "Describe what you need" field at the top of the search panel',
    'If you\'re on free: just show the regular search panel and note where the AI field would appear on paid',
    'Optional: show the OpenAI module in search results to show AI-as-a-step',
]))
story.append(Spacer(1, 10))
story.append(skip('You can skip the AI demo entirely if you don\'t have a Core account. Just explain it verbally and move on.'))

story += divider()


# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT 5 — ACTIVEPIECES OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
story += segment_header(AP_BG, 'Segment 5 — ActivePieces Overview', time_est='Approx. 1-2 min')
story.append(Spacer(1, 12))

story += say_block([
    'Now let\'s look at ActivePieces. Same idea as Make, different interface.',
    'Instead of a canvas, ActivePieces is a vertical flow - steps listed top to bottom. Easier to read.',
    'The free plan is more generous: unlimited flows, 1,000 tasks a month, no credit card.',
    'If/else is called a Branch here - and it\'s free.',
    'One thing Make has that ActivePieces doesn\'t: Make has an AI assistant to help build automations. ActivePieces does not. You build everything manually.',
    'You can add AI as a step - like an OpenAI piece - but you bring your own API key for that.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Switch to the ActivePieces tab in your browser',
    'Show the dashboard (flow list)',
    'Point to the "New Flow" button',
]))
story.append(Spacer(1, 10))
story.append(remember('Key difference from Make: unlimited flows on free (Make gives you 2). No AI builder, but easier interface for beginners.'))

story += divider()


# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT 6 — ACTIVEPIECES DEMO
# ═══════════════════════════════════════════════════════════════════════════
story += segment_header(AP_BG, 'Segment 6 — ActivePieces Live Demo', time_est='Approx. 4-5 min')
story.append(Spacer(1, 12))

story += say_block([
    'Same automation as before - Google Sheets trigger, then an if/else.',
    'Watch how much simpler the interface looks compared to Make.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Click "New Flow" - name it - click Create',
    'Click "Select Trigger" - search Google Sheets - choose "New Row"',
    'Connect Google account - select your spreadsheet - select sheet tab - click Save',
]))
story.append(Spacer(1, 8))

story += say_block([
    'That\'s my trigger. Now I\'ll add the if/else - which in ActivePieces is called a Branch.',
    'I just click the plus and search for Branch. It\'s under Core, not an app.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Click + below the trigger - search Branch - select it',
    'Show the True and False paths that appear',
    'Click "Add condition" - select Status field - set Equals - type Qualified - click Save',
]))
story.append(Spacer(1, 8))

story += say_block([
    'True path runs when Status is Qualified. False path runs for everything else.',
    'I\'ll add a Gmail step in each path.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Click + inside True path - Gmail - Send Email - fill in fields - click Save',
    'Click + inside False path - Gmail - Send Email - different subject - click Save',
    'Click "Test Flow" at the top',
    'Show which path ran - point to the green/grey checkmarks on each step',
    'Click Publish',
]))
story.append(Spacer(1, 10))
story.append(tip('The green checkmarks on steps after testing are great to point out - VAs can use these to '
    'debug their own flows and see exactly where something went wrong.'))
story.append(Spacer(1, 8))
story.append(note_box('Watch out:', 'Case sensitivity in Branch conditions. If the sheet has "Qualified" with a capital Q, '
    'the condition must also use capital Q. Mention this - it\'s the most common beginner mistake.',
    '#FDF0F0', '#C0392B', '#8B0000'))

story += divider()


# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT 7 — WHICH TO USE
# ═══════════════════════════════════════════════════════════════════════════
story += segment_header('#1A4A2A', 'Segment 7 — Which Tool Should You Use?', time_est='Approx. 1 min')
story.append(Spacer(1, 12))

story += say_block([
    'So which one should you start with?',
    'If you\'re brand new to automations - start with ActivePieces. No credit card, unlimited flows, simpler to read.',
    'If you want to eventually build more complex flows with a lot of branches - learn Make.',
    'Both are free. You don\'t have to pick one forever. A lot of people use both.',
    'The big thing to know: Zapier - the most famous tool - locks if/else behind a $49 a month plan. Make and ActivePieces give it to you free. So for VAs doing conditional automations, these two are the smarter choice.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Optional: show the comparison table from the VA PDF on screen',
    'Or just talk to camera - no screen needed for this segment',
]))

story += divider()


# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT 8 — OUTRO
# ═══════════════════════════════════════════════════════════════════════════
story += segment_header('#1A4A2A', 'Segment 8 — Outro', time_est='Approx. 30-60 sec')
story.append(Spacer(1, 12))

story += say_block([
    'That\'s it. Make and ActivePieces, side by side.',
    'I\'ve put together a step-by-step PDF guide for you in the community - it has all the exact steps we went through today plus common mistakes to avoid.',
    'Start with one of these tools, build one automation, and get comfortable with the if/else logic. Once you\'ve done it once, it clicks fast.',
    'Drop any questions in the comments and I\'ll answer them.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Talk to camera for the outro - no screen needed',
    'Optional: show the PDF thumbnail or the community post where you\'ll share it',
]))

# QUICK REFERENCE
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=1, color=MID_GREEN, spaceAfter=14))
story.append(Paragraph('Quick Reference', S('QR', fontName='Helvetica-Bold', fontSize=11,
    textColor=DARK_GREEN, spaceAfter=8, leading=14)))

qr_data = [
    [Paragraph('<b>Term</b>', S('QH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)),
     Paragraph('<b>Make calls it</b>', S('QH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)),
     Paragraph('<b>ActivePieces calls it</b>', S('QH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white))],
    ['One automation', 'Scenario', 'Flow'],
    ['One app action', 'Module', 'Step / Piece'],
    ['Data processed', 'Operation', 'Task'],
    ['If/else logic', 'Router', 'Branch'],
    ['Free monthly limit', '1,000 ops, 2 scenarios', '1,000 tasks, unlimited flows'],
    ['If/else on free?', 'YES', 'YES'],
    ['AI builder', 'Paid only (Core+)', 'No - manual only'],
]

qr_table = Table(qr_data, colWidths=[1.8*inch, 2.3*inch, 2.3*inch])
qr_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0), DARK_GREEN),
    ('TEXTCOLOR',     (0,0),(-1,0), colors.white),
    ('FONTNAME',      (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTNAME',      (0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',      (0,0),(-1,-1), 9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LIGHT_GRAY]),
    ('GRID',          (0,0),(-1,-1), 0.5, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',    (0,0),(-1,-1), 7),
    ('BOTTOMPADDING', (0,0),(-1,-1), 7),
    ('LEFTPADDING',   (0,0),(-1,-1), 10),
    ('RIGHTPADDING',  (0,0),(-1,-1), 10),
    ('VALIGN',        (0,0),(-1,-1),'MIDDLE'),
]))
story.append(qr_table)

# FOOTER
story.append(Spacer(1, 20))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=8))
story.append(Paragraph('For presenter use only  |  KeyPlayers HQ  |  Not for distribution to VAs', footer_s))

doc.build(story)
print('Done:', OUTPUT)

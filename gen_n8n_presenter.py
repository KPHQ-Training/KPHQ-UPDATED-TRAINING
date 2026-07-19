from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

OUTPUT = r'C:\Users\jervi\OneDrive\Documents\Claude\Projects\KP AI TRAINING\github-push\Presenter-Guide-n8n.pdf'

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
SCREEN_BG   = colors.HexColor('#0D1017')
SCREEN_TXT  = colors.HexColor('#9B8FD4')
N8N_COLOR   = colors.HexColor('#2A1F4A')

def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=10, textColor=GRAY_TEXT, leading=16, spaceAfter=4)
    d.update(kw)
    return ParagraphStyle(name, **d)

title_s    = S('T',  fontName='Helvetica-Bold', fontSize=22, textColor=DARK_GREEN, alignment=TA_CENTER, leading=28, spaceAfter=4)
sub_s      = S('Su', fontSize=11, textColor=MED_GRAY, alignment=TA_CENTER, spaceAfter=2)
disc_s     = S('D',  fontName='Helvetica-Oblique', fontSize=8.5, textColor=colors.HexColor('#999999'), alignment=TA_CENTER)
seg_hd_s   = S('SH', fontName='Helvetica-Bold', fontSize=13, textColor=colors.white, leading=18)
seg_sub_s  = S('SS', fontSize=8.5, textColor=colors.HexColor('#CCCCCC'), leading=13)
say_label  = S('SL', fontName='Helvetica-Bold', fontSize=8, textColor=MID_GREEN, leading=11, spaceAfter=3)
bullet_s   = S('BU', fontSize=11, textColor=GRAY_TEXT, leading=18, leftIndent=14, spaceAfter=5)
screen_lbl = S('SCL',fontName='Helvetica-Bold', fontSize=8, textColor=SCREEN_TXT, leading=11, spaceAfter=3)
screen_s   = S('SC', fontName='Helvetica', fontSize=9.5, textColor=colors.HexColor('#BBAAEE'), leading=15, leftIndent=4)
time_s     = S('TM', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#AAAAAA'), alignment=TA_RIGHT, leading=11)
footer_s   = S('F',  fontSize=8, textColor=colors.HexColor('#AAAAAA'), alignment=TA_CENTER)

def segment_header(bg_hex, title, subtitle='', time_est=''):
    bg = colors.HexColor(bg_hex) if isinstance(bg_hex, str) else bg_hex
    rows = [[Paragraph(title, seg_hd_s)]]
    if subtitle:
        rows.append([Paragraph(subtitle, seg_sub_s)])
    tbl = Table(rows, colWidths=[6.4*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), bg),
        ('TOPPADDING',(0,0),(-1,0), 13),
        ('TOPPADDING',(0,1),(-1,1), 2),
        ('BOTTOMPADDING',(0,-1),(-1,-1), 11),
        ('LEFTPADDING',(0,0),(-1,-1), 18),
        ('RIGHTPADDING',(0,0),(-1,-1), 18),
    ]))
    result = [tbl]
    if time_est:
        time_lbl = Table([[Paragraph(time_est, time_s)]], colWidths=[6.4*inch])
        time_lbl.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1), colors.HexColor('#111111')),
            ('TOPPADDING',(0,0),(-1,-1), 4),('BOTTOMPADDING',(0,0),(-1,-1), 4),
            ('LEFTPADDING',(0,0),(-1,-1), 18),('RIGHTPADDING',(0,0),(-1,-1), 18),
        ]))
        result.append(time_lbl)
    return result

def say_block(points):
    out = [Paragraph('WHAT TO SAY', say_label)]
    for p in points:
        out.append(Paragraph('•  ' + p, bullet_s))
    return out

def screen_block(points):
    rows = [[Table([[Paragraph('SHOW ON SCREEN', screen_lbl)]], colWidths=[6.4*inch],
        style=TableStyle([('BACKGROUND',(0,0),(-1,-1),SCREEN_BG),
            ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),2),
            ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14)]))]]
    for p in points:
        rows.append([Table([[Paragraph('▶  ' + p, screen_s)]], colWidths=[6.4*inch],
            style=TableStyle([('BACKGROUND',(0,0),(-1,-1),SCREEN_BG),
                ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
                ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14)]))])
    rows.append([Table([[Paragraph('', S('x'))]], colWidths=[6.4*inch],
        style=TableStyle([('BACKGROUND',(0,0),(-1,-1),SCREEN_BG),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14)]))])
    outer = Table(rows, colWidths=[6.4*inch])
    outer.setStyle(TableStyle([
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ]))
    return outer

def note_box(label, text, bg_hex, border_hex, text_hex):
    s = S('NB', fontSize=9.5, textColor=colors.HexColor(text_hex), leading=15)
    tbl = Table([[Paragraph('<b>' + label + '</b>  ' + text, s)]], colWidths=[6.4*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), colors.HexColor(bg_hex)),
        ('LINEBEFORE',(0,0),(0,-1), 3, colors.HexColor(border_hex)),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
    ]))
    return tbl

tip      = lambda t: note_box('Presenter tip:', t, '#E8F5EA', '#2A6636', '#1A4A2A')
remember = lambda t: note_box('Remember:', t, '#FDF8ED', '#C9A84C', '#5C4000')
skip     = lambda t: note_box('You can skip:', t, '#F5F5F5', '#888888', '#555555')

def divider():
    return [Spacer(1,14), HRFlowable(width='100%', thickness=0.5,
        color=colors.HexColor('#CCCCCC'), spaceAfter=14)]

# ─────────────────────────────────────────────────────────────────────────────
story = []

story.append(Spacer(1, 0.05*inch))
story.append(Paragraph('Presenter Guide', title_s))
story.append(Paragraph('n8n Tutorial Video', sub_s))
story.append(Spacer(1, 4))
story.append(Paragraph('Your talking points and screen cues for recording. Not for sharing with VAs.', disc_s))
story.append(Spacer(1, 8))
story.append(HRFlowable(width='100%', thickness=1.5, color=N8N_COLOR, spaceAfter=14))

story.append(Paragraph('How to Use This Guide', S('HU', fontName='Helvetica-Bold', fontSize=11,
    textColor=DARK_GREEN, spaceBefore=4, spaceAfter=8, leading=15)))
story.append(Paragraph(
    'Each section has <b>WHAT TO SAY</b> (talking points - speak loosely, not word for word) and '
    '<b>SHOW ON SCREEN</b> (what to click or display at that moment). '
    'Rough total recording time: <b>12-18 minutes</b>.', S('HUB', fontSize=10, textColor=GRAY_TEXT, leading=16)))
story.append(Spacer(1, 10))

before = [
    'Have cloud.n8n.io open and logged in (free trial account)',
    'Have a Google Sheet called "Lead Tracker" ready with columns: Name | Budget | Email | VA Name',
    'Add two test rows: one with Budget = "High", one with Budget = "Low"',
    'Gmail open in another tab so you can show the test emails arriving',
    'Close any unrelated tabs - keep the screen clean',
    'Test your mic and recording software before starting',
]
bfr = Table([[Paragraph('✔  ' + b, S('BF', fontSize=10, textColor=GRAY_TEXT, leading=16, spaceAfter=3))] for b in before],
    colWidths=[6.4*inch])
bfr.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1), LIGHT_GREEN),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
    ('LINEBEFORE',(0,0),(0,-1),3, MID_GREEN),
]))
story.append(Paragraph('Before You Hit Record', S('PR', fontName='Helvetica-Bold', fontSize=10,
    textColor=MID_GREEN, spaceAfter=6, leading=14)))
story.append(bfr)
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))

# SEGMENT 1 — INTRO
story += segment_header('#1A4A2A', 'Segment 1 — Intro', time_est='Approx. 1 min')
story.append(Spacer(1, 12))
story += say_block([
    'In this video I\'m going to walk you through n8n - the most powerful of the three automation tools we\'ve covered.',
    'If you\'ve already watched the Make and ActivePieces video, this is the next level up.',
    'n8n is open source - free to self-host - and has a paid cloud version that starts at $20 a month.',
    'The big difference from the other tools: n8n has a built-in AI Agent node that can actually reason through tasks, not just send data from one app to another.',
    'I\'ll cover what it is, the pricing, the AI features, and then build a live example.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Talk to camera or show desktop - nothing specific needed for the intro',
]))
story += divider()

# SEGMENT 2 — WHAT IS N8N
story += segment_header(N8N_COLOR, 'Segment 2 — What Is n8n?', time_est='Approx. 2 min')
story.append(Spacer(1, 12))
story += say_block([
    'n8n is a visual automation tool - you connect blocks called nodes on a canvas.',
    'Each node is one app action. Google Sheets node, Gmail node, IF node - each one does one thing.',
    'The flow reads left to right across the canvas. Trigger on the left, actions on the right.',
    'The if/else node is called an IF node. It has two outputs - TRUE at the top, FALSE at the bottom.',
    'There\'s also a Switch node for when you need more than two paths. I\'ll show both.',
    'One key vocabulary word: an Execution. That\'s one run of your workflow. Cloud plans are billed per execution.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Show the n8n dashboard',
    'Open any workflow or create a new blank one to show the canvas',
    'Point to where nodes sit and how they connect with arrows',
]))
story.append(Spacer(1, 10))
story.append(remember('Workflow = Make Scenario. Node = Make Module. Execution = Make Operation. IF Node = Make Router.'))
story += divider()

# SEGMENT 3 — PRICING
story += segment_header(N8N_COLOR, 'Segment 3 — Pricing & Free vs Paid', time_est='Approx. 1-2 min')
story.append(Spacer(1, 12))
story += say_block([
    'Here\'s the honest picture on pricing.',
    'n8n is open source - so you CAN run it for free if you set up your own server. But that\'s technical. Not something I\'d recommend for a VA just starting out.',
    'The cloud version has a 14-day free trial. After that it\'s $20 a month for the Starter plan - 2,500 executions, 5 active workflows.',
    'So if you\'re looking for free automation with if/else, Make or ActivePieces are still better starting points. Come to n8n when you need more power.',
    'The if/else logic - the IF node and Switch node - is available on all plans including the trial. No paywall on that.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Optional: show n8n.io/pricing page',
    'Or just talk to camera - this segment doesn\'t need a live demo',
]))
story.append(Spacer(1, 10))
story.append(tip('Keep this segment short. VAs who are watching this are probably already comfortable with Make or ActivePieces. '
    'They don\'t need a long pricing lecture - just the headline numbers and move on.'))
story += divider()

# SEGMENT 4 — NATIVE AI
story += segment_header(N8N_COLOR, 'Segment 4 — Native AI in n8n', time_est='Approx. 1-2 min')
story.append(Spacer(1, 12))
story += say_block([
    'This is where n8n stands apart from Make and ActivePieces.',
    'First: there\'s an AI assistant that helps you build workflows. You describe what you want, it suggests nodes. That\'s on paid plans.',
    'Second, and more interesting: there\'s a built-in AI Agent node. This is not just "send text to OpenAI and get a response back." This is an AI that can use tools - like reading a spreadsheet, doing a web search, sending an email - and chain multiple steps together on its own.',
    'Think of it like giving AI a to-do list and letting it figure out how to complete it.',
    'To use either feature you still need your own OpenAI or Anthropic API key. n8n gives you the plumbing, you bring the AI.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Show the node search panel - search "AI Agent" to show it exists',
    'If you have a paid plan: show the AI chat icon in the top right of the canvas',
    'Optional: open the AI Agent node to show its configuration (tools list, model selector)',
]))
story.append(Spacer(1, 10))
story.append(skip('You can skip the AI Agent demo if you don\'t have an API key set up. Just describe it verbally and move on to the live demo.'))
story += divider()

# SEGMENT 5 — LIVE DEMO SETUP
story += segment_header(N8N_COLOR, 'Segment 5 — Live Demo Setup', time_est='Approx. 1 min')
story.append(Spacer(1, 12))
story += say_block([
    'Alright, let me build something live.',
    'I\'ve got a Google Sheet called Lead Tracker with columns: Name, Budget, Email, VA Name.',
    'The automation: when a new row is added, check the Budget column. If it\'s "High" - email the senior account manager. If it\'s "Low" - email the VA handling smaller accounts.',
    'Same if/else shape we\'ve done before - just in n8n\'s interface.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Show the Lead Tracker Google Sheet with the test rows visible',
    'Name the columns out loud as you point to them: Name, Budget, Email, VA Name',
]))
story += divider()

# SEGMENT 6 — DEMO: TRIGGER
story += segment_header(N8N_COLOR, 'Segment 6 — Demo: Setting Up the Trigger', time_est='Approx. 2-3 min')
story.append(Spacer(1, 12))
story += say_block([
    'I\'ll create a new workflow and set the Google Sheets trigger first.',
    'Watch how I connect the Google credential - this is the part that trips people up the first time.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Click New Workflow from the dashboard',
    'Delete the default "When clicking Test workflow" node',
    'Click + or press Tab to open node search - search Google Sheets - select "Trigger on new row added"',
    'Click "Create New" credential - show the Google OAuth window - authorize',
    'Select the Lead Tracker spreadsheet from the Document dropdown',
    'Select the sheet tab - click Save',
    'Point to the node on the canvas - show it is now configured',
]))
story.append(Spacer(1, 10))
story.append(tip('If the spreadsheet does not appear in the dropdown, click the refresh icon next to it. '
    'If it still doesn\'t appear, paste the spreadsheet URL directly into the field instead.'))
story += divider()

# SEGMENT 7 — DEMO: IF NODE
story += segment_header(N8N_COLOR, 'Segment 7 — Demo: Adding the IF Node', time_est='Approx. 2-3 min')
story.append(Spacer(1, 12))
story += say_block([
    'Now the if/else. I\'ll add an IF node after the trigger.',
    'Notice where the TRUE and FALSE outputs are - TRUE on top, FALSE on the bottom.',
    'I\'ll set the condition: Budget column equals "High."',
    'Then I\'ll connect Gmail to the TRUE output, and a different Gmail to the FALSE output.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Click + to the right of the Google Sheets node - search IF - select it',
    'In the IF node panel: click Add condition',
    'First field: click "Add Value" - in the expression editor select the Budget column from the Sheets data',
    'Operator: Equal - Value: High (capital H)',
    'Click Save - point out the TRUE output (top) and FALSE output (bottom)',
    'Click + on the TRUE output - search Gmail - Send a Message - connect Google credential - fill in fields',
    'Click + on the FALSE output - add second Gmail node - different subject line - fill in fields',
    'Click Test workflow',
    'Show the green checkmarks lighting up on each node',
    'Switch to Gmail tab - show the two test emails arrived',
]))
story.append(Spacer(1, 10))
story.append(tip('Slow down during the expression step - selecting data from the left panel is the most confusing part for beginners. '
    'Click clearly and narrate what you\'re selecting.'))
story += divider()

# SEGMENT 8 — SWITCH NODE
story += segment_header(N8N_COLOR, 'Segment 8 — Bonus: The Switch Node', time_est='Approx. 1-2 min')
story.append(Spacer(1, 12))
story += say_block([
    'Quick bonus: if you ever need more than two paths - use the Switch node instead of IF.',
    'Same idea, but you can add as many output paths as you need. One for each value.',
    'Each path gets its own output connector on the right side of the Switch node.',
    'There\'s also a Fallback output at the bottom - it catches anything that didn\'t match any of your rules. Always connect something to it so data doesn\'t get lost.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Add a Switch node to the canvas (or just show it in the search results)',
    'Open it - show the Add routing rule button',
    'Show what the multiple output connectors look like',
    'Point to the Fallback output at the bottom',
]))
story.append(Spacer(1, 10))
story.append(skip('You can skip the Switch node demo if you\'re short on time. Just mention it exists and move to the outro.'))
story += divider()

# SEGMENT 9 — OUTRO
story += segment_header('#1A4A2A', 'Segment 9 — Outro', time_est='Approx. 30-60 sec')
story.append(Spacer(1, 12))
story += say_block([
    'That\'s n8n. More powerful than Make or ActivePieces, and more technical.',
    'My recommendation: if you\'re just starting out, use Make or ActivePieces first. Once you\'ve built a few automations there and you\'re comfortable with the if/else logic, then come to n8n.',
    'I\'ve dropped a step-by-step PDF in the community with everything we covered today.',
    'Any questions, drop them in the comments.',
])
story.append(Spacer(1, 10))
story.append(screen_block([
    'Talk to camera for the outro',
    'Optional: show the n8n tutorial PDF thumbnail',
]))

# QUICK REFERENCE
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=1, color=N8N_COLOR, spaceAfter=14))
story.append(Paragraph('Quick Reference', S('QR', fontName='Helvetica-Bold', fontSize=11,
    textColor=DARK_GREEN, spaceAfter=8, leading=14)))

qr_data = [
    [Paragraph('<b>Concept</b>', S('QH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)),
     Paragraph('<b>n8n term</b>', S('QH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)),
     Paragraph('<b>Make equivalent</b>', S('QH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white))],
    ['One automation',      'Workflow',   'Scenario'],
    ['One app action',      'Node',       'Module'],
    ['Data processed',      'Execution',  'Operation'],
    ['Two-path if/else',    'IF Node',    'Router'],
    ['Multi-path if/else',  'Switch Node','Router (multi-route)'],
    ['Insert data in field','Expression', 'Mapping'],
    ['Saved app login',     'Credential', 'Connection'],
    ['If/else on free?',    'Trial only', 'YES (always free)'],
    ['AI builder',          'Paid (Starter+)', 'Paid (Core+)'],
    ['AI Agent node',       'YES (unique to n8n)', 'Not available'],
]
qr = Table(qr_data, colWidths=[1.9*inch, 1.9*inch, 2.6*inch])
qr.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), DARK_GREEN),
    ('TEXTCOLOR',(0,0),(-1,0), colors.white),
    ('FONTNAME',(0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1), 9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LIGHT_GRAY]),
    ('GRID',(0,0),(-1,-1), 0.5, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
]))
story.append(qr)

story.append(Spacer(1, 20))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=8))
story.append(Paragraph('For presenter use only  |  KeyPlayers HQ  |  Not for distribution to VAs', footer_s))

doc.build(story)
print('Done:', OUTPUT)

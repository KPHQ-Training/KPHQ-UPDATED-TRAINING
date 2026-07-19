from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = r'C:\Users\jervi\OneDrive\Documents\Claude\Projects\KP AI TRAINING\github-push\VA-Make-ActivePieces-Tutorial.pdf'

doc = SimpleDocTemplate(
    OUTPUT, pagesize=letter,
    rightMargin=0.75*inch, leftMargin=0.75*inch,
    topMargin=0.85*inch, bottomMargin=0.85*inch
)

DARK_GREEN  = colors.HexColor('#1A4A2A')
MID_GREEN   = colors.HexColor('#2A6636')
ACCENT      = colors.HexColor('#4A9B5A')
LIGHT_GREEN = colors.HexColor('#E8F5EA')
GOLD_BG     = colors.HexColor('#FDF8ED')
GOLD_BORDER = colors.HexColor('#C9A84C')
GRAY_TEXT   = colors.HexColor('#444444')
LIGHT_GRAY  = colors.HexColor('#F5F5F5')
MAKE_COLOR  = colors.HexColor('#1A3A4A')
AP_COLOR    = colors.HexColor('#3A1A4A')

def S(name, **kw):
    defaults = dict(fontName='Helvetica', fontSize=9.5, textColor=GRAY_TEXT, leading=15, spaceAfter=4)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

title_s    = S('T', fontName='Helvetica-Bold', fontSize=20, textColor=DARK_GREEN, spaceAfter=4, alignment=TA_CENTER, leading=26)
sub_s      = S('Su', fontSize=10, textColor=colors.HexColor('#555555'), spaceAfter=2, alignment=TA_CENTER)
disc_s     = S('D', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#888888'), alignment=TA_CENTER, leading=12)
tool_hd    = S('TH', fontName='Helvetica-Bold', fontSize=15, textColor=colors.white, leading=20)
tool_sub   = S('TS', fontSize=8.5, textColor=colors.HexColor('#CCDDCC'), leading=13)
section_s  = S('SE', fontName='Helvetica-Bold', fontSize=10.5, textColor=MID_GREEN, spaceBefore=14, spaceAfter=6, leading=14)
body_s     = S('B')
step_s     = S('ST', leftIndent=6, spaceAfter=3, leading=14)
note_s     = S('N', fontName='Helvetica-Oblique', fontSize=8.5, textColor=ACCENT, leftIndent=6, spaceAfter=2, leading=13)
pill_s     = S('P', fontName='Helvetica-Bold', fontSize=8, textColor=MID_GREEN)
footer_s   = S('F', fontSize=8, textColor=colors.HexColor('#999999'), alignment=TA_CENTER)
concept_k  = S('CK', fontName='Helvetica-Bold', fontSize=9, textColor=DARK_GREEN, leading=13, spaceAfter=1)
concept_v  = S('CV', fontSize=9, textColor=GRAY_TEXT, leading=13, spaceAfter=6, leftIndent=10)


def tool_header(bg_hex, title, subtitle):
    bg = colors.HexColor(bg_hex)
    tbl = Table([
        [Paragraph(title, tool_hd)],
        [Paragraph(subtitle, tool_sub)],
    ], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('TOPPADDING',    (0,0), (-1,0),  14),
        ('TOPPADDING',    (0,1), (-1,1),  2),
        ('BOTTOMPADDING', (0,-1),(-1,-1), 12),
        ('LEFTPADDING',   (0,0), (-1,-1), 18),
        ('RIGHTPADDING',  (0,0), (-1,-1), 18),
    ]))
    return tbl


def callout(bg_hex, border_hex, label, text):
    cs = S('CB', fontSize=9, textColor=GRAY_TEXT, leading=14)
    tbl = Table([[Paragraph('<b>' + label + '</b>  ' + text, cs)]], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_hex)),
        ('LINEBEFORE',  (0,0), (0,-1), 3, colors.HexColor(border_hex)),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    return tbl

tip     = lambda t: callout('#E8F5EA', '#2A6636', 'Tip:', t)
warning = lambda t: callout('#FDF0F0', '#C0392B', 'Watch out:', t)
ai_note = lambda t: callout('#F5F0FD', '#6C3483', 'Native AI:', t)
concept_box = lambda t: callout('#F0F4F0', '#2A6636', '', t)


def steps(items):
    out = []
    for i, item in enumerate(items, 1):
        text, note = item if isinstance(item, tuple) else (item, None)
        num = Paragraph('<b>' + str(i) + '</b>',
            S('N2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, alignment=TA_CENTER, leading=12))
        nc = Table([[num]], colWidths=[0.26*inch], rowHeights=[0.26*inch])
        nc.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), MID_GREEN),
            ('TOPPADDING', (0,0),(-1,-1), 1), ('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('LEFTPADDING',(0,0),(-1,-1), 0), ('RIGHTPADDING',  (0,0),(-1,-1),0),
        ]))
        content = [Paragraph(text, step_s)]
        if note:
            content.append(Paragraph(note, note_s))
        rt = Table([[nc, content]], colWidths=[0.38*inch, 6.12*inch])
        rt.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),0), ('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('LEFTPADDING',(0,0),(-1,-1),0), ('RIGHTPADDING',(0,0),(-1,-1),0),
        ]))
        out.append(rt)
        out.append(Spacer(1, 5))
    return out


def tier_table(rows):
    hdr = [Paragraph('<b>' + h + '</b>', pill_s) for h in ['Plan', 'Cost', 'What you get', 'If/Else?']]
    t = Table([hdr] + rows, colWidths=[1.0*inch, 0.9*inch, 3.6*inch, 1.0*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0), DARK_GREEN),
        ('TEXTCOLOR',     (0,0),(-1,0), colors.white),
        ('FONTNAME',      (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',      (0,0),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LIGHT_GRAY]),
        ('GRID',          (0,0),(-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING',    (0,0),(-1,-1), 7),  ('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),  ('RIGHTPADDING', (0,0),(-1,-1),8),
        ('VALIGN',        (0,0),(-1,-1),'TOP'),
    ]))
    return t


def side_by_side(left_items, right_items, left_label, right_label):
    def col(label, items, color):
        hdr = Table([[Paragraph('<b>' + label + '</b>',
            S('HL', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, leading=13))]],
            colWidths=[3.1*inch])
        hdr.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1), color),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ]))
        rows = [[hdr]]
        for item in items:
            rows.append([Paragraph('- ' + item,
                S('SI', fontSize=8.5, textColor=GRAY_TEXT, leading=13, leftIndent=8, spaceAfter=2))])
        t = Table(rows, colWidths=[3.1*inch])
        t.setStyle(TableStyle([
            ('GRID',(0,1),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
            ('TOPPADDING',(0,1),(-1,-1),5),('BOTTOMPADDING',(0,1),(-1,-1),5),
            ('LEFTPADDING',(0,1),(-1,-1),10),('RIGHTPADDING',(0,1),(-1,-1),10),
            ('BACKGROUND',(0,1),(-1,-1),colors.HexColor('#FAFAFA')),
        ]))
        return t
    outer = Table([[col(left_label, left_items, MAKE_COLOR), col(right_label, right_items, AP_COLOR)]],
        colWidths=[3.2*inch, 3.3*inch], hAlign='LEFT')
    outer.setStyle(TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    return outer


# ─────────────────────────────────────────────────────────────────────────────
story = []

# TITLE
story.append(Spacer(1, 0.05*inch))
story.append(Paragraph('Make &amp; ActivePieces', title_s))
story.append(Paragraph('A Step-by-Step Tutorial for VAs', sub_s))
story.append(Paragraph('Beginner to intermediate  |  Google Workspace focus', disc_s))
story.append(Spacer(1, 6))
story.append(HRFlowable(width='100%', thickness=1.5, color=MID_GREEN, spaceAfter=14))

# INTRO
story.append(Paragraph('What These Tools Do', section_s))
story.append(Paragraph(
    'Make and ActivePieces are automation tools. They connect your apps together so they can '
    'talk to each other and take actions automatically - without you clicking anything. '
    'You set up the rules once, and the tool runs them in the background.', body_s))
story.append(Paragraph(
    'Both tools work well with Google Workspace apps like Gmail, Google Forms, Google Sheets, '
    'Google Drive, and Google Calendar.', body_s))

story.append(Paragraph('Make vs ActivePieces at a Glance', section_s))
story.append(side_by_side(
    ['Visual canvas (drag-and-drop flowchart)',
     'Called: Scenarios, Modules, Operations',
     'Free: 1,000 ops/month, 2 active scenarios',
     'If/else (Router) - FREE',
     'AI builder - paid plans only',
     'Best for: complex multi-step flows'],
    ['Step-by-step flow builder',
     'Called: Flows, Pieces, Steps',
     'Free: 1,000 tasks/month, unlimited flows',
     'If/else (Branch) - FREE',
     'No native AI builder',
     'Best for: beginners, tight budget'],
    'Make.com', 'ActivePieces'
))
story.append(Spacer(1, 10))
story.append(tip('Not sure which to start with? Use <b>ActivePieces</b> if you want unlimited flows on free. '
    'Use <b>Make</b> if you want to eventually handle more complex logic or run more scenarios at once.'))
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))


# ═══════════════════════════════════════════════════════════════════════════
# MAKE.COM
# ═══════════════════════════════════════════════════════════════════════════
story.append(KeepTogether([
    tool_header('#1A3A4A', 'Make.com Tutorial', 'Visual canvas automation  |  make.com  |  Free to start'),
    Spacer(1, 12),
]))

# CONCEPTS
story.append(Paragraph('Key Concepts', section_s))
story.append(Paragraph(
    'Before you touch the tool, learn these four words. Every step in this tutorial uses them.', body_s))

concepts_make = [
    ('Scenario', 'One complete automation. A scenario watches for something to happen, then does something in response.'),
    ('Module', 'One app action inside a scenario. Examples: "Watch Emails" (Gmail), "Add a Row" (Sheets), "Send an Email" (Gmail).'),
    ('Operation', 'One piece of data processed. If 3 emails come in and your scenario runs on all 3, that\'s 3 operations. The free plan gives you 1,000/month.'),
    ('Router', 'The if/else module. It splits your scenario into branches. Each branch only runs if its condition is met.'),
]
for k, v in concepts_make:
    story.append(Paragraph(k, concept_k))
    story.append(Paragraph(v, concept_v))

# SUBSCRIPTIONS
story.append(Paragraph('Subscriptions', section_s))
story.append(tier_table([
    ['Free',  '$0',     '1,000 operations/month | 2 active scenarios | 15-minute minimum schedule interval | access to most modules', 'YES'],
    ['Core',  '$9/mo',  '10,000 operations/month | unlimited active scenarios | 1-minute schedule intervals', 'YES'],
    ['Pro',   '$16/mo', 'Everything in Core + custom variables + full execution log search', 'YES'],
    ['Teams', '$29/mo', 'Multiple team members + shared scenarios + admin controls', 'YES'],
]))
story.append(Spacer(1, 6))
story.append(tip('Start on the free plan. Only upgrade to Core when you need more than 2 active scenarios '
    'or you need your automation to check for new data faster than every 15 minutes.'))

# NATIVE AI
story.append(Paragraph('Native AI in Make', section_s))
story.append(ai_note(
    'Make has an AI assistant that reads what you describe and suggests which modules to add. '
    'It is available on paid plans (Core and above). On the free plan, you add modules manually by searching. '
    'Separately, you can add an OpenAI or Anthropic module as a step inside any scenario to process text '
    'using AI - but this requires your own API key and is billed by the AI provider, not Make. '
    'To access the AI builder on Core+: inside a scenario, click + to add a module, '
    'then look for the "Describe what you need" field at the top of the search panel.'))

# ACCOUNT SETUP
story.append(Paragraph('Part 1 - Create Your Account', section_s))
story += steps([
    ('Go to <b>make.com</b> in your browser',
     'If you already have an account, log in and skip to Part 2.'),
    ('Click <b>Sign up for free</b>',  None),
    ('Select <b>Continue with Google</b> and choose your work Google account',
     'Signing up with Google means Make can connect to your Google apps without extra configuration later.'),
    ('Skip or complete the onboarding questions - click <b>Get started</b>', None),
    ('You are now in the Make dashboard. You will see your scenario list on the left.', None),
])

# UNDERSTANDING THE CANVAS
story.append(Paragraph('Part 2 - Understanding the Canvas', section_s))
story.append(Paragraph(
    'When you open a scenario, you see a dark canvas - an empty workspace where you drag and '
    'connect modules. Think of it like building a flowchart. Each circle is a module. '
    'Lines between circles show the flow of data.', body_s))
story.append(concept_box(
    'The canvas is just a blank page until you add modules. Every scenario starts with a trigger module '
    '(the first circle, which watches for something to happen) and then one or more action modules '
    '(which do something in response).'))

# BUILD A SCENARIO
story.append(Paragraph('Part 3 - Build Your First Scenario', section_s))
story.append(Paragraph(
    'We will build a simple one: when a new row is added to a Google Sheet, send a Gmail. '
    'This teaches the core shape that every scenario follows.', body_s))
story += steps([
    ('From the Make dashboard, click <b>Create a new scenario</b> (top right button)', None),
    ('You will see a blank canvas with a large <b>+</b> in the center - click it', None),
    ('A search panel opens. Type <b>Google Sheets</b> and select it from the list', None),
    ('Choose the trigger event: <b>Watch Rows</b> - this fires every time a new row appears in a sheet',
     'Every scenario must start with a trigger. "Watch Rows" is the most common Sheets trigger.'),
    ('Click <b>Add</b> next to the Google connection field',
     'A popup will ask you to sign in with Google. Select your work account and click Allow. You only do this once.'),
    ('Configure the trigger: select your spreadsheet from the dropdown, select the sheet tab, set Max results to <b>5</b>, click <b>OK</b>',
     'Max results controls how many new rows are processed each time the scenario runs. 5 is a safe starting number.'),
    ('The trigger module now shows a green checkmark. Click the <b>+</b> that appears to its right on the canvas',
     'The + between or after modules is always how you add the next step.'),
    ('Search for <b>Gmail</b> - select it - choose <b>Send an Email</b>', None),
    ('Fill in: To (your email), Subject (type anything as a test), Body (type anything)',
     'Click in any field and then click the Google Sheets circle on the left panel to map real data from your sheet into the email.'),
    ('Click <b>OK</b>', None),
    ('Click <b>Run once</b> at the bottom left',
     '"Run once" is your test button. Make processes your most recent sheet data through the scenario and shows you exactly what happened at each step.'),
    ('Check your Gmail inbox - the test email should be there', None),
    ('Click the <b>toggle switch</b> at the bottom of the screen to turn the scenario <b>ON</b>',
     'Once ON, the scenario checks for new rows automatically on a schedule (every 15 minutes on free, every 1 minute on Core+).'),
])

# ADDING IF/ELSE
story.append(Paragraph('Part 4 - Adding If/Else Logic (Router)', section_s))
story.append(Paragraph(
    'A Router lets your scenario take different actions depending on the data. '
    'One route for "yes", another for "no" - or as many routes as you need.', body_s))
story += steps([
    ('Inside any scenario, click the <b>+</b> after your trigger (or after any module) to add a new step', None),
    ('Search for <b>Router</b> and select it - it appears as a circle with two arrows branching out',
     'The Router is not an app. It is a built-in Make tool, always free.'),
    ('You will see two empty route boxes. Each route is one branch of your if/else.', None),
    ('Click the <b>wrench icon</b> on Route 1 to set its filter condition',
     'The filter is the "if" part. Only data that matches the filter will travel down this route.'),
    ('In the filter panel: click <b>Add AND rule</b> - choose a field from your data on the left (e.g. Status column) - choose an operator (e.g. Equal to) - type the value (e.g. Qualified)',
     'Make shows all available fields from your trigger data on the left side of the filter panel.'),
    ('Click <b>OK</b>. Now click the <b>+</b> at the end of Route 1 to add the action for this branch.',
     'Each route gets its own action(s). Route 1 does one thing; Route 2 does something different.'),
    ('Set up Route 2 in the same way - or leave it with no filter (no filter = catches everything Route 1 did not)',
     'A route with no filter acts as your "else" - it catches any data that did not match the earlier routes.'),
    ('Click <b>Run once</b> to test both branches. Make will show you which route each piece of data took.', None),
])

story.append(Spacer(1, 8))
story.append(warning('Gmail labels: Create the label inside Gmail before selecting it in Make. '
    'Make reads your existing labels - it cannot create new ones. '
    'Go to Gmail, scroll to the bottom of the left sidebar, click Create new label, then come back to Make.'))

# COMMON MISTAKES
story.append(Paragraph('Common Mistakes to Avoid', section_s))
story += steps([
    ('<b>Scenario left OFF after testing.</b> "Run once" does not turn the scenario on. '
     'You must toggle the switch at the bottom to activate it.', None),
    ('<b>Wrong Google account connected.</b> If Make pulls data from the wrong Drive or inbox, '
     'go to Connections in the left sidebar, find the Google connection, and reconnect with the right account.', None),
    ('<b>Operations run out mid-month.</b> On the free plan, 1,000 operations is not a lot if your sheet gets many rows. '
     'Check your operations count in the dashboard. Upgrade to Core if you keep running out.', None),
    ('<b>Scenario not triggering instantly.</b> The free plan checks every 15 minutes, not in real time. '
     'If you need faster, upgrade to Core (1-minute intervals) or click Run once to force a check.', None),
])

story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))


# ═══════════════════════════════════════════════════════════════════════════
# ACTIVEPIECES
# ═══════════════════════════════════════════════════════════════════════════
story.append(KeepTogether([
    tool_header('#3A1A4A', 'ActivePieces Tutorial', 'Step-by-step flow builder  |  activepieces.com  |  Free, no credit card'),
    Spacer(1, 12),
]))

# CONCEPTS
story.append(Paragraph('Key Concepts', section_s))
story.append(Paragraph(
    'ActivePieces uses different words than Make, but the idea is the same. Learn these before starting.', body_s))

concepts_ap = [
    ('Flow', 'One complete automation. A flow watches for something to happen, then does something in response. Same idea as a Make Scenario.'),
    ('Piece', 'An app integration. The Gmail piece connects your flow to Gmail. The Google Sheets piece connects to Sheets. Same idea as a Make Module.'),
    ('Step', 'One action inside a flow. Your trigger is Step 1. Each action you add is the next step.'),
    ('Branch', 'The if/else step. It splits your flow into a True path and a False path. Works like Make\'s Router but simpler: exactly two paths only.'),
    ('Task', 'One piece of data processed. Same idea as a Make Operation. The free plan gives you 1,000 tasks/month.'),
]
for k, v in concepts_ap:
    story.append(Paragraph(k, concept_k))
    story.append(Paragraph(v, concept_v))

# SUBSCRIPTIONS
story.append(Paragraph('Subscriptions', section_s))
story.append(tier_table([
    ['Free',       '$0',     'Unlimited flows | 1,000 tasks/month | all pieces included | Branch (if/else) included', 'YES'],
    ['Pro/Business','Varies', 'Higher task limits + team members + priority support - check activepieces.com for current pricing', 'YES'],
    ['Self-hosted', '$0',    'Unlimited everything - requires your own server setup (not recommended for beginners)', 'YES'],
]))
story.append(Spacer(1, 6))
story.append(tip('The free plan is genuinely usable for real VA work. Unlimited flows means you can build '
    'as many automations as you need. Only upgrade when you regularly hit 1,000 tasks/month.'))

# NATIVE AI
story.append(Paragraph('Native AI in ActivePieces', section_s))
story.append(ai_note(
    'ActivePieces does not have an AI scenario builder. There is no "describe your flow" feature - '
    'you build flows manually by adding steps one at a time. '
    'However, you can add an AI step inside your flow using the OpenAI piece or Anthropic piece. '
    'These let you send text from a previous step to an AI model and get a response back - '
    'useful for summarizing form responses, classifying leads, or drafting reply text. '
    'These AI pieces require your own API key (free to sign up, but you pay per use) and '
    'are billed directly by OpenAI or Anthropic, not ActivePieces.'))

# ACCOUNT SETUP
story.append(Paragraph('Part 1 - Create Your Account', section_s))
story += steps([
    ('Go to <b>activepieces.com</b> in your browser',
     'If you already have an account, log in and skip to Part 2.'),
    ('Click <b>Get started free</b> - no credit card required', None),
    ('Select <b>Continue with Google</b> and choose your work account', None),
    ('Complete any onboarding questions or skip them - click <b>Go to dashboard</b>', None),
    ('You are now in the ActivePieces dashboard. Your flows will be listed here.', None),
])

# UNDERSTANDING THE INTERFACE
story.append(Paragraph('Part 2 - Understanding the Interface', section_s))
story.append(Paragraph(
    'ActivePieces uses a vertical flow builder instead of a canvas. Steps are listed top to bottom. '
    'You add each step below the previous one. It reads like a checklist: Step 1 happens, '
    'then Step 2 happens, and so on. If you add a Branch, it splits into two vertical columns.', body_s))
story.append(concept_box(
    'The main difference from Make: ActivePieces is linear (top to bottom). '
    'Make is a canvas (you can arrange things anywhere). '
    'Both work well - linear is easier to read for beginners.'))

# BUILD A FLOW
story.append(Paragraph('Part 3 - Build Your First Flow', section_s))
story.append(Paragraph(
    'We will build the same simple automation: when a new row is added to a Google Sheet, send a Gmail. '
    'This is the core pattern used in almost every automation.', body_s))
story += steps([
    ('From the dashboard, click <b>New Flow</b> (top right)',  None),
    ('Give your flow a name (e.g. "Sheet to Gmail") and click <b>Create</b>', None),
    ('Click <b>Select Trigger</b> at the top of the flow builder', None),
    ('Search for <b>Google Sheets</b> and select it',
     'ActivePieces calls app integrations "Pieces." They appear in the search results like apps in an app store.'),
    ('Choose the trigger event: <b>New Row</b>', None),
    ('Click <b>Connect</b> next to the Google connection - sign in with your work account - click Allow',
     'You only do this once. ActivePieces saves the connection for all future flows.'),
    ('Select your spreadsheet from the dropdown, then select the sheet tab, then click <b>Save</b>', None),
    ('Click the <b>+</b> below the trigger to add the next step', None),
    ('Search for <b>Gmail</b> - select it - choose <b>Send Email</b>', None),
    ('Connect your Google account if it is not already connected',
     'ActivePieces may need a separate Google connection for Gmail vs. Sheets. Connect both if prompted.'),
    ('Fill in: To (your email), Subject (anything for now), Body (anything)',
     'Click in any field and use the data panel on the left to insert real data from your sheet - like the Name or Status column.'),
    ('Click <b>Save</b>', None),
    ('Click <b>Test Flow</b> at the top of the screen',
     'Test Flow runs the flow using your existing sheet data. Check that the email arrives in your inbox.'),
    ('Click <b>Publish</b> (top right) to turn the flow on',
     'Once published, the flow runs automatically whenever a new row is added to your sheet.'),
])

# ADDING BRANCH
story.append(Paragraph('Part 4 - Adding If/Else Logic (Branch)', section_s))
story.append(Paragraph(
    'A Branch step splits your flow into two paths: True and False. '
    'You set a condition. If the condition is met, the True path runs. '
    'If not, the False path runs. Only one path runs per piece of data - never both.', body_s))
story += steps([
    ('Inside any flow, click the <b>+</b> where you want the if/else to happen', None),
    ('Search for <b>Branch</b> - it is listed under the Core section, not an app',
     'Branch is always free. It is a built-in tool, not an app integration.'),
    ('Select Branch - it appears as a step with two columns below it: True and False', None),
    ('Click <b>Add condition</b> inside the Branch step', None),
    ('Set your condition: first field (click to select a column from your data, e.g. Status) - operator (Equals, Contains, etc.) - value (e.g. Qualified)',
     'You can add multiple conditions using AND/OR. For beginners, start with one condition.'),
    ('Click <b>Save</b>', None),
    ('Click the <b>+</b> inside the <b>True</b> path to add what happens when the condition is met', None),
    ('Add your action (e.g. Gmail - Send Email) and configure it, then click <b>Save</b>', None),
    ('Click the <b>+</b> inside the <b>False</b> path to add what happens when the condition is NOT met', None),
    ('Add a different action (e.g. Google Sheets - Update Row, or another Gmail), configure it, click <b>Save</b>', None),
    ('Click <b>Test Flow</b> - check that data went down the correct path',
     'ActivePieces shows a green or grey checkmark on each step to indicate whether it ran. Only one path will have a green checkmark per test run.'),
    ('Click <b>Publish</b> to turn the updated flow on', None),
])

story.append(Spacer(1, 8))
story.append(warning('Google Tasks is not confirmed as a stable piece in ActivePieces. '
    'If you need to create a task, use Gmail (send a task reminder email) or Google Sheets '
    '(add a row to a "Tasks" tab) instead. Both are fully supported.'))

# COMMON MISTAKES
story.append(Paragraph('Common Mistakes to Avoid', section_s))
story += steps([
    ('<b>Flow left in Draft.</b> Testing a flow does not publish it. After you finish testing, '
     'click Publish at the top right. If you see a blue Publish button, the flow is not active yet.', None),
    ('<b>Two separate Google connections.</b> ActivePieces sometimes creates separate connections '
     'for different Google apps (one for Sheets, one for Gmail). '
     'Make sure each step is connected to the same Google account.', None),
    ('<b>Branch condition does not match the data exactly.</b> If Status in your sheet is "Qualified" '
     'with a capital Q, your Branch condition must also use "Qualified" with a capital Q. '
     'A lowercase "qualified" will not match.', None),
    ('<b>Flow runs but nothing happens on the False path.</b> If you did not add any steps inside the False path, '
     'nothing will happen for data that does not match your condition. That is fine - just make sure it is intentional.', None),
])

# FOOTER
story.append(Spacer(1, 24))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=10))
story.append(Paragraph(
    'KeyPlayers HQ  |  KP VA AI Training Program  |  Make &amp; ActivePieces Tutorial  |  '
    'Prices accurate as of mid-2025 - verify at make.com and activepieces.com before use.',
    footer_s))

doc.build(story)
print('Done:', OUTPUT)

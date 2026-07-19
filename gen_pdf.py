from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = r'C:\Users\jervi\OneDrive\Documents\Claude\Projects\KP AI TRAINING\github-push\VA-Automation-Examples.pdf'

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
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

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title2',
    fontName='Helvetica-Bold', fontSize=20, textColor=DARK_GREEN,
    spaceAfter=4, alignment=TA_CENTER, leading=26)

subtitle_style = ParagraphStyle('Subtitle',
    fontName='Helvetica', fontSize=10, textColor=GRAY_TEXT,
    spaceAfter=2, alignment=TA_CENTER)

auto_heading = ParagraphStyle('AutoHeading',
    fontName='Helvetica-Bold', fontSize=13, textColor=colors.white,
    spaceBefore=0, spaceAfter=0, leading=18)

part_heading = ParagraphStyle('PartHeading',
    fontName='Helvetica-Bold', fontSize=10.5, textColor=MID_GREEN,
    spaceBefore=14, spaceAfter=6, leading=14)

body = ParagraphStyle('Body2',
    fontName='Helvetica', fontSize=9.5, textColor=GRAY_TEXT,
    spaceAfter=4, leading=15)

step_style = ParagraphStyle('Step',
    fontName='Helvetica', fontSize=9.5, textColor=GRAY_TEXT,
    spaceAfter=3, leading=14, leftIndent=6)

step_note = ParagraphStyle('StepNote',
    fontName='Helvetica-Oblique', fontSize=8.5, textColor=ACCENT,
    spaceAfter=2, leading=13, leftIndent=6)

pill_style = ParagraphStyle('Pill',
    fontName='Helvetica-Bold', fontSize=8, textColor=MID_GREEN)

footer_style = ParagraphStyle('Footer',
    fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#999999'),
    alignment=TA_CENTER)


def section_header(tool_pills, title, desc):
    pill_text = '  '.join(['[ ' + p + ' ]' for p in tool_pills])
    sub_style = ParagraphStyle('ph2',
        fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#CCEECC'), leading=13)
    tbl = Table([
        [Paragraph(title, auto_heading)],
        [Paragraph(pill_text + '  -  ' + desc, sub_style)]
    ], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), MID_GREEN),
        ('TOPPADDING',    (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,-1),(-1,-1), 10),
        ('TOPPADDING',    (0,1), (-1,1), 2),
        ('LEFTPADDING',   (0,0), (-1,-1), 16),
        ('RIGHTPADDING',  (0,0), (-1,-1), 16),
    ]))
    return tbl


def note_box(text):
    nb_style = ParagraphStyle('nb',
        fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#1A4A2A'), leading=14)
    tbl = Table([[Paragraph('<b>Note:</b>  ' + text, nb_style)]], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GREEN),
        ('LINEBEFORE', (0,0), (0,-1), 3, ACCENT),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    return tbl


def drill_box(text):
    db_style = ParagraphStyle('db',
        fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#5C4000'), leading=14)
    tbl = Table([[Paragraph('<b>Practice:</b>  ' + text, db_style)]], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GOLD_BG),
        ('LINEBEFORE', (0,0), (0,-1), 3, GOLD_BORDER),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    return tbl


def make_steps(items):
    result = []
    for i, item in enumerate(items, 1):
        if isinstance(item, tuple):
            text, note = item
        else:
            text, note = item, None

        num_style = ParagraphStyle('num',
            fontName='Helvetica-Bold', fontSize=9, textColor=colors.white,
            alignment=TA_CENTER, leading=12)
        num = Paragraph('<b>' + str(i) + '</b>', num_style)
        num_cell = Table([[num]], colWidths=[0.26*inch], rowHeights=[0.26*inch])
        num_cell.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), MID_GREEN),
            ('TOPPADDING',    (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ]))

        content = [Paragraph(text, step_style)]
        if note:
            content.append(Paragraph(note, step_note))

        row_tbl = Table([[num_cell, content]], colWidths=[0.38*inch, 6.12*inch])
        row_tbl.setStyle(TableStyle([
            ('VALIGN',        (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ]))
        result.append(row_tbl)
        result.append(Spacer(1, 5))
    return result


def condition_table(rows):
    data = [[Paragraph('<b>Condition</b>', pill_style), Paragraph('<b>Action</b>', pill_style)]] + rows
    t = Table(data, colWidths=[2.8*inch, 3.7*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), DARK_GREEN),
        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LIGHT_GRAY]),
        ('GRID',         (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
    ]))
    return t


# ─── BUILD STORY ──────────────────────────────────────────────────────────────
story = []

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph('VA Automation Examples', title_style))
story.append(Paragraph('If/Else Conditions with Make &amp; ActivePieces  |  Google Workspace', subtitle_style))
story.append(Spacer(1, 6))
story.append(HRFlowable(width='100%', thickness=1.5, color=MID_GREEN, spaceAfter=18))

# ── AUTOMATION 1 ──────────────────────────────────────────────────────────────
story.append(section_header(
    ['Make.com', 'Gmail'],
    'Automation 1 - Gmail Label Router',
    'Reads incoming emails and labels them based on subject or sender'
))
story.append(Spacer(1, 10))
story.append(Paragraph('What it does', part_heading))
story.append(Paragraph('Checks every new email and automatically sorts it into a Gmail label.', body))
story.append(condition_table([
    ['Subject contains "invoice"', 'Apply label "Invoices" + star the email'],
    ['Sender from your client domain', 'Apply label "Clients"'],
    ['Neither', 'Do nothing'],
]))
story.append(Spacer(1, 8))

story.append(Paragraph('Part 1 - Account Setup (do once)', part_heading))
story += make_steps([
    ('Go to <b>make.com</b> - Sign up free - click <b>Create a new scenario</b>', None),
    ('Click the <b>+</b> on the canvas - search <b>Gmail</b> - select <b>Watch Emails</b>', None),
    ('Click <b>Add</b> next to Google connection - sign in - click <b>Allow</b>',
     'A Google login popup will appear. Select your work account.'),
    ('Set Folder to <b>Inbox</b>, Max results to <b>5</b> - click <b>OK</b>', None),
])

story.append(Paragraph('Part 2 - Add the Router (the If/Else)', part_heading))
story += make_steps([
    ('Click <b>+</b> after the Gmail circle - search <b>Router</b> - select it',
     'A Router splits one path into two separate branches.'),
    ('You will now see two empty route boxes coming out of the Router', None),
])

story.append(Paragraph('Part 3 - Route 1: Invoice Emails', part_heading))
story += make_steps([
    ('Click the <b>wrench icon</b> on Route 1 - label it: Route 1 - Invoices', None),
    ('Add rule: <b>Subject</b> | <b>Contains (case insensitive)</b> | type  invoice  - click <b>OK</b>', None),
    ('Click <b>+</b> at end of Route 1 - Gmail - Add a Label to an Email', None),
    ('Map <b>Message ID</b> from the left panel - Label Name: select <b>Invoices</b> from the dropdown',
     'The label must already exist in Gmail before Make can find it. Go to Gmail first, create the label "Invoices," then come back here.'),
    ('Click <b>+</b> again - Gmail - Modify an Email - map Message ID - set <b>Starred</b> to <b>Yes</b> - click <b>OK</b>', None),
])

story.append(Paragraph('Part 4 - Route 2: Client Emails', part_heading))
story += make_steps([
    ('Click the <b>wrench icon</b> on Route 2 - label it: Route 2 - Clients', None),
    ('Add rule: <b>From</b> | <b>Contains</b> | type your client\'s email domain (e.g. acmecorp.com) - click <b>OK</b>',
     'You only need the domain - everything after the @.'),
    ('Gmail - Add a Label - map Message ID - select <b>Clients</b> from the dropdown - click <b>OK</b>',
     'Same rule: create the "Clients" label in Gmail first, then it will appear in the dropdown here.'),
])

story.append(Paragraph('Part 5 - Test and Turn On', part_heading))
story += make_steps([
    ('Click <b>Run once</b> (bottom left) - Make processes your last 5 emails through both routes', None),
    ('Open Gmail - check that matching emails have the correct labels', None),
    ('Click the <b>toggle switch</b> at the bottom to turn the scenario <b>ON</b>',
     'Once ON, Make checks for new emails every 15 minutes on the free plan.'),
])

story.append(Spacer(1, 8))
story.append(drill_box(
    'Look at your last 10 emails and decide what two labels would be most useful for YOUR inbox. '
    'Build this scenario using your own label names and filter words instead.'
))
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))

# ── AUTOMATION 2 ──────────────────────────────────────────────────────────────
story.append(section_header(
    ['Make.com', 'Google Forms', 'Gmail', 'Google Sheets'],
    'Automation 2 - Google Form to Conditional Email',
    'Urgent submissions email the manager; normal ones go to a spreadsheet log'
))
story.append(Spacer(1, 10))
story.append(Paragraph('What it does', part_heading))
story.append(Paragraph('Checks the Urgency Level answer on every form submission and takes a different action depending on the answer.', body))
story.append(condition_table([
    ['Urgency Level = "High"', 'Send urgent email alert to manager immediately'],
    ['Anything else (Normal)', 'Log the submission to a Google Sheet only'],
]))
story.append(Spacer(1, 8))

story.append(Paragraph('Part 1 - Build the Google Form', part_heading))
story += make_steps([
    ('Go to <b>forms.google.com</b> - new blank form - title it: Task Request Form', None),
    ('Question 1: Your Name - leave type as Short answer', None),
    ('Click Add question - type: Urgency Level - change type to <b>Dropdown</b>', None),
    ('Add two options: High and Normal', None),
    ('Click the eye icon (Preview) - submit two test responses: one High, one Normal',
     'Make needs real data to detect your form fields. Do not skip this step.'),
])

story.append(Paragraph('Part 2 - Create a Google Sheet for Logging', part_heading))
story += make_steps([
    ('Go to <b>sheets.google.com</b> - new spreadsheet - name it: Task Request Log', None),
    ('Row 1 headers: Name | Urgency | Date Submitted', None),
])

story.append(Paragraph('Part 3 - Set Up Make', part_heading))
story += make_steps([
    ('In Make, new scenario - click + - search Google Forms - select Watch Responses', None),
    ('Connect your Google account if prompted', None),
    ('Under Spreadsheet, find and select the <b>spreadsheet linked to your form</b> - Max results: 5 - click OK',
     'Make connects to the spreadsheet where Google Forms stores responses, not the form itself. Open your form in Google Forms, click Responses at the top, then the Sheets icon to find the linked spreadsheet name.'),
    ('Click + after Google Forms - add Router', None),
])

story.append(Paragraph('Part 4 - Route 1: High Urgency - Email the Manager', part_heading))
story += make_steps([
    ('Wrench on Route 1 - label it: Route 1 - High', None),
    ('Rule: Urgency Level | Equal to | High - click OK', None),
    ('Add action: Gmail - Send an Email', None),
    ('To: manager\'s email  |  Subject: URGENT Task Request from {{Your Name}} (insert form field)  |  Body: short alert message', None),
    ('Click OK', None),
])

story.append(Paragraph('Part 5 - Route 2: Normal - Log to Sheet', part_heading))
story += make_steps([
    ('Wrench on Route 2 - label: Route 2 - Normal - leave NO filter rules - click OK',
     'No filter = catches everything that did not match Route 1. This is your "else."'),
    ('Add action: Google Sheets - Add a Row', None),
    ('Select Task Request Log - map: Name to Your Name field | Urgency to Urgency Level field | Date Submitted: type {{now}}', None),
    ('Click OK', None),
])

story.append(Paragraph('Part 6 - Test and Turn On', part_heading))
story += make_steps([
    ('Click Run once - check Gmail for the URGENT email and check your Sheet for the Normal row', None),
    ('If both worked, toggle the scenario ON', None),
])

story.append(Spacer(1, 8))
story.append(drill_box(
    'Think of a form you currently fill out or receive in your work. What one question could you add an '
    'if/else rule to? Write out the logic: "If the answer is ___, then ___. Otherwise, ___." '
    'You do not need to build it - just write the logic.'
))
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))

# ── AUTOMATION 3 ──────────────────────────────────────────────────────────────
story.append(section_header(
    ['ActivePieces', 'Google Sheets', 'Gmail'],
    'Automation 3 - Google Sheet to Conditional Email',
    'Qualified leads send a follow-up email; everything else sends a review email'
))
story.append(Spacer(1, 10))
story.append(Paragraph('What it does', part_heading))
story.append(Paragraph('When a new row is added to your lead tracker, checks the Status column and takes a different action.', body))
story.append(condition_table([
    ['Status = "Qualified"', 'Send a follow-up email to the person who handles qualified leads'],
    ['Anything else (Junk, No Show, etc.)', 'Send a review email so someone can check it'],
]))
story.append(Spacer(1, 8))

story.append(Paragraph('Part 1 - Build the Google Sheet', part_heading))
story += make_steps([
    ('Go to <b>sheets.google.com</b> - new spreadsheet - name it: Lead Tracker', None),
    ('Row 1 headers: Name | Status | VA Name | Date', None),
    ('Add two test rows:  Row 2: Test Lead 1 | Qualified | Sarah | today\'s date   Row 3: Test Lead 2 | Junk | Sarah | today\'s date', None),
])

story.append(Paragraph('Part 2 - Sign Up for ActivePieces', part_heading))
story += make_steps([
    ('Go to <b>activepieces.com</b> - click Get started free',
     'No credit card required. You can sign up with your Google account.'),
    ('Click New Flow - name it: Lead Status Router - click Create', None),
])

story.append(Paragraph('Part 3 - Set Up the Trigger', part_heading))
story += make_steps([
    ('Click Select Trigger - search Google Sheets - choose New Row', None),
    ('Connect your Google account - select Lead Tracker - select the sheet tab - click Save', None),
])

story.append(Paragraph('Part 4 - Add the Branch (Your If/Else)', part_heading))
story += make_steps([
    ('Click + below the trigger - search Branch - select it',
     'In ActivePieces, a Branch is the if/else step.'),
    ('Click Add condition - first field: select Status from the sheet data | Operator: Equals | Value: Qualified',
     'Use a capital Q - it must match the text in your sheet exactly.'),
    ('Click Save', None),
])

story.append(Paragraph('Part 5 - True Path: Qualified - Send a Follow-Up Email', part_heading))
story += make_steps([
    ('Under True, click + - search Gmail - select Send Email', None),
    ('To: your own email (or whoever handles follow-ups)  |  Subject: Follow up with {{Name}} - Qualified Lead  |  Body: {{Name}} was marked Qualified by {{VA Name}} on {{Date}}. Add them to your follow-up list.',
     'Click in each field and select the matching column from the sheet data on the left.'),
    ('Click Save', None),
])

story.append(Paragraph('Part 6 - False Path: Everything Else - Send Email', part_heading))
story += make_steps([
    ('Under False, click + - search Gmail - select Send Email', None),
    ('To: your email or manager\'s  |  Subject: Lead marked {{Status}} - needs review  |  Body: short summary with Name, Status, VA Name', None),
    ('Click Save', None),
])

story.append(Paragraph('Part 7 - Test and Publish', part_heading))
story += make_steps([
    ('Click Test Flow at the top', None),
    ('Check tasks.google.com - "Follow up with Test Lead 1" should appear as a new task', None),
    ('Check Gmail - review email about Test Lead 2 (Junk) should be there', None),
    ('If both worked, click Publish (top right) to turn the flow on',
     'Once published, the flow triggers automatically every time a new row is added to your sheet.'),
])

story.append(Spacer(1, 8))
story.append(drill_box(
    'Think through the logic for more statuses. Write it out: '
    'If Status = "Callback" -> do what?  '
    'If Status = "No Show" -> do what?  '
    'If Status = "Cold" -> do what?  '
    'You do not need to build it - write the logic first.'
))

# ── FOOTER ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 24))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=10))
story.append(Paragraph('KeyPlayers HQ  |  KP VA AI Training Program  |  Automation Basics', footer_style))

doc.build(story)
print('Done:', OUTPUT)

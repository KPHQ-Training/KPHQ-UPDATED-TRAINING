from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER

OUTPUT = r'C:\Users\jervi\OneDrive\Documents\Claude\Projects\KP AI TRAINING\github-push\VA-n8n-Automation-Example.pdf'

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
N8N_COLOR   = colors.HexColor('#2A1F4A')   # n8n brand is a deep purple-navy
N8N_ACCENT  = colors.HexColor('#EA4B71')   # n8n pink accent

def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9.5, textColor=GRAY_TEXT, leading=15, spaceAfter=4)
    d.update(kw)
    return ParagraphStyle(name, **d)

title_s   = S('T',  fontName='Helvetica-Bold', fontSize=20, textColor=DARK_GREEN, alignment=TA_CENTER, leading=26, spaceAfter=4)
sub_s     = S('Su', fontSize=10, textColor=colors.HexColor('#555555'), alignment=TA_CENTER, spaceAfter=2)
disc_s    = S('D',  fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#888888'), alignment=TA_CENTER)
tool_hd   = S('TH', fontName='Helvetica-Bold', fontSize=13, textColor=colors.white, leading=18)
tool_sub  = S('TS', fontSize=8.5, textColor=colors.HexColor('#CCCCDD'), leading=13)
section_s = S('SE', fontName='Helvetica-Bold', fontSize=10.5, textColor=MID_GREEN, spaceBefore=14, spaceAfter=6, leading=14)
body_s    = S('B')
step_s    = S('ST', leftIndent=6, spaceAfter=3, leading=14)
note_s    = S('N',  fontName='Helvetica-Oblique', fontSize=8.5, textColor=ACCENT, leftIndent=6, spaceAfter=2, leading=13)
pill_s    = S('P',  fontName='Helvetica-Bold', fontSize=8, textColor=MID_GREEN)
footer_s  = S('F',  fontSize=8, textColor=colors.HexColor('#999999'), alignment=TA_CENTER)
concept_k = S('CK', fontName='Helvetica-Bold', fontSize=9, textColor=DARK_GREEN, leading=13, spaceAfter=1)
concept_v = S('CV', fontSize=9, textColor=GRAY_TEXT, leading=13, spaceAfter=6, leftIndent=10)


def tool_header(title, subtitle):
    tbl = Table([
        [Paragraph(title, tool_hd)],
        [Paragraph(subtitle, tool_sub)],
    ], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), N8N_COLOR),
        ('TOPPADDING',    (0,0),(-1,0),  12),
        ('TOPPADDING',    (0,1),(-1,1),  2),
        ('BOTTOMPADDING', (0,-1),(-1,-1),10),
        ('LEFTPADDING',   (0,0),(-1,-1), 16),
        ('RIGHTPADDING',  (0,0),(-1,-1), 16),
    ]))
    return tbl


def callout(bg_hex, border_hex, label, text):
    cs = S('CB', fontSize=9, textColor=GRAY_TEXT, leading=14)
    tbl = Table([[Paragraph('<b>' + label + '</b>  ' + text, cs)]], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor(bg_hex)),
        ('LINEBEFORE',    (0,0),(0,-1),  3, colors.HexColor(border_hex)),
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('LEFTPADDING',   (0,0),(-1,-1), 14),
        ('RIGHTPADDING',  (0,0),(-1,-1), 14),
    ]))
    return tbl

tip     = lambda t: callout('#E8F5EA', '#2A6636', 'Tip:', t)
warning = lambda t: callout('#FDF0F0', '#C0392B', 'Watch out:', t)
ai_note = lambda t: callout('#F5F0FD', '#6C3483', 'Native AI:', t)
note    = lambda t: callout('#F0F4F0', '#2A6636', 'Note:', t)


def steps(items):
    out = []
    for i, item in enumerate(items, 1):
        text, n = item if isinstance(item, tuple) else (item, None)
        num = Paragraph('<b>' + str(i) + '</b>',
            S('NM', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, alignment=TA_CENTER, leading=12))
        nc = Table([[num]], colWidths=[0.26*inch], rowHeights=[0.26*inch])
        nc.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), MID_GREEN),
            ('TOPPADDING',    (0,0),(-1,-1), 1), ('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('LEFTPADDING',   (0,0),(-1,-1), 0), ('RIGHTPADDING',  (0,0),(-1,-1),0),
        ]))
        content = [Paragraph(text, step_s)]
        if n:
            content.append(Paragraph(n, note_s))
        rt = Table([[nc, content]], colWidths=[0.38*inch, 6.12*inch])
        rt.setStyle(TableStyle([
            ('VALIGN',        (0,0),(-1,-1),'TOP'),
            ('TOPPADDING',    (0,0),(-1,-1),0), ('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('LEFTPADDING',   (0,0),(-1,-1),0), ('RIGHTPADDING',  (0,0),(-1,-1),0),
        ]))
        out.append(rt)
        out.append(Spacer(1, 5))
    return out


def tier_table(rows):
    hdr = [Paragraph('<b>' + h + '</b>', pill_s) for h in ['Plan', 'Cost', 'What you get', 'If/Else?']]
    t = Table([hdr] + rows, colWidths=[1.1*inch, 1.0*inch, 3.4*inch, 1.0*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0), DARK_GREEN),
        ('TEXTCOLOR',     (0,0),(-1,0), colors.white),
        ('FONTNAME',      (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',      (0,0),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LIGHT_GRAY]),
        ('GRID',          (0,0),(-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING',    (0,0),(-1,-1), 7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',   (0,0),(-1,-1), 8), ('RIGHTPADDING', (0,0),(-1,-1),8),
        ('VALIGN',        (0,0),(-1,-1),'TOP'),
    ]))
    return t


def condition_table(rows):
    data = [[Paragraph('<b>Condition</b>', pill_s), Paragraph('<b>Action</b>', pill_s)]] + rows
    t = Table(data, colWidths=[2.8*inch, 3.7*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0), DARK_GREEN),
        ('TEXTCOLOR',     (0,0),(-1,0), colors.white),
        ('FONTNAME',      (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',      (0,0),(-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LIGHT_GRAY]),
        ('GRID',          (0,0),(-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING',    (0,0),(-1,-1), 7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),('RIGHTPADDING', (0,0),(-1,-1),10),
    ]))
    return t


# ─────────────────────────────────────────────────────────────────────────────
story = []

# TITLE
story.append(Spacer(1, 0.05*inch))
story.append(Paragraph('n8n Automation Example', title_s))
story.append(Paragraph('If/Else Logic with Google Workspace', sub_s))
story.append(Paragraph('Beginner to intermediate  |  Includes subscription &amp; native AI info', disc_s))
story.append(Spacer(1, 6))
story.append(HRFlowable(width='100%', thickness=1.5, color=N8N_COLOR, spaceAfter=14))

# WHAT IS N8N
story.append(KeepTogether([
    tool_header('n8n', 'Open-source automation tool  |  cloud.n8n.io  |  Self-host for free or use the cloud'),
    Spacer(1, 10),
]))

story.append(Paragraph('What Is n8n?', section_s))
story.append(Paragraph(
    'n8n is an open-source automation tool - meaning anyone can download and run it on their own computer '
    'or server for free with no usage limits. For VAs who don\'t want to manage their own server, '
    'n8n also offers a paid cloud version at cloud.n8n.io. '
    'The interface uses a visual canvas similar to Make - you connect nodes (steps) with lines.', body_s))
story.append(Paragraph(
    'n8n is more powerful and more technical than Make or ActivePieces. It is a good step up '
    'once you are comfortable with basic automations and want more control.', body_s))

story.append(Paragraph('Key Concepts', section_s))
for k, v in [
    ('Workflow',   'One complete automation. Same idea as a Scenario in Make or a Flow in ActivePieces.'),
    ('Node',       'One step inside a workflow - e.g. a Google Sheets node, a Gmail node, an IF node. Same idea as a Module in Make.'),
    ('Execution',  'One run of a workflow. Same idea as an Operation (Make) or Task (ActivePieces). Cloud plans have monthly limits.'),
    ('IF Node',    'The if/else node. Has two output paths: TRUE and FALSE. Works like Make\'s Router or ActivePieces\' Branch.'),
    ('Switch Node','An advanced version of the IF node. Lets you create more than two paths - one for each possible value.'),
    ('Trigger',    'The first node in every workflow. Defines what event starts the automation.'),
]:
    story.append(Paragraph(k, concept_k))
    story.append(Paragraph(v, concept_v))

# SUBSCRIPTIONS
story.append(Paragraph('Subscriptions', section_s))
story.append(tier_table([
    ['Self-hosted',  '$0',       'Unlimited workflows, unlimited executions, all nodes included. Requires setting up your own server - not recommended for non-technical VAs.', 'YES'],
    ['Starter Cloud','$20/mo',   '2,500 executions/month, 5 active workflows, access to all integrations including Google Workspace nodes', 'YES'],
    ['Pro Cloud',    '$50/mo',   '10,000 executions/month, 15 active workflows, version history, custom variables', 'YES'],
    ['Enterprise',   'Custom',   'Unlimited everything, SSO, on-premise option, SLA support', 'YES'],
]))
story.append(Spacer(1, 6))
story.append(warning(
    'The n8n Cloud free trial lasts 14 days. After that, you must be on a paid plan to keep your '
    'workflows running in the cloud. If you want a free option with no time limit, you need to '
    'self-host - which requires technical setup. For VAs who want free automation with if/else, '
    'Make (free) or ActivePieces (free) are easier starting points.'))

# NATIVE AI
story.append(Paragraph('Native AI in n8n', section_s))
story.append(ai_note(
    'n8n has an AI Assistant that helps you build workflows by describing what you want in plain language. '
    'It is available on paid cloud plans (Starter and above). '
    'n8n also has a built-in AI Agent node (powered by LangChain) that can reason through tasks, '
    'use tools, and chain multiple AI calls together - more advanced than what Make or ActivePieces offer. '
    'Like the other tools, adding OpenAI, Anthropic, or other AI models as nodes requires your own API key, '
    'billed directly by the AI provider. '
    'To use the AI Assistant on a paid plan: open any workflow and look for the AI chat icon '
    'in the top right corner of the canvas.'))

story.append(Spacer(1, 8))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=14))

# THE AUTOMATION EXAMPLE
story.append(Paragraph('Automation Example — Lead Budget Router', section_s))

pill_row = [
    Paragraph('<b>n8n</b>', S('PR', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white,
        leading=12, alignment=TA_CENTER)),
    Paragraph('<b>Google Sheets</b>', S('PR2', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white,
        leading=12, alignment=TA_CENTER)),
    Paragraph('<b>Gmail</b>', S('PR3', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white,
        leading=12, alignment=TA_CENTER)),
]
pill_tbl = Table([pill_row], colWidths=[1.3*inch, 1.7*inch, 1.3*inch])
pill_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(0,0), N8N_COLOR),
    ('BACKGROUND',    (1,0),(1,0), DARK_GREEN),
    ('BACKGROUND',    (2,0),(2,0), colors.HexColor('#1A3A1A')),
    ('TOPPADDING',    (0,0),(-1,-1), 5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',   (0,0),(-1,-1), 8), ('RIGHTPADGIN',  (0,0),(-1,-1),8),
    ('ROUNDEDCORNERS',[4]),
]))
story.append(pill_tbl)
story.append(Spacer(1, 10))

story.append(Paragraph(
    'When a new lead is added to a Google Sheet, check their estimated budget. '
    'If the budget is high, email the senior account manager. '
    'If the budget is low, email the VA assigned to handle smaller accounts.', body_s))

story.append(Paragraph('What This Automation Does', section_s))
story.append(condition_table([
    ['Budget column = "High"',  'Send Gmail to senior account manager with lead details'],
    ['Budget column = "Low"',   'Send Gmail to junior VA with lead details'],
]))
story.append(Spacer(1, 10))
story.append(note(
    'This is the same if/else shape as the other tool examples, shown here in n8n\'s interface. '
    'The logic is identical - only the tool and terminology differ.'))

# PREP
story.append(Paragraph('Before You Start', section_s))
story += steps([
    ('Go to <b>cloud.n8n.io</b> and sign up for the 14-day free trial',
     'Use your Google account for fastest signup. No credit card required for the trial.'),
    ('Create a Google Sheet called <b>Lead Tracker</b> with these column headers in Row 1: Name | Budget | Email | VA Name',
     'Budget values should be exactly "High" or "Low" (capital first letter) - the IF node will match against these exactly.'),
    ('Add two test rows:  Row 2: Alex Chen | High | alex@example.com | Sarah   Row 3: Jamie Lee | Low | jamie@example.com | Sarah', None),
])

# BUILD THE WORKFLOW
story.append(Paragraph('Part 1 - Create the Workflow', section_s))
story += steps([
    ('From the n8n dashboard, click <b>New Workflow</b> (top right or center button)',  None),
    ('You will see a blank canvas with a single node in the center labeled "When clicking Test workflow" - ignore this for now',
     'This is n8n\'s manual test trigger. You will replace it with a real trigger in the next step.'),
    ('Click the <b>+</b> icon to the right of the default node to add your first real node',
     'In n8n, nodes connect left to right. The flow reads left to right across the canvas.'),
])

story.append(Paragraph('Part 2 - Set Up the Trigger', section_s))
story += steps([
    ('In the node search panel, type <b>Google Sheets</b> and select it', None),
    ('Under "Select a trigger", choose <b>Row Added</b>',
     'This fires every time a new row appears in your spreadsheet.'),
    ('Click <b>Credential for Google Sheets API</b> - click <b>Create New Credential</b>',
     'n8n connects to Google via OAuth. A Google sign-in window will open. Select your work account and click Allow.'),
    ('Under <b>Document</b>, click the dropdown and select your <b>Lead Tracker</b> spreadsheet',
     'If it doesn\'t appear, click "Refresh list" or paste the spreadsheet URL directly into the field.'),
    ('Under <b>Sheet</b>, select the sheet tab (usually Sheet1)', None),
    ('Click <b>Save</b> in the top right of the node panel', None),
])

story.append(Paragraph('Part 3 - Add the IF Node (the If/Else)', section_s))
story += steps([
    ('Click the <b>+</b> to the right of the Google Sheets node to add the next node', None),
    ('Search for <b>IF</b> and select it - it is listed under the Core category',
     'The IF node is always free. It is a built-in n8n tool, not an app integration.'),
    ('In the IF node panel, click <b>Add condition</b>', None),
    ('Set the condition:',
     'First field: click "Add Value" - in the panel that opens on the left, find your Google Sheets data and select the Budget column. '
     'Operator: select "Equal". '
     'Second field: type  High  (with a capital H).'),
    ('Click <b>Save</b>',
     'The IF node now shows two outputs: TRUE (when Budget equals High) and FALSE (everything else).'),
])

story.append(Paragraph('Part 4 - TRUE Path: High Budget - Email Senior Manager', section_s))
story += steps([
    ('Click the <b>+</b> on the <b>TRUE</b> output of the IF node',
     'The TRUE output is on the top right of the IF node. FALSE is on the bottom right.'),
    ('Search for <b>Gmail</b> and select it - choose <b>Send Email</b> as the action', None),
    ('Connect your Google account credential (same process as before - click Create New Credential if needed)', None),
    ('Fill in the email fields:',
     'To: your senior account manager\'s email address. '
     'Subject: click "Add Expression" - type: New HIGH budget lead: then select the Name column from the left panel. '
     'Message: type your message and insert the Name, Email, and Budget fields from the left panel.'),
    ('Click <b>Save</b>', None),
])

story.append(Paragraph('Part 5 - FALSE Path: Low Budget - Email VA', section_s))
story += steps([
    ('Click the <b>+</b> on the <b>FALSE</b> output of the IF node',
     'Everything that is NOT "High" - including "Low" and any other value - goes down the FALSE path.'),
    ('Search for <b>Gmail</b> - select <b>Send Email</b>', None),
    ('Use the same credential. Fill in:',
     'To: the VA\'s email address. '
     'Subject: New lead assigned - insert Name from the left panel. '
     'Message: include Name, Email, Budget from the data panel.'),
    ('Click <b>Save</b>', None),
])

story.append(Paragraph('Part 6 - Test and Activate', section_s))
story += steps([
    ('Click <b>Test workflow</b> (top center button)',
     'n8n will run the workflow using the data in your sheet. It processes existing rows as a test.'),
    ('Watch the canvas - each node lights up green as it runs. Check for any red error nodes.',
     'If a node turns red, click on it to see the error message. Most common issue: Google credential not connected.'),
    ('Check Gmail - you should have received two emails: one for the High budget lead, one for the Low budget lead', None),
    ('Click the <b>Inactive</b> toggle at the top right of the canvas to switch it to <b>Active</b>',
     'Once Active, the workflow watches your sheet automatically and runs whenever a new row is added.'),
])

story.append(Spacer(1, 8))
story.append(tip(
    'n8n shows you the exact data flowing through each node during a test run. '
    'Click any node after testing to see the input data it received and the output it produced. '
    'This makes it much easier to debug than Make or ActivePieces.'))

story.append(Spacer(1, 10))

# DRILL BOX
drill_tbl = Table([[Paragraph(
    '<b>Practice:</b>  Change the condition from Budget = "High" to a different column. '
    'What if you checked the Source column instead? '
    'If Source = "Referral" - email one person. If Source = "Cold Outreach" - email someone else. '
    'The shape is the same - only the column and values change.',
    S('DB', fontSize=9, textColor=colors.HexColor('#5C4000'), leading=14)
)]], colWidths=[6.5*inch])
drill_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), GOLD_BG),
    ('LINEBEFORE',    (0,0),(0,-1),  3, GOLD_BORDER),
    ('TOPPADDING',    (0,0),(-1,-1), 10),
    ('BOTTOMPADDING', (0,0),(-1,-1), 10),
    ('LEFTPADDING',   (0,0),(-1,-1), 14),
    ('RIGHTPADDING',  (0,0),(-1,-1), 14),
]))
story.append(drill_tbl)

# N8N VS OTHERS
story.append(Spacer(1, 14))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=14))
story.append(Paragraph('How n8n Compares to Make and ActivePieces', section_s))

comp_data = [
    [Paragraph('<b></b>', pill_s),
     Paragraph('<b>n8n</b>', pill_s),
     Paragraph('<b>Make</b>', pill_s),
     Paragraph('<b>ActivePieces</b>', pill_s)],
    ['Free option', 'Self-host only (technical)', 'Yes - 2 scenarios', 'Yes - unlimited flows'],
    ['Cloud free tier', 'No (14-day trial only)', 'Yes - 1,000 ops/month', 'Yes - 1,000 tasks/month'],
    ['If/else on free', 'Self-host only', 'YES', 'YES'],
    ['Paid starts at', '$20/month (cloud)', '$9/month', 'Varies'],
    ['AI builder', 'Paid plans (Starter+)', 'Paid plans (Core+)', 'None'],
    ['AI Agent node', 'YES (advanced)', 'No', 'No'],
    ['Best for', 'Advanced flows, devs, power users', 'Complex multi-step flows', 'Beginners, tight budget'],
]
comp_table = Table(comp_data, colWidths=[1.5*inch, 1.6*inch, 1.6*inch, 1.8*inch])
comp_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0), DARK_GREEN),
    ('TEXTCOLOR',     (0,0),(-1,0), colors.white),
    ('FONTNAME',      (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTNAME',      (0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',      (0,0),(-1,-1), 8.5),
    ('BACKGROUND',    (0,1),(0,-1),  colors.HexColor('#F0F4F0')),
    ('ROWBACKGROUNDS',(1,1),(-1,-1), [colors.white, LIGHT_GRAY]),
    ('GRID',          (0,0),(-1,-1), 0.5, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',    (0,0),(-1,-1), 7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
    ('LEFTPADDING',   (0,0),(-1,-1), 8), ('RIGHTPADDING', (0,0),(-1,-1),8),
    ('VALIGN',        (0,0),(-1,-1),'TOP'),
]))
story.append(comp_table)
story.append(Spacer(1, 8))
story.append(note(
    'n8n is the most powerful of the three tools but also the least beginner-friendly and the most expensive '
    'for cloud use. Recommend Make or ActivePieces for VAs starting out. '
    'Introduce n8n once they are comfortable with if/else logic and want to build more complex flows.'))

# FOOTER
story.append(Spacer(1, 20))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=8))
story.append(Paragraph(
    'KeyPlayers HQ  |  KP VA AI Training Program  |  n8n Automation Example  |  '
    'Prices accurate as of mid-2025 - verify at n8n.io before use.',
    footer_s))

doc.build(story)
print('Done:', OUTPUT)

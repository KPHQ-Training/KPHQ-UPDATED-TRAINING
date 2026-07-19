from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER

OUTPUT = r'C:\Users\jervi\OneDrive\Documents\Claude\Projects\KP AI TRAINING\github-push\VA-n8n-Tutorial.pdf'

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
N8N_COLOR   = colors.HexColor('#2A1F4A')

def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9.5, textColor=GRAY_TEXT, leading=15, spaceAfter=4)
    d.update(kw)
    return ParagraphStyle(name, **d)

title_s   = S('T',  fontName='Helvetica-Bold', fontSize=20, textColor=DARK_GREEN, alignment=TA_CENTER, leading=26, spaceAfter=4)
sub_s     = S('Su', fontSize=10, textColor=colors.HexColor('#555555'), alignment=TA_CENTER, spaceAfter=2)
disc_s    = S('D',  fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#888888'), alignment=TA_CENTER)
tool_hd   = S('TH', fontName='Helvetica-Bold', fontSize=15, textColor=colors.white, leading=20)
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
    tbl = Table([[Paragraph(title, tool_hd)], [Paragraph(subtitle, tool_sub)]], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), N8N_COLOR),
        ('TOPPADDING',    (0,0),(-1,0),  14),
        ('TOPPADDING',    (0,1),(-1,1),  2),
        ('BOTTOMPADDING', (0,-1),(-1,-1),12),
        ('LEFTPADDING',   (0,0),(-1,-1), 18),
        ('RIGHTPADDING',  (0,0),(-1,-1), 18),
    ]))
    return tbl

def callout(bg_hex, border_hex, label, text):
    cs = S('CB', fontSize=9, textColor=GRAY_TEXT, leading=14)
    tbl = Table([[Paragraph('<b>' + label + '</b>  ' + text, cs)]], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor(bg_hex)),
        ('LINEBEFORE',    (0,0),(0,-1),  3, colors.HexColor(border_hex)),
        ('TOPPADDING',    (0,0),(-1,-1), 10), ('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',   (0,0),(-1,-1), 14), ('RIGHTPADDING', (0,0),(-1,-1),14),
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
            ('BACKGROUND',(0,0),(-1,-1), MID_GREEN),
            ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ]))
        content = [Paragraph(text, step_s)]
        if n:
            content.append(Paragraph(n, note_s))
        rt = Table([[nc, content]], colWidths=[0.38*inch, 6.12*inch])
        rt.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ]))
        out.append(rt)
        out.append(Spacer(1, 5))
    return out

def tier_table(rows):
    hdr = [Paragraph('<b>' + h + '</b>', pill_s) for h in ['Plan', 'Cost', 'What you get', 'If/Else?']]
    t = Table([hdr] + rows, colWidths=[1.1*inch, 1.0*inch, 3.4*inch, 1.0*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,0), DARK_GREEN),
        ('TEXTCOLOR',    (0,0),(-1,0), colors.white),
        ('FONTNAME',     (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',     (0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',     (0,0),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LIGHT_GRAY]),
        ('GRID',         (0,0),(-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING',   (0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',  (0,0),(-1,-1),8),('RIGHTPADDING', (0,0),(-1,-1),8),
        ('VALIGN',       (0,0),(-1,-1),'TOP'),
    ]))
    return t

def drill_box(text):
    tbl = Table([[Paragraph('<b>Practice:</b>  ' + text,
        S('DB', fontSize=9, textColor=colors.HexColor('#5C4000'), leading=14))]], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), GOLD_BG),
        ('LINEBEFORE',    (0,0),(0,-1),  3, GOLD_BORDER),
        ('TOPPADDING',    (0,0),(-1,-1), 10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',   (0,0),(-1,-1), 14),('RIGHTPADDING', (0,0),(-1,-1),14),
    ]))
    return tbl

# ─────────────────────────────────────────────────────────────────────────────
story = []

story.append(Spacer(1, 0.05*inch))
story.append(Paragraph('n8n Tutorial', title_s))
story.append(Paragraph('A Step-by-Step Guide for VAs', sub_s))
story.append(Paragraph('Beginner to intermediate  |  Google Workspace focus', disc_s))
story.append(Spacer(1, 6))
story.append(HRFlowable(width='100%', thickness=1.5, color=N8N_COLOR, spaceAfter=14))

story.append(KeepTogether([
    tool_header('n8n Tutorial', 'Open-source automation  |  cloud.n8n.io  |  Most powerful of the three tools'),
    Spacer(1, 12),
]))

# WHAT IS N8N
story.append(Paragraph('What Is n8n?', section_s))
story.append(Paragraph(
    'n8n is an open-source automation tool - meaning it is free to download and run on your own computer or server with no limits. '
    'For VAs who do not want to manage a server, n8n also offers a paid cloud version at cloud.n8n.io. '
    'The interface uses a visual canvas where you connect nodes (steps) with lines - similar to Make, but more powerful.', body_s))
story.append(Paragraph(
    'n8n is a step up from Make and ActivePieces. It has a steeper learning curve but handles more complex logic, '
    'has a built-in AI Agent node, and gives developers full control over every part of the automation. '
    'Recommended once you are comfortable with basic if/else automations in Make or ActivePieces.', body_s))

# CONCEPTS
story.append(Paragraph('Key Concepts', section_s))
story.append(Paragraph('Learn these words before you touch the tool. Every step in this tutorial uses them.', body_s))
for k, v in [
    ('Workflow',    'One complete automation. Same idea as a Scenario in Make or a Flow in ActivePieces.'),
    ('Node',        'One app action or logic step inside a workflow. Each circle on the canvas is a node. '
                    'Same idea as a Module (Make) or Step (ActivePieces).'),
    ('Execution',   'One run of your workflow. Same idea as an Operation (Make) or Task (ActivePieces). '
                    'Cloud plans have a monthly execution limit.'),
    ('IF Node',     'The if/else node. Has two outputs - TRUE and FALSE. Similar to Make\'s Router or ActivePieces\' Branch, '
                    'but limited to exactly two paths. Use a Switch Node if you need more than two.'),
    ('Switch Node', 'An advanced if/else that handles more than two conditions. '
                    'For example: if Status = "New" do A, if Status = "Qualified" do B, if Status = "Closed" do C.'),
    ('Expression',  'A way to insert data from a previous node into a field. '
                    'You click "Add Expression" in any field and select data from the panel on the left. '
                    'Same idea as mapping in Make or ActivePieces.'),
    ('Credential',  'A saved login for an app - e.g. your Google account. You create a credential once and reuse it across nodes.'),
]:
    story.append(Paragraph(k, concept_k))
    story.append(Paragraph(v, concept_v))

# SUBSCRIPTIONS
story.append(Paragraph('Subscriptions', section_s))
story.append(tier_table([
    ['Self-hosted', '$0',
     'Unlimited workflows, unlimited executions, all nodes included. '
     'Requires setting up your own server. Not recommended for non-technical users.',
     'YES'],
    ['Starter Cloud', '$20/mo',
     '2,500 executions/month, 5 active workflows, access to all integrations, 14-day free trial available',
     'YES'],
    ['Pro Cloud', '$50/mo',
     '10,000 executions/month, 15 active workflows, version history, custom variables, debug mode',
     'YES'],
    ['Enterprise', 'Custom',
     'Unlimited everything, SSO, on-premise option, dedicated support',
     'YES'],
]))
story.append(Spacer(1, 6))
story.append(warning(
    'There is no permanent free cloud tier in n8n. The 14-day trial is free, but after that '
    'you need a paid plan ($20/month minimum) to keep workflows running in the cloud. '
    'If you need free automation with if/else, start with Make (free, 2 scenarios) or '
    'ActivePieces (free, unlimited flows) and move to n8n when you need more advanced features.'))

# NATIVE AI
story.append(Paragraph('Native AI in n8n', section_s))
story.append(ai_note(
    'n8n has two AI features. First: an AI Assistant that reads what you describe and suggests which nodes '
    'to add. Available on paid cloud plans (Starter+). On the canvas, look for the AI chat icon in the top right corner. '
    'Second: a built-in AI Agent node that can reason through multi-step tasks, use tools like Google Search or '
    'a spreadsheet, and chain multiple AI calls together. This is more advanced than anything Make or ActivePieces offer '
    'natively. Both features still require your own OpenAI or Anthropic API key for the AI model itself - '
    'n8n provides the orchestration, not the AI credits.'))

# ACCOUNT SETUP
story.append(Paragraph('Part 1 - Create Your Account', section_s))
story += steps([
    ('Go to <b>cloud.n8n.io</b> in your browser',
     'This is the cloud version. If you want the self-hosted version, go to n8n.io and follow the self-hosting docs - but this tutorial assumes cloud.'),
    ('Click <b>Start your free trial</b> - no credit card required for the 14-day trial', None),
    ('Sign up with your Google account or create an email/password account', None),
    ('Complete the onboarding questions or click Skip', None),
    ('You are now in the n8n dashboard. Your workflows will be listed here.', None),
])

# UNDERSTANDING THE CANVAS
story.append(Paragraph('Part 2 - Understanding the Canvas', section_s))
story.append(Paragraph(
    'When you open a workflow, you see a dark canvas. Nodes appear as rounded rectangles connected by arrows. '
    'Data flows from left to right - the leftmost node is always the trigger. '
    'Each node has at least one output connector on its right side. '
    'The IF node has two: one labeled TRUE at the top right and one labeled FALSE at the bottom right.', body_s))
story.append(note(
    'n8n\'s canvas is similar to Make\'s but flows strictly left to right. '
    'You can zoom in and out with your scroll wheel and pan by clicking and dragging the background.'))

# BUILD FIRST WORKFLOW
story.append(Paragraph('Part 3 - Build Your First Workflow', section_s))
story.append(Paragraph(
    'We will build a simple automation: when a new row appears in a Google Sheet, '
    'send a Gmail to yourself. This is the foundation - once you understand this, '
    'you can add if/else logic on top of it.', body_s))
story += steps([
    ('From the dashboard, click <b>New Workflow</b>',
     'A blank canvas opens with a default "When clicking Test workflow" node already placed. This is a manual trigger for testing. You will replace it.'),
    ('Click the default node to select it, then press <b>Delete</b> on your keyboard to remove it',
     'Or click the three-dot menu on the node and select Delete.'),
    ('Click the <b>+</b> button at the top left of the canvas (or press Tab) to open the node search panel', None),
    ('Search for <b>Google Sheets</b> and select it', None),
    ('Under "Select a trigger", choose <b>Trigger on new row added</b>',
     'This fires every time a new row appears in your spreadsheet. If you don\'t see this option, make sure you are in the Triggers tab, not Actions.'),
    ('Click <b>Credential for Google Sheets API</b> - click <b>Create New</b>',
     'A Google OAuth window opens. Select your work Google account and click Allow. n8n saves this credential for all future workflows.'),
    ('Under <b>Document</b>, click the dropdown - your Google Sheets files will appear. Select your spreadsheet.',
     'If nothing appears, click the refresh icon next to the dropdown. Make sure the Google account you connected owns or has access to the spreadsheet.'),
    ('Under <b>Sheet</b>, select the correct tab (usually Sheet1)', None),
    ('Click <b>Save</b> in the top right corner of the node panel - then close the panel by clicking elsewhere on the canvas', None),
    ('Click the <b>+</b> connector on the right side of the Google Sheets node to add the next node', None),
    ('Search for <b>Gmail</b> - select it - choose <b>Send a Message</b> under Actions', None),
    ('Click <b>Credential for Gmail</b> - click <b>Create New</b> - authorize your Google account',
     'You may need to create a separate Gmail credential even if you already created a Google Sheets credential. Both connect to the same Google account but are stored separately in n8n.'),
    ('Fill in the email: To (your own email for testing), Subject (type a test subject), Message (type anything)',
     'To insert data from your spreadsheet into the subject or message, click the field and then click "Add Expression." A panel opens showing all data from the Google Sheets node. Select any column to insert it.'),
    ('Click <b>Save</b>', None),
    ('Click <b>Test workflow</b> at the top of the screen',
     'n8n runs the workflow using the most recent row in your sheet. You will see green checkmarks on each node as it runs. Check your Gmail inbox for the test email.'),
    ('When the test passes, click the <b>Inactive</b> toggle at the top right to set it to <b>Active</b>',
     'Once Active, the workflow monitors your sheet and runs automatically when new rows are added.'),
])

# ADDING IF NODE
story.append(Paragraph('Part 4 - Adding If/Else Logic (IF Node)', section_s))
story.append(Paragraph(
    'An IF node splits your workflow into two paths. '
    'The TRUE path runs when your condition is met. The FALSE path runs when it is not. '
    'You add the IF node between your trigger and your actions.', body_s))
story += steps([
    ('Open your workflow - click on the line connecting your Google Sheets trigger to the Gmail node',
     'Clicking the connection line selects it. You will see a small + appear in the middle of the line.'),
    ('Click the <b>+</b> on the connection line to insert a node between the two existing nodes',
     'This inserts a new node without disconnecting the existing ones.'),
    ('Search for <b>IF</b> and select it - it is in the Core category',
     'The IF node is always free. It is a built-in n8n tool.'),
    ('In the IF node panel, click <b>Add condition</b>', None),
    ('Set your condition:',
     'First field: click "Add Value" - in the Expression editor on the left, find your Google Sheets data and select the column you want to check (e.g. Status). '
     'Operator: choose your comparison (Equals, Contains, Greater Than, etc.). '
     'Second field: type the value to compare against (e.g. Qualified).'),
    ('Click <b>Save</b>',
     'The IF node now has two output connectors: TRUE (top right) and FALSE (bottom right). '
     'The original Gmail node is still connected to one output - you will now route each path to a different action.'),
    ('Disconnect the existing Gmail node from the IF node by clicking the connection line between them and pressing <b>Delete</b>', None),
    ('Click the <b>TRUE</b> output connector on the IF node - drag the line to connect it to your existing Gmail node',
     'This Gmail node now only runs when the condition is TRUE.'),
    ('Click the <b>FALSE</b> output connector - drag it to an empty area of the canvas and release to add a new node',
     'A node search panel opens. Add a second Gmail node here with different content for the FALSE path.'),
    ('Configure the second Gmail node, click Save, then click <b>Test workflow</b> again to verify both paths work', None),
    ('Toggle the workflow <b>Active</b> when ready', None),
])

story.append(Spacer(1, 8))
story.append(tip(
    'After testing, click any node on the canvas to see the exact data it received (Input tab) '
    'and the exact data it produced (Output tab). This is the fastest way to debug a broken workflow.'))

# SWITCH NODE
story.append(Paragraph('Part 5 - Handling More Than Two Conditions (Switch Node)', section_s))
story.append(Paragraph(
    'The IF node handles two paths: yes or no. If you need three or more paths, use the Switch node instead. '
    'Example: Status = "New" goes to path 1, Status = "Qualified" goes to path 2, Status = "Closed" goes to path 3.', body_s))
story += steps([
    ('Add a node and search for <b>Switch</b> - select it from Core', None),
    ('Under <b>Mode</b>, choose <b>Rules</b>',
     'Rules mode lets you define conditions for each output path, like multiple IF statements in one node.'),
    ('Click <b>Add routing rule</b> for each condition you need',
     'Each rule gets its own output connector on the right side of the Switch node. Name them clearly so you know which path is which.'),
    ('Set the condition for each rule the same way as the IF node - field, operator, value', None),
    ('There is also a <b>Fallback</b> output at the bottom - this catches anything that does not match any of your rules. Always connect something to it.', None),
    ('Connect each output to the appropriate action node and click Save', None),
])

# COMMON MISTAKES
story.append(Paragraph('Common Mistakes to Avoid', section_s))
story += steps([
    ('<b>Workflow left Inactive after testing.</b> Testing a workflow does not activate it. '
     'Click the Inactive toggle to turn it Active before closing the editor.', None),
    ('<b>Credential connected to the wrong Google account.</b> n8n stores credentials separately. '
     'If data is coming from the wrong Drive or inbox, go to Settings - Credentials in the left sidebar, '
     'find the credential, and reconnect with the correct account.', None),
    ('<b>IF condition does not match.</b> Conditions are case-sensitive in n8n. '
     '"qualified" will not match "Qualified." Check the exact value in your sheet and match it exactly in the IF node.', None),
    ('<b>Expressions returning empty values.</b> If a mapped field shows up blank in your email, '
     'click the Gmail node, go to the Input tab, and check what data arrived from the previous node. '
     'The column name in your expression must match the sheet header exactly.', None),
    ('<b>Trial expired, workflow stops running.</b> After 14 days on the free trial, workflows will stop '
     'unless you upgrade. Set a reminder before the trial ends.', None),
])

story.append(Spacer(1, 8))
story.append(drill_box(
    'Build the Budget Router from the n8n Example PDF using what you learned here. '
    'Trigger: Google Sheets new row. IF node: Budget = High. '
    'TRUE path: Gmail to senior account manager. FALSE path: Gmail to VA. '
    'Test both paths before activating.'))

# FOOTER
story.append(Spacer(1, 20))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=8))
story.append(Paragraph(
    'KeyPlayers HQ  |  KP VA AI Training Program  |  n8n Tutorial  |  '
    'Prices accurate as of mid-2025 - verify at n8n.io before use.',
    footer_s))

doc.build(story)
print('Done:', OUTPUT)

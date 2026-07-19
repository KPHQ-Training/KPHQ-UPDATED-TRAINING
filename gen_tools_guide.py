from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = r'C:\Users\jervi\OneDrive\Documents\Claude\Projects\KP AI TRAINING\github-push\VA-Automation-Tools-Guide.pdf'

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
RED_SOFT    = colors.HexColor('#FDF0F0')
RED_BORDER  = colors.HexColor('#C0392B')
BLUE_BG     = colors.HexColor('#F0F4FD')
BLUE_BORDER = colors.HexColor('#2C5F8A')
PURPLE_BG   = colors.HexColor('#F5F0FD')
PURPLE_BDR  = colors.HexColor('#6C3483')

title_style = ParagraphStyle('Title2',
    fontName='Helvetica-Bold', fontSize=20, textColor=DARK_GREEN,
    spaceAfter=4, alignment=TA_CENTER, leading=26)

subtitle_style = ParagraphStyle('Subtitle',
    fontName='Helvetica', fontSize=10, textColor=GRAY_TEXT,
    spaceAfter=2, alignment=TA_CENTER)

tool_heading = ParagraphStyle('ToolHeading',
    fontName='Helvetica-Bold', fontSize=13, textColor=colors.white,
    spaceBefore=0, spaceAfter=0, leading=18)

section_head = ParagraphStyle('SectionHead',
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

small_label = ParagraphStyle('SmallLabel',
    fontName='Helvetica-Bold', fontSize=8, textColor=GRAY_TEXT, leading=11)

small_body = ParagraphStyle('SmallBody',
    fontName='Helvetica', fontSize=8.5, textColor=GRAY_TEXT, leading=12)

disclaimer_style = ParagraphStyle('Disclaimer',
    fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#888888'),
    leading=12, alignment=TA_CENTER)


def tool_header(color_hex, title, tagline):
    bg = colors.HexColor(color_hex)
    tbl = Table([
        [Paragraph(title, tool_heading)],
        [Paragraph(tagline, ParagraphStyle('tg',
            fontName='Helvetica', fontSize=8.5,
            textColor=colors.HexColor('#DDDDDD'), leading=13))],
    ], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('TOPPADDING',    (0,0), (-1,0), 12),
        ('TOPPADDING',    (0,1), (-1,1), 2),
        ('BOTTOMPADDING', (0,-1),(-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 16),
        ('RIGHTPADDING',  (0,0), (-1,-1), 16),
    ]))
    return tbl


def callout(bg_hex, border_hex, label, text):
    s = ParagraphStyle('cb',
        fontName='Helvetica', fontSize=9, textColor=GRAY_TEXT, leading=14)
    tbl = Table([[Paragraph('<b>' + label + '</b>  ' + text, s)]], colWidths=[6.5*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_hex)),
        ('LINEBEFORE',  (0,0), (0,-1), 3, colors.HexColor(border_hex)),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    return tbl


def warning_box(text):
    return callout('#FDF0F0', '#C0392B', 'Watch out:', text)


def tip_box(text):
    return callout('#E8F5EA', '#2A6636', 'Tip:', text)


def ai_box(text):
    return callout('#F5F0FD', '#6C3483', 'Native AI:', text)


def make_steps(items):
    result = []
    for i, item in enumerate(items, 1):
        text, note = (item if isinstance(item, tuple) else (item, None))
        num_style = ParagraphStyle('num',
            fontName='Helvetica-Bold', fontSize=9, textColor=colors.white,
            alignment=TA_CENTER, leading=12)
        num = Paragraph('<b>' + str(i) + '</b>', num_style)
        num_cell = Table([[num]], colWidths=[0.26*inch], rowHeights=[0.26*inch])
        num_cell.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), MID_GREEN),
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


def tier_table(rows):
    header = [
        Paragraph('<b>Plan</b>', pill_style),
        Paragraph('<b>Price</b>', pill_style),
        Paragraph('<b>What you get</b>', pill_style),
        Paragraph('<b>If/Else?</b>', pill_style),
    ]
    data = [header] + rows
    col_w = [1.1*inch, 0.95*inch, 3.35*inch, 1.1*inch]
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), DARK_GREEN),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    return t


# ─────────────────────────────────────────────────────────────────────────────
story = []

# TITLE
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph('Automation Tools Guide', title_style))
story.append(Paragraph('Make  |  Zapier  |  ActivePieces  -  Subscriptions, If/Else Logic &amp; Native AI', subtitle_style))
story.append(Paragraph('Written for beginner to intermediate VAs', disclaimer_style))
story.append(Spacer(1, 6))
story.append(HRFlowable(width='100%', thickness=1.5, color=MID_GREEN, spaceAfter=14))

# OVERVIEW COMPARISON TABLE
story.append(Paragraph('Quick Comparison', section_head))

comp_header = [
    Paragraph('<b></b>', pill_style),
    Paragraph('<b>Make</b>', pill_style),
    Paragraph('<b>Zapier</b>', pill_style),
    Paragraph('<b>ActivePieces</b>', pill_style),
]

def c(text): return Paragraph(text, ParagraphStyle('ct', fontName='Helvetica', fontSize=8.5, textColor=GRAY_TEXT, leading=12))
def cb(text): return Paragraph(text, ParagraphStyle('ctb', fontName='Helvetica-Bold', fontSize=8.5, textColor=GRAY_TEXT, leading=12))

comp_rows = [
    comp_header,
    [cb('Free ops/month'), c('1,000 operations'), c('100 tasks'), c('1,000 tasks')],
    [cb('Free scenarios/Zaps'), c('2 active scenarios'), c('5 Zaps (single-step only)'), c('Unlimited flows')],
    [cb('If/else on free?'), c('YES - Router module'), c('NO - needs Professional ($49/mo)'), c('YES - Branch step')],
    [cb('Paid starts at'), c('$9/month'), c('$19.99/month'), c('Varies - check site')],
    [cb('Native AI builder'), c('Yes (paid plans)'), c('Yes (paid plans)'), c('No - add AI pieces manually')],
    [cb('Best for'), c('Complex multi-step flows'), c('Widest app library, ease of use'), c('Beginners, tight budget')],
]

comp_table = Table(comp_rows, colWidths=[1.5*inch, 1.65*inch, 1.65*inch, 1.7*inch])
comp_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), DARK_GREEN),
    ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
    ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 8.5),
    ('BACKGROUND',    (0,1), (0,-1), colors.HexColor('#F0F4F0')),
    ('ROWBACKGROUNDS',(1,1), (-1,-1), [colors.white, LIGHT_GRAY]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',    (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(comp_table)
story.append(Spacer(1, 6))
story.append(Paragraph(
    'Prices verified as of mid-2025. Always check the tool\'s pricing page before recommending to a client.',
    disclaimer_style))
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))


# ═══════════════════════════════════════════════════════════════════════════
# MAKE.COM
# ═══════════════════════════════════════════════════════════════════════════
story.append(KeepTogether([
    tool_header('#1A4A2A', 'Make.com', 'Formerly Integromat  -  Best for complex, multi-step automations'),
    Spacer(1, 10),
]))

story.append(Paragraph('What Is Make?', section_head))
story.append(Paragraph(
    'Make is a visual automation tool where you build "scenarios" - flowcharts that connect your apps. '
    'You drag modules onto a canvas and connect them. It handles complex logic well and the free plan '
    'is generous enough for real VA work.', body))
story.append(Paragraph(
    'Key vocabulary: <b>Scenario</b> = one automation. <b>Module</b> = one app action (e.g. "Watch Gmail"). '
    '<b>Operation</b> = one piece of data processed (one email = one operation). '
    '<b>Router</b> = the if/else module.', body))

story.append(Paragraph('Subscription Tiers', section_head))
story.append(tier_table([
    ['Free', '$0', '1,000 ops/month, 2 active scenarios, 15-min minimum schedule interval, most modules available', 'YES'],
    ['Core', '$9/mo', '10,000 ops/month, unlimited active scenarios, 1-min schedule intervals', 'YES'],
    ['Pro', '$16/mo', 'Everything in Core + custom variables, full execution log search, priority support', 'YES'],
    ['Teams', '$29/mo', 'Multiple users, shared scenarios, team permissions', 'YES'],
]))
story.append(Spacer(1, 8))
story.append(tip_box(
    'The free plan is enough to learn and run real automations. '
    'Upgrade to Core only when you hit the 2-scenario limit or need faster than 15-minute scheduling.'))

story.append(Paragraph('Native AI in Make', section_head))
story.append(ai_box(
    'Make has an AI assistant that can suggest which modules to add based on what you describe. '
    'It is available on paid plans (Core and above). On the free plan, you build manually. '
    'Make also lets you add OpenAI or other AI modules as steps inside any scenario - '
    'but those require your own API key (not included in Make\'s subscription).'))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'How to access Make AI (Core+ plans): Inside a scenario, click the + to add a module. '
    'Look for the "Ask Make AI" or AI suggestion prompt at the top of the module search panel. '
    'Type what you want to do in plain language and it will suggest modules.', body))

story.append(Paragraph('Getting Started - Step by Step', section_head))
story += make_steps([
    ('Go to <b>make.com</b> - click <b>Sign up for free</b> - use your Google account for fastest setup', None),
    ('Once inside, click <b>Create a new scenario</b> (top right)', None),
    ('Click the large <b>+</b> on the canvas to add your first module (the trigger)',
     'The trigger is what starts your automation - e.g. "a new email arrives" or "a form is submitted."'),
    ('Search for the app you want to trigger from (e.g. Gmail, Google Forms, Google Sheets) - select it - choose the trigger event',
     'Each app has multiple trigger options. "Watch Emails" checks for new emails. "Watch Responses" checks for new form submissions.'),
    ('Connect your Google account when prompted - click Allow',
     'You only do this once per app. Make stores the connection for all future scenarios.'),
    ('Configure the trigger settings (which folder, how many results, etc.) - click OK', None),
    ('Click <b>+</b> after the trigger module to add your next step - search for the app and action you need', None),
    ('To add an if/else: click <b>+</b> and search <b>Router</b> - this splits your automation into branches',
     'Each branch can have its own filter (the wrench icon). The branch whose filter matches is the one that runs.'),
    ('Click <b>Run once</b> (bottom left) to test with real data before turning it on', None),
    ('When everything works, click the <b>toggle switch</b> at the bottom to turn the scenario ON', None),
])

story.append(Spacer(1, 8))
story.append(warning_box(
    'Gmail label steps: Before selecting a label inside Make, create the label in Gmail first. '
    'Make reads your existing labels - it cannot create new ones from scratch.'))
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))


# ═══════════════════════════════════════════════════════════════════════════
# ZAPIER
# ═══════════════════════════════════════════════════════════════════════════
story.append(KeepTogether([
    tool_header('#1A2A4A', 'Zapier', 'Widest app library (6,000+ apps)  -  Easiest to learn, but if/else costs extra'),
    Spacer(1, 10),
]))

story.append(Paragraph('What Is Zapier?', section_head))
story.append(Paragraph(
    'Zapier is the most widely used automation tool. You build "Zaps" - each Zap has one trigger '
    'and one or more actions. The interface is very beginner-friendly: step-by-step wizard, '
    'no canvas or flowchart. Zapier connects to more apps than any other tool (6,000+).', body))
story.append(Paragraph(
    'Key vocabulary: <b>Zap</b> = one automation. <b>Trigger</b> = what starts it. '
    '<b>Action</b> = what it does. <b>Task</b> = one piece of data processed. '
    '<b>Paths</b> = Zapier\'s if/else feature (paid only).', body))

story.append(Paragraph('Subscription Tiers', section_head))
story.append(tier_table([
    ['Free', '$0', '100 tasks/month, 5 Zaps max, single-step Zaps only (one trigger, one action)', 'NO'],
    ['Starter', '$19.99/mo', '750 tasks/month, unlimited Zaps, multi-step Zaps (one trigger, multiple actions), filters', 'NO'],
    ['Professional', '$49/mo', '2,000 tasks/month, unlimited Zaps, Paths (if/else branches), custom logic, schedules', 'YES'],
    ['Team', '$69/mo', 'Multiple users, shared Zap folders, premier support', 'YES'],
]))
story.append(Spacer(1, 8))
story.append(warning_box(
    'If/else logic (called "Paths" in Zapier) is locked behind the Professional plan at $49/month. '
    'On Free and Starter, you can only run a straight line: trigger then actions, no branching. '
    'For VA work involving conditional logic, Make or ActivePieces are better free options.'))

story.append(Paragraph('Native AI in Zapier', section_head))
story.append(ai_box(
    'Zapier has two AI features. First: a natural-language Zap builder - describe what you want '
    '("When a Google Form is submitted, email my manager if urgency is high") and Zapier builds '
    'a draft Zap for you. This requires a paid plan (Starter or above). '
    'Second: "AI by Zapier" - a built-in action step that processes text using AI (summarize, '
    'classify, rewrite). This also requires a paid plan and uses Zapier\'s own AI credits, '
    'so no separate API key is needed for basic use.'))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'How to access Zapier AI builder (Starter+ plans): Click <b>Create Zap</b> - at the top of the '
    'editor look for "Describe your Zap" or the AI icon. Type what you want in plain language. '
    'Zapier will pre-fill the trigger and action fields based on your description. '
    'You still review and confirm each step before saving.', body))

story.append(Paragraph('Getting Started - Step by Step', section_head))
story += make_steps([
    ('Go to <b>zapier.com</b> - click <b>Sign up</b> - use your Google account', None),
    ('Click <b>Create Zap</b> (top left)', None),
    ('Click <b>Trigger</b> - search for your app (e.g. Google Forms) - select it',
     'The trigger is what starts the Zap. Every Zap starts with exactly one trigger.'),
    ('Choose the trigger event (e.g. "New Form Response") - click Continue', None),
    ('Click <b>Sign in to Google</b> - authorize your account - click Continue', None),
    ('Set up the trigger (select your form, etc.) - click <b>Test trigger</b> to pull a sample response',
     'Zapier needs a sample so it knows what data is available for the next steps. Submit a test form response first if none exist.'),
    ('Click the <b>+</b> below the trigger to add an Action step - search for your app and action', None),
    ('Map the fields from your trigger data into the action fields - click Continue - click Test step',
     'Zapier shows your real trigger data on the left. Click any field in the action and select from the left panel to map it.'),
    ('Add more Action steps with the <b>+</b> button as needed', None),
    ('When done, click <b>Publish</b> (top right) to turn the Zap on', None),
])

story.append(Spacer(1, 8))
story.append(tip_box(
    'Zapier is the safest choice if your VAs are completely new to automations - the wizard '
    'walks through each step. But if they need if/else conditions, use Make or ActivePieces on free plans '
    'and save the $49/month.'))
story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))


# ═══════════════════════════════════════════════════════════════════════════
# ACTIVEPIECES
# ═══════════════════════════════════════════════════════════════════════════
story.append(KeepTogether([
    tool_header('#3A1A4A', 'ActivePieces', 'Most generous free tier  -  Easiest if/else  -  No credit card needed'),
    Spacer(1, 10),
]))

story.append(Paragraph('What Is ActivePieces?', section_head))
story.append(Paragraph(
    'ActivePieces is a newer, fast-growing automation tool. It is open-source, which means it is '
    'free to self-host if needed. The cloud version has a generous free tier with unlimited flows. '
    'The interface is clean and beginner-friendly - similar to Zapier\'s step-by-step style '
    'but with a visual flow builder.', body))
story.append(Paragraph(
    'Key vocabulary: <b>Flow</b> = one automation. <b>Piece</b> = an app integration (e.g. Gmail piece). '
    '<b>Step</b> = one action inside a flow. <b>Branch</b> = the if/else step. '
    '<b>Task</b> = one piece of data processed.', body))

story.append(Paragraph('Subscription Tiers', section_head))
story.append(tier_table([
    ['Free (Cloud)', '$0', '1,000 tasks/month, unlimited flows, unlimited pieces, Branch (if/else) included', 'YES'],
    ['Pro', 'Varies', 'Higher task limits, team features, priority support - check activepieces.com for current pricing', 'YES'],
    ['Self-hosted', '$0', 'Unlimited everything - requires setting up your own server (technical)', 'YES'],
]))
story.append(Spacer(1, 8))
story.append(tip_box(
    'ActivePieces is the best starting point for VAs on a zero budget. '
    'No credit card, unlimited flows, and if/else (Branch) is free. '
    'The 1,000 task/month limit is enough for learning and light real work.'))

story.append(Paragraph('Native AI in ActivePieces', section_head))
story.append(ai_box(
    'ActivePieces does NOT have a native AI scenario builder. There is no "describe your flow" feature. '
    'You build flows manually by adding steps. '
    'However, you can add AI as a step inside your flow using the OpenAI piece, Anthropic piece, '
    'or similar. These require your own API key (BYOK - bring your own key) and are billed '
    'directly by the AI provider, not ActivePieces. '
    'Example: add an OpenAI step after a form trigger to classify or summarize the response before routing it.'))

story.append(Paragraph('Getting Started - Step by Step', section_head))
story += make_steps([
    ('Go to <b>activepieces.com</b> - click <b>Get started free</b> - sign up (no credit card)',
     'You can use your Google account to sign up in one click.'),
    ('Click <b>New Flow</b> (top right) - give it a name - click <b>Create</b>', None),
    ('Click <b>Select Trigger</b> - search for your app (e.g. Google Sheets) - select it',
     'ActivePieces calls app integrations "Pieces." Most major Google Workspace apps are available.'),
    ('Choose the trigger event (e.g. "New Row") - connect your Google account when prompted - configure the settings - click Save', None),
    ('Click the <b>+</b> below the trigger to add your next step', None),
    ('To add if/else logic: search <b>Branch</b> - select it',
     'Branch is under the "Core" category, not an app. It is always free.'),
    ('Set your condition (e.g. Status equals Qualified) - click Save',
     'The True path runs when the condition is met. The False path runs when it is not.'),
    ('Add steps inside the <b>True</b> and <b>False</b> paths by clicking the + inside each path', None),
    ('Click <b>Test Flow</b> at the top to run through your test data', None),
    ('When everything works, click <b>Publish</b> (top right) to turn the flow on', None),
])

story.append(Spacer(1, 8))
story.append(warning_box(
    'ActivePieces does not yet have a Google Tasks integration confirmed in all versions. '
    'If you need to create tasks, use Gmail (send a task reminder email) or Google Sheets '
    '(log to a "Tasks" tab) instead - both are fully supported.'))

story.append(Spacer(1, 18))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=18))


# ═══════════════════════════════════════════════════════════════════════════
# WHICH TOOL TO USE
# ═══════════════════════════════════════════════════════════════════════════
story.append(Paragraph('Which Tool Should You Use?', section_head))

rec_data = [
    [
        Paragraph('<b>Situation</b>', pill_style),
        Paragraph('<b>Recommended Tool</b>', pill_style),
        Paragraph('<b>Why</b>', pill_style),
    ],
    ['I am completely new to automations', 'Zapier (free) or ActivePieces',
     'Zapier wizard is easiest to follow. ActivePieces if you want if/else from day one.'],
    ['I need if/else conditions and have no budget', 'Make (free) or ActivePieces',
     'Both include if/else on the free plan. Zapier locks it behind $49/month.'],
    ['I want AI to help me build the automation', 'Zapier or Make (paid)',
     'Both have AI builders on paid plans. ActivePieces requires manual building.'],
    ['I need to connect a niche app', 'Zapier',
     'Zapier has 6,000+ app integrations - more than any other tool.'],
    ['I need complex multi-step logic with many branches', 'Make',
     'Make\'s visual canvas is the clearest way to manage complex flows.'],
    ['I want to start free and upgrade later', 'ActivePieces',
     'Unlimited flows on free. Upgrade only when you hit the task limit.'],
    ['I want AI steps inside my automation (e.g. summarize text)', 'Any tool + your own API key',
     'All three tools let you add OpenAI/Anthropic as a step. You pay the AI provider directly.'],
]

rec_col_w = [1.8*inch, 1.8*inch, 2.9*inch]
rec_table = Table(rec_data, colWidths=rec_col_w)
rec_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), DARK_GREEN),
    ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
    ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',      (0,0), (-1,-1), 8.5),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, LIGHT_GRAY]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
    ('TOPPADDING',    (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(rec_table)

# FOOTER
story.append(Spacer(1, 24))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceAfter=10))
story.append(Paragraph(
    'KeyPlayers HQ  |  KP VA AI Training Program  |  Automation Tools Guide  |  '
    'Prices and features accurate as of mid-2025 - verify at each tool\'s pricing page before use.',
    footer_style))

doc.build(story)
print('Done:', OUTPUT)

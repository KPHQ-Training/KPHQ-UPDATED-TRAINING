# UPDATED VA TRAINING — Change Log & Instructions

## Purpose
This folder holds all updated/new KP AI Training modules ready for GitHub push.
Every time a training file is changed, two things must happen:
1. **Save the updated file here** (overwrite if it already exists)
2. **Log the change below** under the correct date

---

## Rules (Claude must follow these every session)

- Any edit to a training HTML file = copy the updated file to this folder immediately after saving
- Log every change below: date, filename, and a one-line description of what changed
- Never skip logging — even small fixes (typos, slide text, nav labels) get logged
- Files in this folder are the source of truth for what's ready to push to GitHub

---

## Changelog

### 2026-06-20
| File | Change |
|------|--------|
| `Day03_Claude.html` | Added "Which Claude Tool?" decision table as first slide; added 2 Claude Code slides to ses=3; updated sidebar nav labels and sesNames array |
| `AI_Glossary.html` | Full rebuild from flat page → slide deck format. 6 sessions: AI Concepts (14 terms), Claude Ecosystem, Other AI Tools, Automation & CRM, Meetings & Comms, KeyCommand (10 terms). Accordion expand/collapse added. |

### 2026-06-21
| File | Change |
|------|--------|
| `Day01_AI_Foundations.html` | Added "More limits VAs run into every day" slide (ses=1); added tricky data security drill slide — incognito trap (ses=2) |
| `Day02_AI_Foundations_Tools.html` | Renamed "Debugging Bad Output" → "Refining & Iterating" (ses=2); added "Why prompting shapes everything" slide with 3 cards (KC briefs / GHL automations / daily tasks) |
| `Day08_AI_Meetings_PM_Messaging.html` | Full restructure — removed entire KeyCommand section (10 slides); replaced with 4 Conditional Logic slides (CL Intro / 5 Key Terms / Logic Map / CL Drill) in ses=3. All nav, sesNames, opener card, agenda, and wrap-up updated. |
| `Day09_KeyCommand.html` | New file — dedicated KeyCommand day. 8 sessions: What Is KC / Agent System / Writing a Brief / Knowledge Graph & Genes / Approval Workflow / Daily Rhythm / Live Scenario Drill / First Week Checklist. ⚠️ Session 1 has dashboard screenshot placeholder — trainer must add live screenshot before use. |
| `Day10_Assessment.html` | KC question tags fixed (Q17/Q18/Q21 → Day 9; Q22 → Day 8); 2 new situational KC scenario questions added (SQ11, SQ12); scoring updated from 37→39 total, passing = 32/39 |

---

### 2026-06-22
| File | Change |
|------|--------|
| `index.html` | Full cover page redesign. Switched from Fraunces/Epilogue to Inter font to match day files. Replaced color variables with the same system used across Day01–Day10 (--bg:#070B09, --accent:#22C55E). Rebuilt layout: sticky header with KP wordmark + confidential badge, hero with 3 stat badges, week dividers (Week 1 / Week 2), day cards with icon + arrow, reference grid with all 5 tiles (AI Glossary, GHL Glossary, Security & Privacy, AI Tools Reference, Tools by Niche). |

### 2026-06-22
| File | Change |
|------|--------|
| `KP_AI_Glossary.html` | Removed "Drafting" entry from D section. Added 3 new terms: **Inference** (I section, Advanced/Technical — what happens when you send a message to Claude), **Fine-tuning** (F section, Advanced — training a model on specific data), **Temperature** (T section, Advanced — controls creativity vs predictability of AI responses). |

---

### 2026-07-08
| File | Change |
|------|--------|
| `Day03_Claude.html` | Follow-up (same day, Jervis): removed the "— free & Pro" / "— Pro" tier/pricing from the four "Which Claude Tool?" opener labels — kept location only (claude.ai / inside Claude Chat / desktop app / terminal). Pricing no longer on the first slide; Cowork slide's "Pro" badge left as-is. Both copies, deployed + verified live. |
| `Day03_Claude.html` | Code-forward Day 3 update (Jervis Confirmed; released freeze for this change only). Ported the 2026-06-20 fork into live root (Which-Claude-Tool opener, nav labels, 2 Claude Code slides, recap rows, sesNames). Removed the jackhammer quiz. Retitled "When VAs encounter Claude Code" → "Using Claude Code as an EA" + reframed intro to encourage use. Added 2 slides to ses=3 (CLI): **Claude Code commands you'll use** (/init, /clear, /compact, /model, /mcp, /help) and **Claude Code best practices for an EA**. Added 2 slides to ses=5 (Projects/Skills/Plugins): **Skills you'll actually use as an EA** (keyplayers-ea, executive-briefing, va-email-responder, schedule, doc-coauthoring) and **Plugins & connectors for an EA** (Slack, Gmail, Granola, Notion, Canva samples). `/goal` requested but omitted — could not verify it as a real command. Deployed to production (kphq-updated-training). Session count unchanged (9); no nav/sesNames bookkeeping needed beyond the fork. |

*Add new date sections above as changes happen. Keep entries short and specific.*

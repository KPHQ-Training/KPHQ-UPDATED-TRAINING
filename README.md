# KP-AI Academy — KeyPlayers VA Academy

The internal AI Operator training program for KeyPlayers HQ virtual assistants.
A self-contained set of interactive HTML lessons taking a VA from AI fundamentals
through to running automated client systems in GoHighLevel.

🔗 **Live:** [kphq-updated-training.vercel.app](https://kphq-updated-training.vercel.app)

> **For internal use only — must be kept confidential.**

---

## Program Structure

### Week 1 — AI Fundamentals & Prompting
| Day | Lesson | Focus |
|-----|--------|-------|
| 1 | [AI Fundamentals](Day01_AI_Fundamentals.html) | AI landscape, benchmarking, CLEAR framework, metaprompting, cross-referencing |
| 2 | [Prompting Mastery](Day02_Prompting_Mastery.html) | The 5 building blocks, prompt formulas, advanced techniques, debugging output |
| 3 | [Tool Selection](Day03_Tool_Selection.html) | 5 core tool categories, pros/cons, compliance, role-based mapping |
| 4 | [Claude Deep Dive](Day04_Claude_Deep_Dive.html) | Haiku/Sonnet/Opus, Artifacts, Projects, context windows, MCP |
| 5 | [Cowork & Agentic AI](Day05_Cowork_Agentic_AI.html) | Cowork mode, power workflows, agentic patterns, oversight & responsible use |

### Week 2 — GoHighLevel Mastery
| Day | Lesson | Focus |
|-----|--------|-------|
| 6 | [GoHighLevel Foundations](Day06_GoHighLevel_Foundations.html) | Agency vs. sub-accounts, contacts & tags, pipelines, conversations, calendars |
| 7 | [GHL Automation, API & MCP](Day07_GHL_Automation_Workflows.html) | Workflows, triggers & actions, APIs, webhooks, MCP, integrations |
| 8 | [AI Meetings, PM & Messaging](Day08_AI_Meetings_PM_Messaging.html) | AI note-takers, project management, Slack/WhatsApp/Telegram, command center |

### Reference
- [AI Glossary](KP_AI_Glossary.html) — core AI terms used across Week 1
- [GoHighLevel Glossary](GHL_Glossary.html) — 56 GHL terms a VA needs, searchable & filterable by category

---

## Navigation

- **[index.html](index.html)** is the hub — it lists every day in both weeks plus both glossaries.
- Each day page has a **Course Navigation** panel linking all 8 days, so learners can jump anywhere.
- Days run in sequence: Day 1 → … → Day 8, with Week 1 flowing straight into Week 2.

---

## Tech & Deployment

- **Stack:** plain, self-contained HTML/CSS/JS — no build step, no dependencies (Google Fonts loaded via CDN).
- **Hosting:** static deploy on Vercel, auto-deployed from `main`.
- **Embedding:** pages are iframe-friendly (e.g. the GoHighLevel Glossary embeds in the GHL community).
- **To update:** edit the relevant `.html` file and push to `main`; Vercel redeploys automatically.

---

_KeyPlayers HQ · KP-AI Academy · Updated June 2026_

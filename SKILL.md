---
name: extreme-survival-requirements
description: Generate and maintain detailed functional requirements specifications for the game project 《末日余生：极限生存》. Use when Codex needs an AI-facing continuation requirements spec, a reader-friendly owner requirements document, a feature inventory, acceptance criteria, gameplay/system/platform requirements, dual-version Game Studio-to-WeChat requirements, or a no-schedule PRD that lets future Codex sessions continue the project without prior chat context.
---

# Extreme Survival Requirements

Use this skill to produce durable functional requirements for 《末日余生：极限生存》. The output must help two readers:

1. **Codex / developer reader**: enough detail to continue implementation in a fresh window.
2. **Human project owner reader**: clear, plain-language requirements that are easy to review and correct.

This skill produces functional requirements only. Do not include schedules, development weeks, dates, sprint plans, launch forecasts, staffing plans, or budget estimates.

## Non-negotiable quality bar

Do not produce a thin feature list. Each core feature must be expanded enough to support implementation and review. For AI-facing requirements, every feature should include:

- Stable requirement ID.
- Module and feature name.
- Owner-facing one-line explanation.
- Purpose and user story.
- Preconditions.
- Main flow.
- Branch/exception flows.
- Rules and boundaries.
- State/data fields.
- Configuration fields.
- UI/feedback elements.
- Error handling.
- Dual-version implementation split:
  - shared logic,
  - Game Studio / Phaser master,
  - WeChat Mini Game adaptation.
- Acceptance criteria.
- Test suggestions.
- Explicit non-goals.
- Open questions.

For reader-friendly requirements, every feature should explain:

- What the feature does.
- How the player uses it.
- What normal operation looks like.
- What can fail.
- What rules must be followed.
- What the player sees.
- What counts as done.
- What is temporarily excluded.
- What the project owner must confirm.

If the output feels shorter or less detailed than the project development plan, enrich it before delivering.

## Core project strategy

Always preserve this strategy unless the user explicitly changes it:

- Build gameplay first in a Game Studio + Phaser/TypeScript browser master version.
- Convert or migrate stable features into a separate WeChat Mini Game adaptation version.
- Keep both code versions:
  - `Game Studio / Phaser master`: fast gameplay iteration, browser playtest, debugging, feature validation.
  - `WeChat Mini Game adaptation`: WeChat runtime bridge, touch/lifecycle/resource/login/adaptation, simulator and real-device verification, publishing.
- Do not let WeChat-specific runtime work pollute platform-independent gameplay logic.

## Standard outputs

When the user asks to generate requirements for this project, create one or both of these files:

- `ai-functional-requirements.md`: implementation-facing, precise, structured, and suitable for Codex handoff.
- `reader-functional-requirements.md`: human-readable, plain Chinese, focused on what the player sees and what the project owner can approve.

If the user asks for Word documents, create `.docx` versions from the same content using the Documents skill.

## Workflow

1. Inspect available project artifacts first:
   - existing PRD/documents in `deliverables/`;
   - current Game Studio/Phaser source;
   - current WeChat Mini Game source;
   - issue/solution journals if present.
2. Extract only functional requirements and project constraints. Ignore schedules and dates.
3. Build a feature inventory before writing prose.
4. Generate the AI-facing specification first.
5. Generate the reader-friendly document from the same requirement inventory.
6. Validate the pair:
   - no schedule/timeline language;
   - both documents describe the same feature set;
   - dual-version strategy is explicit;
   - every core feature has rules, flows, errors, data/config, acceptance criteria, and open questions;
   - open questions are clearly marked instead of guessed.

## Requirement ID conventions

Use stable IDs so later docs, code, tests, and issues can reference the same feature:

- `ES-FR-META-*`: project boundaries and cross-version rules.
- `ES-FR-CORE-*`: core loop, match flow, settlement.
- `ES-FR-PLAYER-*`: player movement, controls, interaction, status, death, revive.
- `ES-FR-MAP-*`: map, camera, collision, safe area, points of interest.
- `ES-FR-ZOMBIE-*`: enemy/zombie spawning, AI, combat.
- `ES-FR-SURVIVAL-*`: health, hunger, thirst, stamina, infection.
- `ES-FR-ITEM-*`: loot, inventory, pickup, drop, use.
- `ES-FR-CRAFT-*`: crafting.
- `ES-FR-BUILD-*`: building and placement.
- `ES-FR-COMBAT-*`: weapons, attacks, hit detection, damage, feedback.
- `ES-FR-NET-*`: matchmaking, rooms, sync, reconnect.
- `ES-FR-WECHAT-*`: WeChat login, lifecycle, resource, ads, ranking, compliance.
- `ES-FR-UI-*`: HUD, menus, prompts, results.
- `ES-FR-DATA-*`: save, config, telemetry, backend records.
- `ES-NFR-*`: non-functional requirements such as performance, compatibility, security, maintainability.

## Helpful script

Use `scripts/generate_requirements.py` to generate the detailed Markdown pair. Prefer running from the project root and passing `--project-root .` so non-ASCII Windows paths do not get mangled by shell encoding:

```powershell
python extreme-survival-requirements/scripts/generate_requirements.py --project-root . --out-dir deliverables/requirements
```

The script includes a schedule-term guard and will fail if it detects common schedule-like terms.

## Do not include

- Development cycles, weekly plans, dates, release forecasts, or staffing estimates.
- Revenue guarantees or platform approval guarantees.
- Hidden chain-of-thought, private credentials, AppSecret, tokens, or personal identifiers.
- Requirements that contradict the dual-version Game Studio → WeChat Mini Game strategy unless the user explicitly changes direction.

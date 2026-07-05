---
name: extreme-survival-requirements
description: Generate and maintain functional requirements documents for the game project 《末日余生：极限生存》. Use when Codex needs to create an AI-facing continuation requirements document, a reader-friendly product requirements document, a feature inventory, acceptance criteria, gameplay/system requirements, platform-adaptation requirements, or a no-schedule PRD that lets future Codex sessions continue the project without prior chat context.
---

# Extreme Survival Requirements

Use this skill to produce durable functional requirements for 《末日余生：极限生存》. The output must help two readers:

1. **Codex / developer reader**: enough detail to continue implementation in a fresh window.
2. **Human project owner reader**: clear, plain-language requirements that are easy to review and correct.

Do not write project schedules, development weeks, dates, sprint plans, launch timelines, staffing plans, or budget estimates. This skill produces functional requirements only.

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
- `reader-functional-requirements.md`: human-readable, plain Chinese, focused on what the player sees and what the product owner can approve.

If the user asks for Word documents, create `.docx` versions from the same content using the Documents skill.

## Required sections: AI-facing document

Use `references/ai-functional-requirements-template.md` as the shape. Each functional requirement should include:

- Stable requirement ID, e.g. `ES-FR-PLAYER-001`.
- Feature name.
- User-facing behavior.
- Game rules and edge cases.
- Data/state fields.
- Input/output events.
- Acceptance criteria.
- Platform split:
  - shared logic,
  - Game Studio / Phaser master behavior,
  - WeChat Mini Game adaptation behavior.
- Test notes.
- Open questions, if any.

Write requirements as implementation-ready contracts. Prefer explicit numbers, state names, and transitions over vague prose.

## Required sections: reader-friendly document

Use `references/reader-functional-requirements-template.md` as the shape. Explain:

- What the feature is.
- What the player can do.
- What the game should show.
- What counts as success/failure.
- What is not included in the first version.
- What the user/project owner should confirm.

Keep the tone direct and readable. Avoid engine jargon unless it affects product decisions.

## Requirement ID conventions

Use stable IDs so later docs, code, tests, and issues can reference the same feature:

- `ES-FR-CORE-*`: core game loop and match flow.
- `ES-FR-PLAYER-*`: player movement, controls, status, death, revive.
- `ES-FR-MAP-*`: map, camera, collision, points of interest.
- `ES-FR-ZOMBIE-*`: enemy/zombie spawning, AI, combat.
- `ES-FR-SURVIVAL-*`: health, hunger, thirst, stamina, infection.
- `ES-FR-ITEM-*`: loot, inventory, pickup, drop, use.
- `ES-FR-CRAFT-*`: crafting and building.
- `ES-FR-COMBAT-*`: attack, weapon, hit, damage, feedback.
- `ES-FR-NET-*`: matchmaking, rooms, sync, reconnect.
- `ES-FR-WECHAT-*`: WeChat login, lifecycle, resource, ads, ranking, compliance.
- `ES-FR-UI-*`: HUD, menus, prompts, results.
- `ES-FR-DATA-*`: save, config, telemetry, backend records.
- `ES-NFR-*`: non-functional requirements such as performance, compatibility, security, accessibility.

## Workflow

1. Inspect available project artifacts first:
   - existing PRD/documents in `deliverables/`;
   - current Game Studio/Phaser source;
   - current WeChat Mini Game source;
   - issue/solution journals if present.
2. Extract only functional requirements and project constraints. Ignore schedules and dates.
3. Build a feature inventory before writing prose.
4. Generate the AI-facing document first.
5. Generate the reader-friendly document from the same requirement inventory.
6. Validate the pair:
   - no schedule/timeline language;
   - both documents describe the same feature set;
   - dual-version strategy is explicit;
   - every core feature has acceptance criteria;
   - open questions are clearly marked instead of guessed.

## Helpful script

Use `scripts/generate_requirements.py` to create starter Markdown files from the bundled templates:

```powershell
python scripts/generate_requirements.py --project-root "D:\末日余生：极限生存" --out-dir "D:\末日余生：极限生存\deliverables\requirements"
```

The script produces a scaffold. After running it, refine the generated files using the actual project context.

## Do not include

- Development cycles, weekly plans, dates, release forecasts, or staffing estimates.
- Revenue guarantees or platform approval guarantees.
- Hidden chain-of-thought, private credentials, AppSecret, tokens, or personal identifiers.
- Requirements that contradict the dual-version Game Studio → WeChat Mini Game strategy unless the user explicitly changes direction.

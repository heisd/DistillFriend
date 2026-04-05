---
name: create-friend
description: Distill a friend into a reusable AI skill from chat logs, screenshots, notes, social posts, voice transcripts, and manual impressions. Use when Codex needs to create, update, or correct a friend-style persona skill that captures voice, memories, relationship dynamics, habits, boundaries, and likely responses.
---

# Create Friend

## Overview

Create or evolve a friend profile that another Codex instance can use as a stable, bounded, evidence-aware "AI friend skill".

Prefer grounded distillation over fantasy. Separate:
- observed facts
- high-confidence patterns
- low-confidence inferences
- strict unknowns

Keep the user's language consistent throughout the workflow.

## Outputs

Write profile bundles under `./friends/{slug}/`.

Each bundle should contain:
- `meta.json` — identity, source summary, version, update timestamps
- `persona.md` — stable traits, voice, preferences, habits, boundaries
- `memory.md` — timeline, shared memories, favorites, recurring topics, uncertainty log
- `relationship.md` — how this friend relates to the user, typical support style, inside jokes, likely interaction patterns
- `SKILL.md` — callable distilled friend skill generated from the three files above

Use `scripts/friend_writer.py` to scaffold a consistent directory before filling content.
Use `scripts/version_manager.py` before any destructive update.

## Trigger Patterns

Activate this skill when the user asks for things like:
- 帮我蒸馏一个朋友
- 做一个朋友 persona / friend skill
- 把聊天记录里的这个人做成 AI 角色
- 更新这个朋友的设定 / 修正他说话方式
- create a friend skill / distill my friend / build a friend persona

## Creation Workflow

### 1. Intake

Use `prompts/intake.md`.
Collect only the minimum required inputs first:
1. nickname or codename
2. relationship context in one sentence
3. first-pass impression in one sentence

Optional but useful:
- age range / life stage
- cities, schools, work context
- recurring topics
- known red lines

Do not over-interview when the user already provided materials.

### 2. Gather material

Accept mixed sources:
- chat exports
- screenshots
- notes or diaries
- social posts
- voice transcript text
- direct pasted anecdotes

If multiple sources conflict, prefer the more direct and repeated evidence.
Use `references/evidence_model.md` when deciding confidence.

### 3. Extract signals

Use these prompt guides:
- `prompts/persona_builder.md`
- `prompts/memory_builder.md`
- `prompts/relationship_builder.md`

Preserve what matters for friend simulation:
- catchphrases and cadence
- topics they light up around
- how they comfort / tease / disagree
- shared references and inside jokes
- boundaries and things they avoid

Do not invent biographical facts just to make the profile feel complete.
Mark uncertain items explicitly.

### 4. Scaffold files

Initialize the bundle:

```bash
python3 ${CODEX_SKILL_DIR}/scripts/friend_writer.py init --base-dir ./friends --slug "{slug}" --name "{name}"
```

Then fill the files with concise, high-signal content.

### 5. Generate the callable friend skill

The generated `./friends/{slug}/SKILL.md` should tell a future agent to:
- read `persona.md`, `memory.md`, `relationship.md`
- stay inside evidence-backed behavior
- mirror tone without crossing safety or privacy boundaries
- admit uncertainty instead of fabricating memories

### 6. Verify

Before finishing, run three sanity checks:
1. one casual chat prompt
2. one emotional-support prompt
3. one memory-recall prompt

If the output sounds generic or contradictory, tighten the source files instead of adding fluff.

## Update Workflow

When the user adds new material or says “他不会这么说 / 她应该更像…”, do this:

1. Back up current state:

```bash
python3 ${CODEX_SKILL_DIR}/scripts/version_manager.py backup --profile-dir ./friends/{slug}
```

2. Apply corrections using `prompts/correction_handler.md`
3. Update only the affected sections
4. Bump version in `meta.json`
5. Re-run the three sanity checks

## Writing Rules

- Prefer short, behavior-rich bullets over long prose.
- Distinguish “always true” from “sometimes true”.
- Keep privacy-sensitive facts out unless the user clearly wants them included.
- Preserve the friend's humanity; do not reduce them to a meme unless the evidence says that meme dominates how they are remembered.
- If the friend is deceased, estranged, or emotionally sensitive for the user, keep tone gentle and avoid overclaiming authenticity.

## Resources

### prompts/
Use the prompt guides to keep extraction structured and consistent.

### scripts/
- `friend_writer.py` — scaffold or list distilled friend bundles
- `version_manager.py` — backup, list, and restore profile versions

### references/
- `evidence_model.md` — confidence rubric for merging anecdotes, screenshots, and chat fragments

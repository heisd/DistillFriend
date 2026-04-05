# Correction Handler

When the user says the profile is off:

1. Identify the exact broken claim.
2. Decide whether it belongs to `persona.md`, `memory.md`, or `relationship.md`.
3. Replace only the narrowest necessary section.
4. If the user gives a hard correction, treat it as stronger than prior inference.
5. If the correction contradicts direct quoted evidence, keep both by recording:
   - observed evidence
   - user override / contextual explanation

Correction notes should reduce future drift, not just patch the current reply.

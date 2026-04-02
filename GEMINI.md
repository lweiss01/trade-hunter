## Holistic - cross-agent session tracking

**At the start of every session, before doing anything else:**
1. Read `HOLISTIC.md` in full.
2. Read `AGENTS.md` - find the section for your agent and follow its setup steps.
3. Summarise to the user: what was last worked on, what's planned next, and any known fixes to protect.
4. Ask: "Continue as planned, tweak the plan, or do something different?"
5. Use `./.holistic/system/holistic resume --agent gemini` on macOS/Linux or `.\.holistic\system\holistic.cmd resume --agent gemini` on Windows to register the session.

**After significant work or on any git commit (hook fires automatically):**
- Run `holistic checkpoint --reason '<what you just did>'`
- To record a fix that must not regress: `holistic checkpoint --fixed '<bug>' --fix-files '<file>' --fix-risk '<what reintroduces it>'`

**At the end of every session:**
- Run `holistic handoff` - this opens a dialog to capture the summary and prepares a pending handoff commit.
- If you want the Holistic files committed, make that git commit explicitly.

**Never touch files listed in the KNOWN FIXES section of HOLISTIC.md without reading that section first.**

## Before ending this session

Run:
```
holistic handoff --summary "..." --next "..."
```
This keeps repo memory current for the next agent.

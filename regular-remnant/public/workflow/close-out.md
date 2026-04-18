---
description: Close out a branch — docs, lint, commit, simplify, wiki-update
---

Create a task list and work through it one item at a time. Be sure to include all fixes from this branch, not just the ones from the last couple of plans.

1. Update any relevant files in `/docs` if important architectural changes were made or relevant debugging findings found since the last document update in this branch.
2. Run relevant linting based on the codebase on the code added since the last time you ran linting.
3. Stage and commit everything.
4. Check whether commits on this branch completed any tasks in the project's wiki task list. Read `~/.obsidian-wiki/config` for `OBSIDIAN_VAULT_PATH`, derive the project name from cwd (basename, lowercased, spaces/underscores → dashes), and read `$OBSIDIAN_VAULT_PATH/projects/<project-name>/tasks.md` if it exists. Compare the `## Next` section against commits on this branch (`git log main..HEAD --oneline`, or against the branch's merge base if `main` isn't the base). For each task that looks completed by the committed work, present the match to the user and — on confirmation — invoke `/task-done` with a unique substring of the task description. Skip this step silently if no task file exists for the project.
5. Run `/simplify`.
6. Run `/wiki-update`.

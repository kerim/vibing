# Writing Style

These notes apply **only to blog post prose** in `regular-remnant/content/posts/`. They do not apply to commit messages, code comments, PR descriptions, or any other writing in this repo.

When drafting or editing a blog post, match Kerim's voice. Observations from existing posts:

## Voice and tone
- First-person, conversational, a little frustrated or self-deprecating. Tools fail, approaches don't work, and he says so plainly.
- Problem-first openings: "One of the more annoying things about…", "When using assisted mode on cars…", "I've been struggling to…", "I want to…". Rarely starts with a triumphant claim.
- Hedges often: "sort of works", "a bit", "I think", "it seems", "more often than not".
- Occasional parenthetical asides are a signature. Examples: "(That's in Claude's own language.)", "(No, I don't think this is intentional.)", "(I had tried doing it in a more radical way earlier, and wasted about three days of coding…)".

## Punctuation
- **No em-dashes.** This is the single biggest Claude-ism tell. Use commas, parentheses, or new sentences instead.
- Rare italics for emphasis. Don't wrap words in `*asterisks*` to make a point.
- Semicolons are rare. Two short sentences beat one compound sentence.
- Sentences are often long and meandering, with clauses joined by "and". Do not try to make every sentence punchy.

## Vocabulary
- Plain, everyday words. "Bang for the buck", "ended up", "a bit ugly", "slow", "magic", "middleman", "messy". Not "elegant", "grounded in", "seamless", "the missing piece", "game-changer".
- No marketing language. No tricolons ("X, Y, and Z" parallel structure). No rhetorical contrasts ("It is not A, it is B").
- Accept typos and informality. Real posts contain things like "hygine" (for hygiene), missing apostrophes, double periods. Do not over-polish.

## Structure
- Short posts (2–5 paragraphs) for a tool announcement or workflow tip. Longer posts use `##` headers for sections; short ones do not.
- Lead image at the top: `![](_filename.ext)`. Filenames are prefixed with `_` so they are excluded from the content collection.
- Links are generous: external links to tools, writers, docs, and other bloggers; internal links to prior posts using the full URL (`https://vibing.kerim.one/posts/<slug>/`).
- Closings are practical: a caveat, a forward-looking note, a wry aside, or an update. Avoid rhetorical flourish closers.

## Frontmatter
- Fields: `title`, `description`, `publishedDate`, `tags`, `previewImage`.
- Tags are lowercase. Multi-word tags use spaces, not hyphens (e.g. `claude code`, `knowledge management`).
- `previewImage` paths start with `./` and reference a `_`-prefixed file in the same directory.

## Before drafting
Read 2–3 existing posts first to calibrate voice. `2026-02-08-debugging.md`, `2026-03-17-xcodebuild-mcp.md`, and `2026-03-25-codebase-to-course.md` are good references for long-form, short-form, and short-form respectively.

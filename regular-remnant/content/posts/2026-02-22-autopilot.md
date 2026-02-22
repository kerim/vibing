---
title: Autopilot
description: Keep your hands on the wheel
publishedDate: 2026-02-22
tags:
  - claude code
  - workflows
previewImage: './_steering-wheel.avif'
---

![](_steering-wheel.avif) 

When using assisted mode on cars they tell you to keep your hands on the wheel. You have to do the same when vibe coding. I'm not really qualified to review the code it generates, so I use agents to review the code for me. I will run each plan by the coding agents over and over again (usually 2-3 times) until you get a review that only discovers minor errors, not "critical" ones. (That's in Claude's own language.) 

But this isn't enough. Even if you can't read the code itself, you can read the explanations given by Claude. I've often caught major problems, as well as solutions this way. And I've occasionally gotten lazy, skipped this step, and regretted it. Most recently I asked claude to fix a feature and it decided the best way to fix it was to remove it altogether. The coding agents agreed! So I went back (using the handy "rewind" command) and did it again, this time making sure it actually fixed the code rather than removing it.

But you can fix a lot just by using logical reasoning. My word processing app has a bibliography feature and when it was building the footnote feature it made a comment about how the footnote feature was having problems because couldn't be implemented in the same way as the bibliography feature. But was that really true? I pressed Claude on this and eventually it admitted that it could, actually, use the same (working) solution for both features. 

Vibe-coding means you can do a lot without knowing the nitty-gritty of writing code, but you still need to pay attention, get Claude to explain what it is doing, and question it when the answers don't make sense. More often than not, when Claude's answers don't make sense to me it is because there is a flaw in its logic, not because there is a problem with my lack of coding experience. 
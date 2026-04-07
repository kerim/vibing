---
title: Obsidian Wiki
description: A knowledge base Claude maintains for you
publishedDate: 2026-04-07
tags:
  - claude code
  - knowledge management
  - workflows
previewImage: './_obsidian.png'
---

![](_obsidian.png)

One of the more annoying things about working with Claude is that every conversation starts from zero. You explain your project, explain your preferences, explain what you tried last week, and a few days later you open a new session and do it all over again. There's `CLAUDE.md`, and there is the built-in memory feature, and those help a bit, but neither of them is really a place where knowledge builds up over time. Meanwhile I have been collecting articles, chat logs, documentation pages, and my own notes in various places, and most of it just sits there unread.

I've been trying out [obsidian-wiki](https://github.com/Ar9av/obsidian-wiki), which is a framework for having Claude maintain an Obsidian vault as a compiled knowledge base. The idea (based on [a pattern from Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) is that Claude doesn't just dump your notes into the vault, but treats itself as a compiler. It reads a source, extracts the concepts, entities, and relationships, and then either creates a new page or updates an existing one, cross-linking everything as it goes. So instead of ending up with a folder full of disconnected summaries, you end up with an interconnected wiki where the same topic lives in one place no matter how many times you've read about it. Before I start a new project I can ask Claude what I already know about a library, a tool, or a workflow, and it pulls answers out of the wiki with links back to the source pages and related topics.

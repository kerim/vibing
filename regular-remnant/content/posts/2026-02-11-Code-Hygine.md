---
title: Code Hygine
description: On the importance of refactoring and linting
publishedDate: 2026-02-11
tags:
  - claude code
  - workflows
  - refactoring
  - linting
previewImage: './_hygine.jpg'
---

![](_hygine.jpg)

In the third installment of my series on basic vibe-coding workflows (see [[Debugging]] and [[Smoke Tests]]), I tackle the subject of "refactoring" and "linting." Both of these can be thought of as forms of code hygine, they keep your code looking neat and tidy, but they are functional as well—especially for AI coding. 

## Refactoring

One of the reasons Claude Code has become so successful as a coding agent isn't that its code is that much smarter than the competitors, but because the developers understand the importance of "context" when working with LLMs. AI agents are easily overwhelmed by too much information and start hallucinating. There are two things Claude Code has done to fix this. One is to increase the amount of context that the agents can handle. Now Claude can handle thousands of lines of code fairly well. The other is to find ways to limit the context. They do this by forcing the conversation to "compact" on a regular basis, summarizing the previous conversation and archiving it. This helps keep the agent on track.

Refactoring is something developers can do in order to help keep LLMs focused. Refactoring involves a number of different tasks, some of the most common are: creating shared subroutines to replace duplicated code, cleaning up complex logical statements to make it clearer when code gets invoked, and simplifying complex functions and classes by breaking them up into smaller ones with a well-defined purpose. This is generally good practice for any developer, but for LLMs in particular, it can help ensure that the AI stays on target. 

The simplistic thing you can do is ask the AI to come up with a plan to break up long files, with thousands of lines of code, into shorter documents that are linked together. In my case I told Claude I didn't want any code with over 800 lines. In some cases this meant breaking up a single document into five or more smaller files. 

At the same time, you don't want to do too much. Each time the AI starts moving things around, there is a chance that something will break. So I told Claude to focus on those changes that could give us the biggest bang for the buck, and not worry about smaller, more complex, files that might not benefit very much from optimization. I also had it backup and check the code every step of the way. (I had tried doing it in a more radical way earlier, and wasted about three days of coding because it broke everything. I ended up trashing that branch and starting over again.)

## Linting

Linting is the process of using an automated tool, known as a linter, to analyze source code for potential errors, bugs, stylistic inconsistencies, and suspicious constructs. These are pretty reliable and fast, and you can easily run a linter on your code every time you write new code or change existing code. It helps catch errors and helps prevent new ones. I use two. I use [SwiftLint](https://github.com/realm/SwiftLint) for the macOS code, and I use [Biome](https://biomejs.dev/linter/) for the Javascript code.


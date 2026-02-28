---
title: Images
description: Thinking of features like a developer
publishedDate: 2026-02-28
tags:
  - claude code
  - ui
  - final-final
  - features 
previewImage: './__painting.webp'
---

![](_painting.webp) 

It is important to remember that no feature, no matter how ordinary and ubiquitous it might be, is "simple" to implement, even with an AI doing much of the coding. You still need to think through how everything will work. 

For instance, inserting images into a document should be easy, right? After all, every single wordprocessor out there can do it. And since I'm using Markdown for my word processor, I can just use the following simple markdown image formatting:
```markdown
![alt](image.png)
```

Not so fast! First of all, Markdown only supports "alt text" not image *captions*. They are different. Alt text is for people who need screen readers and describes the image. An image caption tells you information about the image, like the figure number (in an article or book), as well as the image source. But Markdown doesn't have built-in support for image captions, so how to implement that? 

There are a number of competing formats, but what I worry about most is export. I use Pandoc to export files to PDFs or Word documents, etc. so I need a format that is compatible with Pandoc filters to ensure that I don't break that feature as well. Also, I don't want to add too many non-standard elements to my documents. I already have annotations and citation blocks, as well as some hidden section markers. Handling these effectively without data loss or making the editor too messy has taken up most of my time as a developer. So, the best thing to do is to stick with the conventions I've been using for those, which is to use HTML comment markers alongside the markdown text, and then modify my Pandoc filters to read those.

Secondly, do I want to allow the user to use very large images? Or should I automatically resize images to make them smaller when they are imported? In the end I decided against the complexity of resizing images because the tools that work well for converting one type of image can easily mess up another type of image. Instead I simply warn the user if the image is over 10MB, and have a hard cap at 25MB. 

Third, what happens if the user deletes the image? Does it get deleted from the project bundle? That makes sense, but then the user can't "undo" or restore an older version that had that image. Better to save everything in the project, even if it is no longer referenced, but offer a "cleanup" command to delete unsused images manually if the user is sure they want to do that.

Oops, even as I write this I discover that the version control feature was never updated when I switched the app to a database-first approach. That means that image metadata stored in the database won't be restored. So, I need to go back and re-implement this feature to conform to the new architecture. I'm glad I caught this, but what was one project (add image support) is now two projects (add image support and re-implement version control).

After making all these decisions I have to make sure that the code is robust, that export to PDF and Word keeps the images and captions, and that the new code for image support doesn't accidentally create bugs in other aspects of the app, like zooming in on a particular section, inserting an image, and then zooming back out. 
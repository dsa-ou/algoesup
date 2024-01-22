---
layout: default
title: Background
parent: Deepnote
---
# Background
{: .no_toc}

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .h4 }
- TOC
{:toc}
</details>

## Organisation

Deepnote uses an organisational framework with three major parts:
[workspaces](https://deepnote.com/docs/workspaces)
can contain multiple [projects](https://deepnote.com/docs/projects) and each project
can contain multiple [notebooks](https://deepnote.com/docs/notebooks) and files.

The **workspace** is the highest level structure in Deepnote, and is designed to group related
Projects and enable team collaboration. Every user can create their own workspaces where they
can manage access, set permissions and oversee projects. A workspace can have multiple members
each with their own access permissions, but by default they can see all projects in the
workspace.

**Projects** are the next tier down from workspaces in terms of organisation and provide the main
working environment as well as the integrated file system. When you duplicated our
project, you duplicated all of the notebooks, files
and the environment too.

**Notebooks** are akin to Jupyter notebook. They are interactive documents that combine executable
code with richly formatted text and visualisations. Notebooks are where you will write your
essays.

## Deepnote vs Classic Notebook

Notebooks in Deepnote have similar functionality to classic Jupyter notebooks in that they
combine rich text, visualisations and executable code in a single document. But there are a few
notable differences in the UI and functionality worth mentioning.

Firstly, Deepnote is a cloud-based Jupyter notebook platform: this means no local software
installation is required to get started. It also means you can access your documents from
anywhere with an internet connection. This is a double edged sword of course, if you lose your
connection you lose access to your notebooks.

In Deepnote the divisions within a notebook are referred to as "blocks" instead of "cells",
but we will continue to use the classic terminology.
Deepnote retains the same structure of code and markdown cells as used in Jupyter notebook, but
it also provides additional cell types. Besides cells for data science, Deepnote adds rich text cells.
Unlike standard Jupyter notebooks,
these cells offer a what you see is what you get (WYSIWYG) text editing experience, similar to
applications such as MS word and Google Docs. They include spellchecking and the usual
formatting shortcuts like Ctrl + B for bold, Ctrl + I for italics, and so on. Rich text cells can be
advantageous if you plan to use Deepnote exclusively as they can simplify the writing process.
However, it is important to note that
any formatting from rich text cells will *not* be preserved if you download your notebook.
So if you plan to use your notebooks on other platforms it is advisable to stick
to Markdown cells for writing text.

Finally, there is a key difference in the way Deepnote and Jupyter handle Markdown. Normally to
create a line break in Markdown, either a double space followed by the Enter key, or a
backslash followed by the Enter key is required. This is the approach followed by Jupyter
Notebook and many other notebook interfaces. Deepnote, however, does it differently, simply
pressing Enter creates a line break without the need for explicit characters like double space
or backslash. This alternative approach is a deviation from the Markdown standard and affects
how rendered Markdown looks when moving between platforms.

## Collaboration

Deepnote was designed with collaboration in mind and offers several features to do this which
are not found on some other platforms.

Users in Deepnote can work together on projects simultaneously: any changes made to files and
notebooks within the project can be seen instantaneously by both parties. Real time
collaboration works best when you are also communicating in real time with your peers, say for
example, using Zoom, Teams, Discord or WhatsApp.

Additionally Deepnote offers the option for asynchronous communication through comments.
Comments can be left in a specific cell and are visible by anybody viewing the notebook. The
first comment made in a cell opens a new thread, and anyone commenting in a thread receives
email notifications after a new message is posted. Open threads can be resolved to hide them and
save space; threads can be reopened if needed. Any open threads are displayed in a main
comments panel on the right-hand side of a project.

Comments are one of the ways to give and receive feedback on your essays.
See the [feedback guide]({{site.baseurl}}/feedback) for more details.

## Limitations

As noted at the start of the guidance, Deepnote was selected as the platform for the Learning
Professional Skills with Algorithmic Essays project due to its simple interface, customisable
environment, and features for collaborative working. However, it is important to acknowledge and
assess its limitations.

As mentioned [above](#deepnote-vs-classic-notebook),
Deepnote deviates from Jupyter Notebook by having new types of cell such as rich text cells. It
also handles Markdown in an different way from most other platforms. This has implications for
how your notebooks will be rendered using different jupyter interfaces. The same notebook could
look different on other platforms compared to Deepnote; the length of text lines might be
different and some of the formatting may be altered or lost.

In addition to this, when working on a cloud-based platform such as Deepnote, executing cells
can sometimes feel slow, especially when the virtual machine has been idle for a while.
Furthermore, an issue has been observed when a Markdown cell contains an excessive amount of
text, which appears to slow down performance, potentially due to the autocomplete
functionality.

As a final point, the way Deepnote stores notebooks within the environment must be mentioned.
You can of course [upload a notebook]({{site.baseurl}}/deepnote-how-to#upload-a-notebook-or-file) to the system and access it like
any other file, but if you want to run the notebook, it must be moved to the **NOTEBOOKS**
section. This then becomes a problem if you wish to access the notebook file again, say using
the terminal. When a notebook is moved to this section it effectively takes the notebook out of
the integrated file system and locates it to a separate database which the user no longer has
access to.

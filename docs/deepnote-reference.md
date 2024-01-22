---
layout: default
title: Reference
parent: Deepnote
---
# Reference
{: .no_toc}

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .h4 }
- TOC
{:toc}
</details>

## Workspace interface

The [workspaces](https://deepnote.com/docs/workspaces) interface provides an overview of any
projects in your Workspace. On the left-hand side panel you will find a navigation menu
allowing you to quickly navigate to different sections of your workspace. Starting from the
top, the sections are:
- **Integrations** - This section allows you to set up and manage connections to data sources.
  This is mostly used for data science work.
  <!-- various integrations . An integration in the context of Deepnote refers to a
  connection or link to an outside platform, service or datasource. -->
- **Settings & members** - Manage who has access to the workspace and its resources.
- **Recents** - Projects listed in order of most recently opened.
- **Private projects** - A list of private projects, which only you have access to.
  Other workspace members can't see private projects.
- **Published apps** - This section shows any apps you have published. In DeepNote,
  an app is a notebooks in which some blocks have been hidden to
  abstract away technical details. This may be useful to present your findings to
  stakeholders with non-technical backgrounds.
- **PROJECTS**. - A list of *all* projects within the workspace.

## Project interface

A [project](https://deepnote.com/docs/projects)'s interface has similarities to the interface
for your workspace. Starting from the top, the sections on the left-hand side panel are:
 - **NOTEBOOKS** - This section is where your notebooks live. If you want to
   actively work on your notebooks they must be added to this location.
 - **INTEGRATIONS** - This section allows
   you to use an integration defined for the workspace. Integrations are mainly used in data science.
 - **FILES** - Each project in Deepnote has an integrated file system which you
   can view and access in this section. You can create and
   [upload files]({{site.baseurl}}/deepnote-how-to#upload-a-notebook-or-file)
   and folders here.
 - **TERMINALS** - Deepnote allows you to launch terminals from this section by
   clicking on the "+" icon. As you would expect you can access the local file
   system through the terminal to run scripts or complete other tasks. Note that
   you cannot access any notebooks located in the NOTEBOOKS section from a
   terminal, they are stored in a separate database and not considered part of the
   file system.
 - **TABLE OF CONTENTS** - This section will show the major headings of the
   current notebook you are working on so you can quickly navigate through your
   document by clicking on them.
 - **ENVIRONMENT** - The environment section shows a simple overview of the
   environment you are currently working in. There is an option to expand this
   section into a more detailed view by clicking on the cog symbol next to the
   ENVIRONMENT heading in the top right hand corner of the panel.

## Notebooks

Notebooks in Deepnote have the same core functionality as Jupyter Notebooks:
they combine executable code and text in the same document.

See [Deepnote vs Classic Notebook]({{site.baseurl}}/deepnote-background#deepnote-vs-classic-notebook)
for some differences between the two.

## Access levels

Access levels are the range of permissions or capabilities assigned to a user in Deepnote. They
differ between the contexts of workspaces and projects.

The access levels for projects are:
- **App User**: Can use published app, but cannot view the project source code.
- **View**: Can inspect the project, but cannot view or post comments nor execute or edit files.
- **Comment**: Can post and view comments in addition to inspecting the project.
- **Execute**: Can execute code in addition to viewing and commenting, but cannot change anything or use terminals.
- **Edit**: Can use terminals, connect datasets, comment and edit files as well as view and execute.

The access levels for workspaces are:

- **Viewer**: Viewers can see all projects and members of a workspace.
  They can leave comments in projects but can't make any changes.
  They can duplicate a project to another workspace as well as
  request additional access from the team's owner. <!-- When duplicating a project
      to another workspace, custom environments and integrations are not
      preserved. -->
- **Contributor**: Contributors can execute all notebooks within the workspace as
  well as change input block values. They cannot make changes to code.
- **Editor**: Editors can create and edit workspace projects.
  <!-- Members can also connect or disconnect integrations from projects but they can't edit or create them. -->
- **Admin**: Admins have all access rights, including permission to
manage workspace members.

## Cells

Cells (called 'blocks' in DeepNote) are the divisions within each notebook.
They are a distinct area where code or text can
be added depending on the type of the cell.
See our [how-to guide]({{site.baseurl}}/deepnote-how-to#notebook-operations) for working with cells.

## Terminal

A terminal will give you a command line interface for your project and runs a bash shell.

Launching a Terminal in Deepnote allows you to run scripts or complete tasks where the GUI is
not suitable.

See the DeepNote [documentation on terminals](https://deepnote.com/docs/terminal) for more information.

## Environment

The environment refers to the setup and configuration that supports the execution of code
within your project.

The code in each project runs on a virtual machine which is an isolated computing environment
with its own CPU memory and storage resources. These specifications can be adjusted in a
limited way if required and various software packages can be added to your environment to suit
your needs.

When you copied our project, you also copied the environment.

See DeepNote's [documentation on custom environments](https://deepnote.com/docs/custom-environments)
for more information.

## Real-time collaboration

Real time collaboration refers to the capability of multiple users to work on the same
documents in the same project at the same time. Any changes to documents can be seen by all
users working on the project as and when they happen.

See DeepNote's [documentation on real-time
collaboration](https://deepnote.com/docs/real-time-collaboration) for more details.

## Asynchronous collaboration

Asynchronous collaboration is a method of working where users do not have to be working at
the same time. Users can contribute to projects and documents at their own pace to suit
their own schedule.

The main tool for asynchronous collaboration in Deepnote is the
[comments](https://deepnote.com/docs/comments) system. Users can comment on code and text
in the corresponding cells to communicate with peers.

## Command palette

The command palette provides quick access to all of the files in a project and the most popular
actions.

You can open and close the command pallet by pressing Cmd + P on Mac or Ctrl + P on Windows.

## Members

A member is a DeepNote user associated with a particular workspace.

When a user is a member of a workspace, they typically have access to all the projects within
that workspace, but the access permissions can be adjusted.

Projects do not have members, but you can give or be given access to a project with
certain permissions. See [Access levels](#access-levels) for more information.

## Markdown cheat sheet

| Feature           | Syntax/Example                    |
|-------------------|-----------------------------------|
| **Headers**       |                                   |
| H1 Header         | `# H1 Header`                     |
| H2 Header         | `## H2 Header`                    |
| H3 Header         | `### H3 Header`                   |
| H4 Header         | `#### H4 Header`                  |
| H5 Header         | `##### H5 Header`                 |
| **Code**          |                                   |
| Inline Code       | `` `Code` ``                      |
| Code Block        | ```` ```Code block``` ````        |
| **Formatting**    |                                   |
| Italic            | `_italic_` or `*italic*`          |
| Bold              | `**bold**` or `__bold__`          |
| Strikethrough     | `~~strikethrough~~`               |
| **Links**         |                                   |
| External Link     | `[Google](https://www.google.com)`|
| Section Link      | `[Top](#top)`                     |
| **Lists**         |                                   |
| Bulleted List     | `- List item`                     |
| Numbered List     | `1. List item`                     |
| **Math**          |                                   |
| Inline Math       | `$x=1$`                           |
| Math Block        | `$$$x=1$$$`                       |
| **Other**         |                                   |
| Quote             | `> Quote`                         |
| Divider           | `---`                             |
| HTML              | `<h1>Title</h1>`                  |

## Keyboard shortcuts

Deepnote has many [keyboard shortcuts](https://deepnote.com/docs/keyboard-shortcuts) for
quickly performing typical actions on cells and text.

**General**

| MAC | WINDOWS & LINUX | ACTION |
|---|---|---|
| ⌘ + P | ctrl + P | Show/Hide command palette |

**Block Actions**

| MAC | WINDOWS & LINUX | ACTION |
|---|---|---|
| ⇧ + ↵ | shift + enter | Run current block and move cursor to next block (creates a new cell if at the end of the notebook) |
| ⌘ + ↵ | ctrl + enter | Run current block |
| ⌘ + ⇧ + . | ctrl + shift + . | Stop execution |
| ⌘ + ⇧ + H | ctrl + shift + H | Hide/Show block output |
| ⌘ + ⇧ + M | ctrl + shift + M | Toggle between code and Markdown block |
| ⌘ + ⇧ + ⌫ | ctrl + shift + backspace | Delete block |
| ⌥ + ⇧ + ↑ | alt + shift + ↑ | Move block up |
| ⌥ + ⇧ + ↓ | alt + shift + ↓ | Move block down |
| ⌘ + ⇧ + D | ctrl + shift + D | Duplicate block |
| ⌘ + J | ctrl + J | Add new code block below current one |
| ⌘ + K | ctrl + K | Add new code block above current one |
| ⌘ + Z | ctrl + Z | Undo |
| ⌘ + ⇧ + Z | ctrl + shift + Z | Redo |

**Code Editing**

| MAC | WINDOWS & LINUX | ACTION |
|---|---|---|
| ⌘ + D | ctrl + D | Expand selection (multiple cursors) |
| tab | tab | When caret is at the beginning of a line, add indent; otherwise, show autocomplete suggestions |
| ⇧ + tab | shift + tab | Decrease indent |
| ⌘ + / | ctrl + / | Toggle line/selection comment |
| ⌥ + ↓ | alt + ↓ | Move lines down |
| ⌥ + ↑ | alt + ↑ | Move lines up |

**Terminal**

| MAC | WINDOWS & LINUX | ACTION |
|---|---|---|
| ⌘ + C | ctrl + shift + C | Copy selected text |
| ⌘ + V | ctrl + shift + V | Paste |
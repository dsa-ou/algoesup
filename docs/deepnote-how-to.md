---
layout: default
title: Deepnote How to guides
parent: Deepnote
---
# Deepnote how-to guides
{: .no_toc}

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .h4 }
- TOC
{:toc}
</details>

## Account operations

### Sign up for Deepnote
This is explained in our [Getting Started]({{site.baseurl}}/getting-started#create-a-deepnote-account) guide.

### Log in
If you have logged out, to log back in you need to verify your email again:

1. Go to the [sign-in page](https://deepnote.com/sign-in).
2. Enter your email. Click the CAPTCHA button. Click **Continue with email**.
3. You will receive an email from DeepNote with a link. Click on it.

## Workspace operations
Before any of the following operations, you must change from project view to workspace view:
1. Click on your workspace name in the top left corner of the screen.
2. From the drop-down menu, select **Back to workspace**.

You will now see a list of the projects in your workspace:
![Workspace view](workspace-view.png)
Some projects were automatically added by DeepNote when creating your workspace.

After you completed the desired workspace operations, click in the side panel
on the project you want to work next.

### Enable sharing
1. In the [workspace view](#workspace-operations), click on **Settings & members** in the side panel.
2. Click on the **Project settings** tab.
3. Turn on the option **Allow projects to be shared publicly**.

<!-- ## Create a new workspace
1. Click the drop-down menu in the top left corner labelled with the workspace name.
2. In the drop-down menu, click the + icon next to the email address associated with your
   account.
3. Select your workspace plan.
4. Enter a name for your workspace, and select the appropriate option for what it will be used
   for.
5. Click **continue**.
6. Invite members to the workspace if applicable.
7. Click **Create workspace**. -->

## Project operations

### Rename, duplicate, download or delete a notebook or file
1. In the side panel, hover over the name of the chosen notebook or file.
2. Click on the three dots that appear.
3. From the drop-down menu, select the desired operation.

For notebooks, the download operations are called **Export as .ipynb** and **Export as .pdf**.
If your notebook contains other types of cells besides Markdown and code,
the downloaded `.ipynb` file won't be rendered correctly on other Jupyter platforms.

### Duplicate our project
This is explained in our [Getting Started]({{site.baseurl}}/getting-started#duplicate-our-project) guide.

### Share your project
The following assumes you have [enabled sharing](#enable-sharing) for your workspace.
1. Click the **Share** button in the top right corner of the screen.
2. To the right of **Anyone with a link to this project**, click on the drop-down menu and select **Comment**.
3. Click the highlighted blue **link to this project**, to copy the link.
4. Share that link with your peers by email or by posting in your course's forum.

### Create a new notebook
1. Click on the + icon next to the **Notebooks** heading in the side panel.
2. Enter a name for your new notebook, then press Enter.

### Upload a notebook or file
The simplest way is to drag the notebook or file from your desktop to
the **Notebooks** or **Files** section in the side panel.

Alternatively, to upload a file:
1. Click on the + icon next to the **Files** heading in the left panel.
2. Select **Upload file** from the drop-down menu.
3. In the file browser, navigate to the file you want to upload, then click **Open**.

## Notebook operations

To perform an action on a cell, do *one* of the following:
- Click on the cell to select it: the outline becomes blue. Press the action's keyboard shortcut.
- Hover over the cell. A pop-up menu appears in the top right corner of the cell.
  Click on the action's icon or click the three dots to get a menu of actions.

### Run one or all cells
Running a cell executes the code or formats the Markdown text.

To run one cell, do *one* of the following:
- Press Ctrl + Enter (Mac: Cmd + Enter) if the cell is [selected](#notebook-operations).
- Click the triangle icon in the top right corner of the cell.

To run all cells, click **Run notebook** in the top right corner of the notebook.

{: .note}
The first time you run code, it will take some time, because
DeepNote must first start a server with the necessary software.

### Add a cell
To insert a cell between two existing cells:
1. Hover the mouse between the two cells.
2. Click on the line that appears between both cells and do *one* of the following:
   - To insert a code cell, press `c` followed by Enter.
   - To insert a Markdown cell, press `m` followed by Enter.

To append a cell, scroll down to the end of the notebook and do *one* of the following:
- To add a code cell, click on the **Code** button.
- To add a Markdown cell, click on the **Text** button and select **Markdown**.

### Delete a cell
Do *one* of the following:
- Press Ctrl + Shift + Backspace (Mac: Cmd + Shift + Backspace) if the cell is [selected](#notebook-operations).
- Click the bin icon in the top right corner of the cell.

### Comment on a cell
Do *one* of the following:
- Press Ctrl + Alt + C (Mac: Cmd + Alt + C) if the cell is [selected](#notebook-operations).
- Click the speech bubble icon in the top right corner of the cell.

After typing your comment, press the upwards blue arrow to finish.

{: .warning}
You must be logged into your account to comment on notebooks shared with you.
If you're not logged in, your comments are marked as 'anonymous user' and
the essay's author won't see them.

### Format a code cell
This 'pretty prints' the code. Do *one* of the following:
- Press Alt + Shift + F if the cell is [selected](#notebook-operations).
- Click the three dots in the top right corner of the cell and
  select **Format code** from the drop-down menu.
  (To avoid scrolling all the way down, type `f` in the search box of the menu.)

{: .note}
Formatting takes 1-2 seconds and adds an empty line (which you may delete)
to the end of the cell.

{: .warning}
If you get a message 'parsing failed',
then the code cell is not valid Python and can't be automatically formatted.
This may happen if the cell has IPython commands starting with `%`.
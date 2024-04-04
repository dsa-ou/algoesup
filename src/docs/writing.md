# Writing guide

This document provides guidance on how to produce your essay.
{: .fs-6 .fw-300}

!!! warning
    Although we wish to accommodate novice programmers in the future,
    the guide currently has data structures and algorithms students in mind.

An essay can have more than one author, although more than two is harder to manage.
Deepnote and Colab make it easy to work collaboratively on a single notebook,
at the same time or asynchronously, and leave comments to co-authors.
You may wish to first pitch your essay idea to your peers, to recruit co-authors.

In the rest of this guide, 'you' and 'your' are both singular and plural pronouns,
to refer simultaneously to a single author or multiple authors.

!!! tip
    You may wish to keep this guide open while going through
    your copy of our template.

## Problem
It's worth spending time on choosing an appropriate problem before putting effort into an essay about it.
You may invent your own problem or select an existing one.
For example, it may be a non-assessed exercise from your course, or
it may relate to your hobby or work. If so, provide any information the reader needs to understand the problem.
If the problem is from your work, get permission from your employer or client.

There are [many websites](https://www.freecodecamp.org/news/the-most-popular-coding-challenge-websites/) with thousands of algorithmic problems to choose from.
We have used [Kattis](https://open.kattis.com) and [LeetCode](https://leetcode.com/problemset/all/) in the past.

Some sites, like LeetCode, tag their problems with the data structure or algorithmic technique needed,
like 'array' or 'sorting'. This helps you find problems about a particular topic.

Some sites, like LeetCode, have official and user-provided solutions, but the latter
may be terse (single-letter identifiers, no comments) or not fully analysed.
Other sites, like the [International Olympiad in Informatics](https://ioinformatics.org/page/contests/10),
often have just solution hints or outlines.
You may thus wish to write an essay that fully implements a solution outline or
that improves and compares several user solutions.
Either way would be useful to the user community of those sites.

It is often said that the best way to learn a topic is to have to explain it to others.
You may thus wish to pick a problem on a topic you're *not* comfortable with,
choose two existing solutions, and explain them in an essay.

If you're undecided, make a shortlist of 2–3 problems and ask your peers for their opinion.

## Text
An essay presents two or more algorithmic solutions for a computational problem,
and concludes which one is better, according to some criteria.
Possible criteria include:

- time and space complexity
- empirical run-times and memory used
- simplicity of the solution
- ease of adapting the solution to similar problems.

The essay should thus have a **clear narrative**, going from the problem to the conclusion.

An algorithmic essay contains more text than code, and while code can and should have comments,
the text carries most of the explanation. It's thus important for the text to be clear and error-free.

Essays can be written in any style: it's a personal choice.
For example, you can use 'we', 'I' or an impersonal form.

!!! tip
    Strunk and White's *The Elements of Style* is a classic.
    The examples are dated but the advice is good.

!!! tip "Deepnote"
    Notebooks can have rich-text cells (headings, paragraph, bullet item, etc.) that,
    contrary to the Markdown cells, are spell-checked as you write the text and
    support keyboard shortcuts, like Ctrl + B to put the selected text in bold.
    Unless you want to keep your essays in Deepnote, we do not recommend using rich-text cells,
    as their formatting is lost when downloading the notebook to your computer.

## Structure
An essay starts with a **title** that states the problem or the algorithmic technique to be used.
Next, put your name(s) and the current **date**, which should be updated whenever you edit the essay.

Next, *without* any heading, comes the introduction. It should state what the essay is about.
Normally an essay's aim is to solve a particular problem, but it may also
illustrate a general technique, like space-time trade-offs or recursion,
or highlight an issue, like the difference between complexity analysis and run-time performance.

The introduction should also state what you assume the reader to know,
as no essay can explain everything from first principles. For example,
tell the reader that they must know about binary trees to understand your essay.

Following the introduction, use section headings to structure your essay, for example:

- **Problem**: this section describes the problem, with some examples.
- **Algorithms**: this section outlines two or more algorithms that solve the problem and their complexity.
- **Implementations**: this section implements and tests only the most promising algorithms.
- **Comparison**: this section compares the implemented algorithms according to other criteria, e.g. their run-times.
- **Conclusion**: this section summarises the findings and concludes which approach is best.

The algorithms and implementations sections may have subsections, one per algorithm.

An alternative structure implements each approach before evaluating all of them:

- **Problem**: this section describes the problem, with some examples.
- **First approach**: this section outlines an algorithm, implements it and tests it.
- **Second approach**: this section presents another algorithm and its implementation.
- ...: further sections, one per approach.
- **Evaluation**: this section states the criteria to be used and evaluates each approach according to them.
- **Conclusion**: this section summarises the findings and concludes which approach is best.

If the problem description is a single paragraph, you may include it in the introduction,
rather than having a separate section.
If you didn't invent the problem, indicate its source, e.g. by providing a link to a website
or by writing something like "This is problem 4.5 in [book title] by [author]."

## Algorithms
You should choose at least two sufficiently different algorithms that solve the problem,
and describe each one succinctly, preferably *before* implementing it,
to make the code easier to understand for the reader.

We recommend to not describe algorithms that are only slight variants of each other,
as this is usually of little interest, and 
to only include two algorithms in your first draft.

If you're using solutions by others, e.g. by LeetCode users,
acknowledge the original author and provide a link to their solution.
If you have modified their solutions, state what you have changed and explain why.

You should include worst-case complexity analyses of the various solutions you propose,
as this helps discard the inefficient ones that may not be worth implementing.

## Code
See our [coding guide](coding.ipynb).

## Final check
Whether it's your essay's first draft or final version, before you share it with others,
you should restart the kernel and run all cells, so that you have a 'clean' version.
Then, after a break, read your essay with 'fresh eyes' from start to end
and fix any typos or missing explanations you find.

Look at the table of contents of your notebook and check that your section headings
are at the right level.

!!! tip "Deepnote"
    The table of contents is on the left sidebar.
!!! tip "Colab"
    To see the table of contents, click the bullet list icon in the left sidebar.

Finally, let others comment on your essay and help you produce a better version.
See our [feedback guide](feedback.md) for details.

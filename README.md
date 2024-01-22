# Algorithmic essays support

This repository contains resources to support the creation of **algorithmic essays**,
which we define as short reports, with code, that present at least two different
approaches to solving a computational problem and evaluate each approach against
some criteria, like efficiency, simplicity, ease to modify.

Algorithmic essays may help the development of professional skills,
like writing clearly and succinctly, giving and acting on feedback,
producing clean code, and working collaboratively.

We created these resources:
- **Guides** on how to: write and structure essays;
  lint, format and type check the code; ask for, give and handle feedback on essays.
- **Example essays** for introductory programming
  and data structures and algorithms (DSA) courses.
- **Essay templates** that provide a starting point for writing essays.
- A **library** of helper functions to easily test functions and measure their run-times.

The guides are on our [documentation site](https://dsa-ou.github.io/algoesup) and
the rest is in our [Deepnote project](https://deepnote.com/workspace/lpsae-cc66-cd5cf5e4-ca6e-49d8-b6ee-dbbf202143d3/project/Algorithmic-Essays-acd23b74-5d63-4ef4-a991-3b8a049ddf6b/notebook/example-jewels-21dfeb1e2a8c4abd8ffb5d9ab40bef40),
which you can copy to your Deepnote account.

If you want to adapt this material to your course, this repository has
the guides in the `docs/` folder and the rest in the `Deepnote/` folder.

## Development
If you want to contribute to this repository, create a local virtual environment,
preferably with Python 3.10 for compatibility with Deepnote, and install the software:
```bash
python3.10 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
To preview locally the documentation that will be in GitHub Pages, follow
[this guidance](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll).
The Jekyll installation instructions include how to install Ruby.
Bundler is usually automatically installed during the Ruby installation.

GitHub recommends to regularly do `bundle update github-pages` to ensure that
the local site preview looks like on GitHub Pages.

After accepting a commit to folder `Deepnote/`, the owners will upload the
updated files to the Deepnote project linked above.

## Licences

The code and text in this repository are
Copyright © 2023 by The Open University, UK.
The code is licensed under a [BSD 3-clause licence](LICENSE).
The text is licensed under a
[Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by/4.0).
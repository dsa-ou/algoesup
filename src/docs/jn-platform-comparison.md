# Comparison of Jupyter Notebook Platforms

This document lists and compares aspects of various widely available Jupyter
Notebook (JN) platforms for use in educational settings and writing algorithmic
essays. A [comparison table](#comparison-table) is provided at the bottom of
the page.

The [datasciencenotebook.org](https://datasciencenotebook.org/) website
developed by [Robert Lacok](https://www.linkedin.com/in/robert-lacok/) and the
[awesome-jupyter](https://github.com/markusschanta/awesome-jupyter) GitHub
repository have been invaluable in locating and evaluating many of these
platforms. While some of our assessment criteria overlap with those resources,
we have evaluated the platforms from the perspective of educators with a
specific task in mind: writing and sharing algorithmic essays. 

## Evaluation criteria

We use the following criteria to evaluate the platforms:

- **full compatibility with JN files (.ipynb)**
- **free account**
- **Hosted locally or on the cloud**
- **Customisable run-time environment**
- **Share via links with access levels**
- **GitHub integration**
- **Classic JN interface or a new interface**
- **Real time collaboration**
- **Commenting on cells**
- **Access to terminal and file system**
- **Access to underlying notebook files**

The following paragraphs briefly note why we have chosen each aspect, and why these
features are desirable in educational settings and for writing algorithmic essays.

An important consideration for any platform is whether it is **fully compatible
with `.ipynb` files**. This file type, used by many platforms, originates from
when the platform was called Ipython Notebook. The ability to import and export
these files removes dependency on a single platform, and allows flexibility in
where essays are written and shared.

Being free to use, or having a **free account**, is a highly desirable feature
of any platform. It lowers the barrier to participation for both students and
educators, removes extra budget requirements, and can increase the longevity of
projects.

All platforms are either **hosted locally, or on the cloud**, and this
distinction has implications for setup requirements, UI, and collaboration.
Cloud-based platforms require the least setup and typically support
collaboration and commenting on cells. However, they mostly cater for data
scientists in their documentation and the UI and feature set can change without
notice. Access to the underlying notebook files may be restricted, complicating
code linting and interfaces can vary, increasing the learning curve. In
contrast, locally installed JN platforms tend to have a familiar and consistent
interface, provide unrestricted access to files and have more balanced
documentation. However, many lack simple options for collaboration and
commenting, and they must be installed and configured by the user. 

Any platform suitable for pedagogical practice and particularly writing
algorithmic essays must have a **customisable run-time environment**. It should
be adaptable to different course specifications, allowing the use of 3rd party
libraries and tools. Often, the ability to install new Python packages via pip
is sufficient, but some platforms go further by allowing environment
customisation through a Dockerfile.

Students are often required to share their work with faculty and peers for
marking, receiving  feedback, and collaboration. If a platform has the option
to **share via links with access levels**, students can grant recipients
permission to read only, leave comments on, or edit the document based on their
role. Links can be shared by email to  specific individuals or to a wider
audience on a forum. In some cases, work can be shared without the recipient
needing an account on the same platform.

The ability for a JN platform to integrate with other platforms can be highly
desirable. For instance, **integration with GitHub** allows you to leverage
version control when developing resources, use a single repository to serve
multiple platforms, and back up your materials. 

The UI is often the first element of a platform a user encounters. Ease of use,
familiarity and the available controls are all important factors that can help
reduce the learning curve for students. Since students on our data structures
and algorithms course must install the classic JN locally on their machines,
it's important to consider whether a platform provides the **classic JN
interface or a New interface**

Some platforms allow **real-time collaboration** among their users. This means,
students can work together on documents simultaneously, and see changes
instantly. Collaborating on essays this way fosters good teamwork and communication
skills.

**Commenting on cells** is useful in many ways. Comments are located close to
the relevant code or text, often contained in separate “threads” where they can
be edited, deleted and resolved. This allows for feedback and marking without
modifying the existing structure of the notebook.

Having **access to a terminal and the underlying file system** allows anyone on
the platform to use command line tools like linters and formatters, run custom
scripts, and manage auxiliary files.

Having **access to the underlying notebook** files in combination with access
to a terminal, allows linters and formatters to be used on these files.

## Comparison Table

| Platform                     | .ipynb Compatibility | Free Account | Hosting       | Customisable Run-time | Share via Links | GitHub Integration | Interface     | Real-time Collaboration | Commenting on Cells | Terminal & File System Access | Access to Notebook Files |
|------------------------------|----------------------|--------------|---------------|-----------------------|-----------------|--------------------|---------------|-------------------------|----------------------|-------------------------------|--------------------------|
| [Amazon SageMaker Notebooks](https://aws.amazon.com/sagemaker/notebooks/) | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✓                             | ✓                        |
| [Apache Zeppelin](https://zeppelin.apache.org/)              | ✓                    | ✓            | Local/Cloud   | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✓                             | ✓                        |
| [Azure Notebooks](https://notebooks.azure.com/)              | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [Carnets (iOS)](https://holzschu.github.io/Carnets_Jupyter/)                | ✓                    | ✓            | Local         | ✓                     | ✗               | ✗                  | Classic       | ✗                       | ✗                    | ✓                             | ✓                        |
| [CoCalc](https://cocalc.com/)                       | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✓                             | ✓                        |
| [CodeOcean](https://codeocean.com/)                    | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✓                             | ✓                        |
| [Count](https://count.co/)                        | ✗                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [Datalore (JetBrains)](https://www.jetbrains.com/datalore/)         | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✓                             | ✓                        |
| [Deepnote](https://deepnote.com/)                     | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✓                             | ✓                        |
| [Google Colab](https://colab.research.google.com/)                 | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [Hyperquery](https://hyperquery.io/)                   | ✗                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [IBM Watson Studio](https://www.ibm.com/cloud/watson-studio)            | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [Jupyter Notebook](https://jupyter.org/)             | ✓                    | ✓            | Local         | ✓                     | ✗               | ✓                  | Classic       | ✗                       | ✗                    | ✓                             | ✓                        |
| [JupyterLab](https://jupyter.org/)                   | ✓                    | ✓            | Local         | ✓                     | ✗               | ✓                  | New           | ✓                       | ✗                    | ✓                             | ✓                        |
| [Kaggle Notebooks](https://www.kaggle.com/kernels)             | ✓                    | ✓            | Cloud         | ✗                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [Mode Notebooks](https://mode.com/notebooks/)               | ✗                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [Noteable](https://noteable.io/)                     | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [nteract](https://nteract.io/)                      | ✓                    | ✓            | Local         | ✓                     | ✗               | ✓                  | Classic       | ✗                       | ✗                    | ✓                             | ✓                        |
| [Observable](https://observablehq.com/)                   | ✗                    | ✓            | Cloud         | ✗                     | ✓               | ✗                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [Polynote](https://polynote.org/)                     | ✗                    | ✓            | Local         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✓                             | ✓                        |
| [Pluto.jl](https://plutojl.org/)                     | ✗                    | ✓            | Local         | ✓                     | ✗               | ✗                  | New           | ✗                       | ✗                    | ✓                             | ✓                        |
| [Query.me](https://query.me/)                     | ✗                    | ✗            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
| [Quarto](https://quarto.org/)                       | ✓                    | ✓            | Local         | ✓                     | ✗               | ✓                  | Classic       | ✗                       | ✗                    | ✓                             | ✓                        |
| [Saturn Cloud](https://saturncloud.io/)                 | ✓                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✓                             | ✓                        |
| [VS Code with Jupyter](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)         | ✓                    | ✓            | Local/Cloud   | ✓                     | ✗               | ✓                  | Classic/New   | ✓                       | ✓                    | ✓                             | ✓                        |
| [Zepl](https://www.zepl.com/)                         | ✗                    | ✓            | Cloud         | ✓                     | ✓               | ✓                  | New           | ✓                       | ✓                    | ✗                             | ✗                        |
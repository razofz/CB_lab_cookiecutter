# Analysis project structure

There are many roadblocks inherent in the data analysis workflow, especially
for single-cell genomics. The iterative nature makes it challenging to adhere
to a rigid structure, that might be more helpful in e.g. software engineering
but adds too much overhead for this type of analysis. However, at some point
reproducibility must be considered. Of course for publishing a paper with
accompanying code, but also for collaborating with other bioinformaticians, and
especially for collaborating with oneself; coming back to an analysis weeks,
months or even years later, it is not easy to remember which script generated
which figure, and what version of the script, and also which scripts need to be
run before the actual figure script. This repository is an attempt to help
alleviate those concerns.

This is a [cookiecutter](https://github.com/cookiecutter/cookiecutter). A
cookiecutter is a template for generating a directory structure plus helpful
files for an analysis project. When generating, one is asked questions that
helps tailor the structure to the specific project and data. This one is
inspired by the
[Data Science cookiecutter](https://drivendata.github.io/cookiecutter-data-science/) (this is a good link to read).

## How to use

Have [cookiecutter](https://github.com/cookiecutter/cookiecutter) installed
(through e.g. [conda](https://docs.conda.io/en/latest/)), navigate to the directory you want
to have the project directory in, and run this command:

```bash
cookiecutter gh:razofz/CB_lab_cookiecutter
```

This will result in prompts like this:

    author_name [Your name]:
    github_username []:
    data_owner [Dataniel Ownerson]:
    data_owner_initials [DO]:
    lab_leader [Laboriel Leaderson]:
    lab_leader_initials [LL]:
    one_word_description [analysis]:
    project_name [LL_DO_analysis]:
    repo_name [LL_DO_analysis]:
    description [A short description of the project.]:
    rng_seed [12345]:

One might enter values like these:

    author_name [Your name]: Rasmus Olofzon
    github_username []: razofz
    data_owner [Dataniel Ownerson]: Sara Palo
    data_owner_initials [SP]: 
    lab_leader [Laboriel Leaderson]: Charlotta Böijers
    lab_leader_initials [CB]:
    one_word_description [analysis]: atac
    project_name [CB_SP_atac]: 
    repo_name [CB_SP_atac]:
    description [A short description of the project.]: Analysis of ATAC-seq data.
    rng_seed [12345]:

That will result in a directory structure like this:

    CB_SP_atac/
    ├── data
    │   ├── adhoc
    │   ├── external
    │   ├── interim
    │   ├── processed
    │   └── raw
    ├── envs
    │   ├── Dockerfile
    │   ├── environment.yaml
    │   └── meta
    │       └── snakemake-bioinf.yaml
    ├── figures
    │   └── figure_mapping.csv
    ├── get_setup.sh
    ├── notebooks
    ├── references
    ├── reports
    │   └── smk_report_captions
    │       └── workflow.rst
    ├── Snakefile
    └── src
        ├── smk
        │   └── visualization
        ├── smk_config.yaml
        └── Snakefile

    16 directories, 9 files

*as of now (2022-08-30).*

Values for certain files will be filled according to the questions above:

From `src/smk_config.yaml`:

```yaml
[..]
processed_dir: "data/processed/"
raw_dir: "data/raw/"
report_dir: "reports/"
docs_dir: "docs/"
data_owner: "CB_SP"
data_owner_longname: "Charlotta Böijers: Sara Palo"
project_name: "CB_SP_atac"
[..]
```

Or, from `reports/smk_report_captions/workflow.rst`:

```markdown
CB_SP_atac
-------------------------------

Data generated in Charlotta Böijers lab, by Sara Palo. Data analysed by Rasmus Olofzon,
https://github.com/razofz.

Project description
-------------------

Analysis of ATAC-seq data.

Graph of rules:
```

## How to work with the generated content

The idea is to make use of tools such as:

- [Snakemake](https://snakemake.github.io/)
  - A [workflow management system](https://en.wikipedia.org/wiki/Bioinformatics_workflow_management_system)
    ([WMS](https://en.wikipedia.org/wiki/Scientific_workflow_system)).
  - [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/)
  - [Snakemake tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html#tutorial)
- [git](https://git-scm.com/)
  - [Wikipedia article on git](https://en.wikipedia.org/wiki/Git)
  - [A good tutorial on git](https://www.atlassian.com/git/tutorials/what-is-git),
    this is also good as a reference even after having learnt the basics.
  - [A video explanation of git (15 minutes)](https://www.youtube.com/watch?v=USjZcfj8yxE)
- [Github](https://github.com/)
  - A separate thing from git: git is a software tool, Github is a hosting
    service that hosts git repositories.
  - [Wikipedia article on git](https://en.wikipedia.org/wiki/GitHub)
- [Docker](https://www.docker.com/)
  - A tool for [container technology](https://en.wikipedia.org/wiki/Containerization_(computing)).
  - [Wikipedia article on Docker](https://en.wikipedia.org/wiki/Docker_(software))
- [conda](https://docs.conda.io/en/latest/)
  - A [package manager](https://en.wikipedia.org/wiki/Package_manager) for Python and R packages.
  - [Conda tutorial](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
- [jupytext](https://jupytext.readthedocs.io/en/latest/)
  - A tool that converts between .ipynb and (e.g.) .py format. The reason for
    this is that .ipynb are basically in json format, and contains all cell
    outputs. This makes them not suited for version control, since e.g. a small
    figure title change in a plot can generate a very big diff. So we do not
    keep .ipynb files in version control, but auto-convert them to .py files,
    with no outputs saved, and version control those. Then all diffs are
    changes in the actual code.
- [direnv](https://direnv.net/)
  - A tool for [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).
    As default only used to provide a `$PROJECT_PATH` env variable, so all
    scripts etc can refer to the project root. Partly because it is easier,
    partly to minimise personal information we give out.  

### Good principles

> Separate data processing code from plotting/visualisation code.

The reason for this is that usually data processing takes (much) longer than
visualisation, and usually one wants to tweak plots/figures (or someone else
wants one to tweak them), and it's nice to not have to wait for e.g. an hour
for the processing step before seeing the new version of the plot.

Several good principles from the aforementioned
[Data Science cookiecutter](https://drivendata.github.io/cookiecutter-data-science/)
applies here as well:

> *"**Data is immutable**  
> Don't ever edit your raw data, especially not manually, and especially not in
> Excel. Don't overwrite your raw data. Don't save multiple versions of the raw
> data. Treat the data (and its format) as immutable. The code you write should
> move the raw data through a pipeline to your final analysis. You shouldn't
> have to run all of the steps every time you want to make a new figure (see
> Analysis is a DAG), but anyone should be able to reproduce the final products
> with only the code in src and the data in data/raw."*

This is why there are several sub-directories in the `data` dir:

    ├── data
    │   ├── adhoc
    │   ├── external
    │   ├── interim
    │   ├── processed
    │   └── raw

- `adhoc` is for the iterative, "quick-to-results"-focused work; the work one
  does when exploring data, tries different directions and generates basis for
  decisions on where to take the analysis. I.e. what was mentioned in the
  introduction above as inherent to this work, but also inherently messy.
    - The idea with this is a "sandbox" where one can work and not worry about
      structure, but generate results. *What is important*, though, is to take
      some time when it is clear something will be used/be part of the official
      analysis/project, to lift the relevant parts for that out and put it into
      a script in the `src` dir, to be used for a Snakemake rule (a
      corresponding rule in the `Snakefile`).
- `external` is for external data. Could be data from a related paper to
  compare with, could be a list of genes somewhere, etc.  
  I.e., data that is used in the analysis but has not been generated in the
  project.
- `interim` is for middle-steps with the data, that are not important and can be
  deleted if one needs more hard drive space. For example, splitting data into
  chromosomes and processing them in parallel for speed, and then joining the
  resulting files. Then the chromosome-specific files can go into `interim` and
  the joined result file can go into `processed`.
- `processed` is for, you guessed it, processed data. Lists of differentially
  expressed genes for clusters or subsets of the data, umap plots, rds files
  with a processed Seurat object, anything that is results and/or relevant for
  the paper.
- `raw` is for the *immutable*, raw data. For sequencing data, the count
  matrices/Cellranger output. ***Never*** write to this, or edit the data.
  Everything to do with this dir should *read* from it, and then write to
  somewhere else (e.g. `interim` or `processed`).

> *"The first step in reproducing an analysis is always reproducing the
> computational environment it was run in. You need the same tools, the same
> libraries, and the same versions to make everything play nicely together."*

For this we use conda, Docker and Snakemake. With conda we can record/specify
the packages we used and the exact versions of those packages. With Docker we
get an underlying "computer" that ensures everything not installed by conda is
the same between different persons and physical computers. With Snakemake we
specify what conda environment and Docker container is used for each rule.



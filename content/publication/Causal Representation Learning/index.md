---
title: 'Learning Causal Representations from General Environments: Identifiability and Intrinsic Ambiguity'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - Jikai Jin
  - Vasilis Syrgkanis

# Author notes (optional)
# author_notes:
#  - 'Equal contribution'
#  - 'Equal contribution'

date: '2023-11-20T00:00:00Z'
doi: ''

# Schedule page publish date (NOT publication's date).
publishDate: '2023-11-20T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['3']

# Publication name and optional abbreviated publication name.
publication: In *ArXiv preprint 2311.12267*
publication_short: In *ArXiv preprint 2311.12267*
abstract: This paper studies causal representation learning, the task of recovering high-level latent variables and their causal relationships from low-level data that we observe, assuming access to observations generated from multiple environments. While existing works are able to prove full identifiability of the underlying data generating process, they typically assume access to single-node, hard interventions which is rather unrealistic in practice. The main contribution of this paper is characterize a notion of identifiability which is provably the best one can achieve when hard interventions are not available. First, for linear causal models, we provide identifiability guarantee for data observed from general environments without assuming any similarities between them. While the causal graph is shown to be fully recovered, the latent variables are only identified up to an effect-domination ambiguity (EDA). We then propose an algorithm, LiNGCReL which is guaranteed to recover the ground-truth model up to EDA, and we demonstrate its effectiveness via numerical experiments. Moving on to general non-parametric causal models, we prove the same idenfifiability guarantee assuming access to groups of soft interventions. Finally, we provide counterparts of our identifiability results, indicating that EDA is basically inevitable in our setting.

# Summary. An optional shortened abstract.
summary: We study the best-achievable identification guarantees and provable identification algorithms for causal representation learning when hard interventions are not available.

tags: [Causal machine learning]

# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
links:
  - name: ArXiv
    url: https://arxiv.org/abs/2311.12267
  - name: Slides
    url: https://drive.google.com/file/d/1X6QK4NrqVI0m27A_V7-aqjfowaL9Ry-G/view?usp=sharing


  

url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# image:
#  caption: 'Stanford'
#  focal_point: 'Center'
#  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
# projects:
#  - example

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
# slides: example
---

---
title: 'Minimax Optimal Kernel Operator Learning via Multilevel Training'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - Jikai Jin
  - Yiping Lu
  - Jose Blanchet
  - Lexing Ying

# Author notes (optional)
# author_notes:
#  - 'Equal contribution'
#  - 'Equal contribution'

date: '2022-09-30T00:00:00Z'
doi: ''

# Schedule page publish date (NOT publication's date).
publishDate: '2022-09-30T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['1']

# Publication name and optional abbreviated publication name.
publication: In *The Eleventh International Conference on Learning Representations (spotlight)*
publication_short: In *ICLR 2023 (spotlight)*
abstract: Learning mappings between infinite-dimensional function spaces has achieved empirical success in many disciplines of machine learning, including generative modeling, functional data analysis, causal inference, and multi-agent reinforcement learning. In this paper, we study the statistical limit of learning a Hilbert-Schmidt operator between two infinite-dimensional Sobolev reproducing kernel Hilbert spaces. We establish the information-theoretic lower bound in terms of the Sobolev Hilbert-Schmidt norm and show that a regularization that learns the spectral components below the bias contour and ignores the ones that are above the variance contour can achieve the optimal learning rate. At the same time, the spectral components between the bias and variance contours give us flexibility in designing computationally feasible machine learning algorithms. Based on this observation, we develop a multilevel kernel operator learning algorithm that is optimal when learning linear operators between infinite-dimensional function spaces.

# Summary. An optional shortened abstract.
summary: We consider the problem of learning a linear operator between Sobolev RKHSs from noisy data. Different from its finite-dimensional counterpart where regularized least squares is optimal, we prove that estimators with a certain multilevel structure is necessary (and sufficient) to achieve optimality.

tags: [Machine learning for Science, Non-parametric estimation]

# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
links:
  - name: Paper
    url: https://openreview.net/pdf?id=zEn1BhaNYsC
  - name: ArXiv
    url: https://arxiv.org/abs/2209.14430
  - name: Poster
    url: https://drive.google.com/file/d/1R-Ifc5MaOV32U_ORMaxVfKWEGdBn5qnS/view?usp=drive_link



  

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
image:
  caption: 'Rural area of Rwanda in early morning.'
  focal_point: 'Center'
  preview_only: false

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



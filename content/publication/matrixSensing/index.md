---
title: 'Understanding Incremental Learning of Gradient Descent -- A Fine-grained Analysis of Matrix Sensing'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - Jikai Jin
  - Zhiyuan Li
  - Kaifeng Lyu
  - Simon S. Du
  - Jason D. Lee

# Author notes (optional)
# author_notes:
#  - 'Equal contribution'
#  - 'Equal contribution'

date: '2023-01-27T00:00:00Z'
doi: ''

# Schedule page publish date (NOT publication's date).
publishDate: '2023-01-27T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['1']

# Publication name and optional abbreviated publication name.
publication: In *The Fortieth International Conference on Machine Learning*
publication_short: In *ICML 2023*
abstract: It is believed that Gradient Descent (GD) induces an implicit bias towards good generalization in training machine learning models. This paper provides a fine-grained analysis of the dynamics of GD for the matrix sensing problem, whose goal is to recover a low-rank ground-truth matrix from near-isotropic linear measurements. It is shown that GD with small initialization behaves similarly to the greedy low-rank learning heuristics (Li et al., 2020) and follows an incremental learning procedure (Gissin et al., 2019) -- GD sequentially learns solutions with increasing ranks until it recovers the ground truth matrix. Compared to existing works which only analyze the first learning phase for rank-1 solutions, our result provides characterizations for the whole learning process. Moreover, besides the over-parameterized regime that many prior works focused on, our analysis of the incremental learning procedure also applies to the under-parameterized regime. Finally, we conduct numerical experiments to confirm our theoretical findings.

# Summary. An optional shortened abstract.
summary: We prove that GD applied to the matrix sensing problem has intriguing properties -- with small initialization and early stopping, it follows an incremental/greedy low-rank learning procedure. This form of simplicity bias allows GD to recover the ground-truth, despite over-parameterization and non-convexity.

tags: [Deep Learning Theory]

# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
links:
  - name: paper
    url: https://proceedings.mlr.press/v202/jin23a.html
  - name: ArXiv
    url: https://arxiv.org/abs/2301.11500
  - name: Poster
    url: https://drive.google.com/file/d/1Us3VwASjSbz2nXGJVPgT7715ydTPEb_M/view?usp=drive_link



  

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
  caption: 'Dalian, LN, China'
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

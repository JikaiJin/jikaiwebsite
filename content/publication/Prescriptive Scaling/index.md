---
title: 'Prescriptive Scaling Reveals the Evolution of Language Model Capabilities'

# Authors
authors:
  - Hanlin Zhang
  - Jikai Jin
  - Vasilis Syrgkanis
  - Sham Kakade

date: '2026-02-17T00:00:00Z'
doi: '10.48550/arXiv.2602.15327'

# Schedule page publish date (NOT publication's date).
publishDate: '2026-02-17T00:00:00Z'

# Publication type.
publication_types: ['3']

# Publication name and optional abbreviated publication name.
publication: "arXiv preprint"
publication_short: "arXiv"

abstract: "We study *prescriptive* scaling laws for foundation models: given a pretraining compute budget, what downstream benchmark accuracy is achievable under contemporary post-training practice, and how stable is this mapping over time? Using large-scale observational evaluations, we estimate capability boundaries (high conditional quantiles of scores) as a function of log pretraining FLOPs via a monotone, saturating sigmoid quantile-regression model. We test temporal reliability by fitting on earlier model generations and evaluating on later releases, finding mostly stable boundaries except for math reasoning, which advances over time. We further analyze task-dependent saturation and potential contamination-related shifts for math reasoning, and propose an evaluation strategy that recovers near-full frontiers with about 20% of the evaluation budget. We release the Proteus 2k dataset and provide a practical methodology for translating compute budgets into performance expectations and monitoring boundary shifts."

# Summary. An optional shortened abstract.
summary: 'Prescriptive scaling laws: estimate stable capability boundaries vs. pretraining compute, track temporal shifts, and release the Proteus 2k evaluation dataset.'

tags:
  - Scaling laws
  - Foundation models
  - LLM evaluation
  - Machine learning

# Display this page in the Featured widget?
featured: false

# Custom links
links:
  - name: ArXiv
    url: https://arxiv.org/abs/2602.15327
  - name: Blog
    url: https://jkjin.com/prescriptive-scaling/

url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''
---

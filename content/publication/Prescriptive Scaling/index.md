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
publication: "*The Fortieth International Conference on Machine Learning*"
publication_short: "*ICML 2026 (oral, top 1%)*"

abstract: "Machine learning model performance improvements tend to arise from competition and application. For deployment, we consider prescriptive scaling laws: given a pre-training compute budget, what downstream accuracy is attainable with contemporary post-training practice, and how stable is that mapping as the field evolves? Using large-scale observational evaluations with 5k existing and 2k newly evaluated model checkpoints spanning 2022--2026 across six benchmarks, we estimate capability boundaries---high conditional quantiles of benchmark scores as a function of log pre-training FLOPs, via smoothed quantile regression with a monotone, saturating sigmoid parameterization. We validate temporal reliability by fitting on earlier model generations and evaluating on later releases: across four of six tasks the out-of-distribution coverage error remains below 2%, while math reasoning exhibits a consistently advancing boundary over time. For instance, at a budget of 10^24 FLOPs the estimated attainable accuracies are 0.83 on IFEval and 0.54 on MATH Lvl 5. We then extend our approach to analyze task-dependent saturation and to probe contamination-related shifts on math reasoning tasks. Finally, we introduce a balanced I-optimal sampling algorithm that recovers near-full-data frontiers using roughly 20% of the parameter-count-weighted evaluation budget (as low as 5% on some tasks) while maintaining comparable calibration. Together, our work releases the Proteus-2k, the latest model performance evaluation dataset, and introduces a practical methodology for translating compute budgets into reliable performance expectations and for monitoring when capability boundaries shift across time."

# Summary. An optional shortened abstract.
summary: 'Prescriptive scaling laws: estimate stable capability boundaries vs. pretraining compute, track temporal shifts, and release the Proteus 2k evaluation dataset.'

tags:
  - Scaling laws
  - Foundation models
  - LLM evaluation
  - Machine learning

# Display this page in the Featured widget?
featured: true

# Custom links
links:
  - name: ArXiv
    url: https://arxiv.org/abs/2602.15327
  - name: Blog
    url: https://jkjin.com/prescriptive-scaling/
  - name: Dataset
    url: https://huggingface.co/datasets/hlzhang109/proteus-2k

url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''
---

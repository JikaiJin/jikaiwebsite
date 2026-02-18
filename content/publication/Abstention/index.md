---
title: 'Policy Learning with Abstention'

# Authors
authors:
  - Ayush Sawarni
  - Jikai Jin
  - Justin Whitehouse
  - Vasilis Syrgkanis

date: '2026-01-28T00:00:00Z'
doi: ''

# Schedule page publish date (NOT publication's date).
publishDate: '2026-01-28T00:00:00Z'

# Publication type.
publication_types: ['1']

# Publication name and optional abbreviated publication name.
publication: "In *the Twenty-Ninth Annual Conference on Artificial Intelligence and Statistics*"
publication_short: "In *AISTATS 2026*"

abstract: "Policy learning algorithms are regularly leveraged in domains such as personalized medicine and advertising to develop individualized treatment regimes. However, a critical deficit of existing algorithms is that they force a decision even when predictions are uncertain, a risky approach in high-stakes settings. The ability to abstain — that is, to defer to a safe default or an expert — is crucial but largely unexplored in this context. To remedy this, we introduce a framework for policy learning with abstention, in which policies that choose not to assign a treatment to some customers/patients receive a small, additive reward on top of the value of a random guess. We propose a two–stage learner that first identifies a set of near–optimal policies and then constructs an abstention class based on disagreements between the policies. We establish fast O(1/n)–type regret guarantees for the abstaining policy when propensities are known, and show how to extend these guarantees to the unknown–propensity case via a doubly robust (DR) objective. Furthermore, we demonstrate that our abstention framework is a versatile tool with direct applications to several other core problems in policy learning. We use our algorithm as a black box to obtain improved guarantees under margin conditions without the common realizability assumption. We also show that abstention provides a natural connection to both distributionally robust policy learning, where it acts as a hedge against small data shifts, and safe policy improvement, where the goal is to improve upon a baseline policy with high probability."

# Summary. An optional shortened abstract.
summary: 'We study policy learning with the ability to abstain, and demonstrate its usefulness in ensuring safety.'

tags: 
  - Causal machine learning
  - Econometrics
  - Machine learning theory

# Display this page in the Featured widget?
featured: true

# Custom links
links:
  - name: ArXiv
    url: https://arxiv.org/abs/2510.19672

url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''
---

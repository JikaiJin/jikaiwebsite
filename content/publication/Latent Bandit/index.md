---
title: 'Adaptive Exploration for Latent-State Bandits'

# Authors
authors:
  - Jikai Jin
  - Kenneth Hung
  - Sanath Kumar Krishnamurthy
  - Baoyi Shi
  - Congshan Zhang

date: '2026-02-04T00:00:00Z'
doi: '10.48550/arXiv.2602.05139'

# Schedule page publish date (NOT publication's date).
publishDate: '2026-02-04T00:00:00Z'

# Publication type.
publication_types: ['3']

# Publication name and optional abbreviated publication name.
publication: "*Thirty-second ACM SIGKDD Conference on Knowledge Discovery and Data Mining*"
publication_short: "In *KDD 2026*"

abstract: "We study bandits whose rewards depend on an unobserved Markov state that evolves independently of the learner's actions. The optimal arm can change even though the learner observes only past actions and rewards. We propose algorithms that feed LinUCB with two summaries of the hidden state: a lagged action-reward pair and, when available, a probe fingerprint formed from rewards of multiple arms. The adaptive variants refresh the fingerprint using residual, margin, and staleness tests. In synthetic stress tests over state count, transition rate, noise, and horizon, these methods reduce dynamic regret relative to standard, adversarial, and non-stationary bandit baselines when the summaries distinguish states and are updated often enough. Ablations and misspecification tests identify the main failure modes: weak fingerprint separation, high noise, and state changes during sequential probes."

# Summary. An optional shortened abstract.
summary: 'We propose adaptive, state-model-free bandit algorithms for latent-state (confounded, non-stationary) environments.'

tags:
  - Bandits
  - Sequential decision making
  - Machine learning theory

# Display this page in the Featured widget?
featured: false

# Custom links
links:
  - name: ArXiv
    url: https://arxiv.org/abs/2602.05139

url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''
---

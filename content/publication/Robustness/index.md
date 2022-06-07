---
title: 'Why Robust Generalization in Deep Learning is Difficult: Perspective of Expressive Power'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - Binghui Li
  - Jikai Jin
  - Han Zhong
  - John E. Hopcroft
  - Liwei Wang

# Author notes (optional)
author_notes:
  - 'Equal contribution'
  - 'Equal contribution'

date: '2022-05-27T00:00:00Z'
doi: ''

# Schedule page publish date (NOT publication's date).
publishDate: '2022-05-27T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['1']

# Publication name and optional abbreviated publication name.
publication: arXiv preprint *arXiv 2205.13863*
publication_short: arXiv preprint *arXiv 2205.13863*

abstract: It is well-known that modern neural networks are vulnerable to adversarial examples. To mitigate this problem, a series of robust learning algorithms have been proposed. However, although the robust training error can be near zero via some methods, all existing algorithms lead to a high robust generalization error. In this paper, we provide a theoretical understanding of this puzzling phenomenon from the perspective of expressive power for deep neural networks. Specifically, for binary classification problems with well-separated data, we show that, for ReLU networks, while mild over-parameterization is sufficient for high robust training accuracy, there exists a constant robust generalization gap unless the size of the neural network is exponential in the data dimension d. Even if the data is linear separable, which means achieving low clean generalization error is easy, we can still prove an exp(Ω(d)) lower bound for robust generalization. Moreover, we establish an improved upper bound of exp(O(k)) for the network size to achieve low robust generalization error when the data lies on a manifold with intrinsic dimension k (k≪d). Nonetheless, we also have a lower bound that grows exponentially with respect to k ---- the curse of dimensionality is inevitable. By demonstrating an exponential separation between the network size for achieving low robust training and generalization error, our results reveal that the hardness of robust generalization may stem from the expressive power of practical models.

# Summary. An optional shortened abstract.
summary: We provide theoretical evidence which indicates that the hardness of robust generalization may stem from the expressive power of deep neural networks. 
Even when standard generalization is easy, robust generalization provably requires the size of DNNs to be exponentially large.

tags: []

# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
links:
  - name: ArXiv
    url: https://arxiv.org/abs/2205.13863



  

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
  caption: 'Image credit: [**Unsplash**](https://unsplash.com/photos/pLCdAaMFLTE)'
  focal_point: ''
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

{{% callout note %}}
Click the _Cite_ button above to demo the feature to enable visitors to import publication metadata into their reference management software.
{{% /callout %}}

{{% callout note %}}
Create your slides in Markdown - click the _Slides_ button to check out the example.
{{% /callout %}}

# Supplementary notes can be added here, including [code, math, and images](https://wowchemy.com/docs/writing-markdown-latex/).

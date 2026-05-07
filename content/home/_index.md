---
# Home section root. This file becomes a branch bundle so that each
# sibling widget .md (about.md, featured.md, …) is accessible to
# layouts/index.html as a child page via {{ site.GetPage "/home" }}.Pages.
#
# headless: true suppresses the /home/ list page itself. The cascade
# below stops Hugo from routing the individual widget pages at
# /home/<name>/ — they only exist in the page tree to feed the home
# widget dispatcher; they should not be web-addressable.
type: widget_page
headless: true
cascade:
  - _target:
      path: /home/**
    build:
      # render:never stops Hugo from writing /home/<name>/index.html to disk.
      # list:local keeps the page in its parent's .Pages (so the home-widget
      # dispatcher can still iterate them) while excluding them from global
      # listings like site.RegularPages and the sitemap.
      render: never
      list: local
---

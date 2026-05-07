---
title: "Example album"
date: 2026-04-01
draft: true
summary: "Delete this folder and drop your own — see content/gallery/_index.md for the recipe."

# Cover resolution is the pattern documented in the plan: explicit `cover:`
# wins, then a bundle file named cover.* (this file), then the first image,
# then a placeholder tile. Here we lean on the cover.* rule.
image_order: "name"
---

**Example album — set `draft: false` and replace `cover.png` + any images to make this live.**

An album is a Hugo page bundle. Create `content/gallery/<slug>/index.md` with
the frontmatter shown in the plan at `.omc/plans/gallery-v1.md`, drop
photographs alongside, and Netlify publishes `/gallery/<slug>/` on the next
push.

## How it renders

- **Cover tile** on the home page and the `/gallery/` list page: resolved from
  (in order) an explicit `cover:` frontmatter filename, a file named
  `cover.*` in the bundle, or the first image.
- **Grid** on `/gallery/<slug>/`: every image in the bundle except `cover.*`
  (and optionally the explicit cover, if you set `gallery_exclude_cover: true`).
- **Full resolution**: clicking a thumbnail opens the original in a new tab.
- **Description**: this very prose — Markdown, any length, rendered in
  `.prose-article.no-section-numbers` so h2 headings do NOT get auto-numbered
  `§ N` the way post prose does.

## Typical workflow

1. `mkdir content/gallery/your-album-slug`
2. Drop JPEGs / PNGs / WebPs in.
3. Create `index.md` with `title:`, `date:`, optional `cover:`, optional
   per-image `resources:` list for `alt:` text.
4. `hugo server -D` to preview with drafts shown.
5. Commit, push, unset `draft: true` when ready.

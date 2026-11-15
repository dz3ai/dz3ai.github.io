# dz3ai.github.io

Danny Zeng's homepage — project showcase and blog covering [dz3ai](https://github.com/dz3ai)'s public projects.

**Live:** https://dz3ai.github.io/

## What's here

- **Homepage** (`index.html`) — intro, curated project grid (`_data/projects.yml`), recent posts
- **Blog** (`blog/`) — all posts, grouped by year
- **Original posts** — written in this repo, tagged with project categories
- **Imported posts** — syndicated from source project sites (e.g. [`allclaws`](https://dz3ai.github.io/allclaws/)), stamped with `source_repo` + `canonical_url` front matter

## Post import pipeline

Posts from source repos are imported by `scripts/sync_source_posts.py`:

1. Reads source repos from `_data/sources.yml`
2. Lists each repo's `_posts/*.md` via the GitHub API
3. Copies any post not already present, stamping `source_repo` and `canonical_url` (built from the source site's permalink style)

The GitHub Action [`.github/workflows/sync-source-posts.yml`](.github/workflows/sync-source-posts.yml) runs this daily and on demand (`workflow_dispatch`), committing new imports automatically.

Local run:

```bash
pip install pyyaml
python scripts/sync_source_posts.py
```

To add another source repo, append to `_data/sources.yml`.

## Writing an original post

Create `_posts/YYYY-MM-DD-slug.md` with front matter:

```yaml
---
layout: post
title: "Post title"
date: YYYY-MM-DD HH:MM:SS +0800
author: Danny Zeng
categories: [project-name]
tags: [tag1, tag2]
---
```

## Development

Plain Jekyll (no custom plugins beyond whitelisted `jekyll-feed` / `jekyll-seo-tag`):

```bash
bundle install
bundle exec jekyll serve
```

Built automatically by GitHub Pages on push to `main`.

# HassenChaaben GitHub Profile Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans and superpowers:test-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, test, and deploy the `HassenChaaben/HassenChaaben` GitHub Profile repository with custom Cosmic Solar Nebula & Portfolio SVG assets (`v5`), automated Medium RSS synchronization, and updated GitHub profile metadata.

**Architecture:** Self-contained GitHub-CSP-compliant animated SVG components (`assets/*.svg` using inline `<style>` keyframes and `data:image/jpeg;base64` embedded assets so GitHub's Camo proxy renders every pixel and animation natively), paired with a rich `README.md` and a zero-dependency Python 3.12 RSS synchronization script (`scripts/build_readme.py`) triggered daily via `.github/workflows/build-readme.yml`.

**Tech Stack:** Python 3.12 (`urllib`, `xml.etree.ElementTree`, `pytest`), SVG 1.1 + CSS3 `@keyframes`, GitHub Actions, GitHub REST API.

**Spec:** `docs/superpowers/specs/2026-11-03-github-profile-superdesign-spec.md`

## Global Constraints
- Personal GitHub scope only: account `HassenChaaben`, git author `Hassen Ben Chaaben <hassen.benchaaben01@gmail.com>`, zero AI attribution in commits or files.
- Zero mentions of `LabMACS` or `Researcher` anywhere in `README.md`, `assets/*.svg`, or profile metadata.
- Must include `UNIVPM`, `Master's student at UNIVPM`, `Junior AI Engineer`, and `Part-Time AI Specialist` (`AI Specialist · Part-Time · Present`), alongside `AI Intern · SQOIN` and `Junior ML Engineer · Omdena`.
- All SVG files must use `data:` URIs for embedded raster images (no external `<image href="https://...">` inside SVGs, which GitHub's Camo CSP blocks) and untruncated inline vector paths for the Medium logo.

## Review Focus
- Malformed or unreachable Medium RSS feed must not erase existing articles in `README.md`.
- SVG files must parse as valid XML with `xml.etree.ElementTree.fromstring`.
- Medium URL query parameters (`?source=rss-...`) must be stripped for clean links.
- No overlapping text coordinates in SVG cards.
- GitHub API calls must authenticate strictly as `HassenChaaben`.

---

### Task 1: Medium RSS Sync Script & Profile Invariant Tests

**Files:**
- Create: `scripts/build_readme.py`
- Create: `assets/hero-card.svg`, `assets/bento-phases.svg`, `assets/experience-card.svg`, `assets/badge-portfolio.svg`, `assets/badge-linkedin.svg`, `assets/badge-medium.svg`, `assets/badge-email.svg`
- Create: `README.md`
- Create: `.github/workflows/build-readme.yml`
- Test: `tests/test_build_readme.py`

- [ ] **Step 1: Write the failing test suite in `tests/test_build_readme.py`**
- [ ] **Step 2: Run `pytest` to verify Red state**
- [ ] **Step 3: Implement `scripts/build_readme.py`, `assets/*.svg`, `README.md`, and `.github/workflows/build-readme.yml`**
- [ ] **Step 4: Run `pytest` and `python scripts/build_readme.py` to verify Green state**
- [ ] **Step 5: Dispatch Two-Stage 8-Angle Reviewer Subagent and deploy to `HassenChaaben/HassenChaaben`**

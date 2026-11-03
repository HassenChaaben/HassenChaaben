# HassenChaaben GitHub Profile Homepage — Superdesign Specification

**Date:** 2026-11-03  
**Repository Target:** `https://github.com/HassenChaaben/HassenChaaben`  
**Superdesign Project Canvas:** `https://superdesign.dev/teams/7c4447c6-9b9f-495a-9728-4c295528c4bc/projects/863f8d9d-8335-490b-a4e3-2db2ac47837d`  
**Superdesign Live Draft Preview:** `https://p.superdesign.dev/draft/778cb96e-398b-47e2-aff7-d4c4dd4168c9`

---

## 1. Objective & Design Philosophy
Create a modern, authoritative, high-conversion GitHub Profile repository (`HassenChaaben/HassenChaaben`) that renders at the top of `https://github.com/HassenChaaben`, combining:
1. **Sebastian Raschka (`rasbt`)**: Crisp AI Engineer & M.Sc. Researcher positioning + direct personal links.
2. **Hamel Husain (`hamelsmu`)**: Editorial *"What I'm working on"* narrative + clean `Date | Article` table of technical posts from Medium (`@hassen.benchaaben01`).
3. **Simon Willison (`simonw`)**: Multi-column HTML `<table>` layout (`Flagship AI Systems & Research` | `Writing on Medium & Active LabMACS Research`) kept automatically fresh by a scheduled GitHub Action (`build_readme.py` + `.github/workflows/build-readme.yml`).
4. **Portfolio Brand DNA (`hassenbenchaaben.me`) + Superdesign Visual Craft**:
   - Custom animated SVG hero banner (`assets/hero-banner.svg`) with CSS `@keyframes` animations (pulsing aurora spotlight, animated `THINK -> ACT -> OBSERVE` ReAct loop, and STFT/Sobel bioacoustic waveform).
   - Custom 3-pillar animated SVG cards (`assets/focus-pillars.svg`) showcasing **01 · Agentic AI**, **02 · LabMACS Research**, and **03 · Production AI**.
   - Official brand logos & shields for Portfolio (`hassenbenchaaben.me`), LinkedIn (`in/hassen-ben-chaaben`), Medium (`@hassen.benchaaben01`), Email (`hassen.benchaaben01@gmail.com`), and core stack (`Python`, `PyTorch`, `FastAPI`, `LangChain`, `TypeScript`, `Next.js`, `React`, `Docker`, `PostgreSQL`, `MongoDB`).

---

## 2. Repository Architecture (`HassenChaaben/HassenChaaben`)
```text
HassenChaaben/
├── README.md                              # Rendered on github.com/HassenChaaben with <!-- MEDIUM-POSTS:START --> markers
├── assets/
│   ├── hero-banner.svg                    # Animated SVG hero card (ReAct loop + STFT wave + aurora gradient)
│   └── focus-pillars.svg                  # Animated 3-column SVG cards (Agentic AI | LabMACS Research | Production RAG)
├── scripts/
│   └── build_readme.py                    # Python 3.12 stdlib script fetching Medium RSS (@hassen.benchaaben01) & updating README.md
├── tests/
│   └── test_build_readme.py               # Unit tests for RSS parsing, Markdown table generation, and SVG validity
└── .github/
    └── workflows/
        └── build-readme.yml               # Daily cron + push/workflow_dispatch GitHub Action updating README.md
```

---

## 3. Component & Data Flow Specification
1. **`assets/hero-banner.svg`**:
   - Valid standalone SVG (`viewBox="0 0 920 290"`) using GitHub-safe inline `<style>` and `@keyframes` animations (`pulseGlow`, `flowDash`, `waveShift`).
   - Left column: Live status pill (`BUILDING NEXT-GEN AUTONOMOUS SYSTEMS`), title (`Hi, I'm Hassen Ben Chaaben`), role summary (`AI Engineer & M.Sc. Researcher @ UNIVPM · LabMACS`), experience callout (`SQOIN`, `Omdena`), and 4 domain tags.
   - Right column: Interactive-style telemetry card displaying the `THINK -> ACT -> OBSERVE` ReAct agent diagram and the `STFT · 2D SOBEL · PYTORCH CNN` bioacoustic waveform.
2. **`assets/focus-pillars.svg`**:
   - Valid standalone SVG (`viewBox="0 0 920 175"`) rendering 3 side-by-side glassmorphic cards with subtle glowing borders (`#CBACF9`, `#38BDF8`, `#10B981`).
3. **`scripts/build_readme.py`**:
   - Uses Python standard library (`urllib.request`, `xml.etree.ElementTree`, `email.utils`, `re`, `pathlib`) with zero external third-party dependencies required for RSS syncing.
   - Parses `https://medium.com/feed/@hassen.benchaaben01` into `(date_str, title, clean_url)` rows formatted as `| MMM YYYY | [Title](url) |`.
   - Replaces content between `<!-- MEDIUM-POSTS:START -->` and `<!-- MEDIUM-POSTS:END -->` in `README.md` idempotently.
   - If the network feed is temporarily unreachable, preserves existing posts gracefully without corrupting `README.md`.
4. **Git Identity & Scope Constraint**:
   - Strictly uses personal GitHub account `HassenChaaben` and personal email `hassen.benchaaben01@gmail.com` (`user.name = Hassen Ben Chaaben`, `user.email = hassen.benchaaben01@gmail.com`). Zero AI attribution in commits.

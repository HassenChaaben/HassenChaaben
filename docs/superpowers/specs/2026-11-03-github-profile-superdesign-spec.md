# HassenChaaben GitHub Profile Homepage — Superdesign Specification (v2 · Lunar & Alien Observatory)

**Date:** 2026-11-03  
**Repository Target:** `https://github.com/HassenChaaben/HassenChaaben`  
**Superdesign Project Canvas:** `https://superdesign.dev/teams/7c4447c6-9b9f-495a-9728-4c295528c4bc/projects/863f8d9d-8335-490b-a4e3-2db2ac47837d`  
**Superdesign Live Draft Preview (`v2`):** `https://p.superdesign.dev/draft/778cb96e-398b-47e2-aff7-d4c4dd4168c9`

---

## 1. Objective & Design Philosophy
Create a modern, cosmic, high-conversion GitHub Profile repository (`HassenChaaben/HassenChaaben`) that matches Hassen's **Moon / Astronomy avatar** and his portfolio (`hassenbenchaaben.me` — *"Welcome to my own world"*) while preserving the clean senior-engineer hierarchy of **Hamel Husain (`hamelsmu`)**, **Simon Willison (`simonw`)**, and **Sebastian Raschka (`rasbt`)**:

1. **Astronomy, Moon Craters & Alien UFO Intelligence Theme**:
   - Cohesive with Hassen's profile avatar standing on the lunar surface under deep-space stars.
   - Deep-space obsidian canvas (`#050711` → `#091926`), lunar crater silver (`#E2E8F0` / `#94A3B8`), alien tractor-beam emerald (`#34D399` / `#10B981`), nebula ultraviolet (`#CBACF9` / `#A855F7`), and orbital cyan (`#38BDF8`).
   - Animated SVG scene featuring a **cratered Moon with rotating orbital rings**, **twinkling deep-space stars + shooting comet**, a **hovering Alien UFO saucer with a pulsing emerald tractor beam**, and **lunar horizon craters**.
2. **Zero-Overlap Layout Architecture**:
   - The Hero Banner (`assets/hero-banner.svg`) uses strictly separated left/right coordinate zones (`0..530px` for typography & badges; `550..900px` for the Lunar & Alien UFO Observatory scene), preventing any CSS `transform` from shifting graphics over the title text.
3. **Hamel × Simon × Raschka Editorial Structure**:
   - **What I'm working on · Mission Control**: 3 cosmic cards (`🛸 01 · Alien Intelligence / Autonomous Agents`, `📡 02 · Signal & Vision Lab / LabMACS`, `🌌 03 · Deep-Space Core / Hybrid RAG`) + `SQOIN` & `Omdena` experience.
   - **2-Column Orbital Matrix**:
     - Left column: **🛸 Flagship AI Missions** (`Microsoft Office Antigravity Copilot`, `MonAgent`, `IntreccIAmi`, `Mini_Rag_Application`, `Auction-management-backend-app`).
     - Right column: **📡 Deep-Space Transmissions (`Stardate | Article`)** auto-synced from Medium (`@hassen.benchaaben01`) + **LabMACS Observatory (`AIDD`)** highlight.

---

## 2. Repository Structure (`HassenChaaben/HassenChaaben`)
```text
HassenChaaben/
├── README.md                              # Rendered on github.com/HassenChaaben with <!-- MEDIUM-POSTS:START --> markers
├── assets/
│   ├── hero-banner.svg                    # Animated Lunar, Moon Craters & Alien UFO hero SVG (zero text overlap)
│   └── focus-pillars.svg                  # Animated 3-column Cosmic Mission Control cards SVG
├── scripts/
│   └── build_readme.py                    # Python 3.12 stdlib script fetching Medium RSS (@hassen.benchaaben01) & updating README.md
├── tests/
│   └── test_build_readme.py               # Unit tests for RSS parsing, Markdown table generation, and SVG coordinate safety
└── .github/
    └── workflows/
        └── build-readme.yml               # Daily cron + push/workflow_dispatch GitHub Action updating README.md
```

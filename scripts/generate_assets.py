from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def _b64_data_uri(path: Path) -> str:
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def generate_all() -> None:
    hero_uri = _b64_data_uri(ASSETS / "cosmic-solar-nebula-hero.jpg")
    logo_uri = _b64_data_uri(ASSETS / "hbc-orbital-logo.jpg")

    # 1. Hero Card SVG (Matches Superdesign v5: Cosmic Solar System Panorama + Crisp #CBACF9 Typography)
    hero_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 448" width="100%">
  <defs>
    <clipPath id="cardClip">
      <rect x="0" y="0" width="960" height="448" rx="22" />
    </clipPath>
    <clipPath id="logoTopClip">
      <circle cx="718" cy="34" r="10" />
    </clipPath>
    <linearGradient id="fadeOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#000319" stop-opacity="0.04" />
      <stop offset="50%" stop-color="#000319" stop-opacity="0.45" />
      <stop offset="80%" stop-color="#000319" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#000319" stop-opacity="1" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#CBACF9" stop-opacity="0.55" />
      <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#CBACF9" stop-opacity="0.55" />
    </linearGradient>
    <style>
      .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace; }}
      @keyframes orbitFlow {{
        to {{ stroke-dashoffset: -80; }}
      }}
      @keyframes meteorOne {{
        0% {{ transform: translate(0px, 0px); opacity: 0; }}
        12% {{ opacity: 1; }}
        38% {{ transform: translate(-170px, 82px); opacity: 0; }}
        100% {{ transform: translate(-170px, 82px); opacity: 0; }}
      }}
      @keyframes meteorTwo {{
        0% {{ transform: translate(0px, 0px); opacity: 0; }}
        12% {{ opacity: 0.9; }}
        40% {{ transform: translate(-150px, 72px); opacity: 0; }}
        100% {{ transform: translate(-150px, 72px); opacity: 0; }}
      }}
      @keyframes twinkle {{
        0%, 100% {{ opacity: 0.25; }}
        50% {{ opacity: 1; }}
      }}
      .orbit-arc {{ stroke-dasharray: 6 6; animation: orbitFlow 3.5s linear infinite; }}
      .m1 {{ animation: meteorOne 6.5s ease-out infinite; }}
      .m2 {{ animation: meteorTwo 8.5s ease-out 3s infinite; }}
      .tw1 {{ animation: twinkle 3.2s ease-in-out infinite; }}
      .tw2 {{ animation: twinkle 4.4s ease-in-out 1.4s infinite; }}
    </style>
  </defs>

  <g clip-path="url(#cardClip)">
    <rect x="0" y="0" width="960" height="448" fill="#000319" />
    <image href="{hero_uri}" x="0" y="0" width="960" height="320" preserveAspectRatio="xMidYMid slice" />

    <!-- Animated Celestial & Orbital HUD Overlay -->
    <g class="m1">
      <line x1="790" y1="36" x2="845" y2="10" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
      <circle cx="790" cy="36" r="2.5" fill="#F8FAFC" />
    </g>
    <g class="m2">
      <line x1="550" y1="54" x2="600" y2="28" stroke="#CBACF9" stroke-width="1.8" stroke-linecap="round" />
      <circle cx="550" cy="54" r="2" fill="#F8FAFC" />
    </g>
    <path d="M 285 185 Q 480 95, 735 55" fill="none" stroke="#38BDF8" stroke-opacity="0.55" stroke-width="1.5" class="orbit-arc" />
    <path d="M 315 205 Q 530 165, 695 190" fill="none" stroke="#CBACF9" stroke-opacity="0.65" stroke-width="1.5" class="orbit-arc" />
    <circle cx="485" cy="138" r="3.5" fill="#CBACF9" class="tw1" />
    <circle cx="585" cy="110" r="4" fill="#38BDF8" class="tw2" />
    <circle cx="715" cy="72" r="3.5" fill="#CBACF9" class="tw1" />

    <!-- Smooth Gradient Fade into Portfolio Copy Area -->
    <rect x="0" y="0" width="960" height="330" fill="url(#fadeOverlay)" />

    <!-- Subtle Portfolio Grid on Lower Area -->
    <g stroke="#CBACF9" stroke-opacity="0.045" stroke-width="1">
      <line x1="0" y1="310" x2="960" y2="310" />
      <line x1="0" y1="350" x2="960" y2="350" />
      <line x1="0" y1="390" x2="960" y2="390" />
      <line x1="0" y1="430" x2="960" y2="430" />
    </g>

    <!-- Top-Right Glassmorphic Brand Badge -->
    <rect x="688" y="18" width="252" height="32" rx="16" fill="#000319" fill-opacity="0.84" stroke="#CBACF9" stroke-opacity="0.4" />
    <image href="{logo_uri}" x="708" y="24" width="20" height="20" clip-path="url(#logoTopClip)" />
    <text x="736" y="38" fill="#CBACF9" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.5">WELCOME TO MY OWN WORLD</text>

    <!-- Status Pills Row -->
    <rect x="36" y="248" width="304" height="26" rx="13" fill="#04071D" stroke="#CBACF9" stroke-opacity="0.48" />
    <circle cx="52" cy="261" r="3.5" fill="#CBACF9" class="tw1" />
    <text x="64" y="265" fill="#CBACF9" class="font-mono" font-size="10" font-weight="600" letter-spacing="1.6">WHERE CREATIVITY MEETS INNOVATION</text>

    <rect x="350" y="248" width="286" height="26" rx="13" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.2" />
    <text x="366" y="265" fill="#FFFFFF" class="font-mono" font-size="10" font-weight="600" letter-spacing="1.2">✦ BUILDING NEXT-GEN AUTONOMOUS SYSTEMS</text>

    <!-- Main Hero Heading: Razor-Sharp White + Solid #CBACF9 Portfolio Lavender (Zero Blur) -->
    <text x="36" y="324" class="font-sans" font-size="36" font-weight="800" fill="#FFFFFF">
      Hi, I'm <tspan fill="#CBACF9">Hassen Ben Chaaben</tspan>
    </text>

    <!-- Bio Lines (Approved v5 Text) -->
    <text x="36" y="362" class="font-sans" font-size="15" fill="#BEC1DD">
      I am a <tspan fill="#FFFFFF" font-weight="600">Master's student at UNIVPM</tspan> and <tspan fill="#FFFFFF" font-weight="600">Junior AI Engineer</tspan> (currently working as a <tspan fill="#CBACF9" font-weight="600">Part-Time AI Specialist</tspan>)
    </text>
    <text x="36" y="386" class="font-sans" font-size="15" fill="#BEC1DD">
      focused on building <tspan fill="#CBACF9" font-weight="600">AI agents</tspan> and <tspan fill="#CBACF9" font-weight="600">scalable automation solutions</tspan>. My expertise lies in <tspan fill="#FFFFFF" font-weight="600">Natural Language Processing</tspan>,
    </text>
    <text x="36" y="410" class="font-sans" font-size="15" fill="#BEC1DD">
      <tspan fill="#FFFFFF" font-weight="600">Computer Vision</tspan>, and <tspan fill="#FFFFFF" font-weight="600">Generative AI</tspan>.
    </text>
  </g>

  <rect x="0.75" y="0.75" width="958.5" height="446.5" rx="21.25" fill="none" stroke="url(#borderGrad)" stroke-width="1.5" />
</svg>
"""
    (ASSETS / "hero-card.svg").write_text(hero_svg, encoding="utf-8")
    (ASSETS / "hero-banner-v5.svg").write_text(hero_svg, encoding="utf-8")

    # 2. 3-Phase Cosmic Bento Cards SVG (bento-phases.svg — Wide Pills, Zero Overflow)
    bento_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 194" width="100%">
  <defs>
    <linearGradient id="card1Bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0B102E" />
      <stop offset="100%" stop-color="#04071D" />
    </linearGradient>
    <linearGradient id="card2Bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#07192E" />
      <stop offset="100%" stop-color="#04071D" />
    </linearGradient>
    <linearGradient id="card3Bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#090D26" />
      <stop offset="100%" stop-color="#04071D" />
    </linearGradient>
    <style>
      .font-sans { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace; }
    </style>
  </defs>

  <!-- Card 1: PHASE 01 · AGENTIC AI -->
  <g transform="translate(0, 0)">
    <rect x="1" y="1" width="308" height="190" rx="18" fill="url(#card1Bg)" stroke="#CBACF9" stroke-opacity="0.38" stroke-width="1.2" />
    <rect x="20" y="20" width="174" height="25" rx="12.5" fill="#CBACF9" fill-opacity="0.14" stroke="#CBACF9" stroke-opacity="0.4" />
    <text x="32" y="36.5" fill="#CBACF9" class="font-mono" font-size="10.5" font-weight="600">PHASE 01 · AGENTIC AI</text>
    <text x="20" y="72" fill="#FFFFFF" class="font-sans" font-size="17.5" font-weight="700">Autonomous AI Agents</text>
    <text x="20" y="100" fill="#BEC1DD" class="font-sans" font-size="13">Building <tspan fill="#FFFFFF" font-weight="600">MonAgent</tspan> (<tspan fill="#CBACF9" class="font-mono">Think → Act → Observe</tspan></text>
    <text x="20" y="121" fill="#BEC1DD" class="font-sans" font-size="13">ReAct architecture) and the <tspan fill="#FFFFFF" font-weight="600">Microsoft Office</tspan></text>
    <text x="20" y="142" fill="#BEC1DD" class="font-sans" font-size="13"><tspan fill="#FFFFFF" font-weight="600">Antigravity Copilot</tspan> integrating Gemini into</text>
    <text x="20" y="163" fill="#BEC1DD" class="font-sans" font-size="13">Word, Excel, PowerPoint &amp; Outlook.</text>
  </g>

  <!-- Card 2: PHASE 02 · GENERATIVE AI & CV -->
  <g transform="translate(325, 0)">
    <rect x="1" y="1" width="308" height="190" rx="18" fill="url(#card2Bg)" stroke="#38BDF8" stroke-opacity="0.38" stroke-width="1.2" />
    <rect x="20" y="20" width="226" height="25" rx="12.5" fill="#38BDF8" fill-opacity="0.14" stroke="#38BDF8" stroke-opacity="0.4" />
    <text x="32" y="36.5" fill="#38BDF8" class="font-mono" font-size="10.5" font-weight="600">PHASE 02 · GENERATIVE AI &amp; CV</text>
    <text x="20" y="72" fill="#FFFFFF" class="font-sans" font-size="17.5" font-weight="700">Computer Vision &amp; DL</text>
    <text x="20" y="100" fill="#BEC1DD" class="font-sans" font-size="13">Fine-tuning Diffusion Models with Low-Rank</text>
    <text x="20" y="121" fill="#BEC1DD" class="font-sans" font-size="13">Adaptation (<tspan fill="#FFFFFF" font-weight="600">IntreccIAmi</tspan>) for complex visual</text>
    <text x="20" y="142" fill="#BEC1DD" class="font-sans" font-size="13">synthesis and training deep neural networks</text>
    <text x="20" y="163" fill="#BEC1DD" class="font-sans" font-size="13">in <tspan fill="#FFFFFF" font-weight="600">PyTorch &amp; TensorFlow</tspan>.</text>
  </g>

  <!-- Card 3: PHASE 03 · PRODUCTION NLP -->
  <g transform="translate(650, 0)">
    <rect x="1" y="1" width="308" height="190" rx="18" fill="url(#card3Bg)" stroke="#CBACF9" stroke-opacity="0.32" stroke-width="1.2" />
    <rect x="20" y="20" width="198" height="25" rx="12.5" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.25" />
    <text x="32" y="36.5" fill="#FFFFFF" class="font-mono" font-size="10.5" font-weight="600">PHASE 03 · PRODUCTION NLP</text>
    <text x="20" y="72" fill="#FFFFFF" class="font-sans" font-size="17.5" font-weight="700">Hybrid RAG &amp; Automation</text>
    <text x="20" y="100" fill="#BEC1DD" class="font-sans" font-size="13">Production Retrieval-Augmented Generation</text>
    <text x="20" y="121" fill="#BEC1DD" class="font-sans" font-size="13">pipelines (<tspan fill="#FFFFFF" font-weight="600">FastAPI, LangChain, MongoDB,</tspan></text>
    <text x="20" y="142" fill="#BEC1DD" class="font-sans" font-size="13"><tspan fill="#FFFFFF" font-weight="600">Docker</tspan>), workflow automation (<tspan fill="#FFFFFF" font-weight="600">n8n</tspan>), and</text>
    <text x="20" y="163" fill="#BEC1DD" class="font-sans" font-size="13">scalable <tspan fill="#FFFFFF" font-weight="600">TypeScript</tspan> backends.</text>
  </g>
</svg>
"""
    (ASSETS / "bento-phases.svg").write_text(bento_svg, encoding="utf-8")

    # 3. My Work Experience Card SVG (experience-card.svg — Part-Time AI Specialist + SQOIN + Omdena)
    exp_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 142" width="100%">
  <defs>
    <linearGradient id="activeRoleBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B102E" />
      <stop offset="100%" stop-color="#04071D" />
    </linearGradient>
    <style>
      .font-sans { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace; }
      @keyframes pulseDot {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
      }
      .pulse { animation: pulseDot 2.2s ease-in-out infinite; }
    </style>
  </defs>

  <!-- Card 1: AI Specialist · Part-Time (Present) -->
  <g transform="translate(0, 0)">
    <rect x="1" y="1" width="340" height="138" rx="16" fill="url(#activeRoleBg)" stroke="#CBACF9" stroke-opacity="0.48" stroke-width="1.3" />
    <circle cx="24" cy="28" r="4" fill="#10B981" class="pulse" />
    <text x="36" y="32" fill="#10B981" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.1">CURRENT ROLE · PART-TIME</text>
    <rect x="258" y="17" width="64" height="21" rx="6" fill="#CBACF9" fill-opacity="0.16" stroke="#CBACF9" stroke-opacity="0.38" />
    <text x="270" y="31" fill="#CBACF9" class="font-mono" font-size="10" font-weight="600">Present</text>
    <text x="20" y="63" fill="#FFFFFF" class="font-sans" font-size="16.5" font-weight="700">AI Specialist (Part-Time)</text>
    <text x="20" y="89" fill="#BEC1DD" class="font-sans" font-size="13">Building autonomous AI agents, real-time</text>
    <text x="20" y="110" fill="#BEC1DD" class="font-sans" font-size="13">voice/LLM pipelines &amp; scalable automation.</text>
  </g>

  <!-- Card 2: AI Intern · SQOIN -->
  <g transform="translate(356, 0)">
    <rect x="1" y="1" width="294" height="138" rx="16" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.15" stroke-width="1.2" />
    <text x="20" y="32" fill="#CBACF9" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.1">EXPERIENCE · SQOIN</text>
    <text x="20" y="63" fill="#FFFFFF" class="font-sans" font-size="16.5" font-weight="700">AI Intern · SQOIN</text>
    <text x="20" y="89" fill="#BEC1DD" class="font-sans" font-size="13">Developing autonomous AI agents and</text>
    <text x="20" y="110" fill="#BEC1DD" class="font-sans" font-size="13">integrating LLMs for task-oriented problems.</text>
  </g>

  <!-- Card 3: Junior ML Engineer · Omdena -->
  <g transform="translate(666, 0)">
    <rect x="1" y="1" width="293" height="138" rx="16" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.15" stroke-width="1.2" />
    <text x="20" y="32" fill="#38BDF8" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.1">EXPERIENCE · OMDENA</text>
    <text x="20" y="63" fill="#FFFFFF" class="font-sans" font-size="16.5" font-weight="700">Junior ML Engineer · Omdena</text>
    <text x="20" y="89" fill="#BEC1DD" class="font-sans" font-size="13">Integrated local LLMs into LibreOffice on</text>
    <text x="20" y="110" fill="#BEC1DD" class="font-sans" font-size="13">GPU resources with interactive UI.</text>
  </g>
</svg>
"""
    (ASSETS / "experience-card.svg").write_text(exp_svg, encoding="utf-8")

    # 4. Portfolio Projects 2x2 Bento Grid SVG (projects-bento.svg — Eliminates Crushed HTML Table!)
    projects_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 296" width="100%">
  <defs>
    <linearGradient id="projGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B102E" />
      <stop offset="100%" stop-color="#04071D" />
    </linearGradient>
    <linearGradient id="projGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#07192E" />
      <stop offset="100%" stop-color="#04071D" />
    </linearGradient>
    <style>
      .font-sans { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace; }
    </style>
  </defs>

  <!-- Row 1, Col 1: Microsoft Office Antigravity Copilot -->
  <g transform="translate(0, 0)">
    <rect x="1" y="1" width="470" height="138" rx="16" fill="url(#projGrad1)" stroke="#CBACF9" stroke-opacity="0.38" stroke-width="1.2" />
    <text x="22" y="30" fill="#CBACF9" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.1">01 · AGENTIC OFFICE AUTOMATION</text>
    <rect x="308" y="15" width="144" height="21" rx="6" fill="#CBACF9" fill-opacity="0.14" stroke="#CBACF9" stroke-opacity="0.32" />
    <text x="319" y="29" fill="#CBACF9" class="font-mono" font-size="10" font-weight="600">Python · Gemini · JS</text>
    <text x="22" y="60" fill="#FFFFFF" class="font-sans" font-size="17" font-weight="700">Microsoft Office Antigravity Copilot</text>
    <text x="22" y="87" fill="#BEC1DD" class="font-sans" font-size="13">Autonomous AI Copilot integrating Gemini and the Antigravity</text>
    <text x="22" y="108" fill="#BEC1DD" class="font-sans" font-size="13">agent harness directly into Word, Excel, PowerPoint &amp; Outlook.</text>
  </g>

  <!-- Row 1, Col 2: Autonomous AI Agent (MonAgent) -->
  <g transform="translate(488, 0)">
    <rect x="1" y="1" width="470" height="138" rx="16" fill="url(#projGrad2)" stroke="#38BDF8" stroke-opacity="0.38" stroke-width="1.2" />
    <text x="22" y="30" fill="#38BDF8" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.1">02 · AUTONOMOUS CODING AGENT</text>
    <rect x="296" y="15" width="156" height="21" rx="6" fill="#38BDF8" fill-opacity="0.14" stroke="#38BDF8" stroke-opacity="0.32" />
    <text x="307" y="29" fill="#38BDF8" class="font-mono" font-size="10" font-weight="600">FastAPI · React · Docker</text>
    <text x="22" y="60" fill="#FFFFFF" class="font-sans" font-size="17" font-weight="700">Autonomous AI Agent (MonAgent)</text>
    <text x="22" y="87" fill="#BEC1DD" class="font-sans" font-size="13">Autonomous coding agent translating user intent into executable</text>
    <text x="22" y="108" fill="#BEC1DD" class="font-sans" font-size="13">code via a <tspan fill="#FFFFFF" font-weight="600">Think → Act → Observe</tspan> ReAct loop in Docker sandboxes.</text>
  </g>

  <!-- Row 2, Col 1: Retrieval Augmented Generation (RAG) -->
  <g transform="translate(0, 154)">
    <rect x="1" y="1" width="470" height="138" rx="16" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.2" />
    <text x="22" y="30" fill="#10B981" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.1">03 · HYBRID RETRIEVAL PIPELINE</text>
    <rect x="284" y="15" width="168" height="21" rx="6" fill="#10B981" fill-opacity="0.14" stroke="#10B981" stroke-opacity="0.32" />
    <text x="295" y="29" fill="#10B981" class="font-mono" font-size="10" font-weight="600">LangChain · FastAPI · Mongo</text>
    <text x="22" y="60" fill="#FFFFFF" class="font-sans" font-size="17" font-weight="700">Retrieval Augmented Generation (RAG)</text>
    <text x="22" y="87" fill="#BEC1DD" class="font-sans" font-size="13">Production-grade RAG system using FastAPI, Docker, MongoDB,</text>
    <text x="22" y="108" fill="#BEC1DD" class="font-sans" font-size="13">and LangChain with hybrid search and context-aware prompts.</text>
  </g>

  <!-- Row 2, Col 2: IntreccIAmi — Low-Rank Diffusion -->
  <g transform="translate(488, 154)">
    <rect x="1" y="1" width="470" height="138" rx="16" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.2" />
    <text x="22" y="30" fill="#CBACF9" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.1">04 · GENERATIVE VISION &amp; LORA</text>
    <rect x="302" y="15" width="150" height="21" rx="6" fill="#CBACF9" fill-opacity="0.14" stroke="#CBACF9" stroke-opacity="0.32" />
    <text x="314" y="29" fill="#CBACF9" class="font-mono" font-size="10" font-weight="600">PyTorch · Diffusion · LoRA</text>
    <text x="22" y="60" fill="#FFFFFF" class="font-sans" font-size="17" font-weight="700">IntreccIAmi — Low-Rank Diffusion</text>
    <text x="22" y="87" fill="#BEC1DD" class="font-sans" font-size="13">Taming Diffusion Models with Low-Rank Adaptation (LoRA) for</text>
    <text x="22" y="108" fill="#BEC1DD" class="font-sans" font-size="13">high-precision complex weave pattern synthesis at UNIVPM.</text>
  </g>
</svg>
"""
    (ASSETS / "projects-bento.svg").write_text(projects_svg, encoding="utf-8")

    # 5. Cosmic Tech Stack & Arsenal SVG (tech-stack.svg — Cohesive Portfolio Pill Card)
    tech_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 124" width="100%">
  <defs>
    <linearGradient id="techBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B102E" />
      <stop offset="100%" stop-color="#04071D" />
    </linearGradient>
    <style>
      .font-sans { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace; }
    </style>
  </defs>
  <rect x="1" y="1" width="958" height="122" rx="18" fill="url(#techBg)" stroke="#CBACF9" stroke-opacity="0.35" stroke-width="1.2" />

  <!-- Row 1: AI, Agents & Deep Learning -->
  <text x="24" y="44" fill="#CBACF9" class="font-mono" font-size="11" font-weight="700" letter-spacing="1.2">AI &amp; AGENTS</text>
  <g transform="translate(148, 25)">
    <rect x="0" y="0" width="84" height="28" rx="8" fill="#000319" stroke="#CBACF9" stroke-opacity="0.4" />
    <text x="42" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">Python</text>

    <rect x="94" y="0" width="92" height="28" rx="8" fill="#000319" stroke="#CBACF9" stroke-opacity="0.4" />
    <text x="140" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">PyTorch</text>

    <rect x="196" y="0" width="112" height="28" rx="8" fill="#000319" stroke="#CBACF9" stroke-opacity="0.4" />
    <text x="252" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">TensorFlow</text>

    <rect x="318" y="0" width="142" height="28" rx="8" fill="#000319" stroke="#CBACF9" stroke-opacity="0.4" />
    <text x="389" y="18.5" text-anchor="middle" fill="#CBACF9" class="font-sans" font-size="12.5" font-weight="600">LangChain &amp; RAG</text>

    <rect x="470" y="0" width="154" height="28" rx="8" fill="#000319" stroke="#CBACF9" stroke-opacity="0.4" />
    <text x="547" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">Diffusion &amp; LoRA</text>

    <rect x="634" y="0" width="152" height="28" rx="8" fill="#000319" stroke="#CBACF9" stroke-opacity="0.4" />
    <text x="710" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">n8n Automation</text>
  </g>

  <!-- Row 2: Full-Stack, Backend & Cloud Native -->
  <text x="24" y="88" fill="#38BDF8" class="font-mono" font-size="11" font-weight="700" letter-spacing="1.2">FULL-STACK</text>
  <g transform="translate(148, 69)">
    <rect x="0" y="0" width="90" height="28" rx="8" fill="#000319" stroke="#38BDF8" stroke-opacity="0.38" />
    <text x="45" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">FastAPI</text>

    <rect x="100" y="0" width="106" height="28" rx="8" fill="#000319" stroke="#38BDF8" stroke-opacity="0.38" />
    <text x="153" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">TypeScript</text>

    <rect x="216" y="0" width="136" height="28" rx="8" fill="#000319" stroke="#38BDF8" stroke-opacity="0.38" />
    <text x="284" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">React &amp; Next.js</text>

    <rect x="362" y="0" width="120" height="28" rx="8" fill="#000319" stroke="#38BDF8" stroke-opacity="0.38" />
    <text x="422" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">Tailwind CSS</text>

    <rect x="492" y="0" width="88" height="28" rx="8" fill="#000319" stroke="#38BDF8" stroke-opacity="0.38" />
    <text x="536" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">Docker</text>

    <rect x="590" y="0" width="196" height="28" rx="8" fill="#000319" stroke="#38BDF8" stroke-opacity="0.38" />
    <text x="688" y="18.5" text-anchor="middle" fill="#FFFFFF" class="font-sans" font-size="12.5" font-weight="600">PostgreSQL &amp; MongoDB</text>
  </g>
</svg>
"""
    (ASSETS / "tech-stack.svg").write_text(tech_svg, encoding="utf-8")

    # 6. Action Button Badges (Portfolio, LinkedIn, Untruncated Medium, Email)
    badge_portfolio = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 218 38" width="218" height="38">
  <defs>
    <clipPath id="pLogo"><circle cx="22" cy="19" r="9" /></clipPath>
  </defs>
  <rect x="0.75" y="0.75" width="216.5" height="36.5" rx="10" fill="#0B102E" stroke="#CBACF9" stroke-opacity="0.55" stroke-width="1.2" />
  <image href="{logo_uri}" x="13" y="10" width="18" height="18" clip-path="url(#pLogo)" />
  <text x="39" y="23.5" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12.5" font-weight="700">hassenbenchaaben.me ↗</text>
</svg>
"""
    (ASSETS / "badge-portfolio.svg").write_text(badge_portfolio, encoding="utf-8")

    badge_linkedin = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 124 38" width="124" height="38">
  <rect x="0.75" y="0.75" width="122.5" height="36.5" rx="10" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.2" />
  <rect x="14" y="10" width="18" height="18" rx="3.5" fill="#0A66C2" />
  <text x="18" y="23.5" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" font-weight="800">in</text>
  <text x="41" y="23.5" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12.5" font-weight="600">LinkedIn</text>
</svg>
"""
    (ASSETS / "badge-linkedin.svg").write_text(badge_linkedin, encoding="utf-8")

    badge_medium = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 162 38" width="162" height="38">
  <rect x="0.75" y="0.75" width="160.5" height="36.5" rx="10" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.2" />
  <g transform="translate(14, 11) scale(0.72)">
    <path fill="#FFFFFF" d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z" />
  </g>
  <text x="40" y="23.5" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12.5" font-weight="600">Medium Articles</text>
</svg>
"""
    (ASSETS / "badge-medium.svg").write_text(badge_medium, encoding="utf-8")

    badge_email = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 264 38" width="264" height="38">
  <rect x="0.75" y="0.75" width="262.5" height="36.5" rx="10" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.2" />
  <rect x="14" y="12" width="16" height="13" rx="2" fill="none" stroke="#CBACF9" stroke-width="1.6" />
  <path d="M 14.5 13 L 22 19 L 29.5 13" fill="none" stroke="#CBACF9" stroke-width="1.6" stroke-linecap="round" />
  <text x="38" y="23.5" fill="#BEC1DD" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12.5" font-weight="600">hassen.benchaaben01@gmail.com</text>
</svg>
"""
    (ASSETS / "badge-email.svg").write_text(badge_email, encoding="utf-8")


if __name__ == "__main__":
    generate_all()

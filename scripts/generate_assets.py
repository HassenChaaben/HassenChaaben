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

    # 1. Hero Card SVG (Matches Superdesign v5: Cosmic Solar System Panorama + Animated Meteors/Orbits + #000319 Portfolio Card)
    hero_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 455" width="100%">
  <defs>
    <clipPath id="cardClip">
      <rect x="0" y="0" width="960" height="455" rx="24" />
    </clipPath>
    <clipPath id="logoTopClip">
      <circle cx="718" cy="34" r="10" />
    </clipPath>
    <linearGradient id="fadeOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#000319" stop-opacity="0.05" />
      <stop offset="52%" stop-color="#000319" stop-opacity="0.48" />
      <stop offset="82%" stop-color="#000319" stop-opacity="0.96" />
      <stop offset="100%" stop-color="#000319" stop-opacity="1" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#CBACF9" stop-opacity="0.45" />
      <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#CBACF9" stop-opacity="0.45" />
    </linearGradient>
    <filter id="lavenderGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
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
    <!-- Deep Space Base -->
    <rect x="0" y="0" width="960" height="455" fill="#000319" />

    <!-- High-Res Solar System, Earth Limb, Cratered Moon, Nebula & AI Probe Panorama -->
    <image href="{hero_uri}" x="0" y="0" width="960" height="325" preserveAspectRatio="xMidYMid slice" />

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

    <!-- Gradient Fade into Portfolio Copy Area -->
    <rect x="0" y="0" width="960" height="335" fill="url(#fadeOverlay)" />

    <!-- Subtle Portfolio Grid on Lower Area -->
    <g stroke="#CBACF9" stroke-opacity="0.045" stroke-width="1">
      <line x1="0" y1="310" x2="960" y2="310" />
      <line x1="0" y1="350" x2="960" y2="350" />
      <line x1="0" y1="390" x2="960" y2="390" />
      <line x1="0" y1="430" x2="960" y2="430" />
    </g>

    <!-- Top-Right Glassmorphic Brand Badge -->
    <rect x="698" y="18" width="242" height="32" rx="16" fill="#000319" fill-opacity="0.82" stroke="#CBACF9" stroke-opacity="0.35" />
    <image href="{logo_uri}" x="708" y="24" width="20" height="20" clip-path="url(#logoTopClip)" />
    <text x="736" y="38" fill="#CBACF9" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.6">WELCOME TO MY OWN WORLD</text>

    <!-- Status Pills Row -->
    <rect x="36" y="252" width="295" height="26" rx="13" fill="#04071D" stroke="#CBACF9" stroke-opacity="0.45" />
    <circle cx="52" cy="265" r="3.5" fill="#CBACF9" class="tw1" />
    <text x="64" y="269" fill="#CBACF9" class="font-mono" font-size="10" font-weight="600" letter-spacing="1.7">WHERE CREATIVITY MEETS INNOVATION</text>

    <rect x="342" y="252" width="276" height="26" rx="13" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.18" />
    <text x="358" y="269" fill="#FFFFFF" class="font-mono" font-size="10" font-weight="600" letter-spacing="1.2">✦ BUILDING NEXT-GEN AUTONOMOUS SYSTEMS</text>

    <!-- Main Hero Heading: Crisp White + Signature #CBACF9 Lavender -->
    <text x="36" y="328" class="font-sans" font-size="36" font-weight="800" fill="#FFFFFF">
      Hi, I'm <tspan fill="#CBACF9" filter="url(#lavenderGlow)">Hassen Ben Chaaben</tspan>
    </text>

    <!-- Bio Lines (Exact v5 Approved Text) -->
    <text x="36" y="366" class="font-sans" font-size="15" fill="#BEC1DD">
      I am a <tspan fill="#FFFFFF" font-weight="600">Master's student at UNIVPM</tspan> and <tspan fill="#FFFFFF" font-weight="600">Junior AI Engineer</tspan> (currently working as a <tspan fill="#CBACF9" font-weight="600">Part-Time AI Specialist</tspan>)
    </text>
    <text x="36" y="390" class="font-sans" font-size="15" fill="#BEC1DD">
      focused on building <tspan fill="#CBACF9" font-weight="600">AI agents</tspan> and <tspan fill="#CBACF9" font-weight="600">scalable automation solutions</tspan>. My expertise lies in <tspan fill="#FFFFFF" font-weight="600">Natural Language Processing</tspan>,
    </text>
    <text x="36" y="414" class="font-sans" font-size="15" fill="#BEC1DD">
      <tspan fill="#FFFFFF" font-weight="600">Computer Vision</tspan>, and <tspan fill="#FFFFFF" font-weight="600">Generative AI</tspan>.
    </text>
  </g>

  <!-- Outer Rounded Border -->
  <rect x="0.75" y="0.75" width="958.5" height="453.5" rx="23.25" fill="none" stroke="url(#borderGrad)" stroke-width="1.5" />
</svg>
"""
    (ASSETS / "hero-card.svg").write_text(hero_svg, encoding="utf-8")

    # 2. 3-Phase Cosmic Bento Cards SVG (bento-phases.svg)
    bento_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 190" width="100%">
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
    <rect x="1" y="1" width="308" height="186" rx="18" fill="url(#card1Bg)" stroke="#CBACF9" stroke-opacity="0.35" stroke-width="1.2" />
    <rect x="20" y="20" width="142" height="24" rx="12" fill="#CBACF9" fill-opacity="0.14" stroke="#CBACF9" stroke-opacity="0.35" />
    <text x="32" y="36" fill="#CBACF9" class="font-mono" font-size="10.5" font-weight="600">PHASE 01 · AGENTIC AI</text>
    <text x="20" y="72" fill="#FFFFFF" class="font-sans" font-size="17" font-weight="700">Autonomous AI Agents</text>
    <text x="20" y="100" fill="#BEC1DD" class="font-sans" font-size="12.5">Building <tspan fill="#FFFFFF" font-weight="600">MonAgent</tspan> (<tspan fill="#CBACF9" class="font-mono">Think → Act → Observe</tspan></text>
    <text x="20" y="120" fill="#BEC1DD" class="font-sans" font-size="12.5">ReAct architecture) and the <tspan fill="#FFFFFF" font-weight="600">Microsoft Office</tspan></text>
    <text x="20" y="140" fill="#BEC1DD" class="font-sans" font-size="12.5"><tspan fill="#FFFFFF" font-weight="600">Antigravity Copilot</tspan> integrating Gemini into</text>
    <text x="20" y="160" fill="#BEC1DD" class="font-sans" font-size="12.5">Word, Excel, PowerPoint &amp; Outlook.</text>
  </g>

  <!-- Card 2: PHASE 02 · GENERATIVE AI & CV -->
  <g transform="translate(325, 0)">
    <rect x="1" y="1" width="308" height="186" rx="18" fill="url(#card2Bg)" stroke="#38BDF8" stroke-opacity="0.35" stroke-width="1.2" />
    <rect x="20" y="20" width="182" height="24" rx="12" fill="#38BDF8" fill-opacity="0.14" stroke="#38BDF8" stroke-opacity="0.35" />
    <text x="32" y="36" fill="#38BDF8" class="font-mono" font-size="10.5" font-weight="600">PHASE 02 · GENERATIVE AI &amp; CV</text>
    <text x="20" y="72" fill="#FFFFFF" class="font-sans" font-size="17" font-weight="700">Computer Vision &amp; DL</text>
    <text x="20" y="100" fill="#BEC1DD" class="font-sans" font-size="12.5">Fine-tuning Diffusion Models with Low-Rank</text>
    <text x="20" y="120" fill="#BEC1DD" class="font-sans" font-size="12.5">Adaptation (<tspan fill="#FFFFFF" font-weight="600">IntreccIAmi</tspan>) for complex visual</text>
    <text x="20" y="140" fill="#BEC1DD" class="font-sans" font-size="12.5">synthesis and training deep neural networks</text>
    <text x="20" y="160" fill="#BEC1DD" class="font-sans" font-size="12.5">in <tspan fill="#FFFFFF" font-weight="600">PyTorch &amp; TensorFlow</tspan>.</text>
  </g>

  <!-- Card 3: PHASE 03 · PRODUCTION NLP -->
  <g transform="translate(650, 0)">
    <rect x="1" y="1" width="308" height="186" rx="18" fill="url(#card3Bg)" stroke="#CBACF9" stroke-opacity="0.28" stroke-width="1.2" />
    <rect x="20" y="20" width="172" height="24" rx="12" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.22" />
    <text x="32" y="36" fill="#FFFFFF" class="font-mono" font-size="10.5" font-weight="600">PHASE 03 · PRODUCTION NLP</text>
    <text x="20" y="72" fill="#FFFFFF" class="font-sans" font-size="17" font-weight="700">Hybrid RAG &amp; Automation</text>
    <text x="20" y="100" fill="#BEC1DD" class="font-sans" font-size="12.5">Production Retrieval-Augmented Generation</text>
    <text x="20" y="120" fill="#BEC1DD" class="font-sans" font-size="12.5">pipelines (<tspan fill="#FFFFFF" font-weight="600">FastAPI, LangChain, MongoDB,</tspan></text>
    <text x="20" y="140" fill="#BEC1DD" class="font-sans" font-size="12.5"><tspan fill="#FFFFFF" font-weight="600">Docker</tspan>), workflow automation (<tspan fill="#FFFFFF" font-weight="600">n8n</tspan>), and</text>
    <text x="20" y="160" fill="#BEC1DD" class="font-sans" font-size="12.5">scalable <tspan fill="#FFFFFF" font-weight="600">TypeScript</tspan> backends.</text>
  </g>
</svg>
"""
    (ASSETS / "bento-phases.svg").write_text(bento_svg, encoding="utf-8")

    # 3. My Work Experience Card SVG (experience-card.svg — Part-Time AI Specialist + SQOIN + Omdena)
    exp_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 140" width="100%">
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
    <rect x="1" y="1" width="340" height="136" rx="16" fill="url(#activeRoleBg)" stroke="#CBACF9" stroke-opacity="0.45" stroke-width="1.3" />
    <circle cx="24" cy="28" r="4" fill="#10B981" class="pulse" />
    <text x="36" y="32" fill="#10B981" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.2">CURRENT ROLE · PART-TIME</text>
    <rect x="262" y="17" width="60" height="20" rx="6" fill="#CBACF9" fill-opacity="0.16" stroke="#CBACF9" stroke-opacity="0.35" />
    <text x="273" y="31" fill="#CBACF9" class="font-mono" font-size="10" font-weight="600">Present</text>
    <text x="20" y="62" fill="#FFFFFF" class="font-sans" font-size="16.5" font-weight="700">AI Specialist (Part-Time)</text>
    <text x="20" y="88" fill="#BEC1DD" class="font-sans" font-size="12.5">Building autonomous AI agents, real-time</text>
    <text x="20" y="108" fill="#BEC1DD" class="font-sans" font-size="12.5">voice/LLM pipelines &amp; scalable automation.</text>
  </g>

  <!-- Card 2: AI Intern · SQOIN -->
  <g transform="translate(356, 0)">
    <rect x="1" y="1" width="294" height="136" rx="16" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1.2" />
    <text x="20" y="32" fill="#CBACF9" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.2">EXPERIENCE · SQOIN</text>
    <text x="20" y="62" fill="#FFFFFF" class="font-sans" font-size="16.5" font-weight="700">AI Intern · SQOIN</text>
    <text x="20" y="88" fill="#BEC1DD" class="font-sans" font-size="12.5">Developing autonomous AI agents and</text>
    <text x="20" y="108" fill="#BEC1DD" class="font-sans" font-size="12.5">integrating LLMs for task-oriented problems.</text>
  </g>

  <!-- Card 3: Junior ML Engineer · Omdena -->
  <g transform="translate(666, 0)">
    <rect x="1" y="1" width="293" height="136" rx="16" fill="#04071D" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1.2" />
    <text x="20" y="32" fill="#38BDF8" class="font-mono" font-size="10.5" font-weight="600" letter-spacing="1.2">EXPERIENCE · OMDENA</text>
    <text x="20" y="62" fill="#FFFFFF" class="font-sans" font-size="16.5" font-weight="700">Junior ML Engineer · Omdena</text>
    <text x="20" y="88" fill="#BEC1DD" class="font-sans" font-size="12.5">Integrated local LLMs into LibreOffice on</text>
    <text x="20" y="108" fill="#BEC1DD" class="font-sans" font-size="12.5">GPU resources with interactive UI.</text>
  </g>
</svg>
"""
    (ASSETS / "experience-card.svg").write_text(exp_svg, encoding="utf-8")

    # 4. Action Button Badges (Portfolio, LinkedIn, Untruncated Medium, Email)
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

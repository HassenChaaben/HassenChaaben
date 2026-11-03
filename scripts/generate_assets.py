from __future__ import annotations

import base64
import io
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def _b64_data_uri(path: Path, mime: str = "image/jpeg") -> str:
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _pil_to_data_uri(img: Image.Image, fmt: str = "PNG", quality: int = 92) -> str:
    buf = io.BytesIO()
    if fmt.upper() == "JPEG":
        img.convert("RGB").save(buf, format="JPEG", quality=quality, optimize=True)
        mime = "image/jpeg"
    else:
        img.save(buf, format="PNG", optimize=True)
        mime = "image/png"
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _prepare_three_planet_layers() -> tuple[str, str, str, str]:
    """
    Extracts 4 photographic layers from Hassen's uploaded 3-planet image
    (assets/three-planets-source.png):
      1. Clean deep-space starfield background (with Google Lens icon & static planets removed)
      2. MarsRGBA sprite (cx=304.6, cy=62.3, r=41.9 + warm orange corona)
      3. Moon RGBA sprite (cx=549.7, cy=120.5, r=94.6 + silver-white lunar glow)
      4. Earth RGBA horizon sprite (cx=306.5, cy=983.1, r=675.7 + cyan atmospheric limb)
    """
    src_path = ASSETS / "three-planets-source.png"
    raw_img = Image.open(src_path).convert("RGB")
    w, h = raw_img.size  # 650 x 368

    # Crop 4px outer screenshot border and resize back to 650x368 cleanly
    cropped = raw_img.crop((4, 4, w - 4, h - 4)).resize((w, h), Image.Resampling.LANCZOS)
    arr = np.array(cropped, dtype=np.float32)

    # Remove rounded white screenshot corner arcs at all 4 corners
    for y in range(28):
        for x in range(28):
            if x + y < 24:
                arr[y, x, :] = arr[24, 24, :]
            if (w - 1 - x) + y < 24:
                arr[y, w - 1 - x, :] = arr[24, w - 25, :]

    # Clean out ONLY the circular Google Lens icon at (cx=36, cy=330, r=26)
    # Sample the clean sky ring immediately surrounding the icon (r=27..34) so Earth's natural atmosphere is 100% untouched
    yy, xx = np.mgrid[0:h, 0:w]
    lens_dist = np.sqrt((xx - 36.0) ** 2 + (yy - 330.0) ** 2)
    ring_mask = (lens_dist >= 27.0) & (lens_dist <= 35.0)
    ring_median = np.median(arr[ring_mask], axis=0)
    lens_alpha = np.clip((28.0 - lens_dist) / 5.0, 0.0, 1.0)[..., None]
    arr = (1.0 - lens_alpha) * arr + lens_alpha * ring_median

    # Save cleaned full reference image to assets/three-planets-hero.jpg
    clean_full = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    clean_full.resize((960, 544), Image.Resampling.LANCZOS).save(
        ASSETS / "three-planets-hero.jpg", format="JPEG", quality=93, optimize=True
    )

    yy, xx = np.mgrid[0:h, 0:w]

    # 1. Extract Mars RGBA Sprite (box: x=228..382, y=0..140; center=(304.6, 62.3), r=41.9)
    mars_cx, mars_cy, mars_r = 304.6, 62.3, 41.9
    dist_mars = np.sqrt((xx - mars_cx) ** 2 + (yy - mars_cy) ** 2)
    lum_mars = np.max(arr, axis=2) - 6.0
    alpha_mars = np.where(
        dist_mars <= mars_r + 0.8,
        255.0,
        np.clip((lum_mars / 38.0) * 255.0, 0.0, 255.0)
        * np.clip(1.0 - (dist_mars - mars_r) / 30.0, 0.0, 1.0) ** 1.5,
    )
    mx0, my0, mx1, my1 = 228, 0, 382, 138
    mars_rgba = np.zeros((my1 - my0, mx1 - mx0, 4), dtype=np.uint8)
    mars_rgba[..., :3] = np.clip(arr[my0:my1, mx0:mx1, :], 0, 255).astype(np.uint8)
    mars_rgba[..., 3] = np.clip(alpha_mars[my0:my1, mx0:mx1], 0, 255).astype(np.uint8)
    mars_uri = _pil_to_data_uri(Image.fromarray(mars_rgba, mode="RGBA"), fmt="PNG")

    # 2. Extract Moon RGBA Sprite (box: x=424..650, y=6..244; center=(549.7, 120.5), r=94.6)
    moon_cx, moon_cy, moon_r = 549.7, 120.5, 94.6
    dist_moon = np.sqrt((xx - moon_cx) ** 2 + (yy - moon_cy) ** 2)
    lum_moon = np.max(arr, axis=2) - 5.0
    alpha_moon = np.where(
        dist_moon <= moon_r + 0.8,
        255.0,
        np.clip((lum_moon / 42.0) * 255.0, 0.0, 255.0)
        * np.clip(1.0 - (dist_moon - moon_r) / 34.0, 0.0, 1.0) ** 1.5,
    )
    lx0, ly0, lx1, ly1 = 424, 6, 650, 244
    moon_rgba = np.zeros((ly1 - ly0, lx1 - lx0, 4), dtype=np.uint8)
    moon_rgba[..., :3] = np.clip(arr[ly0:ly1, lx0:lx1, :], 0, 255).astype(np.uint8)
    moon_rgba[..., 3] = np.clip(alpha_moon[ly0:ly1, lx0:lx1], 0, 255).astype(np.uint8)
    moon_uri = _pil_to_data_uri(Image.fromarray(moon_rgba, mode="RGBA"), fmt="PNG")

    # 3. Extract Earth Horizon RGBA Sprite (box: x=0..650, y=200..368; center=(306.5, 983.1), r=675.7)
    earth_cx, earth_cy, earth_r = 306.5, 983.1, 675.7
    dist_earth = np.sqrt((xx - earth_cx) ** 2 + (yy - earth_cy) ** 2)
    alpha_earth = np.where(
        dist_earth <= earth_r + 2.0,
        255.0,
        255.0 * np.clip(1.0 - (dist_earth - (earth_r + 2.0)) / 58.0, 0.0, 1.0) ** 1.6,
    )
    ey0, ey1 = 200, h
    earth_rgba = np.zeros((ey1 - ey0, w, 4), dtype=np.uint8)
    earth_rgba[..., :3] = np.clip(arr[ey0:ey1, :, :], 0, 255).astype(np.uint8)
    bottom_fade = np.clip((h - 1 - yy) / 26.0, 0.0, 1.0)
    earth_rgba[..., 3] = np.clip(alpha_earth[ey0:ey1, :] * bottom_fade[ey0:ey1, :], 0, 255).astype(np.uint8)
    earth_uri = _pil_to_data_uri(Image.fromarray(earth_rgba, mode="RGBA"), fmt="PNG")

    # 4. Build Clean Deep-Space Starfield Background (remove static Mars, Moon & Earth so animated sprites leave zero ghost trail)
    bg_arr = arr.copy()
    dark_space = np.percentile(arr[20:180, 70:190, :], 30, axis=(0, 1))
    for y in range(h):
        for x in range(w):
            if dist_mars[y, x] < mars_r + 36.0 or dist_moon[y, x] < moon_r + 40.0 or y > 195:
                bg_arr[y, x, :] = dark_space

    bg_img = Image.fromarray(np.clip(bg_arr, 0, 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(radius=0.6)
    )
    bg_uri = _pil_to_data_uri(bg_img, fmt="JPEG", quality=90)
    return bg_uri, mars_uri, moon_uri, earth_uri


def generate_all() -> None:
    bg_uri, mars_uri, moon_uri, earth_uri = _prepare_three_planet_layers()
    logo_uri = _b64_data_uri(ASSETS / "hbc-orbital-logo.jpg")

    # Coordinate scale from 650x368 photo to 960px wide SVG space panorama (scale S = 960/650 = 1.476923, y_offset = -22)
    # Photo height scaled = 368 * 1.476923 = 543.5px. Placing y_offset = -115 puts:
    # - Mars center at (450, 42) -> wait: let's place the 650x368 coordinate space inside a `<g transform="translate(0, -18) scale(1.476923)">`
    # Wait: if y_offset = -18 and scale = 1.476923:
    # - Mars (cy=62.3) is at y = -18 + 62.3 * 1.477 = 74px!
    # - Moon (cy=120.5) is at y = -18 + 120.5 * 1.477 = 160px!
    # - Earth horizon crest (y=260..325 in photo) is at y = -18 + 265 * 1.477 = 373px!
    # Wait: if we want ALL 3 PLANETS (Mars, Moon, AND Earth's bright cyan horizon!) to sit cleanly in the upper 315px above "Hi, I'm Hassen Ben Chaaben" (which is at y=340):
    # Let's check! In the 650x368 photo:
    # - Mars is at y = 20..104
    # - Moon is at y = 26..215
    # - Earth is at y = 255..368
    # If we shift Earth up by just 42px in the 650x368 space (or use scaleY = 0.92 / translate Earth to y=162 in 650-space), then:
    # - Mars is at y = 68px (top-center)
    # - Moon is at y = 148px (right)
    # - Earth's bright glowing cyan/white horizon crest is at y = 245..315px — 100% visible right above "Hi, I'm Hassen Ben Chaaben" (at y=342)!

    hero_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 462" width="100%">
  <defs>
    <clipPath id="cardClip">
      <rect x="0" y="0" width="960" height="462" rx="22" />
    </clipPath>
    <clipPath id="logoTopClip">
      <circle cx="718" cy="34" r="10" />
    </clipPath>
    <radialGradient id="marsHaloGrad" cx="42%" cy="48%" r="52%">
      <stop offset="0%" stop-color="#FB923C" stop-opacity="0.55" />
      <stop offset="55%" stop-color="#EA580C" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#EA580C" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="moonHaloGrad" cx="42%" cy="50%" r="54%">
      <stop offset="0%" stop-color="#F8FAFC" stop-opacity="0.38" />
      <stop offset="60%" stop-color="#94A3B8" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#94A3B8" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="earthAtmoGrad" cx="50%" cy="18%" r="65%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.48" />
      <stop offset="45%" stop-color="#0284C7" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#000319" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="textPanelFade" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#000319" stop-opacity="0" />
      <stop offset="62%" stop-color="#000319" stop-opacity="0.0" />
      <stop offset="74%" stop-color="#000319" stop-opacity="0.72" />
      <stop offset="84%" stop-color="#000319" stop-opacity="0.96" />
      <stop offset="100%" stop-color="#000319" stop-opacity="1" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#CBACF9" stop-opacity="0.55" />
      <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#CBACF9" stop-opacity="0.55" />
    </linearGradient>
    <style>
      .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace; }}

      /* Realistic 3-Planet Orbital and Rotational Physics */
      @keyframes marsOrbit {{
        0%   {{ transform: translate(0px, 0px) rotate(0deg) scale(1); }}
        25%  {{ transform: translate(14px, -7px) rotate(2.2deg) scale(1.03); }}
        50%  {{ transform: translate(24px, 3px) rotate(0deg) scale(1.05); }}
        75%  {{ transform: translate(10px, 9px) rotate(-2.2deg) scale(1.02); }}
        100% {{ transform: translate(0px, 0px) rotate(0deg) scale(1); }}
      }}
      @keyframes moonOrbit {{
        0%   {{ transform: translate(0px, 0px) rotate(0deg) scale(1); }}
        33%  {{ transform: translate(-18px, 8px) rotate(-1.8deg) scale(1.025); }}
        66%  {{ transform: translate(-8px, -10px) rotate(1.6deg) scale(0.985); }}
        100% {{ transform: translate(0px, 0px) rotate(0deg) scale(1); }}
      }}
      @keyframes earthOrbit {{
        0%   {{ transform: translate(0px, 0px) rotate(0deg); }}
        50%  {{ transform: translate(-12px, -6px) rotate(0.9deg); }}
        100% {{ transform: translate(0px, 0px) rotate(0deg); }}
      }}
      @keyframes coronaPulse {{
        0%, 100% {{ opacity: 0.65; }}
        50%      {{ opacity: 1; }}
      }}
      @keyframes orbitFlow {{
        to {{ stroke-dashoffset: -96; }}
      }}
      @keyframes twinkle {{
        0%, 100% {{ opacity: 0.25; }}
        50%      {{ opacity: 1; }}
      }}

      #mars-planet {{
        transform-box: fill-box;
        transform-origin: center;
        animation: marsOrbit 14s ease-in-out infinite;
      }}
      #moon-planet {{
        transform-box: fill-box;
        transform-origin: center;
        animation: moonOrbit 18s ease-in-out infinite;
      }}
      #earth-planet {{
        transform-box: fill-box;
        transform-origin: 50% 85%;
        animation: earthOrbit 22s ease-in-out infinite;
      }}
      .corona {{ animation: coronaPulse 4.5s ease-in-out infinite; }}
      .orbit-arc {{ stroke-dasharray: 7 7; animation: orbitFlow 4.5s linear infinite; }}
      .tw1 {{ animation: twinkle 3.2s ease-in-out infinite; }}
      .tw2 {{ animation: twinkle 4.6s ease-in-out 1.5s infinite; }}
      .tw3 {{ animation: twinkle 3.8s ease-in-out 0.8s infinite; }}
    </style>
  </defs>

  <g clip-path="url(#cardClip)">
    <!-- Deep Space Base -->
    <rect x="0" y="0" width="960" height="462" fill="#000319" />

    <!-- Scene Group Uniformly Scaled (1.476923x) so Mars and Moon remain 100% True Circles -->
    <g transform="translate(0, -14) scale(1.476923)">
      <!-- Layer 0: Clean Deep-Space Starfield from Uploaded Image -->
      <image href="{bg_uri}" x="0" y="0" width="650" height="368" preserveAspectRatio="none" />

      <!-- Twinkling Deep-Space Stars -->
      <circle cx="88" cy="48" r="1.1" fill="#FFFFFF" class="tw1" />
      <circle cx="145" cy="96" r="1.3" fill="#38BDF8" class="tw2" />
      <circle cx="192" cy="36" r="1.0" fill="#CBACF9" class="tw3" />
      <circle cx="395" cy="118" r="1.2" fill="#FFFFFF" class="tw1" />
      <circle cx="418" cy="44" r="1.1" fill="#CBACF9" class="tw2" />

      <!-- Subtle Animated Orbital Trajectory Arcs Connecting Earth -> Mars -> Moon -->
      <path d="M 110 215 Q 245 105, 305 62 T 550 120" fill="none" stroke="#38BDF8" stroke-opacity="0.28" stroke-width="0.9" class="orbit-arc" />
      <path d="M 190 225 Q 370 148, 550 120" fill="none" stroke="#CBACF9" stroke-opacity="0.32" stroke-width="0.9" class="orbit-arc" />

      <!-- PLANET 1: MARS (Top-Center Glowing Orange Crescent Planet) -->
      <g id="mars-planet">
        <circle cx="304.6" cy="62.3" r="62" fill="url(#marsHaloGrad)" class="corona" />
        <image href="{mars_uri}" x="228" y="0" width="154" height="138" />
      </g>

      <!-- PLANET 2: THE MOON (Right Cratered Lunar Crescent) -->
      <g id="moon-planet">
        <circle cx="549.7" cy="120.5" r="122" fill="url(#moonHaloGrad)" class="corona" />
        <image href="{moon_uri}" x="424" y="6" width="226" height="238" />
      </g>

      <!-- PLANET 3: EARTH (Glowing Cyan/Blue Curved Horizon Limb) -->
      <g id="earth-planet">
        <ellipse cx="315" cy="212" rx="310" ry="65" fill="url(#earthAtmoGrad)" class="corona" />
        <image href="{earth_uri}" x="0" y="124" width="650" height="168" />
      </g>
    </g>

    <!-- Smooth Translucent Portfolio Overlay preserving Earth's Glowing Cyan Horizon at y=225..310 -->
    <rect x="0" y="0" width="960" height="462" fill="url(#textPanelFade)" />

    <!-- Top-Left & Top-Right Glassmorphic Status Pills (Leaves Center 3-Planet Panorama 100% Unobstructed) -->
    <rect x="24" y="18" width="304" height="28" rx="14" fill="#000319" fill-opacity="0.78" stroke="#CBACF9" stroke-opacity="0.45" />
    <circle cx="42" cy="32" r="3.5" fill="#CBACF9" class="tw1" />
    <text x="54" y="36" fill="#CBACF9" class="font-mono" font-size="10" font-weight="600" letter-spacing="1.6">WHERE CREATIVITY MEETS INNOVATION</text>

    <rect x="688" y="18" width="248" height="28" rx="14" fill="#000319" fill-opacity="0.78" stroke="#CBACF9" stroke-opacity="0.42" />
    <image href="{logo_uri}" x="708" y="22" width="20" height="20" clip-path="url(#logoTopClip)" />
    <text x="735" y="36" fill="#CBACF9" class="font-mono" font-size="10" font-weight="600" letter-spacing="1.5">WELCOME TO MY OWN WORLD</text>

    <!-- Main Hero Heading: Razor-Sharp White + Solid #CBACF9 Portfolio Lavender -->
    <text x="36" y="340" class="font-sans" font-size="36" font-weight="800" fill="#FFFFFF">
      Hi, I'm <tspan fill="#CBACF9">Hassen Ben Chaaben</tspan>
    </text>

    <!-- Bio Lines (Approved v5 Text) -->
    <text x="36" y="376" class="font-sans" font-size="15" fill="#BEC1DD">
      I am a <tspan fill="#FFFFFF" font-weight="600">Master's student at UNIVPM</tspan> and <tspan fill="#FFFFFF" font-weight="600">Junior AI Engineer</tspan> (currently working as a <tspan fill="#CBACF9" font-weight="600">Part-Time AI Specialist</tspan>)
    </text>
    <text x="36" y="400" class="font-sans" font-size="15" fill="#BEC1DD">
      focused on building <tspan fill="#CBACF9" font-weight="600">AI agents</tspan> and <tspan fill="#CBACF9" font-weight="600">scalable automation solutions</tspan>. My expertise lies in <tspan fill="#FFFFFF" font-weight="600">Natural Language Processing</tspan>,
    </text>
    <text x="36" y="424" class="font-sans" font-size="15" fill="#BEC1DD">
      <tspan fill="#FFFFFF" font-weight="600">Computer Vision</tspan>, and <tspan fill="#FFFFFF" font-weight="600">Generative AI</tspan>.
    </text>
  </g>

  <rect x="0.75" y="0.75" width="958.5" height="460.5" rx="21.25" fill="none" stroke="url(#borderGrad)" stroke-width="1.5" />
</svg>
"""
    (ASSETS / "hero-card.svg").write_text(hero_svg, encoding="utf-8")

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

    # 4. Portfolio Projects 2x2 Bento Grid SVG (projects-bento.svg)
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

    # 5. Cosmic Tech Stack & Arsenal SVG (tech-stack.svg)
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

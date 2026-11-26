"""Builds the static BrainEase site into dist/. Pure Python, no dependencies.
Each page = layout(head, header, main, footer). Edit content here, run `python3 build.py`."""
import json, os, html
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
SITE = 'https://braineasehealth.org'

# ---------- drawings ----------
POSES = {
    'sit': [('c', -2, -41, 9), ('p', 'M-1.5 -32 L0 0'), ('p', 'M-1 -23 L9 -12 L15 -4'), ('p', 'M0 0 L16 1'), ('leg', 'M16 1 L18 19 L25 19')],
    'wave': [('c', 0, -63, 9), ('p', 'M0 -54 L0 -24'), ('p', 'M0 -24 L-7 0'), ('p', 'M0 -24 L7 0'), ('p', 'M0 -46 L-9 -31'), ('wv', 'M0 -46 L11 -56 L14 -69')],
    'think': [('c', 2, -42, 9), ('p', 'M-1 -33 L0 0'), ('p', 'M-1 -24 L11 -21 L7 -32'), ('p', 'M0 0 L16 1'), ('leg', 'M16 1 L18 19 L25 19')],
    'stand': [('c', 0, -63, 9), ('p', 'M0 -54 L0 -24'), ('p', 'M0 -24 L-7 0'), ('p', 'M0 -24 L7 0'), ('p', 'M0 -46 L-7 -30'), ('p', 'M0 -46 L7 -30')],
    'lie': [('c', -36, -9, 8), ('p', 'M-27 -6 L8 -5'), ('p', 'M8 -5 L19 -14 L29 -5'), ('p', 'M-20 -6 L-27 -17 L-37 -20')],
}

def fig(pose, d0=0.0, col='var(--ez,#3d7f1f)', w=3.4, step=.2, br=False):
    out = []
    for i, s in enumerate(POSES[pose]):
        st = f'style="--d:{d0 + i * step:.2f}s"'
        if s[0] == 'c':
            out.append(f'<circle class="d" cx="{s[1]}" cy="{s[2]}" r="{s[3]}" pathLength="1" {st}/>')
        else:
            p = f'<path class="d" d="{s[1]}" pathLength="1" {st}/>'
            out.append(f'<g class="leg">{p}</g>' if s[0] == 'leg' else f'<g class="wv">{p}</g>' if s[0] == 'wv' else p)
    return f'<g class="{"br" if br else ""}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{"".join(out)}</g>'

def E(x, y, s=1, col='#e1891f'):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{col}"><rect width="13" height="90" rx="1"/><rect width="70" height="13" rx="1"/>'
            f'<rect y="39" width="58" height="12" rx="1"/><rect y="77" width="70" height="13" rx="1"/></g>')

def braina(d0=0.0, col='#8aa281'):
    """Braina the tortoise: one line, sage, shell arcs echo the office rug."""
    return (f'<g fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
            f'<path class="d" pathLength="1" style="--d:{d0:.2f}s" d="M-34 0 C-30 -32 30 -32 34 0 Z"/>'
            f'<path class="d" pathLength="1" style="--d:{d0 + .3:.2f}s" d="M-22 -2 C-18 -16 18 -16 22 -2 M-11 -2 C-9 -9 9 -9 11 -2"/>'
            f'<path class="d" pathLength="1" style="--d:{d0 + .5:.2f}s" d="M34 -4 C44 -5 50 -12 46 -18 C42 -24 34 -18 32 -9"/>'
            f'<path class="d" pathLength="1" style="--d:{d0 + .6:.2f}s" d="M-22 0 L-25 9 M22 0 L25 9"/></g>'
            f'<circle cx="43" cy="-14" r="1.6" fill="{col}"/>')

def logo_svg(tagline=False, cls='', aria='BrainEase'):
    h = 222 if tagline else 176
    tg = ('<text x="8" y="186" font-family="Figtree,sans-serif" font-size="15.5" font-weight="600" fill="#a6540a" '
          'textLength="584" lengthAdjust="spacing">YOUR PARTNER IN MENTAL HEALTH CARE</text>') if tagline else ''
    return (f'<svg class="ez {cls}" viewBox="0 -26 600 {h}" role="img" aria-label="{aria}">'
            f'<text x="6" y="140" font-family="Outfit,sans-serif" font-size="128" fill="#4a8a22" textLength="282" lengthAdjust="spacingAndGlyphs">Brain</text>'
            f'{E(302, 50)}<text x="384" y="140" font-family="Outfit,sans-serif" font-size="128" fill="#e1891f" textLength="206" lengthAdjust="spacingAndGlyphs">ase</text>'
            f'<g transform="translate(346 50) scale(1.2)">{fig("sit", .3, w=3.2, step=.28)}</g>{tg}</svg>')

def scene(kind):
    if kind == 'bench':
        return (f'<svg class="ez" viewBox="-120 -110 260 160" aria-hidden="true"><path d="M-110 30 H130" stroke="#e7e0d3" stroke-width="2"/>'
                f'{E(-20, -60)}<g transform="translate(26 -60) scale(1.25)">{fig("sit", .2, br=True)}</g>'
                f'<g transform="translate(-75 30) scale(.9)">{braina(1.1)}</g></svg>')
    if kind == 'duo':
        return (f'<svg class="ez" viewBox="-110 -80 220 100" aria-hidden="true"><path d="M-110 12 H110" stroke="#e7e0d3" stroke-width="2"/>'
                f'<g transform="translate(-40 12)">{fig("wave", .1)}</g><g transform="translate(40 4)">{braina(.8)}</g></svg>')
    if kind == 'ep':
        return (f'<svg class="ez" viewBox="-70 -110 170 150" aria-hidden="true" style="--ez:#cfe7b4">{E(-40, -60, .9)}'
                f'<g transform="translate(-2 -60)">{fig("sit", .1)}</g><g transform="translate(60 26) scale(.7)">{braina(.6, "#9fb596")}</g></svg>')
    if kind == 'lost':
        return (f'<svg class="ez" viewBox="-80 -110 200 150" aria-hidden="true">{E(-40, -60)}'
                f'<g transform="translate(62 30) scale(.9)">{fig("lie", .2)}</g></svg>')
    if kind == 'cover':
        return (f'<svg class="ez" viewBox="-110 -110 220 150" aria-hidden="true" style="--ez:#cfe7b4">{E(-60, -60, .9)}'
                f'<g transform="translate(-20 -60)">{fig("think", .1)}</g><g transform="translate(55 28) scale(.8)">{braina(.6, "#9fb596")}</g></svg>')
    raise KeyError(kind)

ICON = {
    'dna': '<path d="M14 4c0 12 16 14 16 26s-16 4-16 10M30 4c0 12-16 14-16 26s16 4 16 10M16 12h12M16 32h12"/>',
    'leaf': '<path d="M8 36C8 18 20 8 38 6c0 18-10 30-28 30M8 36l16-16"/>',
    'one': '<circle cx="22" cy="10" r="6"/><path d="M22 16v14M22 30l-7 10M22 30l7 10M12 22h20"/>',
    'ear': '<path d="M14 18a10 10 0 1 1 18 6c-3 4-6 4-6 9a5 5 0 0 1-9 2M20 18a3 3 0 0 1 6 0c0 3-3 4-3 6"/>',
    'chat': '<path d="M6 10h32v20H18l-8 7v-7H6z"/>',
    'pill': '<rect x="6" y="15" width="32" height="14" rx="7"/><path d="M22 15v14"/>',
    'home': '<path d="M6 20L22 7l16 13v17H6z M17 37V26h10v11"/>',
    'screen': '<rect x="5" y="8" width="34" height="22" rx="3"/><path d="M15 37h14M22 30v7"/>',
}
def icon(k): return f'<svg class="ic" viewBox="0 0 44 44" aria-hidden="true">{ICON[k]}</svg>'

def pic(name, alt, cls='photo', pos='50% 30%', w=787, h=1400, eager=False):
    load = 'eager' if eager else 'lazy'
    return (f'<div class="{cls}"><picture><source srcset="/img/{name}.webp" type="image/webp">'
            f'<img src="/img/{name}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}" loading="{load}" decoding="async" style="object-position:{pos}"></picture></div>')

# ---------- layout ----------
NAV = [('/about.html', 'About Sariette'), ('/services.html', 'Services'), ('/genetic-testing.html', 'Genetic Testing'),
       ('/videos.html', 'Videos'), ('/blog/', 'Blog'), ('/faq.html', 'FAQ'), ('/contact.html', 'Contact')]

def header(path):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{u}"{cur if u == path else ""}>{t}</a>' for u, t in NAV)
    dl = ''.join(f'<a href="{u}">{t}</a>' for u, t in [('/', 'Home')] + NAV + [('/conditions.html', 'Conditions'), ('/for-professionals.html', 'For Professionals')])
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="wrap">
  <a class="brand" href="/" aria-label="BrainEase home">{logo_svg()}</a>
  <nav class="nav" aria-label="Main">{links}</nav>
  <a class="btn sm" href="/contact.html#request" data-eze="book">Free intro call</a>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><span></span></button>
</div></header>
<nav class="drawer" id="drawer" aria-label="Mobile">{dl}<a class="btn" href="/contact.html#request" data-eze="book">Book your free 15-min intro call</a><p class="small"><span data-cfg="phone">331-330-7228</span> · call or text</p></nav>'''

FOOTER = '''<footer class="ft"><div class="wrap">
  <div class="cols">
    <div class="stack">
      <a href="/" aria-label="BrainEase home" style="display:inline-block;background:#fbf8f2;border-radius:16px;padding:10px 14px">LOGO</a>
      <p>Functional, integrative psychiatric care for children, teens and adults. In English and French.</p>
      <p><a href="/contact.html#request" data-eze="book">Book your free 15-minute intro call →</a></p>
    </div>
    <div><h4>Visit</h4><ul>
      <li><a data-href="mapsUrl" href="#" target="_blank" rel="noopener" data-cfg="address">440 Quadrangle Dr., Suite I, Bolingbrook, IL 60440</a></li>
      <li>In person on Thursdays</li><li>Telehealth across Illinois</li><li data-cfg="hours">Monday to Friday, 9 am to 5 pm</li></ul></div>
    <div><h4>Contact</h4><ul>
      <li><a data-href="phoneHref" href="tel:+13313307228" data-cfg="phone">331-330-7228</a> · call or text</li>
      <li><a href="mailto:wecare@braineasehealth.org" data-cfg="email">wecare@braineasehealth.org</a></li>
      <li><a href="/for-professionals.html">Referrals for professionals</a></li></ul></div>
    <div><h4>Explore</h4><ul>
      <li><a href="/services.html">Services</a></li><li><a href="/conditions.html">Conditions</a></li><li><a href="/genetic-testing.html">Genetic testing</a></li>
      <li><a href="/videos.html">Take a Seat videos</a></li><li><a href="/blog/">Blog</a></li><li><a href="/faq.html">FAQ</a></li></ul></div>
  </div>
  <p class="crisis"><b>In crisis?</b> BrainEase is not an emergency service. Call or text <b>988</b> (Suicide &amp; Crisis Lifeline) or call <b>911</b>.</p>
  <div class="base"><span>© <span id="yr">2026</span> BrainEase PLLC · Your Partner in Mental Health Care</span>
  <span><a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a> · Website by HOMCO Agency</span></div>
</div></footer>'''

ORG = {
    "@context": "https://schema.org", "@type": "MedicalClinic", "name": "BrainEase PLLC", "url": SITE + "/",
    "slogan": "Your Partner in Mental Health Care", "telephone": "+1-331-330-7228", "email": "wecare@braineasehealth.org",
    "image": SITE + "/img/sariette-sofa-orange.jpg", "medicalSpecialty": "Psychiatric",
    "address": {"@type": "PostalAddress", "streetAddress": "440 Quadrangle Dr., Suite I", "addressLocality": "Bolingbrook",
                "addressRegion": "IL", "postalCode": "60440", "addressCountry": "US"},
    "areaServed": {"@type": "State", "name": "Illinois"}, "availableLanguage": ["English", "French"],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}],
    "founder": {"@type": "Person", "name": "Sariette Ngandjo", "honorificSuffix": "APRN, PMHNP-BC", "jobTitle": "Psychiatric Mental Health Nurse Practitioner"},
}

def page(path, title, desc, body, schema=None):
    url = SITE + path
    ld = json.dumps(schema or ORG, ensure_ascii=False)
    ft = FOOTER.replace('LOGO', logo_svg(aria='BrainEase').replace('class="ez ', 'style="height:40px;width:auto" class="ez '))
    rl = (lambda p, d: d) if path == '/404.html' else relink
    return rl(path, f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="BrainEase">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/img/sariette-sofa-orange.jpg">
<meta name="theme-color" content="#1c3a29">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{ft}
<script src="/assets/site.js" defer></script>
</body>
</html>
''')

def cta_band():
    return f'''<section class="band deep"><div class="wrap grid2">
  <div class="stack reveal"><h2>Take a seat.<br><span style="color:#e1891f">Your first conversation is free.</span></h2>
  <p class="lead">A 15-minute call by phone with Sariette, to meet, ask your questions and see if BrainEase is the right fit. In English or French.</p>
  <div class="btns"><a class="btn" href="/contact.html#request" data-eze="book">Request your free intro call</a><a class="btn ghost" data-href="phoneHref" href="tel:+13313307228">Call or text <span data-cfg="phone">331-330-7228</span></a></div></div>
  <div style="max-width:420px;justify-self:center;width:100%">{scene("cover")}</div>
</div></section>'''

def phead(crumb, h1, lead):
    return f'''<section class="phead"><div class="wrap stack"><p class="crumb"><a href="/">Home</a> / {crumb}</p><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'''

import re
def relink(path, doc):
    """Root-relative links become relative, so the site works on GitHub Pages and in any preview folder."""
    depth = path.count('/') - 1 if not path.endswith('/') else path.count('/') - 1
    pre = '../' * depth
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url == '' : url = 'index.html'
        elif url.endswith('/') or url.split('#')[0].endswith('/'):
            base, _, frag = url.partition('#'); url = base + 'index.html' + ('#' + frag if frag else '')
        return f'{attr}="{pre}{url}'
    return re.sub(r'(href|src|srcset)="/(?!/)([^"]*)', lambda m: fix(m) + '', doc)

PAGES = {}

# ---------- HOME ----------
PAGES['/'] = ('index.html', 'BrainEase | Psychiatric care in Bolingbrook and telehealth across Illinois',
 'Functional, integrative psychiatric care for children, teens and adults. In person in Bolingbrook on Thursdays, telehealth across Illinois, in English and French. Free 15-minute intro call.',
f'''<section class="hero"><div class="wrap grid2">
  <div class="stack">
    <h1>Take a seat.<br><em>Let's talk.</em></h1>
    <p class="lead">Functional, integrative psychiatric care for children, teens and adults. We look at the whole person, not just a list of symptoms.</p>
    <div class="btns"><a class="btn" href="/contact.html#request" data-eze="book">Book your free 15-min intro call</a><a class="btn ghost" href="#how">How it works</a></div>
    <div class="facts"><span class="chip">In person in Bolingbrook, Thursdays</span><span class="chip">Telehealth across Illinois</span><span class="chip">English &amp; French</span><span class="chip">Ages 8 to 65</span></div>
  </div>
  <div class="hero-pic">{pic("sariette-sofa-orange", "Sariette Ngandjo, APRN, PMHNP-BC, in the BrainEase office", eager=True, pos="50% 26%")}
    <div class="ezb">{scene("bench")}</div></div>
</div></section>

<section class="band sand tight"><div class="wrap">
  <div class="stack reveal"><p class="kicker">Why BrainEase</p><h2>Care that starts with you.</h2></div>
  <div class="cards c4" style="margin-top:32px">
    <div class="card reveal">{icon("dna")}<h3>Medication guided by biology</h3><p>Genetic testing and lab work inform medication choices, alongside your full clinical picture.</p></div>
    <div class="card reveal">{icon("leaf")}<h3>Lifestyle first</h3><p>Sleep, nutrition and daily habits are part of the plan from day one, before and during any medication change.</p></div>
    <div class="card reveal">{icon("one")}<h3>One clinician, start to finish</h3><p>The same person from your intro call to every follow-up. No hand-offs.</p></div>
    <div class="card reveal">{icon("ear")}<h3>Time to listen</h3><p>Visits leave room for your story, your questions and your priorities.</p></div>
  </div>
</div></section>

<section class="band" id="how"><div class="wrap">
  <div class="stack reveal"><p class="kicker">How it starts</p><h2>Three simple steps.</h2></div>
  <ol class="steps" style="margin-top:32px">
    <li class="reveal"><h3>A free 15-minute call</h3><p>Send a request or call us. Sariette calls you back to get to know you and answer your questions. No commitment.</p></li>
    <li class="reveal"><h3>A full psychiatric evaluation</h3><p>A comprehensive look at the biological, lifestyle and environmental factors behind what you're living with.</p></li>
    <li class="reveal"><h3>Your plan, then follow-ups</h3><p>A plan built with you, and the same clinician at every follow-up, in person or by telehealth.</p></li>
  </ol>
</div></section>

<section class="band sand"><div class="wrap grid2 rev">
  <div class="stack reveal"><p class="kicker">Meet Sariette</p><h2>Sariette Ngandjo, APRN, PMHNP-BC</h2>
    <p class="lead">Founder of BrainEase and its only provider. A board-certified psychiatric mental health nurse practitioner, practicing with full practice authority in Illinois since 2021.</p>
    <p>She blends evidence-based psychiatry with a functional, integrative lens, and sees children, teens and adults in English and French.</p>
    <a class="btn ghost" href="/about.html">About Sariette</a></div>
  <div class="reveal" style="max-width:460px;width:100%;justify-self:center">{pic("sariette-chair", "Sariette Ngandjo in her office", pos="50% 22%").replace('class="photo"', 'class="photo" style="aspect-ratio:4/5"')}</div>
</div></section>

<section class="band"><div class="wrap">
  <div class="stack reveal"><p class="kicker">Services</p><h2>What we offer.</h2></div>
  <div class="cards c4" style="margin-top:32px">
    <a class="card reveal" href="/services.html#evaluation" style="text-decoration:none;color:inherit">{icon("chat")}<h3>Psychiatric evaluation</h3><p>A comprehensive evaluation, not just a checklist.</p></a>
    <a class="card reveal" href="/services.html#medication" style="text-decoration:none;color:inherit">{icon("pill")}<h3>Medication management</h3><p>Individualized prescribing informed by genetics and labs.</p></a>
    <a class="card reveal" href="/services.html#lifestyle" style="text-decoration:none;color:inherit">{icon("leaf")}<h3>Lifestyle coaching</h3><p>Nutrition, sleep and daily habits, woven into your plan.</p></a>
    <a class="card reveal" href="/genetic-testing.html" style="text-decoration:none;color:inherit">{icon("dna")}<h3>Genetic testing</h3><p>Pharmacogenomic testing to help guide medication choices.</p></a>
  </div>
</div></section>

<section class="band deep"><div class="wrap grid2">
  <div class="stack reveal"><p class="kicker">Take a Seat, the series</p><h2>Meet Eze and Braïna.</h2>
    <p class="lead">Eze is the little figure sitting on our E. Braïna is the wise tortoise who already lives in our waiting room. Together, they tell short stories about everyday life with other people.</p>
    <p>Short videos about boundaries, phones at the table, winter days and more. Never a diagnosis, never medical advice.</p>
    <a class="btn ghost" href="/videos.html" style="color:#f3efe6">Watch the series</a></div>
  <div style="--ez:#cfe7b4;max-width:460px;width:100%;justify-self:center">{scene("duo")}</div>
</div></section>

<section class="band"><div class="wrap grid2">
  <div class="stack reveal"><p class="kicker">Practical details</p><h2>Two ways to see us.</h2>
    <dl class="info" style="margin:0">
      <div><dt>In person</dt><span>Thursdays at <span data-cfg="address">440 Quadrangle Dr., Suite I, Bolingbrook, IL 60440</span></span></div>
      <div><dt>Telehealth</dt><span>Anywhere in Illinois, Monday to Friday</span></div>
      <div><dt>Hours</dt><span data-cfg="hours">Monday to Friday, 9 am to 5 pm</span></div>
      <div><dt>Languages</dt><span>English and French</span></div>
      <div><dt>Insurance</dt><span><ul class="list" data-cfg="insurance" style="margin-top:4px"><li>BCBSIL</li><li>Aetna</li><li>UnitedHealthcare / Optum</li><li>Blue Cross Community Health Plans (BCCHP)</li></ul></span></div>
    </dl></div>
  <div class="reveal">{pic("waiting-room", "The BrainEase waiting room, with Braïna's terrarium", w=1400, h=788, pos="50% 50%").replace('class="photo"', 'class="photo" style="aspect-ratio:4/3"')}</div>
</div></section>
{cta_band()}''')

# ---------- ABOUT ----------
PAGES['/about.html'] = ('about.html', 'About Sariette Ngandjo, APRN, PMHNP-BC | BrainEase',
 'Sariette Ngandjo is a board-certified psychiatric mental health nurse practitioner and the founder of BrainEase in Bolingbrook, Illinois.',
phead('About Sariette', 'Sariette Ngandjo, APRN, PMHNP-BC', 'Founder of BrainEase and its only provider. The same clinician, from your first call to every follow-up.') + f'''
<section class="band" style="padding-top:0"><div class="wrap grid2">
  <div class="reveal" style="max-width:480px;width:100%">{pic("sariette-sofa-art", "Sariette Ngandjo on the sofa in her office", pos="50% 62%").replace('class="photo"', 'class="photo" style="aspect-ratio:4/5"')}</div>
  <div class="stack prose reveal">
    <p>Sariette is a board-certified psychiatric mental health nurse practitioner. She has practiced with full practice authority in Illinois since 2021 and founded BrainEase to offer the kind of care she believes in: careful, personal and grounded in evidence.</p>
    <p>Her approach is functional and integrative. Before anything else, she wants to understand the whole person: biology, lifestyle, environment and what matters most to you. Medication decisions draw on genetic testing and lab work when they are useful, and sleep, nutrition and daily habits are part of the plan from the start.</p>
    <p>BrainEase is intentionally small. Sariette is its only provider, so the person you meet on your first call is the person you see at every visit.</p>
    <p>She sees children from age 8, teens and adults up to 65, in English and French, in person on Thursdays in Bolingbrook and by telehealth across Illinois.</p>
  </div>
</div></section>
<section class="band sand"><div class="wrap">
  <div class="cards c3">
    <div class="card reveal">{icon("ear")}<h3>Listening first</h3><p>Visits leave room for your story and your questions.</p></div>
    <div class="card reveal">{icon("dna")}<h3>Evidence-based</h3><p>Decisions informed by your clinical picture, labs and, when useful, genetic testing.</p></div>
    <div class="card reveal">{icon("one")}<h3>Continuity</h3><p>One clinician who knows you and follows you over time.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap grid2 rev">
  <div class="stack reveal"><h2>A space made to feel calm.</h2><p class="lead">Green velvet, soft light, plants, books and games for younger patients. And Braïna the tortoise in the waiting room.</p></div>
  <div class="reveal">{pic("office", "Sariette's office: green sofa, orange throw, plants and a play corner", w=1400, h=788, pos="50% 50%").replace('class="photo"', 'class="photo" style="aspect-ratio:16/10"')}</div>
</div></section>
{cta_band()}''')

# ---------- SERVICES ----------
PAGES['/services.html'] = ('services.html', 'Services | Psychiatric evaluation, medication management, lifestyle coaching | BrainEase',
 'Comprehensive psychiatric evaluations, medication management informed by genetics and labs, lifestyle coaching and pharmacogenomic testing, in Bolingbrook and by telehealth across Illinois.',
phead('Services', 'Services built around the whole person.', 'Four services that work together, with the same clinician throughout.') + f'''
<section class="band" style="padding-top:0"><div class="wrap cards">
  <article class="card reveal" id="evaluation">{icon("chat")}<h3>Psychiatric evaluation</h3><p>A comprehensive evaluation exploring the biological, lifestyle and environmental factors behind your symptoms, not just a checklist. It is the first clinical visit after your free intro call.</p></article>
  <article class="card reveal" id="medication">{icon("pill")}<h3>Medication management</h3><p>Precise, individualized prescribing informed by your full clinical picture, lab work and, when useful, genetic testing. Follow-ups adjust the plan with you over time.</p></article>
  <article class="card reveal" id="lifestyle">{icon("leaf")}<h3>Lifestyle coaching</h3><p>Support with nutrition, sleep and daily habits, woven directly into your treatment plan, before and during any medication change.</p></article>
  <article class="card reveal" id="genetic">{icon("dna")}<h3>Genetic testing</h3><p>Pharmacogenomic testing that looks at how your body may process certain medications, to help guide choices. <a href="/genetic-testing.html">How it works</a></p></article>
</div></section>
<section class="band sand"><div class="wrap grid2">
  <div class="stack reveal"><h2>Who we see, and how.</h2>
    <ul class="list"><li>Children, teens and adults, ages 8 to 65</li><li>In person in Bolingbrook, on Thursdays</li><li>Telehealth anywhere in Illinois, Monday to Friday</li><li>In English and French</li></ul></div>
  <div class="stack reveal"><h2 style="font-size:clamp(26px,3vw,36px)">What we don't offer</h2>
    <ul class="list no"><li>Couples or marriage therapy</li><li>Long-term psychotherapy on its own</li><li>Requests outside psychiatric care</li><li>Emergency or crisis care: call or text 988, or call 911</li></ul>
    <p class="small">Not sure? The free intro call is the place to ask.</p></div>
</div></section>
<section class="band"><div class="wrap stack reveal"><h2>Insurance</h2><p class="lead">We accept:</p><ul class="list" data-cfg="insurance"><li>BCBSIL</li><li>Aetna</li><li>UnitedHealthcare / Optum</li><li>Blue Cross Community Health Plans (BCCHP)</li></ul><p class="small">Another plan, or no insurance? Ask us about your options.</p></div></section>
{cta_band()}''')

# ---------- GENETIC TESTING ----------
PAGES['/genetic-testing.html'] = ('genetic-testing.html', 'Pharmacogenomic (genetic) testing for medication | BrainEase',
 'How BrainEase uses pharmacogenomic testing to help guide medication choices, explained simply: what it is, how it works and what it can and cannot tell you.',
phead('Genetic Testing', 'Genetic testing, explained simply.', 'Pharmacogenomic testing looks at how your genes may affect the way your body processes certain medications. At BrainEase, it is one tool among others to help guide choices.') + f'''
<section class="band" style="padding-top:0"><div class="wrap">
  <ol class="steps">
    <li class="reveal"><h3>A simple sample</h3><p>The test usually needs only a simple sample, such as a cheek swab. Sariette tells you if and when it makes sense for you.</p></li>
    <li class="reveal"><h3>The lab looks at your genes</h3><p>A laboratory studies genes involved in how the body breaks down and responds to certain medications.</p></li>
    <li class="reveal"><h3>Choices, made together</h3><p>Sariette reads the results alongside your history, labs and goals, and talks the options through with you.</p></li>
  </ol>
</div></section>
<section class="band sand"><div class="wrap grid2">
  <div class="stack reveal"><h2>What it can, and can't, tell you.</h2>
    <p class="lead">Genetic testing can help inform medication choices. It cannot predict on its own how you will feel, and it never replaces a full evaluation.</p></div>
  <div class="faq reveal">
    <details><summary>Will the test tell me which medication will work?</summary><div><p>No single test can guarantee that. Results add information about how your body may process certain medications, which Sariette weighs with everything else she knows about you.</p></div></details>
    <details><summary>Do I need genetic testing?</summary><div><p>Not everyone does. It is discussed during your evaluation, and the decision is made together.</p></div></details>
    <details><summary>Is it covered by insurance?</summary><div><p>Coverage varies by plan and situation. We will help you check before any test is ordered.</p></div></details>
    <details><summary>Who sees my results?</summary><div><p>Your results are part of your medical record and are protected like the rest of your health information.</p></div></details>
  </div>
</div></section>
{cta_band()}''')

# ---------- CONDITIONS ----------
COND = [('Anxiety disorders', 'Persistent worry, tension or fear that gets in the way of daily life, school, work or sleep.'),
        ('ADHD', 'Attention, focus, organization and impulsivity, in children, teens and adults. Evaluations are available in person and by telehealth.'),
        ('Depression and mood disorders', 'Low mood, loss of interest, changes in energy or sleep, and other shifts in mood that last.'),
        ('Trauma', 'The lasting effects that difficult or frightening experiences can have on daily life.')]
PAGES['/conditions.html'] = ('conditions.html', 'Conditions we treat | Anxiety, ADHD, depression, trauma | BrainEase',
 'BrainEase provides evaluation and treatment for anxiety disorders, ADHD, depression and mood disorders, and trauma, for ages 8 to 65 in Illinois.',
phead('Conditions', 'Conditions we treat.', 'BrainEase provides evaluation and treatment for the conditions below, for children, teens and adults. These descriptions are general information, not a diagnosis.') +
'<section class="band" style="padding-top:0"><div class="wrap cards">' + ''.join(f'<article class="card reveal"><h3>{t}</h3><p>{d}</p></article>' for t, d in COND) +
'<article class="card reveal"><h3>And more</h3><p>Other concerns can be discussed during the free intro call, to see whether BrainEase is the right place.</p></article>'
'<article class="card reveal" style="background:var(--sand)"><h3>Not offered here</h3><p>Couples or marriage therapy, long-term psychotherapy on its own, and emergency care. In a crisis, call or text 988 or call 911.</p></article>'
'</div></section>' + cta_band())

# ---------- FOR PROFESSIONALS ----------
PAGES['/for-professionals.html'] = ('for-professionals.html', 'Referrals for healthcare professionals | BrainEase',
 'Refer patients to BrainEase: call or email with the patient details. We contact the patient within 1 to 2 business days and confirm once they are scheduled.',
phead('For Professionals', 'Now accepting referrals.', 'Fast, warm handoffs for your patients, and the same clinician from intake to follow-up.') + f'''
<section class="band" style="padding-top:0"><div class="wrap">
  <ol class="steps">
    <li class="reveal"><h3>Send your referral</h3><p>Call <a data-href="phoneHref" href="tel:+13313307228" data-cfg="phone">331-330-7228</a> or email <a href="mailto:wecare@braineasehealth.org" data-cfg="email">wecare@braineasehealth.org</a> with the patient's name, date of birth, reason for referral and insurance.</p></li>
    <li class="reveal"><h3>We reach out</h3><p>Our office contacts the patient within 1 to 2 business days to schedule and send intake paperwork.</p></li>
    <li class="reveal"><h3>We confirm</h3><p>You receive a brief confirmation once the patient is scheduled.</p></li>
  </ol>
</div></section>
<section class="band sand"><div class="wrap grid2">
  <div class="stack reveal"><h2>Who we see</h2><ul class="list"><li>Patients aged 8 to 65</li><li>Anxiety disorders, ADHD, depression and mood disorders, trauma</li><li>In person in Bolingbrook on Thursdays, telehealth across Illinois</li><li>English and French</li></ul></div>
  <div class="stack reveal"><h2>Insurance</h2><ul class="list" data-cfg="insurance"><li>BCBSIL</li><li>Aetna</li><li>UnitedHealthcare / Optum</li><li>Blue Cross Community Health Plans (BCCHP)</li></ul></div>
</div></section>''')

# ---------- VIDEOS ----------
EPS = [('The Kind No', 'Setting limits without breaking ties'), ('Heavy Rooms', 'When a relationship starts to weigh on you'),
       ('Wait, Did That Happen?', 'When someone makes you doubt what you saw'), ('Shorter Days', 'Keeping a gentle rhythm in winter'),
       ('Phones at the Table', 'When screens wear relationships down'), ('Asking Is Strong', 'Asking for help, at work and at home'),
       ('Homework Wars', 'Parents, kids and evening homework'), ('Back to Monday', 'Getting going again after a break')]
PAGES['/videos.html'] = ('videos.html', 'Take a Seat, short videos with Eze and Braïna | BrainEase',
 'Take a Seat: short videos about everyday life with other people, told by Eze and Braïna the tortoise. Never a diagnosis, never medical advice.',
phead('Videos', 'Take a Seat, the series.', 'Short videos about the small things of life with other people. Eze sets the scene, and Braïna the tortoise closes each story with a word of wisdom.') + f'''
<section class="band" style="padding-top:0"><div class="wrap">
  <div class="grid2" style="margin-bottom:40px"><div class="stack reveal"><h2>Meet the duo.</h2><p class="lead"><b>Eze</b> (say it “easy”) is the little figure sitting on our E: curious, warm, always ready to welcome you. <b>Braïna</b> is the wise tortoise: slow, clear-sighted, inspired by Kulu, the tortoise of Cameroonian tales. Braïna and Eze: Brain and Ease.</p></div><div class="reveal" style="max-width:440px;width:100%;justify-self:center">{scene("duo")}</div></div>
  <div class="stack reveal"><p class="kicker">Season 1 · premiering soon</p></div>
  <div class="eps" style="margin-top:18px">''' + ''.join(
    f'<article class="ep reveal"><div class="th">{scene("ep")}<span>Ep. {i + 1}</span></div><div class="bd"><h3>{t}</h3><p>{d}</p></div></article>' for i, (t, d) in enumerate(EPS)) + '''</div>
  <p class="small" style="margin-top:24px">Episodes will also be on YouTube, Instagram, TikTok and Facebook. These videos share everyday reflections; they are not medical advice.</p>
</div></section>''' + cta_band())

# ---------- FAQ ----------
FAQ = [
 ('How do I get started?', 'Send a request through Eze or the contact page, or call or text 331-330-7228. Everything starts with a free 15-minute intro call by phone.'),
 ('What is the free intro call?', 'A brief 15-minute phone call to meet Sariette, ask your questions and see if BrainEase is the right fit. It is not a psychiatric evaluation.'),
 ('Can I book online?', 'Not directly. You can send a request in under a minute through Eze or the contact form, with your preferred days and time. Sariette aims to get back to you within one business day.'),
 ('Which insurance plans do you accept?', 'BCBSIL, Aetna, UnitedHealthcare / Optum and Blue Cross Community Health Plans (BCCHP). If you have another plan or no insurance, ask us about your options.'),
 ('Do you offer telehealth?', 'Yes, anywhere in Illinois, Monday to Friday. You need to be in Illinois at the time of your visit.'),
 ('When can I come in person?', 'In-person visits are on Thursdays at 440 Quadrangle Dr., Suite I, Bolingbrook, IL 60440.'),
 ('Who do you see?', 'Children, teens and adults from 8 to 65 years old.'),
 ('Do you see patients in French?', 'Yes. Sariette sees patients in English and French.'),
 ('How do I reschedule or change an appointment?', 'Email wecare@braineasehealth.org or call or text 331-330-7228.'),
 ("What don't you offer?", 'Couples or marriage therapy, long-term psychotherapy on its own, requests outside psychiatric care, and emergency care.'),
 ('What if I am in crisis?', 'BrainEase is not an emergency service. Call or text 988 (Suicide & Crisis Lifeline) or call 911 right away.'),
]
FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
PAGES['/faq.html'] = ('faq.html', 'Frequently asked questions | BrainEase',
 'Insurance, telehealth across Illinois, in-person visits on Thursdays, the free 15-minute intro call, languages and more.',
phead('FAQ', 'Questions, answered.', 'Can\'t find yours? Ask Eze, or call or text 331-330-7228.') +
'<section class="band" style="padding-top:0"><div class="wrap"><div class="faq" style="max-width:820px">' +
''.join(f'<details class="reveal"><summary>{html.escape(q)}</summary><div><p>{html.escape(a)}</p></div></details>' for q, a in FAQ) +
'</div></div></section>' + cta_band(), FAQ_LD)

# ---------- CONTACT ----------
PAGES['/contact.html'] = ('contact.html', 'Contact and appointment requests | BrainEase',
 'Request your free 15-minute intro call or an appointment in under a minute. Call or text 331-330-7228, email wecare@braineasehealth.org.',
phead('Contact', 'Take a seat. Let\'s talk.', 'Send a request in under a minute. Sariette aims to get back to you within one business day.') + f'''
<section class="band" style="padding-top:0" id="request"><div class="wrap grid2" style="align-items:start">
  <div class="form-card reveal" data-booking-page></div>
  <div class="stack reveal">
    <dl class="info" style="margin:0">
      <div><dt>Call or text</dt><span><a data-href="phoneHref" href="tel:+13313307228" data-cfg="phone">331-330-7228</a></span></div>
      <div><dt>Email</dt><span><a href="mailto:wecare@braineasehealth.org" data-cfg="email">wecare@braineasehealth.org</a></span></div>
      <div><dt>Hours</dt><span data-cfg="hours">Monday to Friday, 9 am to 5 pm</span></div>
      <div><dt>In person</dt><span>Thursdays · <a data-href="mapsUrl" href="#" target="_blank" rel="noopener" data-cfg="address">440 Quadrangle Dr., Suite I, Bolingbrook, IL 60440</a></span></div>
      <div><dt>Telehealth</dt><span>Anywhere in Illinois</span></div>
    </dl>
    <p class="note">For your privacy, please don't include health information in your request. Sariette will talk with you directly.</p>
    <p class="note" style="background:#fde7dc;color:#5a1d05"><b>In crisis?</b> Call or text 988 or call 911. BrainEase is not an emergency service.</p>
    <div style="max-width:340px">{scene("bench")}</div>
  </div>
</div></section>''')

# ---------- BLOG ----------
POSTS = [
 ('what-to-expect', 'What to expect when you reach out to BrainEase', 'First steps', 'From your first message to your first follow-up, here is how getting started works, step by step.',
  '''<p>Reaching out about your mental health, or your child's, can feel like a big step. Here is exactly what happens when you contact BrainEase, so there are no surprises.</p>
<h2 id="s1">1. You send a request or call</h2>
<p>You can send a request in under a minute through Eze, our assistant on the website, or through the contact page. You choose the days and the time of day that suit you. You can also call or text 331-330-7228, or email wecare@braineasehealth.org.</p>
<p>Please don't include health details in your request: Sariette will talk with you directly. She aims to get back to you within one business day.</p>
<h2 id="s2">2. A free 15-minute intro call</h2>
<p>Your first conversation is a short, free phone call. It is a chance to meet Sariette, ask your questions, talk about insurance and logistics, and see whether BrainEase is the right fit. It is not a psychiatric evaluation, and there is no commitment.</p>
<h2 id="s3">3. Your psychiatric evaluation</h2>
<p>If you decide to move forward, the next step is a comprehensive psychiatric evaluation. Sariette takes the time to understand the whole picture: your history, your daily life, sleep, nutrition, stress and what matters most to you. When useful, lab work or genetic testing may be discussed.</p>
<div class="callout"><b>Good to know.</b> Visits happen in person on Thursdays in Bolingbrook, or by telehealth anywhere in Illinois, in English or French.</div>
<h2 id="s4">4. A plan, and follow-ups with the same clinician</h2>
<p>Together, you build a plan. Follow-up visits adjust it over time. Because Sariette is the only provider at BrainEase, you see the same person every time.</p>
<h2 id="s5">Insurance</h2>
<p>BrainEase accepts BCBSIL, Aetna, UnitedHealthcare / Optum and Blue Cross Community Health Plans (BCCHP). If you have another plan or no insurance, ask during your intro call.</p>'''),
 ('in-person-or-telehealth', 'In person or telehealth: how to choose', 'Practical', 'Both are available at BrainEase. A few practical questions help you pick what fits your week.',
  '''<p>At BrainEase, you can see Sariette in person in Bolingbrook on Thursdays, or by telehealth anywhere in Illinois, Monday to Friday. Many people use both. Here are a few practical questions to help you choose.</p>
<h2 id="s1">Where will you be?</h2>
<p>Telehealth visits are available anywhere in Illinois. You need to be physically in Illinois at the time of the visit, even if you live elsewhere.</p>
<h2 id="s2">Do you have a quiet, private space?</h2>
<p>A telehealth visit works best in a room where you can talk freely without being overheard: a closed room, a parked car, headphones. If that's hard at home, an in-person Thursday visit may be easier.</p>
<h2 id="s3">What does your schedule look like?</h2>
<p>Telehealth saves travel time and fits more easily into a workday or a school day. In-person visits are only on Thursdays, so they suit people who can plan around that day.</p>
<h2 id="s4">Is the visit for a child or teen?</h2>
<p>Both options work for younger patients. Some children feel more at ease in the office, with its games and books; others prefer the comfort of home. You can ask Sariette what she recommends during the free intro call.</p>
<div class="callout"><b>Before a telehealth visit:</b> charge your device, test your camera and microphone, find your quiet spot and keep your insurance card nearby.</div>
<h2 id="s5">You can change your mind</h2>
<p>Choosing one format doesn't lock you in. Many patients switch between in person and telehealth depending on the week.</p>'''),
]
def post_card(slug, title, cat, ex):
    return f'<a class="post reveal" href="/blog/{slug}.html"><div class="cov">{scene("cover")}</div><div class="bd"><span class="kicker">{cat}</span><h3>{title}</h3><p>{ex}</p></div></a>'
PAGES['/blog/'] = ('blog/index.html', 'Blog | Practical guides from BrainEase',
 'Short, practical articles from BrainEase: getting started, telehealth in Illinois, genetic testing explained, and more.',
phead('Blog', 'Practical, short and clear.', 'Answers to the questions patients and families ask us most, reviewed by Sariette.') +
'<section class="band" style="padding-top:0"><div class="wrap"><div class="posts">' + ''.join(post_card(*p[:4]) for p in POSTS) + '</div></div></section>' + cta_band())
for slug, title, cat, ex, body in POSTS:
    toc = ''.join(f'<li><a href="#s{i}">{h}</a></li>' for i, h in enumerate([x.split('</h2>')[0].split('>')[-1] for x in body.split('<h2 ')[1:]], 1))
    art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "author": {"@type": "Person", "name": "Sariette Ngandjo, APRN, PMHNP-BC"},
           "publisher": {"@type": "Organization", "name": "BrainEase PLLC"}, "mainEntityOfPage": f"{SITE}/blog/{slug}.html"}
    PAGES[f'/blog/{slug}.html'] = (f'blog/{slug}.html', f'{title} | BrainEase', ex,
      f'''<section class="phead"><div class="wrap stack"><p class="crumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {cat}</p><h1 style="max-width:16em">{title}</h1><p class="lead">{ex}</p><p class="small">By Sariette Ngandjo, APRN, PMHNP-BC · 4 min read</p></div></section>
<section class="band" style="padding-top:0"><div class="wrap artgrid">
  <article class="prose">{body}
  <div class="callout" style="background:var(--deep);color:#f3efe6"><b>Take a seat.</b> Your first conversation is a free 15-minute call. <a href="/contact.html#request" data-eze="book" style="color:#f2b66b">Request it in under a minute →</a></div></article>
  <aside class="toc" style="position:sticky;top:96px"><b>In this article</b><ol>{toc}</ol></aside>
</div></section>''', art)

# ---------- LEGAL ----------
PAGES['/privacy.html'] = ('privacy.html', 'Privacy policy | BrainEase', 'How BrainEase handles the information you share through this website.',
phead('Privacy', 'Privacy policy.', 'How we handle what you share through this website. Last updated November 2026.') + '''
<section class="band" style="padding-top:0"><div class="wrap"><div class="prose">
<h2>What we collect</h2><p>When you send a request through Eze or the contact form, we collect only what you enter: your name, phone number and/or email, whether you are a new or current patient, your preferred days, time and language. We ask you not to include health information.</p>
<p>When you use the Eze chat, your questions are used only to answer them. Eze does not keep conversations after you leave the site.</p>
<h2>How we use it</h2><p>Only to respond to your request and schedule your visit. We do not sell or rent your information.</p>
<h2>Newsletter</h2><p>If you sign up for our newsletter, we use your email address to send it. Every email includes a link to unsubscribe.</p>
<h2>Cookies and analytics</h2><p>This site uses only what it needs to work and, if enabled, privacy-friendly visit statistics that do not identify you.</p>
<h2>Patients</h2><p>If you become a patient, your health information is protected under HIPAA. Our Notice of Privacy Practices is provided at intake and is available on request.</p>
<h2>Contact</h2><p>Questions about privacy: wecare@braineasehealth.org or 331-330-7228.</p>
</div></div></section>''')
PAGES['/terms.html'] = ('terms.html', 'Terms of use | BrainEase', 'Terms of use for the BrainEase website.',
phead('Terms', 'Terms of use.', 'Last updated November 2026.') + '''
<section class="band" style="padding-top:0"><div class="wrap"><div class="prose">
<h2>General information only</h2><p>The content of this website, including the blog, the Take a Seat videos and the Eze assistant, is general information. It is not medical advice and does not create a patient-provider relationship.</p>
<h2>Not for emergencies</h2><p>BrainEase is not an emergency service. If you are in crisis, call or text 988 or call 911.</p>
<h2>Requests are not appointments</h2><p>A request sent through this website is not a confirmed appointment until BrainEase confirms it with you.</p>
<h2>Content</h2><p>The BrainEase name, logo, Eze and Braïna characters, and site content belong to BrainEase PLLC.</p>
</div></div></section>''')
PAGES['/404.html'] = ('404.html', 'Page not found | BrainEase', 'This page could not be found.',
f'''<section class="band"><div class="wrap grid2"><div class="stack"><h1>Oops, Eze slipped off the E.</h1><p class="lead">This page doesn't exist, or it has moved. Let's get you back on your seat.</p><div class="btns"><a class="btn" href="/">Back to home</a><a class="btn ghost" href="/contact.html">Contact us</a></div></div><div style="max-width:420px;width:100%;justify-self:center">{scene("lost")}</div></div></section>''')

# ---------- write ----------
def main():
    for path, (fname, title, desc, body, *ld) in PAGES.items():
        out = os.path.join(DIST, fname)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(page(path, title, desc, body, ld[0] if ld else None))
    urls = [p for p in PAGES if p != '/404.html']
    today = date.today().isoformat()
    open(os.path.join(DIST, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    open(os.path.join(DIST, 'CNAME'), 'w').write('braineasehealth.org\n')
    open(os.path.join(DIST, 'assets', 'favicon.svg'), 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><rect width="120" height="120" rx="28" fill="#e1891f"/>'
        f'<g transform="translate(52 84) scale(1.25)">{fig("sit", w=3.6, col="#fffaf2")}</g></svg>')
    print(len(PAGES), 'pages')
main()

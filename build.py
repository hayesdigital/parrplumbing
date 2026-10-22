"""Builds the Parr Plumbing static site into ./public. Run: python3 build.py"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent / "public"
SITE = "https://parrplumbing.com"
BIZ = "Parr Plumbing"
PHONE = "(580) 304-4967"
PHONE_TEL = "+15803044967"
SMS = "sms:+15803044967"
TOWNS = ["Ponca City", "McCord", "Newkirk", "Tonkawa"]
AREA = "Ponca City, McCord, Newkirk and Tonkawa"
HOURS = "Monday to Saturday, 9 AM to 6 PM"
LICENSE = "00141707"
YEAR = 2026

FONTS = ('<link rel="preload" href="/fonts/archivo-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>'
         '<link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>')

PHONE_ICO = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'

LOGO = ('<svg viewBox="0 0 300 80" role="img" aria-label="Parr Plumbing logo">'
        '<rect x="4" y="6" width="292" height="68" fill="#fff" stroke="#111" stroke-width="6"/>'
        '<rect x="16" y="17" width="112" height="46" fill="#111"/>'
        '<text x="72" y="49.5" text-anchor="middle" font-family="Archivo,Arial,sans-serif" font-weight="500" font-size="27" letter-spacing="3.5" fill="#e3c16f">PARR</text>'
        '<text x="209" y="50" text-anchor="middle" font-family="Archivo,Arial Black,sans-serif" font-weight="800" font-size="26" letter-spacing=".5" fill="#111">PLUMBING</text>'
        '</svg>')

# ---------------------------------------------------------------- schema
BUSINESS = {
    "@context": "https://schema.org",
    "@type": "Plumber",
    "@id": SITE + "/#business",
    "name": BIZ,
    "alternateName": "Greg Parr Plumbing",
    "url": SITE + "/",
    "telephone": PHONE_TEL,
    "description": "Licensed Ponca City, Oklahoma plumber specializing in water heater repair and replacement, plus leak repair, garbage disposals, water filtration systems and general residential and commercial plumbing.",
    "image": SITE + "/img/plumber-checking-water-heater-ponca-city-ok.webp",
    "logo": SITE + "/logo.png",
    "address": {"@type": "PostalAddress", "addressLocality": "Ponca City", "addressRegion": "OK", "addressCountry": "US"},
    "areaServed": [{"@type": "City", "name": t + ", OK"} for t in ["Ponca City", "McCord", "Newkirk", "Tonkawa"]],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "18:00"}],
    "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_TEL, "contactType": "customer service", "areaServed": "US-OK", "availableLanguage": "English"},
    "founder": {"@type": "Person", "@id": SITE + "/#greg", "name": "Greg Parr", "jobTitle": "Owner and Licensed Plumbing Contractor", "url": SITE + "/about/"},
    "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                      "name": "Oklahoma Plumbing Contractor License #" + LICENSE,
                      "recognizedBy": {"@type": "Organization", "name": "Oklahoma Construction Industries Board"}},
    "knowsAbout": ["Water heater repair", "Water heater replacement", "Tankless water heaters", "Leak repair", "Garbage disposal repair", "Reverse osmosis water filtration", "Residential plumbing", "Commercial plumbing"],
}

def service_schema(name, path, desc, stype):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": stype,
            "url": SITE + path, "description": desc,
            "provider": {"@id": SITE + "/#business"},
            "areaServed": [{"@type": "City", "name": t + ", OK"} for t in TOWNS]}

def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in items]}

def crumbs_schema(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}

# ---------------------------------------------------------------- layout
OG_DEFAULT = "/img/parr-plumbing-ponca-city-share.jpg"

def head(title, desc, path, schemas=(), og_image=OG_DEFAULT, robots=None):
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, separators=(",", ":"))}</script>' for s in [BUSINESS, *schemas])
    rb = f'<meta name="robots" content="{robots}">\n' if robots else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{rb}<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BIZ}"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{og_image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Parr Plumbing, licensed plumber in Ponca City, OK">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}{og_image}">
<meta name="theme-color" content="#12131f">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon-32x32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
{FONTS}
<link rel="stylesheet" href="/styles.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="container">
  <span class="lic">Licensed Oklahoma Plumbing Contractor #{LICENSE} &middot; Mon to Sat, 9 AM to 6 PM</span>
  <span>Call or text <a href="tel:{PHONE_TEL}">{PHONE}</a></span>
</div></div>
<header class="site-header"><div class="container">
  <a class="logo" href="/" aria-label="Parr Plumbing home">{LOGO}</a>
  <nav class="nav" aria-label="Main">
    <a href="/water-heater-repair-ponca-city-ok/">Water Heater Repair</a>
    <a href="/water-heater-replacement-ponca-city-ok/">Water Heater Replacement</a>
    <a href="/services/">All Services</a>
    <a href="/about/">About Greg</a>
    <a href="/contact/">Contact</a>
    <a class="btn" href="tel:{PHONE_TEL}">{PHONE_ICO}<span>{PHONE}</span></a>
  </nav>
</div></header>
<main id="main">
"""

FOOT = f"""</main>
<footer class="site-footer"><div class="container">
  <div class="cols">
    <div>
      <a class="logo" href="/" aria-label="Parr Plumbing home">{LOGO}</a>
      <p style="margin-top:14px;max-width:44ch">Water heater repair and replacement, leak repair, garbage disposals, water filtration and everyday plumbing for homes and businesses in Ponca City, McCord, Newkirk and Tonkawa, Oklahoma.</p>
      <p style="margin-top:10px">Oklahoma Plumbing Contractor License #{LICENSE}</p>
    </div>
    <div><h3>Services</h3><ul>
      <li><a href="/water-heater-repair-ponca-city-ok/">Water Heater Repair</a></li>
      <li><a href="/water-heater-replacement-ponca-city-ok/">Water Heater Replacement</a></li>
      <li><a href="/leak-repair-ponca-city-ok/">Leak Repair</a></li>
      <li><a href="/garbage-disposal-repair-ponca-city-ok/">Garbage Disposal Repair</a></li>
      <li><a href="/water-filtration-ponca-city-ok/">Water Filtration Systems</a></li>
      <li><a href="/services/">All Plumbing Services</a></li>
    </ul></div>
    <div><h3>Parr Plumbing</h3><ul>
      <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
      <li>Text: <a href="{SMS}">{PHONE}</a></li>
      <li>Mon to Sat: 9 AM to 6 PM<br>Sunday: Closed</li>
      <li>Serving {AREA}, OK</li>
      <li><a href="/about/">About Greg Parr</a></li>
      <li><a href="/contact/">Contact</a></li>
    </ul></div>
  </div>
  <div class="bottom"><span>&copy; {YEAR} Parr Plumbing. All rights reserved. &middot; <a href="/privacy/">Privacy Policy</a></span><span>Website by <a href="https://toddhayes.com/">Hayes Digital Marketing</a></span></div>
</div></footer>
<div class="callbar"><a class="btn" href="tel:{PHONE_TEL}">{PHONE_ICO} Call Now</a><a class="btn dark" href="{SMS}">Text Us</a></div>
</body>
</html>
"""

SMS_BODY = {
    "Water heater repair": "Hi Greg, I need help with water heater repair.",
    "Water heater replacement (tank or tankless)": "Hi Greg, I need a new water heater.",
    "Leak repair": "Hi Greg, I have a plumbing leak.",
    "Garbage disposal repair or replacement": "Hi Greg, my garbage disposal needs work.",
    "Water filtration / reverse osmosis system": "Hi Greg, I'm interested in a water filtration system.",
}

def sms_link(preselect=None):
    body = SMS_BODY.get(preselect, "Hi Greg, I need a plumber.")
    return SMS + "?&body=" + body.replace(" ", "%20").replace(",", "%2C").replace("'", "%27")

def form(heading="Call or text Greg", sub="No forms, no call center. Call or text and you'll reach Greg directly.", preselect=None):
    return f"""<div class="form-card contact-card" id="contact">
  <p class="h">{heading}</p>
  <p class="sub">{sub}</p>
  <a class="btn big" href="tel:{PHONE_TEL}">{PHONE_ICO} Call {PHONE}</a>
  <a class="btn dark big" href="{sms_link(preselect)}"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H8l-4 4V6a2 2 0 0 1 2-2z"/></svg> Text {PHONE}</a>
  <p class="tip">Texting? Send a quick note about the problem and a photo if you can. It helps Greg show up ready.</p>
  <div class="cc-grid">
    <div><b>Hours</b><span>Mon to Sat: 9 AM to 6 PM</span><span>Sunday: Closed</span></div>
    <div><b>Service area</b><span>Ponca City &middot; McCord</span><span>Newkirk &middot; Tonkawa</span></div>
  </div>
</div>"""

def img(name, alt, cls="photo", eager=False, w=1400, h=789):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="{cls}"><img src="/img/{name}-sm.webp" srcset="/img/{name}-sm.webp 720w, /img/{name}.webp 1400w" '
            f'sizes="(max-width:900px) 100vw, 560px" width="{w}" height="{h}" alt="{alt}" {load} decoding="async"></figure>')

def hero(eyebrow, h1, lead, bg, bullets, trail=None, form_kw=None):
    cr = ""
    if trail:
        cr = '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(
            f'<a href="{p}">{n}</a>' if i < len(trail) - 1 else n for i, (n, p) in enumerate(trail)) + "</nav>"
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""<section class="hero">
  <img class="hero-bg" src="/img/{bg}-sm.webp" srcset="/img/{bg}-sm.webp 720w, /img/{bg}.webp 1400w" sizes="100vw" alt="" fetchpriority="high">
  <div class="container hero-grid">
    <div>
      {cr}
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="hero-cta"><a class="btn" href="tel:{PHONE_TEL}">{PHONE_ICO} Call {PHONE}</a><a class="btn ghost" href="{SMS}">Text Us</a></div>
      <ul class="trust">{lis}</ul>
    </div>
    {form(**(form_kw or {}))}
  </div>
</section>"""

def faq_block(items, heading="Common questions"):
    d = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    return f'<section class="alt"><div class="container"><div class="section-head"><span class="eyebrow">FAQ</span><h2>{heading}</h2></div><div class="faq">{d}</div></div></section>'

def band(text):
    return f'<div class="band"><div class="container"><p>{text}</p><a class="btn dark" href="tel:{PHONE_TEL}">{PHONE_ICO} Call {PHONE}</a></div></div>'

def cta_final(heading, text):
    return f"""<section class="cta-final"><div class="container grid-2">
  <div><h2>{heading}</h2><p class="lead">{text}</p>
  <a class="big-phone" href="tel:{PHONE_TEL}">{PHONE}</a>
  <p style="color:#b9bccb">Tap to call. Licensed Oklahoma plumbing contractor #{LICENSE}.</p></div>
  <div>{form(heading="Call or text anytime", sub="Leave a voicemail or send a text after hours and Greg will get back to you during business hours.")}</div>
</div></section>"""

SERVICES = [
    ("/water-heater-repair-ponca-city-ok/", "Water Heater Repair", "plumber-repairing-water-heater-piping", "Plumber repairing the piping on top of a water heater",
     "No hot water, lukewarm showers or a tank making noise? We repair gas and electric water heaters of every make and model."),
    ("/water-heater-replacement-ponca-city-ok/", "Water Heater Replacement", "water-heater-replacement-parts-ponca-city", "New water heater fittings, hoses and tools laid out for an install",
     "When a repair isn't worth it, we swap in a new standard tank or tankless water heater, sized right for your home."),
    ("/leak-repair-ponca-city-ok/", "Leak Repair", "water-leak-on-floor-under-water-heater", "Water pooled on the floor from a plumbing leak",
     "Kitchens, bathrooms, water heaters and underground lines. We find the leak, fix it and help you stop the damage."),
    ("/garbage-disposal-repair-ponca-city-ok/", "Garbage Disposal Repair", "plumbing-repair-tools-and-fittings", "Pipe wrench, copper fittings and plumbing repair tools",
     "Jammed, humming, leaking or just dead? We repair or replace noisy and broken garbage disposals."),
    ("/water-filtration-ponca-city-ok/", "Water Filtration Systems", "clean-filtered-water-kitchen-faucet", "Clean water running from a kitchen faucet into a white sink",
     "Quality residential reverse osmosis systems, installed under your sink for better tasting drinking water."),
    ("/services/", "Everyday Plumbing", "plumbing-valves-and-fittings", "Assorted brass plumbing valves and fittings",
     "Faucets, fixtures, drains, sewer lines and commercial plumbing. If it carries water, give us a call."),
]

def service_cards(exclude=None, heading="How we can help", sub=None):
    cards = ""
    for p, n, im, alt, d in SERVICES:
        if p == exclude:
            continue
        cards += (f'<article class="card svc"><img src="/img/{im}-sm.webp" width="720" height="405" alt="{alt}" loading="lazy" decoding="async">'
                  f'<div class="in"><h3>{n}</h3><p>{d}</p><a class="more" href="{p}">{n} in Ponca City &rarr;</a></div></article>')
    s = f'<p class="lead">{sub}</p>' if sub else ""
    return f'<section><div class="container"><div class="section-head"><span class="eyebrow">Plumbing services</span><h2>{heading}</h2>{s}</div><div class="grid-3">{cards}</div></div></section>'

def write(path, html):
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)

# ================================================================ HOME
HOME_FAQ = [
    ("Do you fix water heaters or just replace them?",
     "Both, and we'd honestly rather fix it if a repair makes sense. Heating elements, thermostats, pressure relief valves and many leaks can be repaired. If the tank itself is rusting through or leaking from the body, replacement is the safer call, and we'll tell you why."),
    ("What areas do you serve?",
     "We serve homes and businesses in Ponca City, McCord (just across the bridge on Highway 60), Newkirk and Tonkawa. Somewhere close by and not sure if you're in range? Call or text <a href=\"tel:" + PHONE_TEL + "\">" + PHONE + "</a> and ask."),
    ("Are you licensed and insured?",
     "Yes. Parr Plumbing is a fully licensed and insured Oklahoma plumbing contractor, license #" + LICENSE + "."),
    ("Do you install tankless water heaters?",
     "Yes. We install both standard tank water heaters and tankless units, and we can talk through which one fits your home, your hot water use and your budget."),
    ("Do you work on commercial plumbing?",
     "Yes. Along with homes, we handle plumbing repairs and installs for businesses around Ponca City."),
    ("What's the fastest way to get help?",
     "Call or text <a href=\"tel:" + PHONE_TEL + "\">" + PHONE + "</a>. If you can't talk right now, a text works great. Tell us what's going on and send a photo if you can."),
    ("What are your hours?",
     "Monday through Saturday, 9 AM to 6 PM. We're closed Sunday. Texts and voicemails left after hours get answered the next business day."),
]

home = head("Plumber in Ponca City, OK | Water Heater Repair & Replacement | Parr Plumbing",
            "Licensed plumber in Ponca City, OK. Parr Plumbing specializes in fast water heater repair and replacement, plus leak repair, garbage disposals and water filtration. Call (580) 304-4967.",
            "/", [faq_schema(HOME_FAQ)])
home += hero("Your local water heater specialist",
             "Plumber in Ponca City, OK",
             "Cold shower this morning? Water where it shouldn't be? We get it... it throws your whole day off. Parr Plumbing fixes water heaters, leaks and everyday plumbing problems for Ponca City homes and businesses, and we'll tell you straight what it needs.",
             "plumber-checking-water-heater-ponca-city-ok",
             [f"Licensed &amp; insured Oklahoma plumbing contractor, #{LICENSE}",
              "Owned by Greg Parr, a lifetime Ponca City resident",
              f"Serving {AREA}",
              "Water heater repair and replacement is our specialty",
              "Tank and tankless, gas and electric, all makes and models"])
home += f"""<section><div class="container grid-2">
  <div>
    <span class="eyebrow">Water heaters are our specialty</span>
    <h2>No hot water? We can usually fix that fast.</h2>
    <p>Most plumbers do a little bit of everything. We do too, but water heaters are where we spend most of our days. That means we've already seen the noise your tank is making, the drip under the drain valve and the pilot light that won't stay lit.</p>
    <p>We repair heating elements, thermostats, pressure relief valves and leaks on every make and model. And when a repair just isn't worth your money, we'll replace it with an efficient new tank or a tankless unit.</p>
    <p style="margin-top:20px;display:flex;flex-wrap:wrap;gap:12px"><a class="btn dark" href="/water-heater-repair-ponca-city-ok/">Water heater repair</a><a class="btn" href="/water-heater-replacement-ponca-city-ok/">Water heater replacement</a></p>
  </div>
  {img("water-heater-repair-testing-elements-ponca-city", "Plumber testing a water heater with a multimeter during a repair")}
</div></section>"""
home += band("Real local plumber. Real Oklahoma license. No call center.")
home += service_cards(heading="Plumbing services in Ponca City", sub="From a dead water heater to a slow leak under the sink, here's what we take care of most.")
home += f"""<section class="alt"><div class="container grid-2">
  {img("plumber-inspecting-electric-water-heater", "Plumber writing notes while inspecting a water heater")}
  <div>
    <span class="eyebrow">Why Ponca City calls Parr</span>
    <h2>A plumber who lives here, too</h2>
    <p>Greg Parr has lived in Ponca City his whole life and has been a licensed plumbing contractor for over a decade. When you call, you're not reaching a national franchise or a dispatch center three states away. You're calling a local plumber who wants to do the job right, because this is his town.</p>
    <ul class="list">
      <li><b>Honest repair or replace advice.</b> If a simple part fixes it, that's what we'll recommend.</li>
      <li><b>Clear answers.</b> We explain what broke and what it'll take before we start.</li>
      <li><b>Homes and businesses.</b> Residential and commercial plumbing across Ponca City.</li>
      <li><b>Licensed and insured.</b> Oklahoma plumbing contractor license #{LICENSE}.</li>
    </ul>
    <p style="margin-top:20px"><a class="btn dark" href="/about/">Meet Greg</a></p>
  </div>
</div></section>"""
home += f"""<section><div class="container">
  <div class="section-head"><span class="eyebrow">How it works</span><h2>Getting help is simple</h2></div>
  <ol class="steps">
    <li><h3>Call or text</h3><p>Call or text <a href="tel:{PHONE_TEL}">{PHONE}</a>. Tell us what's happening, like no hot water, a leak or a jammed disposal.</p></li>
    <li><h3>We find the problem</h3><p>We'll diagnose it, explain what's wrong in plain English and give you your options before any work starts.</p></li>
    <li><h3>We fix it right</h3><p>We make the repair or install, test everything, clean up after ourselves and make sure you're happy before we leave.</p></li>
  </ol>
</div></section>"""
home += f"""<section class="alt"><div class="container grid-2 top">
  <div>
    <span class="eyebrow">Service area</span>
    <h2>Plumbing service in Ponca City and nearby towns</h2>
    <p>Parr Plumbing is a mobile plumbing service, so we come to you. No shop to drive to. We cover Ponca City plus a few close neighbors:</p>
    <ul class="list">
      <li><b>Ponca City</b> and all of town</li>
      <li><b>McCord</b>, just across the bridge on Highway 60</li>
      <li><b>Newkirk</b>, north of Ponca</li>
      <li><b>Tonkawa</b>, west of Ponca on Highway 60</li>
    </ul>
    <p style="margin-top:14px">Close by but not on the list? Call or text <a href="tel:{PHONE_TEL}">{PHONE}</a> and ask.</p>
  </div>
  <div class="card" style="border-top:6px solid var(--yellow)">
    <h3>Hours</h3>
    <ul class="list"><li>Monday to Saturday: 9 AM to 6 PM</li><li>Sunday: Closed</li></ul>
    <h3 style="margin-top:18px">How to reach us</h3>
    <ul class="list"><li>Call: <a href="tel:{PHONE_TEL}">{PHONE}</a></li><li>Text: <a href="{SMS}">{PHONE}</a></li></ul>
  </div>
</div></section>"""
home += faq_block(HOME_FAQ, "Questions Ponca City homeowners ask us")
home += cta_final("Need a plumber in Ponca City today?", "Whether it's a water heater that quit or a leak you can't track down, give us a call. We'll help you figure out what's going on.")
home += FOOT
write("/", home)

# ================================================================ SERVICE PAGE BUILDER
def service_page(path, title, desc, h1, eyebrow, lead, bg, bullets, body, faqs, stype, preselect, cta_h, cta_t, name):
    trail = [("Home", "/"), ("Services", "/services/"), (name, path)]
    html = head(title, desc, path, [service_schema(h1, path, desc, stype), faq_schema(faqs), crumbs_schema(trail)])
    html += hero(eyebrow, h1, lead, bg, bullets, trail=trail, form_kw={"preselect": preselect})
    html += body
    html += faq_block(faqs, f"{name} questions")
    html += service_cards(exclude=path, heading="Other ways we can help")
    html += cta_final(cta_h, cta_t)
    html += FOOT
    write(path, html)

# ---------------------------------------------------------------- WATER HEATER REPAIR
WHR_FAQ = [
    ("How much does water heater repair cost in Ponca City?",
     "It depends on what failed. Swapping a heating element or thermostat costs a lot less than replacing a gas control valve, and all of it costs less than a new water heater. We'll diagnose it first and tell you the price before we do the work."),
    ("Is it worth repairing an old water heater?",
     "Usually yes if the tank itself is sound and the problem is a part, like an element, thermostat or valve. If the tank is leaking from the body or rusting through, or it's well past 10 years old and needing repairs often, replacement is usually the better spend."),
    ("Why do I have hot water, but not much of it?",
     "On an electric water heater, that's often a failed lower heating element or thermostat. On a gas unit, it can be sediment buildup, a burner problem or a dip tube issue. These are common, fixable repairs."),
    ("Why is my water heater leaking from the top or bottom?",
     "Leaks at the top are often loose or corroded fittings, which can be repaired. A drip from the pressure relief valve can mean the valve or the pressure needs attention. Water coming from the tank body itself usually means the tank is failing and should be replaced."),
    ("Do you repair both gas and electric water heaters?",
     "Yes. We repair gas and electric tank water heaters on every make and model, and we work on tankless units too."),
    ("Should I turn off my water heater if it's leaking?",
     "If it's a steady leak, yes. Shut the cold water valve on top of the heater, then turn off the gas (set it to pilot or off) or flip the breaker for an electric unit. Then give us a call."),
]
WHR_BODY = f"""<section><div class="container grid-2 top">
  <div class="prose">
    <h2>Water heater trouble? Here's what's probably going on</h2>
    <p>Nobody plans for the water heater to quit. It just happens... usually on a cold morning, right before work. The good news is most water heater problems come down to a handful of parts, and many of them are a straightforward repair.</p>
    <p>Parr Plumbing has made water heaters our specialty here in Ponca City. We fix leaks and replace heating elements, thermostats and pressure valves on all makes and models, gas or electric.</p>
    <h3>Signs your water heater needs a repair</h3>
    <ul class="signs">
      <li><b>No hot water at all</b><span>Often a tripped element, bad thermostat or a pilot that won't stay lit.</span></li>
      <li><b>Hot water runs out fast</b><span>A failed lower element or heavy sediment in the tank.</span></li>
      <li><b>Popping or rumbling noises</b><span>Sediment baking on the bottom of the tank.</span></li>
      <li><b>Rusty or smelly water</b><span>Corrosion inside the tank or a worn out anode rod.</span></li>
      <li><b>Dripping relief valve</b><span>Too much pressure or temperature, or a failing valve.</span></li>
      <li><b>Water around the base</b><span>Could be a fitting or drain valve, or the tank itself.</span></li>
    </ul>
  </div>
  <div>{img("gas-water-heater-thermostat-repair", "Plumber adjusting the thermostat dial on a gas water heater", "photo tall", w=1400, h=1750)}</div>
</div></section>
<section class="alt"><div class="container grid-2 top">
  <div class="prose">
    <h2>The water heater repairs we make most</h2>
    <h3>Heating element replacement</h3>
    <p>Electric water heaters have one or two elements. When one burns out you get lukewarm water or none at all. We test them and replace the bad one, usually in a single visit.</p>
    <h3>Thermostat repair and replacement</h3>
    <p>If the water's too hot, too cold or all over the place, the thermostat is a likely suspect. We'll test it and replace it if it's failing.</p>
    <h3>Pressure relief valve replacement</h3>
    <p>The temperature and pressure relief valve is a safety part. If it's leaking or not working, it needs attention right away, and it's a quick fix.</p>
    <h3>Leak repair</h3>
    <p>Leaks at the fittings, supply lines or drain valve can usually be repaired. We'll find exactly where the water's coming from first.</p>
  </div>
  <div class="prose">
    <h2>Repair or replace? We'll give you the honest answer</h2>
    <p>Here's a simple rule of thumb we share with folks all the time. If the tank is solid and a part failed, repair it. If the tank is leaking from the body, or it's getting up there in years and the repairs keep stacking up, it's time to think about a new one.</p>
    <div class="table-wrap"><table class="compare">
      <tr><th>Usually a repair</th><th>Usually time to replace</th></tr>
      <tr><td>Burned out heating element</td><td>Water leaking from the tank body</td></tr>
      <tr><td>Bad thermostat</td><td>Rust coming through the tank</td></tr>
      <tr><td>Leaking relief valve or fitting</td><td>Tank well past 10 years and failing</td></tr>
      <tr><td>Pilot or control problem</td><td>Repairs costing close to a new unit</td></tr>
    </table></div>
    <div class="callout"><p>If replacement makes more sense, we can handle that too. See our <a href="/water-heater-replacement-ponca-city-ok/">water heater replacement</a> page for standard tank and tankless options.</p></div>
  </div>
</div></section>
{band("Water heater acting up? Call the Ponca City water heater specialist.")}
<section><div class="container grid-2">
  {img("plumber-repairing-water-heater-piping", "Plumber working on the piping and connections of a home water heater")}
  <div class="prose">
    <h2>What to expect when you call</h2>
    <p>Call <a href="tel:{PHONE_TEL}">{PHONE}</a> and tell us what's happening. Is it gas or electric? How old is it? Any water on the floor? That helps us show up ready.</p>
    <p>Once we're there, we'll diagnose the problem, explain it in plain English and give you the price before we touch anything. Then we make the repair, test it and make sure the hot water's back before we leave.</p>
    <p>And if there's water on the floor right now, shut off the cold water valve on top of the heater and turn off the gas or the breaker. Then call us.</p>
  </div>
</div></section>"""
service_page("/water-heater-repair-ponca-city-ok/",
             "Water Heater Repair in Ponca City, OK | Gas, Electric & Tankless | Parr Plumbing",
             "Fast water heater repair in Ponca City, OK. We fix no hot water, leaks, bad elements, thermostats and relief valves on all makes and models. Licensed plumber. Call (580) 304-4967.",
             "Water Heater Repair in Ponca City, OK", "Ponca City water heater specialist",
             "Cold showers get old fast. Parr Plumbing repairs gas, electric and tankless water heaters on all makes and models, and we'll tell you honestly whether a repair is worth it.",
             "water-heater-repair-testing-elements-ponca-city",
             ["Heating elements, thermostats, relief valves and leaks", "All makes and models, gas and electric", f"Licensed Oklahoma plumber #{LICENSE}", "Honest repair or replace advice"],
             WHR_BODY, WHR_FAQ, "Water heater repair", "Water heater repair",
             "No hot water? Let's get it back.", "Call now and tell us what your water heater is doing. We'll take it from there.",
             "Water Heater Repair")

# ---------------------------------------------------------------- WATER HEATER REPLACEMENT
WHX_FAQ = [
    ("How long does a water heater last?",
     "A standard tank water heater often lasts around 8 to 12 years, depending on water quality and upkeep. Tankless units usually last longer. If yours is in that range and starting to have problems, it's worth planning for a replacement before it fails."),
    ("Should I get a tankless water heater?",
     "Tankless is a great fit if you want endless hot water, save space or plan to stay in the home a long time. A standard tank costs less up front and is simpler to swap. We'll walk you through both based on your home and how your family uses hot water."),
    ("What size water heater do I need?",
     "It depends on how many people live in the home, how many bathrooms you have and how much hot water you use at once. Many homes do well with a 40 or 50 gallon tank. We'll size it right so you don't run out or overpay."),
    ("How long does water heater replacement take?",
     "A straight swap of a standard tank water heater usually takes a few hours. Moving to tankless or relocating the heater takes longer. We'll give you a time estimate up front."),
        ("How much does a new water heater cost in Ponca City?",
     "Price depends on the type, size and fuel (gas or electric), plus any updates the install needs. Call us and we'll give you a clear price for your home before any work starts."),
]
WHX_BODY = f"""<section><div class="container grid-2 top">
  <div class="prose">
    <h2>When it's time for a new water heater</h2>
    <p>There's a point where patching an old water heater just doesn't make sense anymore. Maybe the tank is leaking from the bottom. Maybe it's rusting, or it's the third repair in two years. Either way, you want hot water you don't have to think about.</p>
    <p>That's where we come in. Parr Plumbing replaces water heaters all over Ponca City, swapping in brand new, efficient standard tank or tankless units. We size it right and install it to code.</p>
    <h3>Signs you need a replacement</h3>
    <ul class="signs">
      <li><b>Water leaking from the tank</b><span>Once the tank body leaks, it can't be repaired.</span></li>
      <li><b>Rust on the tank or in the water</b><span>A sign the inside of the tank is corroding.</span></li>
      <li><b>10+ years old</b><span>Many tanks start failing in this range.</span></li>
      <li><b>Repairs keep adding up</b><span>Money that could go toward a new unit.</span></li>
      <li><b>Never enough hot water</b><span>Your household may have outgrown it.</span></li>
      <li><b>Higher energy bills</b><span>Older units work harder to keep up.</span></li>
    </ul>
  </div>
  <div>{img("old-rusted-water-heater-needs-replacement", "Close up of corrosion and rust on an old water heater that needs replacement", "photo")}</div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head"><span class="eyebrow">Your options</span><h2>Standard tank or tankless water heater?</h2>
  <p class="lead">Both are good choices. The right one depends on your home, your budget and how much hot water your family goes through.</p></div>
  <div class="table-wrap"><table class="compare">
    <tr><th></th><th>Standard tank water heater</th><th>Tankless water heater</th></tr>
    <tr><td><b>Up front cost</b></td><td>Lower</td><td>Higher</td></tr>
    <tr><td><b>Hot water supply</b></td><td>Limited to the tank size</td><td>Heats on demand, so it doesn't run out</td></tr>
    <tr><td><b>Space</b></td><td>Needs floor space for the tank</td><td>Mounts on the wall, saves space</td></tr>
    <tr><td><b>Lifespan</b></td><td>Often 8 to 12 years</td><td>Often longer than a tank</td></tr>
    <tr><td><b>Energy use</b></td><td>Keeps a tank hot all day</td><td>Only heats water when you use it</td></tr>
    <tr><td><b>Best for</b></td><td>Quick, budget friendly swaps</td><td>Long term homeowners and big hot water users</td></tr>
  </table></div>
</div></section>
{band("Ready for hot water you don't have to think about?")}
<section><div class="container grid-2">
  {img("water-heater-replacement-parts-ponca-city", "New water heater supply lines, valves and tools ready for an installation")}
  <div class="prose">
    <h2>How a water heater replacement works</h2>
    <ul class="list">
      <li><b>We look at your setup.</b> Gas or electric, the space, the venting and how much hot water you need.</li>
      <li><b>You pick the unit.</b> We'll recommend the right size and type and give you a clear price.</li>
      <li><b>We install it right.</b> New connections, proper venting and a working relief valve, done to code.</li>
      <li><b>We test it and clean up.</b> You get hot water and a clean utility space.</li>
    </ul>
    <p style="margin-top:16px">Not sure if yours can be saved? Start with our <a href="/water-heater-repair-ponca-city-ok/">water heater repair</a> page, or just call and ask. We'll tell you honestly.</p>
  </div>
</div></section>"""
service_page("/water-heater-replacement-ponca-city-ok/",
             "Water Heater Replacement in Ponca City, OK | Tank & Tankless Install | Parr Plumbing",
             "Water heater replacement in Ponca City, OK. New standard tank and tankless water heaters, sized right, installed to code, old unit hauled away. Licensed plumber. Call (580) 304-4967.",
             "Water Heater Replacement in Ponca City, OK", "New tank and tankless water heaters",
             "When repair isn't a good option, we swap in a brand new, efficient water heater. Standard tank or tankless, gas or electric, sized for your home and installed right.",
             "water-heater-replacement-parts-ponca-city",
             ["Standard tank and tankless installs", "Gas and electric water heaters", "Sized right for your household", f"Licensed Oklahoma plumber #{LICENSE}"],
             WHX_BODY, WHX_FAQ, "Water heater replacement", "Water heater replacement (tank or tankless)",
             "Time for a new water heater?", "Call and we'll help you pick the right one and get it installed.",
             "Water Heater Replacement")

# ---------------------------------------------------------------- LEAK REPAIR
LEAK_FAQ = [
    ("How do I know if I have a hidden water leak?",
     "Watch for a water bill that jumps for no reason, the sound of running water when everything's off, damp spots on floors or walls, a musty smell or a water meter that keeps moving when no water is in use."),
    ("What should I do first if I have a leak?",
     "Shut off the water. Use the valve under the sink or behind the toilet if the leak is there, or the main shutoff for the house if you can't isolate it. Then call us."),
    ("Do you repair underground water line leaks?",
     "Yes. We find and fix leaks in kitchens, bathrooms and underground lines."),
    ("Can a small drip really cause damage?",
     "It can. A slow drip under a sink or behind a wall can rot cabinets, warp floors and grow mold over time. It's cheaper to fix early."),
    ("Is my water heater leaking?",
     "If there's water around the base of your water heater, check our <a href=\"/water-heater-repair-ponca-city-ok/\">water heater repair</a> page. Some leaks are an easy fix and some mean the tank needs replacing."),
]
LEAK_BODY = f"""<section><div class="container grid-2 top">
  <div class="prose">
    <h2>A leak is never just a little water</h2>
    <p>That small drip under the sink? It's been going longer than you think. Leaks have a way of hiding until there's a stain on the ceiling, a soft spot in the floor or a water bill that makes you do a double take.</p>
    <p>Parr Plumbing finds and fixes leaks in kitchens, bathrooms and underground lines all over Ponca City. We track down where the water's actually coming from, fix it properly and help you stop the damage before it spreads.</p>
    <h3>Leaks we fix</h3>
    <ul class="signs">
      <li><b>Under sink leaks</b><span>Supply lines, drain traps, shutoff valves and faucets.</span></li>
      <li><b>Bathroom leaks</b><span>Toilets, tub and shower valves, and vanity plumbing.</span></li>
      <li><b>Water heater leaks</b><span>Fittings, relief valves and drain valves.</span></li>
      <li><b>Underground line leaks</b><span>Water lines between the meter and your home.</span></li>
      <li><b>Dripping faucets</b><span>That steady drip adds up on your water bill.</span></li>
      <li><b>Running toilets</b><span>One of the biggest hidden water wasters in a home.</span></li>
    </ul>
  </div>
  <div>{img("leaking-water-heater-drain-valve", "Water dripping from a valve at the base of a water heater onto the floor", "photo")}</div>
</div></section>
<section class="alt"><div class="container grid-2 top">
  <div class="prose">
    <h2>Signs of a hidden plumbing leak</h2>
    <ul class="list">
      <li>Your water bill went up and your habits didn't change</li>
      <li>You hear water running when every faucet is off</li>
      <li>Water stains on ceilings or walls</li>
      <li>Warped, soft or stained flooring</li>
      <li>A musty smell or mold in cabinets</li>
      <li>Wet or extra green spots in the yard over your water line</li>
      <li>The water meter keeps spinning with everything off</li>
    </ul>
  </div>
  <div class="prose">
    <h2>Got a leak right now? Do this first</h2>
    <p>Find the closest shutoff valve and turn it off. Most sinks and toilets have one right underneath. If you can't stop it there, shut off the main water valve to the house.</p>
    <p>Move anything valuable out of the way, soak up what you can and snap a few photos for your records. Then call <a href="tel:{PHONE_TEL}">{PHONE}</a> and we'll take it from there.</p>
    <div class="callout"><p>Every hour a leak runs, the cleanup gets bigger. Don't wait on it. <a href="tel:{PHONE_TEL}">Call {PHONE}</a></p></div>
  </div>
</div></section>"""
service_page("/leak-repair-ponca-city-ok/",
             "Plumbing Leak Repair in Ponca City, OK | Sinks, Baths & Water Lines | Parr Plumbing",
             "Plumbing leak repair in Ponca City, OK. We find and fix leaks in kitchens, bathrooms, water heaters and underground water lines. Licensed local plumber. Call (580) 304-4967.",
             "Plumbing Leak Repair in Ponca City, OK", "Find it. Fix it. Stop the damage.",
             "Drips, puddles, stains and surprise water bills. Parr Plumbing tracks down leaks in kitchens, bathrooms and underground lines and fixes them right.",
             "water-leak-on-floor-under-water-heater",
             ["Kitchen, bathroom and water heater leaks", "Underground water line leaks", "We find the source, not just the puddle", f"Licensed Oklahoma plumber #{LICENSE}"],
             LEAK_BODY, LEAK_FAQ, "Leak repair", "Leak repair",
             "Leak? Let's stop it.", "Shut off the water if you can, then give us a call. We'll find it and fix it.",
             "Leak Repair")

# ---------------------------------------------------------------- GARBAGE DISPOSAL
GD_FAQ = [
    ("Why is my garbage disposal humming but not spinning?",
     "That usually means it's jammed. Turn it off and unplug it or flip the breaker. Never put your hand inside. If you can't free it safely, or it keeps jamming, give us a call."),
    ("Should I repair or replace my garbage disposal?",
     "Jams, clogs and loose connections are usually repairable. If the unit is leaking from the bottom, is old and rusted, or the motor is burned out, a replacement is often the smarter buy."),
    ("Why is my garbage disposal leaking?",
     "Leaks can come from the sink flange, the dishwasher hose connection or the drain line, which can usually be fixed. A leak from the bottom of the unit usually means it's time to replace it."),
    ("What shouldn't go down a garbage disposal?",
     "Grease, cooking oil, bones, fruit pits, coffee grounds, eggshells, pasta, rice and stringy vegetables like celery are the usual troublemakers."),
    ("Can you install a new garbage disposal?",
     "Yes. We replace worn out disposals and install new ones."),
]
GD_BODY = f"""<section><div class="container grid-2 top">
  <div class="prose">
    <h2>A broken disposal stops the whole kitchen</h2>
    <p>You flip the switch and get a hum. Or a grinding noise. Or nothing at all. Meanwhile there's a sink full of dishes and water that won't go down. It's one of those small things that throws the whole house off.</p>
    <p>We repair or replace noisy, non-functioning and jammed garbage disposals for homes around Ponca City. If it can be fixed, we'll fix it. If it's worn out, we'll put in a new one and get your kitchen back to normal.</p>
    <h3>Common garbage disposal problems</h3>
    <ul class="signs">
      <li><b>Humming but not spinning</b><span>Usually jammed or a stuck flywheel.</span></li>
      <li><b>Won't turn on at all</b><span>A tripped reset button, breaker or a burned out motor.</span></li>
      <li><b>Leaking under the sink</b><span>Flange, dishwasher hose or drain connections.</span></li>
      <li><b>Loud grinding or rattling</b><span>Something hard stuck inside, or worn parts.</span></li>
      <li><b>Slow draining sink</b><span>A clog in the disposal or the drain line.</span></li>
      <li><b>Bad smells that won't go away</b><span>Built up food waste inside the unit.</span></li>
    </ul>
  </div>
  <div>{img("plumbing-repair-tools-and-fittings", "Pipe wrench, adjustable wrench and copper fittings used for kitchen plumbing repairs", "photo")}</div>
</div></section>
<section class="alt"><div class="container grid-2 top">
  <div class="prose">
    <h2>Try this first (safely)</h2>
    <ul class="list">
      <li>Turn the disposal off and unplug it or shut off the breaker</li>
      <li>Press the red reset button on the bottom of the unit</li>
      <li>Never put your hand down the disposal</li>
      <li>Don't pour drain cleaner into a disposal, it can damage it and splash back</li>
    </ul>
    <p style="margin-top:14px">Still not working? That's our cue. Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
  </div>
  <div class="prose">
    <h2>Repair or replace?</h2>
    <p>Jams, clogs and loose connections are usually quick repairs. But if the unit is leaking from the body, the motor's burned out or it's rusted and old, a new disposal is often the better value. We'll tell you which one makes sense and why.</p>
    <div class="callout"><p>Sink also leaking somewhere else? We handle <a href="/leak-repair-ponca-city-ok/">leak repair</a> too.</p></div>
  </div>
</div></section>"""
service_page("/garbage-disposal-repair-ponca-city-ok/",
             "Garbage Disposal Repair in Ponca City, OK | Repair & Replacement | Parr Plumbing",
             "Garbage disposal repair and replacement in Ponca City, OK. We fix jammed, humming, leaking and dead disposals or install a new one. Licensed plumber. Call (580) 304-4967.",
             "Garbage Disposal Repair in Ponca City, OK", "Jammed, humming or dead disposal?",
             "We repair or replace noisy, non-functioning and jammed garbage disposals, so you can get the kitchen sink working again.",
             "plumbing-repair-tools-and-fittings",
             ["Jams, leaks and disposals that won't turn on", "New disposal installs and replacements", "Honest repair or replace advice", f"Licensed Oklahoma plumber #{LICENSE}"],
             GD_BODY, GD_FAQ, "Garbage disposal repair", "Garbage disposal repair or replacement",
             "Disposal giving you trouble?", "Call and tell us what it's doing. We'll get your kitchen sink working again.",
             "Garbage Disposal Repair")

# ---------------------------------------------------------------- WATER FILTRATION
WF_FAQ = [
    ("What is a reverse osmosis system?",
     "A reverse osmosis (RO) system pushes water through a very fine membrane plus a few filters to remove much of what's dissolved in it. Most home systems sit under the kitchen sink and feed a small faucet for drinking and cooking water."),
    ("Where does a reverse osmosis system go?",
     "Most residential RO systems install under the kitchen sink, with a dedicated faucet on the sink or countertop."),
    ("How often do the filters need changing?",
     "Pre-filters are commonly changed about once a year and the RO membrane every few years, depending on your water and how much you use. We'll tell you the schedule for your system."),
    ("Is a reverse osmosis system worth it?",
     "If you buy bottled water or don't like how your tap water tastes, many families find an RO system pays for itself and is a lot more convenient than hauling cases of water home."),
    ("Do you install whole house filtration too?",
     "Our focus is quality residential reverse osmosis drinking water systems. Call and tell us what you're looking for and we'll talk through options."),
]
WF_BODY = f"""<section><div class="container grid-2 top">
  <div class="prose">
    <h2>Better tasting water, right from your kitchen sink</h2>
    <p>Tired of hauling cases of bottled water home? Or maybe the tap water just doesn't taste the way you want it to. Either way, a reverse osmosis system under your sink gives you clean, great tasting drinking water on demand.</p>
    <p>Parr Plumbing installs quality residential reverse osmosis water filtration systems for homes in Ponca City. We'll help you choose a system, install it cleanly under the sink and show you how to keep it running.</p>
    <h3>Why families add an RO system</h3>
    <ul class="signs">
      <li><b>Better taste</b><span>Coffee, tea, ice and cooking all taste cleaner.</span></li>
      <li><b>No more bottled water</b><span>Save money and stop hauling cases home.</span></li>
      <li><b>Convenient</b><span>Filtered water from its own faucet, any time.</span></li>
      <li><b>Healthier habits</b><span>When water tastes good, everybody drinks more of it.</span></li>
    </ul>
  </div>
  <div>{img("clean-filtered-water-kitchen-faucet", "Hands under clean water flowing from a kitchen faucet", "photo tall", w=1400, h=1750)}</div>
</div></section>
<section class="alt"><div class="container grid-2 top">
  <div class="prose">
    <h2>How a reverse osmosis system works</h2>
    <p>Water passes through a sediment filter and a carbon filter first, which catch grit and improve taste and odor. Then it's pushed through the reverse osmosis membrane, which removes much of what's dissolved in the water. The clean water is stored in a small tank under the sink and runs to its own faucet.</p>
  </div>
  <div class="prose">
    <h2>Installed by a licensed plumber</h2>
    <p>An RO system connects to your water supply and your drain, so a clean, leak free install matters. We'll mount the system, tie it into your plumbing, add the faucet, test for leaks and flush it so it's ready to use.</p>
    <div class="callout"><p>Want one installed? <a href="tel:{PHONE_TEL}">Call</a> or <a href="{SMS}">text {PHONE}</a> and we'll set up a time.</p></div>
  </div>
</div></section>"""
service_page("/water-filtration-ponca-city-ok/",
             "Water Filtration System Installation in Ponca City, OK | Reverse Osmosis | Parr Plumbing",
             "Reverse osmosis water filtration system installation in Ponca City, OK. Clean, great tasting drinking water under your kitchen sink. Licensed plumber. Call (580) 304-4967.",
             "Water Filtration System Installation in Ponca City, OK", "Reverse osmosis drinking water",
             "Better tasting water without the bottled water runs. We install quality residential reverse osmosis systems under your kitchen sink.",
             "clean-filtered-water-kitchen-faucet",
             ["Residential reverse osmosis systems", "Clean under sink install with dedicated faucet", "Better tasting water for drinking and cooking", f"Licensed Oklahoma plumber #{LICENSE}"],
             WF_BODY, WF_FAQ, "Water filtration system installation", "Water filtration / reverse osmosis system",
             "Ready for better water?", "Call and we'll help you pick a system and get it installed.",
             "Water Filtration")

# ================================================================ SERVICES HUB
SV_FAQ = [
    ("Do you handle residential and commercial plumbing?", "Yes. We work on homes and businesses across Ponca City."),
    ("What plumbing work do you do most?", "Water heaters are our specialty, both repair and replacement. We also handle leak repair, garbage disposals, water filtration systems, faucets, fixtures and sewer line repairs."),
    ("Do you do faucet and fixture installs?", "Yes. From swapping a kitchen faucet to replacing bathroom fixtures, we take care of it."),
]
trail = [("Home", "/"), ("Services", "/services/")]
sv = head("Plumbing Services in Ponca City, OK | Residential & Commercial | Parr Plumbing",
          "Plumbing services in Ponca City, OK from Parr Plumbing: water heater repair and replacement, leak repair, garbage disposals, water filtration, faucets, fixtures and sewer lines. Call (580) 304-4967.",
          "/services/", [faq_schema(SV_FAQ), crumbs_schema(trail)])
sv += hero("Residential and commercial plumbing", "Plumbing Services in Ponca City, OK",
           "Fast, reliable and affordable plumbing for Ponca City homes and businesses. Water heaters are our specialty, but if it carries water, we can probably help.",
           "plumbing-valves-and-fittings",
           ["Water heater repair and replacement", "Leaks, disposals, faucets and fixtures", "Sewer line repairs and water filtration", f"Licensed Oklahoma plumber #{LICENSE}"], trail=trail)
sv += service_cards(exclude="/services/", heading="Our plumbing services")
sv += f"""<section class="alt"><div class="container grid-2 top">
  <div class="prose">
    <h2>Residential plumbing</h2>
    <p>From faucet installation to sewer line repairs, we cover the plumbing needs of homes across Ponca City. That includes:</p>
    <ul class="list">
      <li>Kitchen and bathroom faucet installation and repair</li>
      <li>Toilet repairs and running toilets</li>
      <li>Fixture replacement</li>
      <li>Sewer line repairs</li>
      <li>Shutoff valve replacement</li>
      <li>Water heater, leak, disposal and filtration work</li>
    </ul>
  </div>
  <div class="prose">
    <h2>Commercial plumbing</h2>
    <p>Businesses in Ponca City can't afford to be down because of a plumbing problem. We handle repairs, water heater service and installs for local businesses, with the same honest approach we bring to homes.</p>
    <p>Have a project or a problem at your business? Call <a href="tel:{PHONE_TEL}">{PHONE}</a> and let's talk about it.</p>
  </div>
</div></section>"""
sv += faq_block(SV_FAQ, "Plumbing service questions")
sv += cta_final("Need a plumber?", "Call or text now. We'll help you figure out what's going on.")
sv += FOOT
write("/services/", sv)

# ================================================================ ABOUT
trail = [("Home", "/"), ("About Greg Parr", "/about/")]
person = {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "/#greg", "name": "Greg Parr",
          "jobTitle": "Owner and Licensed Plumbing Contractor", "worksFor": {"@id": SITE + "/#business"},
          "homeLocation": {"@type": "City", "name": "Ponca City, OK"}, "url": SITE + "/about/"}
ab = head("About Greg Parr | Licensed Ponca City Plumber | Parr Plumbing",
          "Meet Greg Parr, owner of Parr Plumbing. A lifetime Ponca City resident and licensed Oklahoma plumbing contractor for over a decade, specializing in water heaters.",
          "/about/", [person, crumbs_schema(trail)])
ab += f"""<section class="hero" style="padding:52px 0">
  <img class="hero-bg" src="/img/plumbing-valves-and-fittings-sm.webp" alt="" fetchpriority="high">
  <div class="container"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / About Greg Parr</nav>
  <span class="eyebrow">About Parr Plumbing</span>
  <h1>Meet Greg Parr, Your Ponca City Plumber</h1>
  <p class="lead">Lifetime Ponca City resident. Licensed plumbing contractor for over a decade. The guy you call when the hot water's gone.</p>
  <div class="hero-cta"><a class="btn" href="tel:{PHONE_TEL}">{PHONE_ICO} Call {PHONE}</a></div></div>
</section>
<section><div class="container grid-2 top">
  <div class="prose">
    <h2>Local roots, licensed work</h2>
    <p>Greg Parr has lived in Ponca City his entire life. He's been a licensed Oklahoma plumbing contractor for over a decade, and Parr Plumbing is how he takes care of his neighbors' plumbing, one house and one business at a time.</p>
    <p>Over the years, water heaters became Greg's specialty. Repairing them, replacing them and helping people figure out which one makes sense. It's the kind of job where honest advice matters, because the difference between a repair and a replacement can be a lot of money.</p>
    <h2>How we work</h2>
    <ul class="list">
      <li><b>Straight answers.</b> We tell you what's wrong and what it'll cost before we start.</li>
      <li><b>Repair first when it makes sense.</b> We won't sell you a new water heater you don't need.</li>
      <li><b>Done right.</b> Licensed, insured and installed to code.</li>
      <li><b>Respect for your home.</b> We clean up when we're done.</li>
    </ul>
  </div>
  <div>
    <div class="card" style="border-top:6px solid var(--yellow)">
      <h3>Parr Plumbing at a glance</h3>
      <ul class="list">
        <li>Owner: Greg Parr</li>
        <li>Oklahoma Plumbing Contractor License #{LICENSE}</li>
        <li>Fully licensed and insured</li>
        <li>Licensed contractor for over a decade</li>
        <li>Lifetime Ponca City resident</li>
        <li>Residential and commercial plumbing</li>
        <li>Call or text: <a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        <li>Hours: Mon to Sat, 9 AM to 6 PM</li>
        <li>Serving {AREA}</li>
      </ul>
    </div>
  </div>
</div></section>"""
ab += service_cards(heading="What Greg can help with")
ab += cta_final("Give Greg a call or text", "Water heater, leak or something else? Call or text and tell him what's going on.")
ab += FOOT
write("/about/", ab)

# ================================================================ CONTACT
trail = [("Home", "/"), ("Contact", "/contact/")]
ct = head("Contact Parr Plumbing | Plumber in Ponca City, OK | (580) 304-4967",
          "Contact Parr Plumbing, a licensed plumber in Ponca City, OK. Call or text (580) 304-4967 for water heater repair, leaks, disposals and more. Serving Ponca City, McCord, Newkirk and Tonkawa.",
          "/contact/", [crumbs_schema(trail)])
ct += hero("Call or text", "Contact Parr Plumbing in Ponca City, OK",
           "Call or text (580) 304-4967 and you'll reach Greg directly. Can't talk right now? Send a text with what's going on, and a photo if you can.",
           "plumber-checking-water-heater-ponca-city-ok",
           [f'Call or text: <a href="tel:{PHONE_TEL}" style="color:#f9d71c">{PHONE}</a>', "Monday to Saturday, 9 AM to 6 PM. Closed Sunday.", f"Serving {AREA}",
            f"Licensed Oklahoma plumbing contractor #{LICENSE}", "Residential and commercial plumbing"], trail=trail)
ct += service_cards(heading="What can we help with?")
ct += FOOT
write("/contact/", ct)

# ================================================================ PRIVACY
pv = head("Privacy Policy | Parr Plumbing", "How Parr Plumbing handles the information you share when you call, text or visit parrplumbing.com, the website for our Ponca City, OK plumbing service.", "/privacy/")
pv += f"""<section><div class="container prose">
  <h1>Privacy Policy</h1>
  <p style="margin-top:14px">This policy explains what information Parr Plumbing collects on parrplumbing.com and how we use it.</p>
  <h2>Information you give us</h2>
  <p>This website doesn't use contact forms. If you call or text us, we use your name, number and the details you share only to respond and provide plumbing service.</p>
  <h2>Information collected automatically</h2>
  <p>Like most websites, our hosting provider may log basic technical information such as IP address, browser type and pages visited for security and performance.</p>
  <h2>Sharing</h2>
  <p>We don't sell, rent or trade your personal information. We only share it with service providers who help us run this website and our business, or when required by law.</p>
  <h2>Contact</h2>
  <p>To ask us to update or delete information you've shared, call or text <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
</div></section>"""
pv += FOOT
write("/privacy/", pv)

# ================================================================ 404
nf = head("Page Not Found | Parr Plumbing", "That page doesn't exist.", "/404.html", robots="noindex")
nf += f"""<section><div class="container prose" style="text-align:center;margin:0 auto">
  <h1>Sorry, that page sprung a leak</h1>
  <p class="lead" style="margin-top:14px">We couldn't find what you were looking for. Try the homepage, or just give us a call.</p>
  <div class="hero-cta" style="justify-content:center"><a class="btn dark" href="/">Go to homepage</a><a class="btn" href="tel:{PHONE_TEL}">{PHONE_ICO} Call {PHONE}</a></div>
</div></section>"""
nf += service_cards(heading="Popular services")
nf += FOOT
(ROOT / "404.html").write_text(nf)

# ================================================================ SUPPORT FILES
PAGES = ["/", "/water-heater-repair-ponca-city-ok/", "/water-heater-replacement-ponca-city-ok/", "/leak-repair-ponca-city-ok/",
         "/garbage-disposal-repair-ponca-city-ok/", "/water-filtration-ponca-city-ok/", "/services/", "/about/", "/contact/", "/privacy/"]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{p}</loc></url>\n" for p in PAGES) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
(ROOT / "site.webmanifest").write_text(json.dumps({"name": BIZ, "short_name": "Parr Plumbing",
    "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}],
    "theme_color": "#12131f", "background_color": "#ffffff", "display": "browser"}))
# IndexNow key file (Bing, Yandex and other IndexNow engines)
INDEXNOW_KEY = "18f7aba30490cbc419dfd18c131c3d6a"
(ROOT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY)
# old GoHighLevel URLs -> new pages
(ROOT / "_redirects").write_text("""/home / 301
/home/ / 301
/about-us /about/ 301
/about-us/ /about/ 301
/contact-us /contact/ 301
/contact-us/ /contact/ 301
""")
print("Built", len(PAGES) + 1, "pages into", ROOT)

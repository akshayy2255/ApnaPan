# -*- coding: utf-8 -*-
"""ApnaPan — page builders. Every page is prerendered to static HTML."""
from content import (BRAND, PRODUCTS, TESTIMONIALS, TIMELINE, IMPACT, ALLOCATION, EDUCATION,
                     FARMER_WHY, FARMER_STEPS, FARMER_FAQ, JOBS, BENEFITS, CAREER_FAQ,
                     POSTS, FAQS_HOME, FAQS_SHIPPING, TRUST_BADGES, CATEGORIES)
from render import (T, Traw, A, AP, E, icon, live_categories, mark, TYPE_KEY, SPICE_KEY, DIET_KEY, BADGE_KEY, logo_svg, head, header, marquee, footer, section_head,
                    stars, rating_line, product_card, stat_card, badge_card, quote_card, faq_block,
                    check_list, newsletter_block, impact_band, trust_strip, breadcrumbs,
                    ld_org, ld_product, ld_faq, ld_breadcrumb, Urls)


def by_slug(slug):
    return next(p for p in PRODUCTS if p["slug"] == slug)


def money(n):
    return f'₹{n:,}'


# =============================================================== HOME
def home(u):
    hero = f'''
<section class="hero">
  <div class="wrap hero__inner">
    <div class="hero__copy">
      <span class="eyebrow" {A("home.hero.eyebrow")}>{T("home.hero.eyebrow")}</span>
      <h1><span {A("home.hero.title")}>{T("home.hero.title")}</span>
        <span class="line-2" {A("home.hero.line2")}>{T("home.hero.line2")}</span></h1>
      <p class="hero__lede" {A("home.hero.lede")}>{T("home.hero.lede")}</p>
      <div class="btn-row hero__cta">
        <a class="btn btn--lg" href="{u('shop.html')}">{icon("cart")} <span {A("common.shop")}>{T("common.shop")}</span></a>
        <a class="btn btn--outline btn--lg" href="{u('impact.html')}">{icon("sunrise")} <span {A("common.impact")}>{T("common.impact")}</span></a>
      </div>
      <p class="hero__meta">
        <span>{icon("truck")} <span {A("home.hero.meta1")}>{T("home.hero.meta1")}</span></span>
        <span>{icon("flame")} <span {A("home.hero.meta2")}>{T("home.hero.meta2")}</span></span>
        <span>{icon("leaf")} <span {A("common.nopreservative")}>{T("common.nopreservative")}</span></span>
      </p>
    </div>
    <div class="hero__art">
      <div class="hero__photo">
        <img src="{u('assets/images/hero-farm.jpg')}" alt="Three women farmers harvesting red chillies at sunrise in a Karnataka field" width="1376" height="768" fetchpriority="high">
        <span class="hero__badge-float">{icon("award")} Women-led</span>
      </div>
      <div class="hero__stamp">
        {icon("hand-heart")}
        <span><b>{IMPACT["women"]["value"]} women · {IMPACT["farmers"]["value"]} farmers</b>
        <span {A("home.hero.stamp")}>{T("home.hero.stamp")}</span></span>
      </div>
    </div>
  </div>
</section>'''

    pairs = [
        {"icon": "rupee",
         "p_title": "Farmers have no market they can trust",
         "p_text": "A chilli farmer in Haveri sells to whoever turns up at the gate. The rate is fixed after the weighing, payment comes in six weeks, and the best-quality crop earns the same as the worst.",
         "s_title": "A price agreed before sowing",
         "s_text": "We agree the rate for the season in writing, weigh at the farm in front of the farmer, and transfer payment within 7 working days — an average 22% above the local mandi rate."},
        {"icon": "women",
         "p_title": "Women have skills and no work close to home",
         "p_text": "Women in Doddaballapur cook, grade and manage money for their families, but formal work within a safe commute is scarce. Where factories do hire women, it is minimum wage for the heaviest work.",
         "s_title": "128 women, real pay, real promotion",
         "s_text": "Nine in ten of our team are women and every factory supervisor is a woman. Wages run 12–18% above the local median, there are no night shifts, and 7 of 11 supervisors were promoted from within."},
        {"icon": "school",
         "p_title": "A child's schooling ends quietly in Class 10",
         "p_text": "Fees, coaching, books and travel add up to ₹15,000–₹20,000 in the year that decides a child's next ten years. For a family on daily wages, that is where school stops.",
         "s_title": "6% of every sale, written into our rules",
         "s_text": "The Class 10 Fund pays school and board fees, books, uniforms, evening coaching and travel for every employee's child — plus a tablet for high scorers. 216 children covered."},
    ]
    vs_rows = ""
    for r in pairs:
        vs_rows += f'''
    <div class="vs reveal">
      <div class="ps-card">
        <h4>{icon(r["icon"])} {E(r["p_title"])}</h4>
        <p>{E(r["p_text"])}</p>
      </div>
      <div class="ps-arrow">{icon("arrow-r")}</div>
      <div class="ps-card ps-card--solution">
        <h4>{icon("check")} {E(r["s_title"])}</h4>
        <p>{E(r["s_text"])}</p>
      </div>
    </div>'''

    problem = f'''
<section class="section section--sand" id="why">
  <div class="wrap">
    {section_head("home.problem.eyebrow", "home.problem.title", None, center=True)}
    <div class="grid mt-4" style="gap:1.1rem">
      <div class="vs" style="grid-template-columns:1fr auto 1fr">
        <div class="ps-card" style="box-shadow:none;background:transparent;border:0;padding-bottom:0">
          <span class="tag tag--terracotta" {A("home.problem.tag")}>{T("home.problem.tag")}</span>
        </div>
        <span></span>
        <div class="ps-card" style="box-shadow:none;background:transparent;border:0;padding-bottom:0">
          <span class="tag tag--green" {A("home.solution.tag")}>{T("home.solution.tag")}</span>
        </div>
      </div>
      {vs_rows}
    </div>
    <p class="small muted mt-3 center">{E('Illustrative figures. See the note on our impact page.')}</p>
  </div>
</section>'''

    featured = [by_slug("mavina-midi-pickle"), by_slug("bisibelebath-masala"), by_slug("ghee-roast-masala"), by_slug("maddur-vada-mix")]
    cards = "".join(product_card(p, u) for p in featured)
    shop_block = f'''
<section class="section" id="shop">
  <div class="wrap">
    <div class="shop-toolbar">
      {section_head("home.featured.eyebrow", "home.featured.title", "home.featured.sub")}
      <a class="btn btn--outline" href="{u('shop.html')}">{icon("cart")} <span {A("common.viewall")}>{T("common.viewall")}</span></a>
    </div>
    <div class="product-grid mt-3">{cards}</div>
  </div>
</section>'''

    jsteps = [
        {"n": "01", "h": "Sourcing", "p": "Bought at the farm gate, weighed in front of the farmer.", "img": "assets/images/hands-spices.jpg"},
        {"n": "02", "h": "Processing", "p": "Slow-roasted and stone-ground in small batches.", "img": "assets/images/factory-women.jpg"},
        {"n": "03", "h": "Quality Control", "p": "Moisture, salt, pH and microbial checks on every batch.", "img": "assets/images/quality-control.jpg"},
        {"n": "04", "h": "Packaging", "p": "Sealed the same week, labelled with the batch code and names.", "img": "assets/images/products/akki-rotti-mix.jpg"},
        {"n": "05", "h": "Distribution", "p": "To homes, stores and gifting partners across India.", "img": "assets/images/distribution.jpg"},
    ]
    journey_steps = ""
    for i, s in enumerate(jsteps):
        journey_steps += f'''<div class="jstep">
        <span class="jstep__num">{s["n"]}</span>
        <span class="jstep__img"><img src="{u(s["img"])}" alt="{E(s["h"])}" loading="lazy" width="120" height="120"></span>
        <h5>{E(s["h"])}</h5>
        <p>{E(s["p"])}</p>
        <span class="jstep__icon">{icon("arrow-r")}</span>
      </div>'''
    journey = f'''
<section class="section section--cream" id="journey">
  <div class="wrap">
    {section_head("home.journey.eyebrow", "home.journey.title", None, center=True)}
    <div class="journey mt-4">{journey_steps}</div>
    <div class="btn-row btn-row--center mt-3">
      <a class="btn btn--green" href="{u('how-it-works.html')}">{icon("scale")} See how each step is checked</a>
      <a class="btn btn--outline" href="{u('products/' + 'mavina-midi-pickle' + '.html')}">{icon("leaf")} Trace one jar to its farmer</a>
    </div>
  </div>
</section>'''

    testi = "".join(quote_card(t, u("")) for t in [TESTIMONIALS[0], TESTIMONIALS[2], TESTIMONIALS[3], TESTIMONIALS[1]])
    testi_block = f'''
<section class="section section--sand" id="stories">
  <div class="wrap">
    {section_head("home.testi.eyebrow", "home.testi.title", None, center=True)}
    <div class="grid grid--2 mt-4">{testi}</div>
  </div>
</section>'''

    press = [("The Hindu", "Metro"), ("Deccan Herald", "Business"), ("YourStory", "Impact"), ("Krishi Jagran", "Agri"), ("The Better India", "People")]
    press_logos = "".join(f'<div class="presslogo"><b>{E(n)}</b><span>{E(s)}</span></div>' for n, s in press)
    press_block = f'''
<section class="section section--tight">
  <div class="wrap">
    <p class="center small muted" style="letter-spacing:.14em;text-transform:uppercase">Featured in — sample placements, replace with your real press</p>
    <div class="logo-strip mt-2">{press_logos}</div>
    <div class="grid grid--4 mt-3">{''.join(badge_card(b) for b in TRUST_BADGES[2:])}</div>
  </div>
</section>'''

    body = hero + trust_strip() + problem + shop_block + impact_band(u) + journey + testi_block + press_block + newsletter_block(u)
    body = f'<main id="main">{marquee()}{body}</main>'
    jsonld = [ld_org(), ld_faq(FAQS_HOME),
              {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND["name"], "url": BRAND["url"]}]
    return head(f"{BRAND['name']} — Women-led farm-direct spices, masalas & pickles from Karnataka",
                "ApnaPan buys spices and produce direct from 480 Karnataka farmers, processes them in a unit run by 128 women, and funds employees' children's education. Shop masalas, ready mixes and pickles.",
                "index.html", u("assets/css/styles.css"), u, jsonld) + header("nav.home", u) + body + footer(u) + "</body></html>"


# =============================================================== STORY
def story(u):
    hero = f'''
<section class="section post-hero">
  <div class="wrap">
    <span class="eyebrow" {A("st.eyebrow")}>{T("st.eyebrow")}</span>
    <h1 class="mt-2" style="max-width:22ch" {A("st.title")}>{T("st.title")}</h1>
    <p class="lede mt-2" style="max-width:62ch">In 2019 one woman, six neighbours and a rented kitchen shed in Doddaballapur. Today 128 women, 480 farmer families and 216 children in school. Nothing about it was quick, and most of it was learned the hard way.</p>
    <div class="grid grid--4 mt-4">
      {stat_card(IMPACT["women"])}{stat_card(IMPACT["farmers"])}{stat_card(IMPACT["children"])}{stat_card(IMPACT["training"])}
    </div>
  </div>
</section>'''

    problem = f'''
<section class="section">
  <div class="wrap split split--2">
    <div>
      <span class="eyebrow" {A("st.problem")}>{T("st.problem")}</span>
      <h2 class="mt-2">Three quiet problems in one supply chain</h2>
      <p class="lede mt-2">Lakshmi Devi spent eleven years as a field officer for a commodity trading company in northern Karnataka. She watched the same three things break, season after season.</p>
      <ul class="x-list mt-3">
        <li>{icon("x")}<span><b>The farmer carried all the risk.</b> Rate decided after weighing, payment delayed by weeks, no penalty when the trader defaulted — but a deduction every time the market dipped.</span></li>
        <li>{icon("x")}<span><b>Women did the work without the wage.</b> Post-harvest cleaning, grading, drying and packing are done almost entirely by women, in their homes, unpaid and invisible in the price chain.</span></li>
        <li>{icon("x")}<span><b>The last mile was where quality died.</b> Produce that left a village clean arrived at a factory mixed, damp and full of stones. Everyone blamed everyone else and the consumer paid for the filler.</span></li>
      </ul>
    </div>
    <figure style="margin:0">
      <img src="{u('assets/images/hands-spices.jpg')}" alt="A woman's hands sorting dried red chillies and spices" style="border-radius:var(--r-lg);box-shadow:var(--shadow-md)" loading="lazy">
      <figcaption class="small muted mt-1">Grading and sorting at our unit — work that used to happen unpaid, in homes.</figcaption>
    </figure>
  </div>
</section>'''

    solution = f'''
<section class="section section--sand">
  <div class="wrap">
    <div class="split split--2">
      <div>
        <span class="eyebrow" {A("st.solution")}>{T("st.solution")}</span>
        <h2 class="mt-2">Buy well, make well, and share the upside</h2>
        <p class="lede mt-2">Our mission is one sentence long: <em>every woman on our team should be able to pay for her child's education out of the work she does, without asking anyone for help.</em> Everything else — the sourcing rules, the factory, the products — exists to make that sentence true and keep it true.</p>
      </div>
      <div class="grid" style="gap:1rem">
        <div class="info-tile">{icon("rupee")}<h4>Sourcing rules we do not bend</h4>
        <p>Rate agreed before sowing, bought at the farm gate, weighed in front of the farmer, paid within 7 working days, and the whole lot taken — not just the best bags.</p></div>
        <div class="info-tile">{icon("women")}<h4>Work designed for women</h4>
        <p>No night shifts, 12 pick-up routes, a creche room, all supervisors promoted from within, and a wage band published on the internal notice before every vacancy.</p></div>
        <div class="info-tile">{icon("school")}<h4>A permanent education fund</h4>
        <p>6% of every sale goes into the Class 10 Fund — a payment obligation in our articles of association, ranked like a farmer's invoice. 216 children today.</p></div>
      </div>
    </div>
  </div>
</section>'''

    founder = f'''
<section class="section">
  <div class="wrap split split--wide-right" style="gap:clamp(1.6rem,4vw,3.2rem)">
    <figure style="margin:0">
      <img src="{u('assets/images/founder-note.jpg')}" alt="Lakshmi Devi R., founder of ApnaPan, at the processing unit" style="border-radius:var(--r-lg);box-shadow:var(--shadow-lg)" loading="lazy">
    </figure>
    <div>
      <span class="eyebrow" {A("st.founder")}>{T("st.founder")}</span>
      <h2 class="mt-2">“I did not want to build a brand. I wanted to fix a price.”</h2>
      <div class="prose mt-3" style="max-width:64ch">
        <p>In 2018 I sat on a plastic chair in a farmer's front yard in Byadagi and watched him sell 900 kilos of chilli for ₹82 a kilo. Two hours later, the same chilli was being resold in a yard across the road at ₹121. He knew. He had always known. He simply had no other buyer with a truck.</p>
        <p>That is the whole business case. Everything ApnaPan does — the grinding stones, the glass jars, the women on the packing line, the six percent — is downstream of one decision: buy from the person who grew it, at a price agreed before they sow, and keep that promise even when it costs us.</p>
        <p>What I did not expect was what the women's side of this would do to me. Shivamma, who runs our roasting line, learned to sign her name in 2022 so she could open a bank account for her daughter's fees. She now checks every batch by smell and has sent two batches back this year. Her daughter is in Class 11. I have signed off on a lot of spreadsheets in my life. That one still gets me.</p>
        <p>We are not a large company and we have no ambition to become one at any cost. We want five factories, each one standing next to the crops it processes, each one staffed mostly by women from the villages around it, and each one funded by the sales of the one before. If we do that properly, the rest follows.</p>
      </div>
      <p class="signature mt-3">Lakshmi Devi R.</p>
      <p class="small muted">Founder, ApnaPan Foods · Doddaballapur, Karnataka</p>
      <div class="btn-row mt-3">
        <a class="btn" href="{u('impact.html')}">{icon("sunrise")} See what it added up to</a>
        <a class="btn btn--outline" href="{u('blog.html')}">{icon("book")} Read the kitchen notes</a>
      </div>
    </div>
  </div>
</section>'''

    tl = ""
    for t in TIMELINE:
        tags = "".join(f'<span class="tag{" tag--gold" if t["now"] else ""}">{E(x)}</span>' for x in t["tags"])
        tl += f'''<div class="tl-item{" tl-item--now" if t["now"] else ""}">
        <span class="tl-year">{E(t["year"])}</span>
        <h4>{E(t["title"])}</h4>
        <p>{E(t["text"])}</p>
        <div class="tag-row">{tags}</div>
      </div>'''
    timeline = f'''
<section class="section section--sand">
  <div class="wrap">
    {section_head("st.timeline", "st.timeline", None, center=True)}
    <div class="timeline mt-4" style="max-width:78ch;margin-inline:auto">{tl}</div>
  </div>
</section>'''

    loop_items = [
        ("01", "One factory", "A unit built next to the crops it processes, run by women from the villages around it."),
        ("02", "More products", "Each new product uses more of the same crop, so we buy more from the same farmers."),
        ("03", "More farmers", "Bigger, steadier orders justify a rate agreed a season in advance."),
        ("04", "More women", "Every 8–10 new products add a shift, and a shift adds 12–15 women."),
        ("05", "More factories", "The next unit is funded by the sales of the last one — not by borrowing against promises."),
    ]
    loop = "".join(f'<div class="loop__item"><span class="loop__idx">{n}</span><b>{E(h)}</b><span>{E(p)}</span></div>' for n, h, p in loop_items)
    model = f'''
<section class="section">
  <div class="wrap">
    {section_head(None, "st.model", "st.modeltext", center=True)}
    <div class="loop mt-4">{loop}</div>
    <div class="callout mt-4" style="max-width:80ch;margin-inline:auto">
      <h4>Why the loop matters more than the growth chart</h4>
      <p>A second factory is not a marketing decision for us — it is a financial one. Unit #2 near Kalaburagi opens when unit #1 can fund its equipment out of operating profit and when we have 600 farmer families in the dal belt to supply it. That is slower than a venture-funded plan. It is also why our payments to farmers have never been late.</p>
    </div>
  </div>
</section>'''

    body = hero + problem + solution + founder + timeline + model + impact_band(u) + newsletter_block(u)
    body = f'<main id="main">{body}</main>'
    return head(f"Our Story — {BRAND['name']}", "How ApnaPan started with six women in a rented kitchen in Doddaballapur and grew into a women-run food processing company sourcing from 480 Karnataka farmers.",
                "story.html", u("assets/css/styles.css"), u, [ld_org(), ld_breadcrumb([("Home", "index.html"), ("Our Story", "story.html")])]) + header("nav.story", u) + body + footer(u) + "</body></html>"


# =============================================================== IMPACT
def impact(u):
    hero = f'''
<section class="section post-hero">
  <div class="wrap">
    <span class="eyebrow" {A("imp.eyebrow")}>{T("imp.eyebrow")}</span>
    <h1 class="mt-2" style="max-width:24ch" {A("imp.title")}>{T("imp.title")}</h1>
    <p class="lede mt-2" style="max-width:64ch">These are the numbers we track monthly and publish every quarter. They are audited with our annual accounts, and the sample figures on this demonstration site are marked as illustrative.</p>
    <div class="stat-grid mt-4">
      {stat_card(IMPACT["women"])}{stat_card(IMPACT["farmers"])}{stat_card(IMPACT["children"])}{stat_card(IMPACT["mandi"])}
      {stat_card(IMPACT["training"])}{stat_card(IMPACT["shipped"])}
    </div>
  </div>
</section>'''

    women = f'''
<section class="section" id="women">
  <div class="wrap">
    <div class="split split--2">
      <div>
        <span class="eyebrow" {A("imp.women")}>{T("imp.women")}</span>
        <h2 class="mt-2">128 jobs, and a ladder behind each one</h2>
        <p class="lede mt-2">It is easy to put a woman on a packing line. The harder promise is that she can move up it. So we publish the wage band with every internal vacancy and we post every vacancy internally first.</p>
        {check_list([
            "128 women employed across processing, quality, packing, field and office",
            "Wages 12–18% above the Doddaballapur industrial median for the same skill",
            "Provident fund and ESI from day one · 20 days paid leave · 6 months paid maternity leave",
            "4,800+ hours of certified skill training in 2025, on paid work time",
            "7 of 11 supervisors and above were promoted from within the company",
            "Zero night shifts for women · 12 pick-up and drop routes · creche room at the unit",
            "Salary paid by bank transfer in every woman's own name, and a bank account opened for anyone who did not have one",
        ])}
      </div>
      <div>
        <div class="float-card">
          <h4>{icon("award")} Skill training academy</h4>
          <p class="small muted mt-1">Every woman on the team takes four certified modules in her first year — food safety and hygiene, machine handling, quality awareness and basic accounts. After year two she can choose a specialisation: roasting, quality testing, packing line supervision or field documentation.</p>
          <div class="alloc__row"><span class="alloc__name">Food safety & hygiene</span><span class="alloc__val">100% of team</span></div>
          <div class="alloc__row"><span class="alloc__name">Machine handling</span><span class="alloc__val">62 women</span></div>
          <div class="alloc__row"><span class="alloc__name">Quality testing (lab)</span><span class="alloc__val">9 women</span></div>
          <div class="alloc__row"><span class="alloc__name">Accounts & documentation</span><span class="alloc__val">14 women</span></div>
          <div class="alloc__row"><span class="alloc__name">Spoken English (weekly class)</span><span class="alloc__val">34 attending</span></div>
        </div>
        <div class="float-card mt-3">
          <h4>{icon("megaphone")} What we are still fixing</h4>
          <p class="small muted mt-1">Our field sourcing team is still mostly men, because the role needs a two-wheeler and long travel. We are training two women into field roles this year and will publish how it goes — including if it fails.</p>
        </div>
      </div>
    </div>
    <div class="grid grid--2 mt-4">
      {quote_card(TESTIMONIALS[2], u(""))}{quote_card(TESTIMONIALS[3], u(""))}
    </div>
  </div>
</section>'''

    districts = [
        ("Haveri", "Byadagi chilli, maize", "148 farmers"),
        ("Gadag", "Coriander, wheat", "96 farmers"),
        ("Kolar", "Mango midi, chilli, vegetables", "72 farmers"),
        ("Ramanagara", "Mango midi, ragi", "58 farmers"),
        ("Mandya", "Paddy, jaggery, sugarcane", "54 farmers"),
        ("Tumakuru", "Copra, paddy, amla", "52 farmers"),
    ]
    rows = "".join(f'<tr><th scope="row">{E(d)}</th><td>{E(c)}</td><td>{E(n)}</td></tr>' for d, c, n in districts)
    farmers = f'''
<section class="section section--sand" id="farmers">
  <div class="wrap">
    <div class="split split--2">
      <div>
        <span class="eyebrow" {A("imp.farmers")}>{T("imp.farmers")}</span>
        <h2 class="mt-2">480 families, six districts, one price rule</h2>
        <p class="lede mt-2">We buy at the farm gate, weigh in front of the farmer, and pay within seven working days. In 2025 that averaged 22% above the local mandi rate for the same grade — and it was paid on time, every single month.</p>
        {check_list([
            "480 farmer families · 34 villages · 6 districts",
            "11 crops bought directly — chilli, coriander, turmeric, dal, groundnut, copra, paddy, jaggery, tamarind, amla, mango midi",
            "72% of our farmers are smallholders under 5 acres",
            "Free soil testing and seed for chilli, coriander and groundnut",
            "Post-harvest training on drying and grading — the difference between ₹80 and ₹140 a kilo",
            "Average payment time: 4.2 working days",
        ])}
        <div class="btn-row mt-3">
          <a class="btn btn--green" href="{u('farmers.html')}">{icon("seed")} Partner with us as a farmer</a>
        </div>
      </div>
      <div class="float-card">
        <h4>{icon("pin")} Where our produce comes from</h4>
        <table class="nutrition mt-2" style="max-width:100%">
          <thead><tr><th>District</th><th>What we buy</th><th>Farmers</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        <p class="small muted mt-2">Plus partner growers in Koppal, Chitradurga, Chikkaballapur and Hassan.</p>
        <div class="placeholder-img mt-2" style="min-height:170px">
          <span style="text-align:center;max-width:80%">Regional map of Karnataka showing the six sourcing districts —
          <a href="{u('farmers.html')}">see the full sourcing list on our farmers page</a>.</span>
        </div>
      </div>
    </div>
  </div>
</section>'''

    edu_cards = "".join(stat_card(s) for s in EDUCATION["stats"])
    edu_list = check_list(EDUCATION["what_it_covers"])
    education = f'''
<section class="section" id="education">
  <div class="wrap">
    {section_head("imp.education", "st.title" if False else "imp.education", None, center=True)}
    <div class="split split--2 mt-4">
      <div>
        <span class="tag tag--gold">{E(EDUCATION["headline"])}</span>
        <h3 class="mt-2">The year that decides the next ten</h3>
        <p class="lede mt-2">{E(EDUCATION["intro"])}</p>
        <h4 class="mt-3" style="font-size:1.15rem">What the fund covers</h4>
        <div class="mt-2">{edu_list}</div>
        <p class="small muted mt-2">{E(EDUCATION["footnote"])}</p>
      </div>
      <div>
        <img src="{u('assets/images/education-children.jpg')}" alt="Children of ApnaPan employees studying with a teacher" style="border-radius:var(--r-lg);box-shadow:var(--shadow-md)" loading="lazy">
        <div class="grid grid--2 mt-3" style="gap:1rem">{edu_cards}</div>
      </div>
    </div>
    <div class="callout mt-4">
      <h4>{icon("book")} Classic example: what ₹185 of masala actually pays for</h4>
      <p>One 200 g jar of bisibelebath masala sells for ₹185. Roughly ₹11 of that — the six percent — goes into the education fund. Nineteen jars fund a complete Class 10 year for one child, including coaching and the exam fee. Our best-selling pickle funds one child for a year for every 46 jars sold.</p>
    </div>
  </div>
</section>'''

    alloc_rows = ""
    for a in ALLOCATION:
        alloc_rows += f'''<div class="alloc__row">
        <span class="alloc__name"><i class="alloc__dot" style="background:{a["color"]}"></i>{E(a["name"])}</span>
        <span class="alloc__val">{a["pct"]}%</span>
        <span class="alloc__bar"><i data-alloc="{a["pct"]}" style="background:{a["color"]}"></i></span>
      </div>'''
    money_block = f'''
<section class="section section--sand">
  <div class="wrap split split--2">
    <div>
      <span class="eyebrow" {A("imp.money")}>{T("imp.money")}</span>
      <h2 class="mt-2">Where the money goes</h2>
      <p class="lede mt-2">Of every ₹100 you spend with us, ₹73 stays inside the village-to-jar chain: the farmer, the women who process it, and the school fund. Here is the full split for 2025.</p>
      <div class="btn-row mt-3">
        <a class="btn btn--outline" href="{u('blog.html')}">{icon("book")} Why we pay above the mandi</a>
      </div>
    </div>
    <div class="alloc">{alloc_rows}
      <p class="small muted mt-2">Illustrative allocation based on our 2025 cost structure. Figures rounded; audited statements available on request.</p>
    </div>
  </div>
</section>'''

    gallery = f'''
<section class="section" id="stories-photo">
  <div class="wrap">
    {section_head("imp.stories", "imp.stories", None, center=True)}
    <div class="gallery gallery--wide mt-4">
      <figure><img src="{u('assets/images/factory-women.jpg')}" alt="Women packing spices at the ApnaPan unit" loading="lazy">
        <figcaption><b>Packing hall, Doddaballapur</b>Seven women, one line, 4,000 packs a day.</figcaption></figure>
      <figure><img src="{u('assets/images/farmer-portrait.jpg')}" alt="Farmer Rudrappa H. in his field" loading="lazy">
        <figcaption><b>Rudrappa H., Byadagi</b>Chilli farmer of 22 years, partner since 2022.</figcaption></figure>
      <figure><img src="{u('assets/images/education-children.jpg')}" alt="Children studying" loading="lazy">
        <figcaption><b>Class 10 study circle</b>Evening coaching at the unit, twice a week.</figcaption></figure>
      <figure><img src="{u('assets/images/quality-control.jpg')}" alt="Quality control testing" loading="lazy">
        <figcaption><b>The lab</b>Moisture, salt and pH tested on every batch.</figcaption></figure>
      <figure><img src="{u('assets/images/distribution.jpg')}" alt="Loading boxes into a van" loading="lazy">
        <figcaption><b>Dispatch, 6am</b>From the unit to Bengaluru and beyond.</figcaption></figure>
      <figure><img src="{u('assets/images/hands-spices.jpg')}" alt="Hands sorting spices" loading="lazy">
        <figcaption><b>Grading table</b>Work that used to be unpaid, at home.</figcaption></figure>
    </div>
    <p class="script center mt-3" style="font-size:1.15rem">Photography from our unit and partner farms. No stock images.</p>
  </div>
</section>'''

    body = hero + women + farmers + education + money_block + gallery + newsletter_block(u)
    body = f'<main id="main">{body}</main>'
    return head(f"Our Impact — {BRAND['name']}", "Women's employment, farmer partnerships and the Class 10 education fund: the numbers, the programme and the stories behind ApnaPan's social impact in Karnataka.",
                "impact.html", u("assets/css/styles.css"), u, [ld_org(), ld_breadcrumb([("Home", "index.html"), ("Our Impact", "impact.html")])]) + header("nav.impact", u) + body + footer(u) + "</body></html>"


# =============================================================== SHOP
def shop(u):
    cats = live_categories()
    chips = "".join(f'''<button class="chip" type="button" data-filter="cat" data-value="{c["id"]}" aria-pressed="false">
        {E(c["label"])} <small>{sum(1 for p in PRODUCTS if p["category"] == c["id"])}</small></button>''' for c in cats)
    all_tag = sorted({t for p in PRODUCTS for t in p["tags"]})
    tag_chips = "".join(f'<button class="chip" type="button" data-filter="tag" data-value="{t}" aria-pressed="false">{t.title()}</button>' for t in all_tag)
    diets = sorted({d for p in PRODUCTS for d in p["diet"]})
    diet_chips = "".join(f'<button class="chip" type="button" data-filter="diet" data-value="{d.lower()}" aria-pressed="false">{E(d)}</button>' for d in diets)
    lo = min(p["price"] for p in PRODUCTS); hi = max(p["price"] for p in PRODUCTS)
    cards = "".join(product_card(p, u) for p in PRODUCTS)
    cat_intro = "".join(
        f'<div class="info-tile" id="cat-{c["id"]}">{icon("leaf")}<h4>{E(c["label"])}</h4><p>{E(c["blurb"])}</p></div>' for c in cats)

    filters = f'''
<aside class="filters" data-filters>
  <h3 style="font-family:var(--font-body);font-weight:700">
    <span>{icon("filter", size=16)} <span {A("shop.filters")}>{T("shop.filters")}</span></span>
    <button class="filter-toggle chip" type="button" data-filter-toggle aria-expanded="false">Show</button>
  </h3>
  <div class="filters__inner">
    <div class="filters__group">
      <h4 {A("shop.category")}>{T("shop.category")}</h4>
      <div class="chip-list">
        <button class="chip" type="button" data-filter="cat" data-value="" aria-pressed="true" {A("shop.all")}>{T("shop.all")}</button>
        {chips}
      </div>
    </div>
    <div class="filters__group">
      <h4 {A("shop.price")}>{T("shop.price")}</h4>
      <div class="range-row">
        <span class="small muted">₹100</span>
        <input type="range" min="{lo}" max="{hi}" step="5" value="{hi}" data-price-range aria-label="Maximum price">
        <span class="small muted" data-price-out>₹{hi}</span>
      </div>
      <p class="small muted" style="margin-top:.4rem">Maximum price · all sizes from {money(lo)} to {money(hi)}</p>
    </div>
    <div class="filters__group">
      <h4 {A("shop.tags")}>{T("shop.tags")}</h4>
      <div class="chip-list">{tag_chips}</div>
    </div>
    <div class="filters__group">
      <h4 {A("shop.diet")}>{T("shop.diet")}</h4>
      <div class="chip-list">{diet_chips}</div>
    </div>
    <div class="filters__foot">
      <button class="btn btn--outline btn--sm btn--block" type="button" data-filter-clear>{icon("trash")} <span {A("shop.clear")}>{T("shop.clear")}</span></button>
      <div class="ticker-note mt-2">{icon("truck")}<span>{T("common.freeship")}</span></div>
    </div>
  </div>
</aside>'''

    body = f'''
<section class="section post-hero">
  <div class="wrap">
    <span class="eyebrow">{BRAND["wordmark"]}</span>
    <h1 class="mt-2" {A("shop.title")}>{T("shop.title")}</h1>
    <p class="lede mt-2" style="max-width:64ch" {A("shop.lede")}>{T("shop.lede")}</p>
    <div class="grid grid--4 mt-4">{cat_intro}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap shop-layout">
    {filters}
    <div>
      <div class="shop-toolbar">
        <p class="shop-toolbar__count"><b data-result-count>{len(PRODUCTS)}</b> <span {A("shop.count")}>{T("shop.count")}</span></p>
        <label class="shop-toolbar__sort">
          <span {A("shop.sort")}>{T("shop.sort")}</span>
          <select class="select" data-sort>
            <option value="featured" {A("shop.sort_featured")}>{T("shop.sort_featured")}</option>
            <option value="price-low" {A("shop.sort_price_low")}>{T("shop.sort_price_low")}</option>
            <option value="price-high" {A("shop.sort_price_high")}>{T("shop.sort_price_high")}</option>
            <option value="rating" {A("shop.sort_rating")}>{T("shop.sort_rating")}</option>
            <option value="new" {A("shop.sort_new")}>{T("shop.sort_new")}</option>
          </select>
        </label>
      </div>
      <div class="active-filters" data-active-filters hidden></div>
      <div class="product-grid" data-grid>{cards}</div>
      <div class="no-results mt-3" data-no-results hidden>
        {icon("search", size=34)}
        <p class="mt-2" {A("shop.empty")}>{T("shop.empty")}</p>
        <button class="btn btn--outline mt-2" type="button" data-filter-clear {A("shop.emptycta")}>{T("shop.emptycta")}</button>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap grid grid--3">
    <div class="info-tile">{icon("gift")}<h4>Corporate gifting</h4>
    <p>Festival and onboarding hampers from 50 boxes, with your logo on a co-branded label and a card telling the story of the farmer behind each jar.</p>
    <a class="btn btn--outline btn--sm mt-2" href="{u('contact.html')}">Enquire</a></div>
    <div class="info-tile">{icon("box")}<h4>Wholesale & retail</h4>
    <p>Offered from 24 units per SKU across Karnataka and Maharashtra, with a 14-day credit cycle and merchandising support.</p>
    <a class="btn btn--outline btn--sm mt-2" href="{u('contact.html')}">Become a partner</a></div>
    <div class="info-tile">{icon("truck")}<h4>Shipping & returns</h4>
    <p>Free shipping above ₹599, dispatched within 24 hours from Bengaluru, and a no-argument replacement if anything arrives damaged.</p>
    <a class="btn btn--outline btn--sm mt-2" href="#shop-faq">Read the FAQs</a></div>
  </div>
</section>

<section class="section" id="shop-faq">
  <div class="wrap wrap--narrow">
    {faq_block(FAQS_SHIPPING, "footer.support")}
  </div>
</section>
{newsletter_block(u)}'''

    body = f'<main id="main">{body}</main>'
    jsonld = [ld_org(), ld_breadcrumb([("Home", "index.html"), ("Shop", "shop.html")]),
              {"@context": "https://schema.org", "@type": "ItemList", "name": "ApnaPan products",
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["name"],
                                    "url": f'{BRAND["url"]}/products/{p["slug"]}.html'} for i, p in enumerate(PRODUCTS)]}]
    return head(f"Shop — women-led spices, masalas & pickles made in Karnataka | {BRAND['name']}",
                "Buy farm-direct Karnataka masalas, ready mixes and pickles made by a women-run factory. Filter by category, size and price. Free shipping above ₹599.",
                "shop.html", u("assets/css/styles.css"), u, jsonld) + header("nav.shop", u) + body + footer(u) + "</body></html>"


# =============================================================== PRODUCT
def product(u, p):
    thumbs = [
        (p["img"], f'{p["name"]} {p["unit"]} pack'),
        ("assets/images/hands-spices.jpg", "Hands sorting spices at the ApnaPan unit"),
        ("assets/images/factory-women.jpg", "Women packing the product at the ApnaPan unit"),
    ]
    thumb_html = "".join(
        f'<button type="button" data-thumb aria-pressed="{"true" if i == 0 else "false"}">'
        f'<img src="{u(src)}" alt="{E(alt)}" loading="lazy"></button>' for i, (src, alt) in enumerate(thumbs))

    sizes = "".join(
        f'''<button class="size-opt" type="button" data-size-opt="{i}" data-price="{s["price"]}" aria-pressed="{"true" if i == 0 else "false"}">
        <b>{E(s["label"])}</b><span>{money(s["price"])}</span></button>''' for i, s in enumerate(p["sizes"]))

    ings = "".join(f'<li>{icon("leaf")}<span><b>{E(i["name"])}</b><span>{E(i["note"])}</span></span></li>' for i in p["ingredients"])
    nutr = "".join(f'<tr><th scope="row">{E(k)}</th><td>{E(v)}</td></tr>' for k, v in p["nutrition"])
    revs = "".join(f'''<article class="review">
        <div class="review__head">
          <div><b>{E(r["name"])}</b> <span class="muted small">· {E(r["city"])}</span></div>
          <div class="review__stars">{stars(r["rating"], "review__stars")} <time class="small muted">{E(r["date"])}</time></div>
        </div>
        <p>{E(r["text"])}</p>
      </article>''' for r in p["reviews"])

    related = [q for q in PRODUCTS if q["slug"] != p["slug"]][:3]
    related_cards = "".join(product_card(q, u) for q in related)

    sizes_g = " / ".join(s["label"] for s in p["sizes"])
    body = f'''
{breadcrumbs([("Home", "index.html"), ("Shop", "shop.html"), (p["name"], None)], u)}
<section class="section" style="padding-top:0">
  <div class="wrap pdp">
    <div class="pdp__gallery">
      <div class="pdp__main">
        <img src="{u(thumbs[0][0])}" alt="{E(p['name'])} — {E(p['type'])}, {E(p['unit'])}, made by ApnaPan in Karnataka"
             data-main-img width="620" height="1029" fetchpriority="high">
        <span class="pcard__flags" style="position:absolute;top:.9rem;left:.9rem">
          {"".join(f'<span class="tag{" tag--gold" if "bestseller" in p["tags"] else " tag--green"}">{mark(b, BADGE_KEY)}</span>' for b in p["badges"][:2])}
        </span>
      </div>
      <div class="pdp__thumbs">{thumb_html}</div>
      <div class="grid grid--2" style="gap:.6rem;margin-top:.4rem">
        <div class="badge-trust">{icon("women")}<div><b>Made by {E(p["made_by"]["name"])}</b><span>{E(p["made_by"]["role"])}</span></div></div>
        <div class="badge-trust">{icon("farm")}<div><b>{E(p["sourced"]["farmer"])}</b><span>{E(p["sourced"]["village"])}, {E(p["sourced"]["district"])}</span></div></div>
      </div>
    </div>

    <div>
      <span class="eyebrow">{mark(p["type"], TYPE_KEY)} · {E(p["unit"])}</span>
      <h1 class="pdp__title" data-pname="{p["slug"]}">{E(p["name"])}</h1>
      <p class="muted" style="font-family:var(--font-display);font-size:1.05rem">{E(p["name_kn"])} · {E(p["name_hi"])}</p>
      <div class="mt-1">{rating_line(p, u)}</div>
      <p class="lede mt-2">{E(p["short"])}</p>

      <div class="pdp__price-row">
        <span class="pdp__price" data-price-now>₹{p["price"]}<s>₹{p["mrp"]}</s></span>
        <span class="pdp__tax">Inclusive of all taxes · {E(p["unit"])}</span>
      </div>

      <div class="mt-3">
        <span class="field__label"><span {A("common.size")}>{T("common.size")}</span> <span class="muted">({sizes_g})</span></span>
        <div class="size-options">{sizes}</div>
      </div>

      <div class="pdp__buy">
        <button class="btn btn--lg" type="button" data-add="{p["slug"]}" data-size="0">{icon("cart")} <span {A("common.addcart")}>{T("common.addcart")}</span></button>
        <button class="btn btn--green btn--lg" type="button" data-buy="{p["slug"]}" data-size="0">{icon("check")} <span {A("common.buynow")}>{T("common.buynow")}</span></button>
      </div>

      <div class="made-by">
        {icon("women")}
        <div>
          <b>{T("common.madeby")}</b>
          <p><b>{E(p["made_by"]["name"])}</b>, {E(p["made_by"]["role"])} — with us since {E(p["made_by"]["since"])}. “{E(p["made_by"]["quote"])}”</p>
        </div>
      </div>

      <div class="pdp__trust">
        <div class="badge-trust">{icon("farm")}<div><b>{T("common.farmdirect")}</b><span>No middlemen</span></div></div>
        <div class="badge-trust">{icon("leaf")}<div><b>{T("common.nopreservative")}</b><span>Nothing artificial</span></div></div>
        <div class="badge-trust">{icon("flask")}<div><b>{T("pdp.qc")}</b><span>Lab-checked lot</span></div></div>
        <div class="badge-trust">{icon("school")}<div><b>6% to school</b><span>₹{round(p["price"] * 0.06)} from this jar</span></div></div>
      </div>

      <div class="tag-row mt-3">
        {"".join(f'<span class="tag tag--outline">{mark(b, BADGE_KEY)}</span>' for b in p["badges"])}
        {"".join(f'<span class="tag tag--green">{mark(d, DIET_KEY)}</span>' for d in p["diet"])}
        <span class="tag">{mark(p["spice_level"], SPICE_KEY)}</span>
      </div>
    </div>
  </div>
</section>

<section class="wrap pdp__tabs">
  <div class="tablist" role="tablist" aria-label="Product details">
    <button class="tab" role="tab" id="tab-story" aria-controls="panel-story" aria-selected="true" type="button">{T("pdp.story")}</button>
    <button class="tab" role="tab" id="tab-ing" aria-controls="panel-ing" aria-selected="false" type="button">{T("pdp.ingredients")}</button>
    <button class="tab" role="tab" id="tab-nutr" aria-controls="panel-nutr" aria-selected="false" type="button">{T("pdp.nutrition")}</button>
    <button class="tab" role="tab" id="tab-src" aria-controls="panel-src" aria-selected="false" type="button">{T("pdp.sourcing")}</button>
    <button class="tab" role="tab" id="tab-rev" aria-controls="panel-rev" aria-selected="false" type="button">{T("pdp.reviews")} ({p["reviews_count"]})</button>
  </div>

  <div class="tabpanel" role="tabpanel" id="panel-story" aria-labelledby="tab-story">
    <div class="split split--2">
      <div class="prose" style="max-width:64ch">
        <h3 style="margin-top:0">{T("pdp.story")}</h3>
        <p>{E(p["story"])}</p>
        <h4 style="font-size:1.15rem">How to use it</h4>
        <p>{E(p["how_to_use"])}</p>
        <p class="small muted">Storage: {E(p["storage"])} · Shelf life: {E(p["shelf_life"])} · Spice level: {E(p["spice_level"])}</p>
      </div>
      <div class="grid grid--2" style="gap:1rem;align-content:start">
        <div class="info-tile">{icon("clock")}<h4>Shelf life</h4><p>{E(p["shelf_life"])}</p></div>
        <div class="info-tile">{icon("sun")}<h4>Storage</h4><p>{E(p["storage"])}</p></div>
        <div class="info-tile">{icon("flame")}<h4>Spice level</h4><p>{E(p["spice_level"])}</p></div>
        <div class="info-tile">{icon("flask")}<h4>Batch tested</h4><p>Moisture, salt, pH and microbial tests on every lot. Batch code on the pack traces to the lab report.</p></div>
      </div>
    </div>
  </div>

  <div class="tabpanel" role="tabpanel" id="panel-ing" aria-labelledby="tab-ing" hidden>
    <div class="split split--2">
      <div>
        <h3>{T("pdp.ingredients")}</h3>
        <p class="lede">Nothing in this jar except what the label says. Each line names the farmer or the district it came from.</p>
        <ul class="ing-list mt-3">{ings}</ul>
      </div>
      <img src="{u('assets/images/hands-spices.jpg')}" alt="Raw spices being sorted before grinding" style="border-radius:var(--r-lg);box-shadow:var(--shadow-sm);align-self:start" loading="lazy">
    </div>
  </div>

  <div class="tabpanel" role="tabpanel" id="panel-nutr" aria-labelledby="tab-nutr" hidden>
    <div class="split split--2">
      <div>
        <h3>{T("pdp.nutrition")}</h3>
        <p class="lede">{T("pdp.per100")}</p>
        <table class="nutrition mt-3"><tbody>{nutr}</tbody></table>
        <p class="small muted mt-2">Values are typical averages for a spice blend and vary slightly by batch. Not a substitute for medical or dietary advice.</p>
      </div>
      <div class="info-tile">{icon("info")}<h4>What is not in it</h4>
        <p>No preservatives, no artificial colours, no anti-caking agents, no added starch or bulking flour, no refined sugar. Pickles use no acetic acid or vinegar — only rock salt, sun and oil.</p></div>
    </div>
  </div>

  <div class="tabpanel" role="tabpanel" id="panel-src" aria-labelledby="tab-src" hidden>
    <h3>{T("pdp.sourcing")}</h3>
    <p class="lede" style="max-width:70ch">This is the part most brands leave out. Here is exactly who grew what went into this batch, and what it was bought at.</p>
    <div class="split split--2 mt-3">
      <div class="sourcing-card">
        <img src="{u('assets/images/farmer-portrait.jpg')}" alt="{E(p['sourced']['farmer'])}" loading="lazy">
        <div class="sourcing-card__body">
          <span class="tag tag--green">{T("common.sourcedfrom")}</span>
          <h4 class="mt-1">{E(p["sourced"]["farmer"])}</h4>
          <p class="small muted">{E(p["sourced"]["village"])}, {E(p["sourced"]["district"])} · {E(p["sourced"]["crop"])}</p>
          <p class="mt-2" style="font-size:.94rem">Partner since {E(p["sourced"]["since"])}. “{E(p["sourced"]["quote"])}”</p>
        </div>
      </div>
      <div class="sourcing-card">
        <img src="{u('assets/images/factory-women.jpg')}" alt="{E(p['made_by']['name'])}" loading="lazy">
        <div class="sourcing-card__body">
          <span class="tag tag--terracotta">{T("pdp.madeby")}</span>
          <h4 class="mt-1">{E(p["made_by"]["name"])}</h4>
          <p class="small muted">{E(p["made_by"]["role"])} · with ApnaPan since {E(p["made_by"]["since"])}</p>
          <p class="mt-2" style="font-size:.94rem">“{E(p["made_by"]["quote"])}”</p>
        </div>
      </div>
    </div>
    <div class="callout mt-3" style="max-width:75ch">
      <h4>{icon("rupee")} What we paid for this crop</h4>
      <p>Our agreement price for this produce averaged 22% above the local mandi rate for the same grade, and payment was transferred within 7 working days of weighing at the farm gate. Full cost sheet: <a href="{u('blog.html')}">read the sourcing note</a>.</p>
    </div>
  </div>

  <div class="tabpanel" role="tabpanel" id="panel-rev" aria-labelledby="tab-rev" hidden>
    <h3>{T("pdp.reviews")}</h3>
    <div class="rating-summary">
      <div>
        <div class="rating-summary__big">{p["rating"]:.1f}</div>
        <div class="stars-bar">{stars(p["rating"], "stars-bar")}</div>
      </div>
      <div>
        <p><b>{p["reviews_count"]}</b> verified reviews</p>
        <p class="small muted">Ratings from customers who bought this product on our store, WhatsApp catalogue or at partner stores in Bengaluru.</p>
      </div>
      <button class="btn btn--outline btn--sm" type="button" data-review-open>Write a review</button>
    </div>
    <div class="grid" style="gap:1rem">{revs}</div>
    <form class="form-card mt-3" data-form="review" hidden style="max-width:640px">
      <h4>Write a review</h4>
      <p class="small muted">This demonstration form validates and thanks you, but does not submit anywhere — connect it to your review platform or database.</p>
      <label class="field"><span class="field__label">Your name <span class="req">*</span></span>
        <input class="input" name="name" required><span class="field__error">Please enter your name.</span></label>
      <label class="field"><span class="field__label">Rating <span class="req">*</span></span>
        <select class="select" name="rating" required><option value="">Choose…</option>
          <option>5 — Excellent</option><option>4 — Good</option><option>3 — Average</option><option>2 — Poor</option><option>1 — Very poor</option></select>
        <span class="field__error">Please choose a rating.</span></label>
      <label class="field"><span class="field__label">Your review <span class="req">*</span></span>
        <textarea class="textarea" name="text" required></textarea><span class="field__error">Please write a few words.</span></label>
      <div class="form-msg form-msg--ok" data-msg="ok" hidden>{icon("check")}<span>Thank you — your review has been noted.</span></div>
      <button class="btn" type="submit">{icon("check")} Send review</button>
    </form>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <h2>{T("pdp.related")}</h2>
    <div class="product-grid mt-3">{related_cards}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap wrap--narrow">
    {faq_block(FAQS_SHIPPING, "pdp.shipinfo")}
  </div>
</section>

<div class="sticky-buybar" data-sticky-buy data-visible="false">
  <div class="sticky-buybar__info">
    <b>{E(p["name"])} · {E(p["unit"])}</b>
    <span>₹{p["price"]} · {T("common.freeship")}</span>
  </div>
  <button class="btn" type="button" data-add="{p["slug"]}" data-size="0">{icon("cart")} <span {A("common.addcart")}>{T("common.addcart")}</span></button>
</div>'''

    body = f'<main id="main">{body}</main>'
    jsonld = [ld_product(p), ld_breadcrumb([("Home", "index.html"), ("Shop", "shop.html"), (p["name"], f'products/{p["slug"]}.html')])]
    return head(f'{p["name"]} — {p["type"]}, {p["unit"]} | {BRAND["name"]}',
                f'{p["short"]} Made by {p["made_by"]["name"]} with produce from {p["sourced"]["farmer"]}, {p["sourced"]["village"]}. ₹{p["price"]} for {p["unit"]}.',
                f'products/{p["slug"]}.html', u("assets/css/styles.css"), u, jsonld) + header("nav.shop", u) + body + footer(u) + "</body></html>"


# =============================================================== HOW IT WORKS
def how_it_works(u):
    steps = [
        {"n": 1, "k": "Sourcing", "t": "Bought at the farm gate, never at a mandi",
         "d": "Our field coordinator visits the farm before harvest, tests moisture on the spot with a handheld meter and agrees the grade-wise rate with the farmer in writing. On collection day we weigh at the village on a scale the farmer can read, print a slip, and take the whole lot — not just the best bags.",
         "img": "assets/images/hands-spices.jpg",
         "facts": [("4.2 days", "average payment time"), ("22%", "above mandi rate, 2025"), ("11 crops", "bought direct")]},
        {"n": 2, "k": "Processing", "t": "Slow-roasted, stone-ground, small batch",
         "d": "Spices are shade-dried for two days, then roasted in 12 kg batches in a drum roaster. Whole spices are added in a fixed order — coriander and cumin first, dals next, chilli last — because each reaches its right point at a different time. Grinding happens on a slow stone mill that keeps the oils in the powder instead of heating them out.",
         "img": "assets/images/factory-women.jpg",
         "facts": [("12 kg", "batch size"), ("62°C", "max grind temperature"), ("Tue & Fri", "roast days")]},
        {"n": 3, "k": "Quality control", "t": "Every batch tested, and one woman who can stop the line",
         "d": "Our in-house lab checks moisture, salt, pH, water activity and microbial load on every lot. A sensory panel of three tastes each batch against a retained reference sample. Our quality head, Nasreen Taj, has the authority to reject a batch outright and the founder cannot overrule her. Rejected lots are never blended into good ones.",
         "img": "assets/images/quality-control.jpg",
         "facts": [("7 tests", "per batch"), ("100%", "lots traceable"), ("2 batches", "rejected in 2026 so far")]},
        {"n": 4, "k": "Packaging", "t": "Sealed the same week, with names on the label",
         "d": "Glass jars for pickles and masalas that need to stay warm and aromatic; food-grade laminated pouches for ready mixes. Every pack carries a batch code, the packing date, the FSSAI licence number, the name of the woman who packed it and the farmer who grew the main ingredient. Nitrogen flushing is used for mixes to push shelf life without preservatives.",
         "img": "assets/images/products/akki-rotti-mix.jpg",
         "facts": [("Same week", "grind to pack"), ("Batch code", "on every pack"), ("Glass & recyclable", "packaging choices")]},
        {"n": 5, "k": "Distribution", "t": "Out of the door in 24 hours",
         "d": "Orders received before 4pm are dispatched the same day by our own team, from our unit to doorstep couriers, retail partners in Karnataka and Maharashtra, and gifting orders for corporates. Direct-to-home customers get a WhatsApp message with the tracking link the moment the pack leaves the building.",
         "img": "assets/images/distribution.jpg",
         "facts": [("24 hrs", "dispatch promise"), ("6 states", "retail presence"), ("3 partners", "logistics")]},
    ]
    blocks = ""
    for s in steps:
        facts = "".join(f'<div class="step__fact"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in s["facts"])
        blocks += f'''<article class="step reveal">
        <div class="step__media"><img src="{u(s["img"])}" alt="{E(s["k"])} at ApnaPan" loading="lazy"></div>
        <div class="step__body">
          <span class="step__kicker"><b>{s["n"]}</b> {E(s["k"])}</span>
          <h3>{E(s["t"])}</h3>
          <p>{E(s["d"])}</p>
          <div class="step__facts">{facts}</div>
        </div>
      </article>'''

    body = f'''
<section class="section post-hero">
  <div class="wrap">
    <span class="eyebrow" {A("how.eyebrow")}>{T("how.eyebrow")}</span>
    <h1 class="mt-2" style="max-width:26ch" {A("how.title")}>{T("how.title")}</h1>
    <p class="lede mt-2" style="max-width:64ch">Five steps, each with a check that a person signs their name to. This is what happens between a farmer's field and the jar in your kitchen.</p>
    <div class="journey mt-4">
      {"".join(f'<div class="jstep"><span class="jstep__num">0{i+1}</span><h5>{E(s["k"])}</h5><p>{E(s["facts"][0][0])} {E(s["facts"][0][1])}</p><span class="jstep__icon">{icon("arrow-r")}</span></div>' for i, s in enumerate(steps))}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="steps">{blocks}</div>
  </div>
</section>

<section class="section section--green">
  <div class="wrap split split--2">
    <div>
      <span class="eyebrow eyebrow--light">Traceability</span>
      <h2 class="mt-2">Type the batch code. See the whole story.</h2>
      <p class="lede mt-2" style="color:rgba(253,248,240,.85)">Every pack carries a code in the format <b>AP-2609-BIS-114</b>. Customers can enter it on our site to see the farmer, the village, the sourcing rate and the lab report for that exact lot. This is the piece of infrastructure we are proudest of, because it forces us to be accurate about everything else.</p>
      <div class="btn-row mt-3">
        <a class="btn btn--gold" href="{u('shop.html')}">{icon("cart")} Buy a pack and try it</a>
        <a class="btn btn--light" href="{u('blog.html')}">{icon("book")} Read a sourcing note</a>
      </div>
    </div>
    <div class="float-card" style="background:rgba(253,248,240,.06);border-color:rgba(253,248,240,.2);color:var(--cream)">
      <span class="eyebrow eyebrow--light">Batch AP-2609-BIS-114</span>
      <div class="alloc mt-2" style="background:transparent;border-color:rgba(253,248,240,.2);padding:0;box-shadow:none">
        <div class="alloc__row" style="border-color:rgba(253,248,240,.18)"><span class="alloc__name">Farmer</span><span class="alloc__val">Rudrappa H., Byadagi</span></div>
        <div class="alloc__row" style="border-color:rgba(253,248,240,.18)"><span class="alloc__name">Sourcing rate</span><span class="alloc__val">₹138 / kg</span></div>
        <div class="alloc__row" style="border-color:rgba(253,248,240,.18)"><span class="alloc__name">Roasted on</span><span class="alloc__val">9 Sept 2026</span></div>
        <div class="alloc__row" style="border-color:rgba(253,248,240,.18)"><span class="alloc__name">Ground & packed by</span><span class="alloc__val">Shivamma B.</span></div>
        <div class="alloc__row" style="border-color:rgba(253,248,240,.18)"><span class="alloc__name">Lab result</span><span class="alloc__val">Pass · moisture 7.4%</span></div>
      </div>
      <p class="small mt-2" style="color:rgba(253,248,240,.72)">Sample traceability record — the live lookup is on the roadmap for our next release.</p>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap wrap--narrow center">
    <h2>What happens after you order</h2>
    <div class="timeline mt-4" style="text-align:left;max-width:60ch;margin-inline:auto">
      <div class="tl-item"><span class="tl-year">Within 4 hours</span><h4>Order confirmed</h4><p>A confirmation email, and a WhatsApp message if you gave us a mobile number.</p></div>
      <div class="tl-item"><span class="tl-year">Same day, before 4pm</span><h4>Picked and packed</h4><p>Your pack is picked from the same week's batch, packed in recycled paper padding and weighed.</p></div>
      <div class="tl-item"><span class="tl-year">Next morning</span><h4>Leaves the unit</h4><p>Handed to the courier with a tracking link sent to you. Bengaluru delivery usually same or next day.</p></div>
      <div class="tl-item tl-item--now"><span class="tl-year">Day 3–6</span><h4>Arrives, and keeps improving</h4><p>Pickles get better for the first three months. If anything is wrong, tell us on WhatsApp within 7 days — we replace or refund without an argument.</p></div>
    </div>
  </div>
</section>
{newsletter_block(u)}'''
    body = f'<main id="main">{body}</main>'
    return head(f"How It Works — sourcing, processing, QC, packing, delivery | {BRAND['name']}",
                "Follow an ApnaPan jar through five steps: farm-gate sourcing, small-batch roasting, lab testing, packing with a traceable batch code, and 24-hour dispatch.",
                "how-it-works.html", u("assets/css/styles.css"), u, [ld_org(), ld_breadcrumb([("Home", "index.html"), ("How It Works", "how-it-works.html")])]) + header("nav.how", u) + body + footer(u) + "</body></html>"


# =============================================================== CAREERS
def careers(u):
    jobs = ""
    for j in JOBS:
        asks = "".join(f'<li>{icon("check")}<span>{E(a)}</span></li>' for a in j["asks"])
        jobs += f'''<article class="job reveal" id="{j["title"].lower().replace(" ", "-")}">
        <div class="job__top">
          <div>
            <h4>{E(j["title"])}</h4>
            <div class="job__meta mt-1">
              <span>{icon("building")} {E(j["dept"])}</span>
              <span>{icon("pin")} {E(j["location"])}</span>
              <span>{icon("clock")} {E(j["type"])}</span>
              <span>{icon("award")} {E(j["exp"])}</span>
            </div>
          </div>
          <span class="tag tag--green">{j["openings"]} opening{"s" if j["openings"] > 1 else ""}</span>
        </div>
        <p>{E(j["about"])}</p>
        <div>
          <span class="field__label">What we look for</span>
          <ul class="check-list">{asks}</ul>
        </div>
        <div class="job__foot">
          <span class="job__pay">{E(j["pay"])}</span>
          <button class="btn btn--sm" type="button" data-apply="{E(j["title"])}">{icon("arrow-r")} Apply for this role</button>
        </div>
      </article>'''

    benefits = "".join(badge_card(b) for b in BENEFITS)
    role_opts = "".join(f'<option>{E(j["title"])}</option>' for j in JOBS)

    body = f'''
<section class="post-hero">
  <div class="wrap section--tight">
    <span class="eyebrow" {A("car.eyebrow")}>{T("car.eyebrow")}</span>
    <h1 class="mt-2" {A("car.title")}>{T("car.title")}</h1>
    <p class="lede mt-2" style="max-width:64ch" {A("car.lede")}>{T("car.lede")}</p>
    <div class="btn-row mt-3">
      <a class="btn btn--lg" href="#apply">{icon("arrow-r")} <span {A("car.form")}>{T("car.form")}</span></a>
      <a class="btn btn--outline btn--lg" href="#roles">{icon("users")} <span {A("car.openings")}>{T("car.openings")}</span> ({len(JOBS)})</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--2">
    <div>
      <span class="eyebrow">{T("car.why")}</span>
      <h2 class="mt-2">A job here should change your household, not just your month</h2>
      <p class="lede mt-2">Half of our team had never worked outside their home before joining. We train on paid time, we promote from within, and we publish the wage band before we interview so nobody has to negotiate from a weak position.</p>
      <div class="grid grid--2 mt-3" style="gap:1rem">{benefits}</div>
    </div>
    <div>
      <img src="{u('assets/images/factory-women.jpg')}" alt="Women working on the ApnaPan packing line" style="border-radius:var(--r-lg);box-shadow:var(--shadow-md)" loading="lazy">
      <div class="callout mt-3">
        <h4>{icon("school")} Your child is enrolled in the education fund from your first month</h4>
        <p>Not after a year, not on performance — from the month you join. Fees, books, uniform, coaching and travel for the Class 10 year, and continuing support into Class 11 and 12.</p>
      </div>
      <div class="float-card mt-3">
        <h4>{icon("pause" if False else "info")} The honestly awkward questions</h4>
        <p class="small muted mt-1">Three quarters of our applications ask the same three things, so we answered them in full before you apply. Scroll to the FAQs below.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand" id="roles">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow" {A("car.openings")}>{T("car.openings")}</span>
      <h2>{len(JOBS)} roles open · September 2026</h2>
      <p class="lede">All roles are open to everyone and assessed on the same criteria. No night shifts for women, ever. Wages shown are the band for the role, not a starting offer to negotiate down from.</p>
    </div>
    <div class="grid grid--2 mt-4">{jobs}</div>
  </div>
</section>

<section class="section" id="apply">
  <div class="wrap split split--2">
    <div>
      <span class="eyebrow">{T("car.form")}</span>
      <h2 class="mt-2">Apply in two minutes</h2>
      <p class="lede mt-2">You can apply in Kannada, Hindi or English, and you can apply by WhatsApp voice note if writing is easier. We reply to every single application within 7 working days — including a no.</p>
      <div class="contact-line mt-3">{icon("whatsapp")}<div><b>Prefer WhatsApp?</b><span>Send a voice note to <a href="https://wa.me/{BRAND["whatsapp"]}">{BRAND["phone_display"]}</a> with your name, the role and your village or town.</span></div></div>
      <div class="contact-line mt-2">{icon("phone")}<div><b>Call the unit</b><span><a href="tel:{BRAND["phone"]}">{BRAND["phone_display"]}</a> · Mon–Sat, 9:30am–6:30pm</span></div></div>
      <div class="contact-line mt-2">{icon("women")}<div><b>Walk-in interviews</b><span>Every Wednesday, 10am–1pm at the Doddaballapur unit. Bring any ID and your qualification certificate if you have one.</span></div></div>
      <img src="{u('assets/images/quality-control.jpg')}" alt="Quality control training at the unit" class="mt-3" style="border-radius:var(--r-lg);box-shadow:var(--shadow-sm)" loading="lazy">
    </div>

    <form class="form-card" data-form="career" novalidate>
      <h3>{T("car.form")}</h3>
      <div class="form-msg form-msg--ok" data-msg="ok" hidden>{icon("check")}<span>Thank you. Your application is with us — we reply to every application within 7 working days.</span></div>
      <div class="form-msg form-msg--err" data-msg="err" hidden>{icon("info")}<span>Please check the highlighted fields and try again.</span></div>

      <label class="field"><span class="field__label">Full name <span class="req">*</span></span>
        <input class="input" name="name" required autocomplete="name" {AP("co.name")}>
        <span class="field__error">Please enter your name.</span></label>

      <div class="field-row">
        <label class="field"><span class="field__label">Mobile number <span class="req">*</span></span>
          <input class="input" name="phone" type="tel" required inputmode="numeric" autocomplete="tel" {AP("co.phone")}>
          <span class="field__error">Enter a 10-digit mobile number.</span></label>
        <label class="field"><span class="field__label">Email <span class="optional">(optional)</span></span>
          <input class="input" name="email" type="email" {AP("co.email")}></label>
      </div>

      <label class="field"><span class="field__label">Role you are applying for <span class="req">*</span></span>
        <select class="select" name="role" required data-role-select>
          <option value="">Choose a role…</option>
          {role_opts}
          <option>{T("car.anyrole")}</option>
        </select>
        <span class="field__error">Please choose a role.</span></label>

      <div class="field-row">
        <label class="field"><span class="field__label">Your qualification</span>
          <input class="input" name="qual" {AP("car.qual")} placeholder="10th pass / Diploma / BSc…"></label>
        <label class="field"><span class="field__label">Years of experience</span>
          <select class="select" name="exp"><option>None — first job</option><option>Less than 1 year</option><option>1–3 years</option><option>3–6 years</option><option>More than 6 years</option></select></label>
      </div>

      <label class="field"><span class="field__label">Your current town or village <span class="req">*</span></span>
        <input class="input" name="place" required {AP("car.currentloc")}>
        <span class="field__error">Please tell us where you are based.</span></label>

      <label class="field"><span class="field__label" {A("car.whyjoin")}>{T("car.whyjoin")}</span>
        <textarea class="textarea" name="why" placeholder="Two or three lines are enough."></textarea></label>

      <label class="check"><input type="checkbox" name="consent" required>
        <span>I agree to ApnaPan contacting me about this application. We never share your details with anyone else.</span></label>

      <button class="btn btn--block btn--lg" type="submit">{icon("check")} <span {A("common.submit")}>{T("common.submit")}</span></button>
      <p class="form-note">This demonstration form validates and confirms your entry but does not send it anywhere — connect it to your email service, Google Form or ATS before going live.</p>
    </form>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap wrap--narrow">
    {faq_block(CAREER_FAQ, "footer.support")}
  </div>
</section>
{newsletter_block(u)}'''
    body = f'<main id="main">{body}</main>'
    jobs_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Open roles at ApnaPan",
               "itemListElement": [{"@type": "JobPosting", "title": j["title"], "description": j["about"],
                                    "datePosted": "2026-09-01", "employmentType": "FULL_TIME",
                                    "hiringOrganization": {"@type": "Organization", "name": BRAND["name"]},
                                    "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress",
                                                   "addressLocality": j["location"], "addressRegion": "Karnataka", "addressCountry": "IN"}},
                                    "baseSalary": {"@type": "MonetaryAmount", "currency": "INR", "value": {"@type": "QuantitativeValue", "value": j["pay"]}}}
                                   for j in JOBS]}
    return head(f"Careers — work at a women-led food company in Karnataka | {BRAND['name']}",
                "Six open roles in spice processing, quality control, packaging, field sourcing, accounts and marketing. Fair wages, skill training and funded education for your children.",
                "careers.html", u("assets/css/styles.css"), u, [ld_org(), jobs_ld, ld_breadcrumb([("Home", "index.html"), ("Careers", "careers.html")])]) + header("nav.careers", u) + body + footer(u) + "</body></html>"


# =============================================================== FARMERS
def farmers(u):
    why = "".join(f'<div class="info-tile">{icon(w["icon"])}<h4>{E(w["title"])}</h4><p>{E(w["text"])}</p></div>' for w in FARMER_WHY)
    steps = "".join(f'''<div class="float-card">
        <span class="loop__idx">STEP {s["n"]}</span>
        <h4 class="mt-1">{E(s["title"])}</h4>
        <p class="small muted mt-1">{E(s["text"])}</p>
      </div>''' for s in FARMER_STEPS)

    rates = [
        ("Byadagi chilli (dry)", "Haveri, Gadag", "Dec–Mar", "₹118–145 / kg", "300 kg"),
        ("Coriander seed", "Gadag, Koppal", "Feb–Apr", "₹78–96 / kg", "300 kg"),
        ("Turmeric (dry finger)", "Mysuru, Chamarajanagara", "Jan–Mar", "₹92–118 / kg", "300 kg"),
        ("Groundnut (kernel)", "Koppal, Tumakuru", "Oct–Dec", "₹68–82 / kg", "500 kg"),
        ("Amla (fresh)", "Chitradurga, Tumakuru", "Dec–Feb", "₹42–56 / kg", "200 kg"),
        ("Mango midi (baby mango)", "Kolar, Ramanagara", "May–Jun", "₹60–85 / kg", "200 kg"),
        ("Toor / chana dal", "Kalaburagi, Bidar", "Nov–Jan", "₹105–128 / kg", "500 kg"),
        ("Copra (dry coconut)", "Tumakuru, Hassan", "Round the year", "₹96–124 / kg", "300 kg"),
    ]
    rate_rows = "".join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td></tr>' for a, b, c, d, e in rates)

    body = f'''
<section class="post-hero">
  <div class="wrap section--tight">
    <span class="eyebrow" {A("far.eyebrow")}>{T("far.eyebrow")}</span>
    <h1 class="mt-2" style="max-width:26ch" {A("far.title")}>{T("far.title")}</h1>
    <p class="lede mt-2" style="max-width:64ch">480 families across six districts sell to us directly. No commission agent, no deduction after loading, no waiting for money. If you grow chilli, coriander, turmeric, dal, groundnut, copra, paddy, amla or mango midi, we would like to buy from you this season.</p>
    <div class="btn-row mt-3">
      <a class="btn btn--lg btn--green" href="#farmer-form">{icon("seed")} <span {A("far.form")}>{T("far.form")}</span></a>
      <a class="btn btn--outline btn--lg" href="https://wa.me/{BRAND["whatsapp"]}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp us</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{T("far.why")}</span>
      <h2>Six reasons farmers stay with us</h2>
    </div>
    <div class="grid grid--3 mt-4">{why}</div>
  </div>
</section>

<section class="section section--sand" id="how">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{T("far.how")}</span>
      <h2>Four steps, one page of paper, no paperwork in a language you cannot read</h2>
      <p class="lede">The whole agreement fits on one page in Kannada and you keep a signed copy. If anything in it is violated, you can call the founder's number printed at the bottom.</p>
    </div>
    <div class="grid grid--4 mt-4">{steps}</div>

    <div class="float-card mt-4">
      <h3 class="mt-0">Indicative rate card · 2026–27 season</h3>
      <p class="small muted">These are indicative farm-gate bands for cleaned, properly dried produce. The final rate is agreed after a field visit and a moisture test, in writing, before your sowing season begins.</p>
      <div style="overflow-x:auto">
        <table class="nutrition mt-2" style="max-width:100%;min-width:620px">
          <thead><tr><th>Crop</th><th>Districts</th><th>Window</th><th>Indicative rate</th><th>Minimum quantity</th></tr></thead>
          <tbody>{rate_rows}</tbody>
        </table>
      </div>
      <p class="small muted mt-2">We hold the agreed rate even if the mandi price falls. If the mandi price rises by more than 10% before your harvest, we revise your rate upward.</p>
    </div>
  </div>
</section>

<section class="section" id="farmer-form">
  <div class="wrap split split--2">
    <div>
      <span class="eyebrow">{T("far.form")}</span>
      <h2 class="mt-2">Tell us about your farm</h2>
      <p class="lede mt-2">Two minutes is enough. Our field coordinator for your district will call you within two working days and visit your field within ten days.</p>
      {check_list([
          "Free soil test for the plot you plan to sow this season",
          "Certified seed for chilli, coriander and groundnut on request",
          "A written rate before sowing, held for the season",
          "Payment by bank transfer in your own account within 7 working days",
          "No deductions after the goods have left your village",
      ])}
      <div class="contact-line mt-3">{icon("phone")}<div><b>Talk to the sourcing desk</b><span><a href="tel:{BRAND["phone"]}">{BRAND["phone_display"]}</a> · <a href="mailto:{BRAND["emails"]["farmers"]}">{BRAND["emails"]["farmers"]}</a> · Kannada, Hindi and English</span></div></div>
      <img src="{u('assets/images/farmer-portrait.jpg')}" alt="A farmer partner of ApnaPan" class="mt-3" style="border-radius:var(--r-lg);box-shadow:var(--shadow-sm)" loading="lazy">
    </div>

    <form class="form-card" data-form="farmer" novalidate>
      <h3>{T("far.form")}</h3>
      <div class="form-msg form-msg--ok" data-msg="ok" hidden>{icon("check")}<span>Thank you. Our sourcing desk will call you within 2 working days — usually the same day.</span></div>
      <div class="form-msg form-msg--err" data-msg="err" hidden>{icon("info")}<span>Please check the highlighted fields and try again.</span></div>

      <label class="field"><span class="field__label">Your name <span class="req">*</span></span>
        <input class="input" name="name" required autocomplete="name" placeholder="e.g. Rudrappa H.">
        <span class="field__error">Please enter your name.</span></label>

      <div class="field-row">
        <label class="field"><span class="field__label">Mobile number <span class="req">*</span></span>
          <input class="input" name="phone" type="tel" inputmode="numeric" required autocomplete="tel" placeholder="10-digit mobile">
          <span class="field__error">Enter a 10-digit mobile number.</span></label>
        <label class="field"><span class="field__label">Village / taluk <span class="req">*</span></span>
          <input class="input" name="village" required {AP("far.village")}>
          <span class="field__error">Please tell us your village or taluk.</span></label>
      </div>

      <div class="field-row">
        <label class="field"><span class="field__label">District <span class="req">*</span></span>
          <select class="select" name="district" required>
            <option value="">Choose…</option>
            <option>Haveri</option><option>Gadag</option><option>Koppal</option><option>Kolar</option>
            <option>Ramanagara</option><option>Mandya</option><option>Tumakuru</option><option>Chitradurga</option>
            <option>Chikkaballapur</option><option>Hassan</option><option>Mysuru</option><option>Kalaburagi</option>
            <option>Bengaluru Rural</option><option>Other Karnataka district</option><option>Outside Karnataka</option>
          </select>
          <span class="field__error">Please choose your district.</span></label>
        <label class="field"><span class="field__label">Land under cultivation</span>
          <select class="select" name="land"><option>Under 2 acres</option><option>2–5 acres</option><option>5–10 acres</option><option>More than 10 acres</option></select></label>
      </div>

      <label class="field"><span class="field__label">Crops you grow <span class="req">*</span></span>
        <input class="input" name="crops" required placeholder="e.g. Byadagi chilli, coriander, groundnut" {AP("far.crops")}>
        <span class="field__error">Please list your main crops.</span></label>

      <div class="field-row">
        <label class="field"><span class="field__label">Approximate quantity <span class="req">*</span></span>
          <input class="input" name="qty" required placeholder="e.g. 1,200 kg chilli" {AP("far.qty")}>
          <span class="field__error">Please tell us roughly how much you can supply.</span></label>
        <label class="field"><span class="field__label">Harvest window</span>
          <select class="select" name="window"><option>Ready within 1 month</option><option>1–3 months</option><option>3–6 months</option><option>Next season</option></select></label>
      </div>

      <label class="field"><span class="field__label">Anything else we should know?</span>
        <textarea class="textarea" name="notes" placeholder="Storage facility, previous buyers, moisture problems, transport…"></textarea></label>

      <label class="check"><input type="checkbox" name="consent" required>
        <span>ApnaPan may call or WhatsApp me about this enquiry.</span></label>

      <button class="btn btn--green btn--block btn--lg" type="submit">{icon("seed")} <span {A("common.submit")}>{T("common.submit")}</span></button>
      <p class="form-note">This demonstration form validates and confirms your entry but does not send it anywhere — connect it to your email service, CRM or WhatsApp Business API before going live.</p>
    </form>
  </div>
</section>

<section class="section section--green">
  <div class="wrap">
    <div class="section-head section-head--center">
      <span class="eyebrow eyebrow--light">In their words</span>
      <h2>Farmers who were our first calls in 2019</h2>
    </div>
    <div class="grid grid--3 mt-4">
      {quote_card(TESTIMONIALS[0], u(""))}{quote_card(TESTIMONIALS[1], u(""))}{quote_card(TESTIMONIALS[5], u(""))}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    {faq_block(FARMER_FAQ, "footer.support")}
  </div>
</section>
{newsletter_block(u)}'''
    body = f'<main id="main">{body}</main>'
    return head(f"For Farmers — sell directly to ApnaPan, paid in 7 days",
                "A price agreed before you sow, weighing in front of you, payment within 7 working days and free soil testing. Partner with ApnaPan as a spice or produce supplier in Karnataka.",
                "farmers.html", u("assets/css/styles.css"), u, [ld_org(), ld_faq(FARMER_FAQ), ld_breadcrumb([("Home", "index.html"), ("For Farmers", "farmers.html")])]) + header("nav.farmers", u) + body + footer(u) + "</body></html>"


# =============================================================== BLOG
def blog(u):
    cards = ""
    for i, p in enumerate(POSTS):
        big = ' style="grid-column:span 2"' if i == 0 else ""
        cards += f'''<article class="card card--hover"{big}>
        <a class="card__media" href="{u('blog/' + p["slug"] + '.html')}" style="display:block">
          <img src="{u(p["img"])}" alt="{E(p["title"])}" loading="lazy" style="aspect-ratio:16/9;width:100%;object-fit:cover">
        </a>
        <div class="card__body">
          <div class="tag-row"><span class="tag tag--green">{E(p["category"])}</span>
            <span class="tag tag--outline">{E(p["date_display"])}</span>
            <span class="tag tag--outline">{E(p["read"])}</span></div>
          <h3 style="font-size:1.28rem"><a href="{u('blog/' + p["slug"] + '.html')}">{E(p["title"])}</a></h3>
          <p class="small muted">{E(p["excerpt"])}</p>
          <div class="card__foot">
            <span class="small muted">{E(p["author"])}</span>
            <a class="btn btn--outline btn--sm" href="{u('blog/' + p["slug"] + '.html')}">{T("common.readmore")} {icon("arrow-r")}</a>
          </div>
        </div>
      </article>'''

    body = f'''
<section class="post-hero">
  <div class="wrap section--tight">
    <span class="eyebrow" {A("blog.eyebrow")}>{T("blog.eyebrow")}</span>
    <h1 class="mt-2" {A("blog.title")}>{T("blog.title")}</h1>
    <p class="lede mt-2" style="max-width:64ch">Sourcing notes, ingredient guides, what we got wrong, and the occasional argument about how much jaggery belongs in an amla pickle. Written by the people doing the work.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid--2" style="align-items:stretch">{cards}</div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="newsletter">
      <div class="newsletter__inner">
        <div>
          <span class="eyebrow eyebrow--light">Every month</span>
          <h2>The harvest letter</h2>
          <p>What we bought, from which farms, at what rate — plus one recipe and the school results we are proud of.</p>
        </div>
        <form data-form="newsletter" novalidate>
          <div class="form-msg form-msg--ok" data-msg="ok" hidden>{icon("check")}<span>You are on the list — the next letter goes out on the 1st.</span></div>
          <label class="field" style="margin-bottom:.7rem"><span class="sr-only">Email</span>
            <input class="input" type="email" name="email" required placeholder="your@email.com"></label>
          <button class="btn btn--gold" type="submit">{icon("mail")} Subscribe</button>
        </form>
      </div>
    </div>
  </div>
</section>'''
    body = f'<main id="main">{body}</main>'
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "ApnaPan Kitchen Notes",
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "datePublished": p["date"],
                        "url": f'{BRAND["url"]}/blog/{p["slug"]}.html', "author": {"@type": "Person", "name": p["author"]}} for p in POSTS]}
    return head(f"Blog — sourcing notes, ingredient guides & impact updates | {BRAND['name']}",
                "Notes from ApnaPan's unit and partner farms: why we pay above the mandi, how Byadagi chilli behaves in a pan, and inside our Class 10 education fund.",
                "blog.html", u("assets/css/styles.css"), u, [ld_org(), ld, ld_breadcrumb([("Home", "index.html"), ("Blog", "blog.html")])]) + header("nav.blog", u) + body + footer(u) + "</body></html>"


def post_page(u, p):
    body_html = ""
    toc = []
    for kind, val in p["body"]:
        if kind == "p":
            body_html += f'<p>{E(val)}</p>'
        elif kind == "h2":
            anchor = val.lower().replace(" ", "-").replace(",", "").replace(":", "").replace("’", "")[:46]
            toc.append((val, anchor))
            body_html += f'<h2 id="{anchor}">{E(val)}</h2>'
        elif kind == "blockquote":
            body_html += f'<blockquote>{E(val)}</blockquote>'
        elif kind == "ul":
            body_html += "<ul>" + "".join(f"<li>{E(x)}</li>" for x in val) + "</ul>"
    toc_html = "".join(f'<li><a href="#{a}">{E(t)}</a></li>' for t, a in toc)
    others = [q for q in POSTS if q["slug"] != p["slug"]][:3]
    rel = "".join(f'''<article class="card card--hover">
        <a class="card__media" href="{u('blog/' + q["slug"] + '.html')}" style="display:block">
          <img src="{u(q["img"])}" alt="{E(q["title"])}" loading="lazy" style="aspect-ratio:16/9;object-fit:cover"></a>
        <div class="card__body"><span class="tag tag--green" style="align-self:flex-start">{E(q["category"])}</span>
          <h4><a href="{u('blog/' + q["slug"] + '.html')}">{E(q["title"])}</a></h4>
          <p class="small muted">{E(q["excerpt"])}</p></div></article>''' for q in others)

    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
          "description": p["excerpt"], "datePublished": p["date"], "dateModified": p["date"],
          "image": f'{BRAND["url"]}/{p["img"]}', "author": {"@type": "Person", "name": p["author"]},
          "publisher": {"@type": "Organization", "name": BRAND["name"]},
          "mainEntityOfPage": f'{BRAND["url"]}/blog/{p["slug"]}.html', "articleSection": p["category"]}

    body = f'''
{breadcrumbs([("Home", "index.html"), ("Blog", "blog.html"), (p["title"][:44] + "…", None)], u)}
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="article-meta">
      <span class="tag tag--green">{E(p["category"])}</span>
      <span>{icon("calendar", size=14)} {E(p["date_display"])}</span>
      <span>{icon("clock", size=14)} {E(p["read"])}</span>
      <span>{icon("users", size=14)} {E(p["author"])}</span>
    </div>
    <h1 class="mt-2" style="max-width:30ch">{E(p["title"])}</h1>
    <p class="lede mt-2" style="max-width:66ch">{E(p["excerpt"])}</p>
    <img src="{u(p["img"])}" alt="{E(p["title"])}" class="mt-3" style="border-radius:var(--r-lg);box-shadow:var(--shadow-md);width:100%;max-height:520px;object-fit:cover" fetchpriority="high">
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap split split--2-3" style="gap:clamp(1.6rem,4vw,3rem);align-items:start">
    <aside style="position:sticky;top:96px">
      <div class="toc"><h4>{T("blog.related") if False else "On this page"}</h4><ol>{toc_html}</ol></div>
      <div class="share-row mt-3">
        <span>{T("common.share")}:</span>
        <a href="https://wa.me/?text={p["title"].replace(" ", "%20")}" target="_blank" rel="noopener" aria-label="Share on WhatsApp">{icon("whatsapp")}</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={BRAND["url"]}/blog/{p["slug"]}.html" target="_blank" rel="noopener" aria-label="Share on Facebook">{icon("facebook")}</a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={BRAND["url"]}/blog/{p["slug"]}.html" target="_blank" rel="noopener" aria-label="Share on LinkedIn">{icon("linkedin")}</a>
        <button type="button" data-copy-link aria-label="Copy link">{icon("info")}</button>
      </div>
      <div class="callout mt-3">
        <h4>{icon("cart")} Try it yourself</h4>
        <p>Every claim in this post is in a jar on our shop. Free shipping above ₹599.</p>
        <a class="btn btn--sm mt-2" href="{u('shop.html')}">{T("common.shop")}</a>
      </div>
    </aside>
    <div class="prose">{body_html}
      <hr>
      <p class="small muted">Written by {E(p["author"])} for ApnaPan. Figures quoted are from our own records and are illustrative on this demonstration site.</p>
      <div class="btn-row mt-2">
        <a class="btn btn--outline" href="{u('blog.html')}">{icon("arrow-r")} All posts</a>
        <a class="btn" href="{u('shop.html')}">{icon("cart")} {T("common.shop")}</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <h2>{T("blog.related")}</h2>
    <div class="grid grid--3 mt-3">{rel}</div>
  </div>
</section>
{newsletter_block(u)}'''
    body = f'<main id="main">{body}</main>'
    return head(f'{p["title"]} | {BRAND["name"]}', p["excerpt"], f'blog/{p["slug"]}.html',
                u("assets/css/styles.css"), u, [ld, ld_breadcrumb([("Home", "index.html"), ("Blog", "blog.html"), (p["title"], f'blog/{p["slug"]}.html')])]) + header("nav.blog", u) + body + footer(u) + "</body></html>"


# =============================================================== CONTACT
def contact(u):
    a0, a1 = BRAND["addresses"]
    subjects = ["con.order", "con.wholesale", "con.csr", "con.gifting", "con.visit", "con.press", "con.other"]
    subj_opts = "".join(f'<option {A(k)}>{T(k)}</option>' for k in subjects)

    body = f'''
<section class="post-hero">
  <div class="wrap section--tight">
    <span class="eyebrow" {A("con.eyebrow")}>{T("con.eyebrow")}</span>
    <h1 class="mt-2" style="max-width:24ch" {A("con.title")}>{T("con.title")}</h1>
    <p class="lede mt-2" style="max-width:64ch" {A("con.lede")}>{T("con.lede")}</p>
    <div class="btn-row mt-3">
      <a class="btn btn--lg btn--wa" href="https://wa.me/{BRAND["whatsapp"]}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp {BRAND["phone_display"]}</a>
      <a class="btn btn--outline btn--lg" href="tel:{BRAND["phone"]}">{icon("phone")} Call us</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--2-3" style="gap:clamp(1.6rem,4vw,3rem);align-items:start">
    <div class="contact-aside">
      <div class="contact-line">{icon("phone")}<div><b>Phone & WhatsApp</b><span><a href="tel:{BRAND["phone"]}">{BRAND["phone_display"]}</a></span><span class="small muted">{BRAND["hours"]}</span></div></div>
      <div class="contact-line">{icon("mail")}<div><b>Email</b>
        <span><a href="mailto:{BRAND["emails"]["hello"]}">{BRAND["emails"]["hello"]}</a> — orders, shipping, general</span>
        <span><a href="mailto:{BRAND["emails"]["farmers"]}">{BRAND["emails"]["farmers"]}</a> — farmer sourcing</span>
        <span><a href="mailto:{BRAND["emails"]["careers"]}">{BRAND["emails"]["careers"]}</a> — jobs</span>
        <span><a href="mailto:{BRAND["emails"]["csr"]}">{BRAND["emails"]["csr"]}</a> — CSR & partnerships</span></div></div>
      <div class="contact-line">{icon("building")}<div><b>{E(a0["label"])}</b>
        <span>{E(", ".join(a0["lines"]))}</span><span class="small muted">{E(a0["note"])}</span></div></div>
      <div class="contact-line">{icon("pin")}<div><b>{E(a1["label"])}</b>
        <span>{E(", ".join(a1["lines"]))}</span><span class="small muted">{E(a1["note"])}</span></div></div>
      <div class="contact-line">{icon("calendar")}<div><b>Factory visits</b>
        <span>Tuesday and Thursday, 10am–4pm, by appointment. You will see the roasting line, the QC lab and the packing table — and meet the team. Wheelchair accessible.</span></div></div>
      <div class="map-frame">
        <div class="placeholder-img" style="min-height:220px">
          <span style="text-align:center;max-width:80%">Map placeholder — embed your Google Maps location here.
            <br><a href="https://www.google.com/maps/search/?api=1&amp;query=KIADB+Industrial+Area+Doddaballapur" target="_blank" rel="noopener">Open the unit in Google Maps →</a></span>
        </div>
      </div>
      <div class="float-card" id="csr">
        <h4>{icon("gift")} CSR, partnership & gifting enquiries</h4>
        <p class="small muted mt-1">We work with CSR programmes, retail distributors, exporters, restaurant groups and corporate gifting teams. What we can offer:</p>
        {check_list([
            "Co-branded festival hampers from 50 boxes, with the farmer story in each box",
            "Employee gifting with a printed card and a QR code to the batch traceability page",
            "CSR partnership: fund the Class 10 programme for a named cohort, with quarterly reporting",
            "Farm exposure visits for CSR teams and their leadership",
            "Wholesale supply from 24 units per SKU with merchandising support",
        ])}
        <p class="small muted mt-2">For partnership decks and price lists, write to <a href="mailto:{BRAND["emails"]["csr"]}">{BRAND["emails"]["csr"]}</a> — we reply within two working days.</p>
      </div>
    </div>

    <div>
      <form class="form-card" data-form="contact" novalidate>
        <h3>{T("con.form")}</h3>
        <div class="form-msg form-msg--ok" data-msg="ok" hidden>{icon("check")}<span>Thank you — your message is with us. We reply within one working day.</span></div>
        <div class="form-msg form-msg--err" data-msg="err" hidden>{icon("info")}<span>Please check the highlighted fields and try again.</span></div>

        <label class="field"><span class="field__label">Your name <span class="req">*</span></span>
          <input class="input" name="name" required autocomplete="name"><span class="field__error">Please enter your name.</span></label>

        <div class="field-row">
          <label class="field"><span class="field__label">Mobile number <span class="req">*</span></span>
            <input class="input" name="phone" type="tel" inputmode="numeric" required autocomplete="tel"><span class="field__error">Enter a 10-digit mobile number.</span></label>
          <label class="field"><span class="field__label">Email</span>
            <input class="input" name="email" type="email" autocomplete="email"></label>
        </div>

        <label class="field"><span class="field__label" {A("con.reason")}>{T("con.reason")}</span>
          <select class="select" name="subject">{subj_opts}</select></label>

        <label class="field"><span class="field__label">Organisation <span class="optional">(if applicable)</span></span>
          <input class="input" name="org" placeholder="Company / NGO / press outlet"></label>

        <label class="field"><span class="field__label">Message <span class="req">*</span></span>
          <textarea class="textarea" name="message" required placeholder="Tell us what you need and we will come back with specifics."></textarea>
          <span class="field__error">Please write a short message.</span></label>

        <label class="check"><input type="checkbox" name="consent" required>
          <span>I agree to ApnaPan contacting me about this enquiry.</span></label>
        <span class="field__error" style="display:none" data-consent-error>Please tick the consent box.</span>

        <button class="btn btn--block btn--lg" type="submit">{icon("mail")} <span {A("common.submit")}>{T("common.submit")}</span></button>
        <p class="form-note">Demonstration form — it validates and confirms but does not send anywhere. Connect it to your email service or CRM before going live.</p>
      </form>

      <div class="grid grid--2 mt-3" style="gap:1rem">
        <div class="info-tile">{icon("truck")}<h4>Order support</h4><p>Free shipping above ₹599 · dispatch within 24 hours · 7-day no-argument replacement on damaged or wrong items.</p></div>
        <div class="info-tile">{icon("users")}<h4>Wholesale desk</h4><p>Retail and distribution partners from 24 units per SKU. 14-day credit cycle for repeat partners, with merchandising support.</p></div>
        <div class="info-tile">{icon("megaphone")}<h4>Press & media</h4><p>Photographs, the founder's bio and impact data available on request. We are happy to arrange farmer and employee interviews with consent.</p></div>
        <div class="info-tile">{icon("shield")}<h4>Certifications</h4><p>{E(BRAND["reg"]["fssai"])}<br>{E(BRAND["reg"]["gstin"])}<br>{E(BRAND["reg"]["udyam"])}</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap wrap--narrow">
    {faq_block(FAQS_SHIPPING, "footer.support")}
  </div>
</section>
{newsletter_block(u)}'''
    body = f'<main id="main">{body}</main>'
    places = {"@context": "https://schema.org", "@type": "Organization", "name": BRAND["name"],
              "url": BRAND["url"], "email": BRAND["emails"]["hello"], "telephone": BRAND["phone"],
              "address": [{"@type": "PostalAddress", "streetAddress": a["lines"][0], "addressLocality": a["lines"][1],
                           "addressRegion": "Karnataka", "addressCountry": "IN"} for a in BRAND["addresses"]]}
    return head(f"Contact {BRAND['name']} — factory visits, wholesale, CSR & orders",
                "Call, WhatsApp or write to ApnaPan. Factory visits on Tuesdays and Thursdays, wholesale and CSR partnerships, order support and press enquiries.",
                "contact.html", u("assets/css/styles.css"), u, [places, ld_faq(FAQS_SHIPPING), ld_breadcrumb([("Home", "index.html"), ("Contact", "contact.html")])]) + header("nav.contact", u) + body + footer(u) + "</body></html>"


# =============================================================== CHECKOUT
def checkout(u):
    body = f'''
<section class="section post-hero">
  <div class="wrap section--tight">
    <div class="steps-indicator">
      <b><span class="si-num">1</span> Basket</b> <span>→</span>
      <b><span class="si-num">2</span> Details</b> <span>→</span>
      <p><span class="si-num" style="background:var(--line-strong)">3</span> Payment</p>
    </div>
    <h1 {A("co.title")}>{T("co.title")}</h1>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap checkout-layout">
    <form data-form="checkout" novalidate id="checkout-form">
      <div class="checkout-card">
        <h3><span class="step-no">1</span> <span {A("co.contact")}>{T("co.contact")}</span></h3>
        <div class="field-row">
          <label class="field"><span class="field__label">{T("co.name")} <span class="req">*</span></span>
            <input class="input" name="name" required autocomplete="name"><span class="field__error">Please enter your name.</span></label>
          <label class="field"><span class="field__label">{T("co.phone")} <span class="req">*</span></span>
            <input class="input" name="phone" type="tel" inputmode="numeric" required autocomplete="tel">
            <span class="field__error">Enter a 10-digit mobile number.</span></label>
        </div>
        <label class="field"><span class="field__label">{T("co.email")} <span class="req">*</span></span>
          <input class="input" name="email" type="email" required autocomplete="email">
          <span class="field__error">Please enter a valid email address.</span></label>
      </div>

      <div class="checkout-card">
        <h3><span class="step-no">2</span> <span {A("co.delivery")}>{T("co.delivery")}</span></h3>
        <label class="field"><span class="field__label">{T("co.address1")} <span class="req">*</span></span>
          <input class="input" name="address1" required autocomplete="address-line1"><span class="field__error">Please enter your address.</span></label>
        <label class="field"><span class="field__label">{T("co.address2")}</span>
          <input class="input" name="address2" autocomplete="address-line2"></label>
        <div class="field-row">
          <label class="field"><span class="field__label">{T("co.city")} <span class="req">*</span></span>
            <input class="input" name="city" required autocomplete="address-level2"><span class="field__error">Please enter your city.</span></label>
          <label class="field"><span class="field__label">{T("co.state")} <span class="req">*</span></span>
            <select class="select" name="state" required>
              <option value="">Choose…</option>
              <option>Karnataka</option><option>Maharashtra</option><option>Tamil Nadu</option><option>Telangana</option>
              <option>Andhra Pradesh</option><option>Kerala</option><option>Goa</option><option>Delhi NCR</option>
              <option>Gujarat</option><option>West Bengal</option><option>Uttar Pradesh</option><option>Other state</option>
            </select><span class="field__error">Please choose your state.</span></label>
        </div>
        <div class="field-row">
          <label class="field"><span class="field__label">{T("co.pincode")} <span class="req">*</span></span>
            <input class="input" name="pincode" inputmode="numeric" required autocomplete="postal-code" pattern="[0-9]{6}">
            <span class="field__error">Enter a 6-digit PIN code.</span></label>
          <label class="field"><span class="field__label">{T("co.notes")}</span>
            <input class="input" name="notes" placeholder="Gate code, landmark, delivery timing…"></label>
        </div>
      </div>

      <div class="checkout-card">
        <h3><span class="step-no">3</span> <span {A("co.payment")}>{T("co.payment")}</span></h3>
        <div class="pay-methods">
          <label class="pay-opt">
            <input type="radio" name="payment" value="upi" checked>
            <span><b>{T("co.upi")}</b><span>{T("co.upinote")}</span></span>
          </label>
          <label class="pay-opt">
            <input type="radio" name="payment" value="cod">
            <span><b>{T("co.cod")}</b><span>{T("co.codnote")}</span></span>
          </label>
        </div>
        <p class="secure-note">{icon("lock")} <span {A("co.secure")}>{T("co.secure")}</span></p>
      </div>

      <div class="form-msg form-msg--err" data-msg="err" hidden>{icon("info")}<span>Please check the highlighted fields and try again.</span></div>
      <button class="btn btn--lg btn--block" type="submit" data-place-order>{icon("lock")} <span {A("co.place")}>{T("co.place")}</span></button>
      <p class="form-note center">{T("co.demo")}</p>
    </form>

    <aside class="order-summary">
      <h3>{T("co.summary")}</h3>
      <div data-checkout-lines></div>
      <div class="summary-row"><span>{T("common.subtotal")}</span><span data-co-subtotal>₹0</span></div>
      <div class="summary-row"><span>{T("co.handling")}</span><span data-co-cod>—</span></div>
      <div class="summary-row"><span>{T("cart.ship")}</span><span data-co-ship>—</span></div>
      <div class="summary-row summary-row--total"><span>{T("common.total")}</span><span data-co-total>₹0</span></div>
      <div class="ticker-note mt-2">{icon("school")}<span>6% of this order (₹<span data-co-school>0</span>) goes into the children's education fund.</span></div>
      <div class="secure-note" style="margin-top:.9rem">{icon("shield")} Secure checkout · Razorpay / UPI / cards / COD</div>
    </aside>
  </div>
</section>

<section class="section section--sand" data-checkout-success hidden>
  <div class="wrap wrap--narrow center">
    <div class="form-card">
      {icon("check", size=46)}
      <h2 class="mt-2">{T("co.thanks")}</h2>
      <p class="lede mt-2">{T("co.thankssub")}</p>
      <p class="mt-2"><b>{T("co.orderid")}:</b> <span data-order-id>—</span></p>
      <div class="btn-row btn-row--center mt-3">
        <a class="btn" href="{u('shop.html')}">{icon("cart")} {T("common.continue")}</a>
        <a class="btn btn--outline" href="{u('index.html')}">{icon("arrow-r")} Home</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid--4">{''.join(badge_card(b) for b in TRUST_BADGES[:4])}</div>
  </div>
</section>'''
    body = f'<main id="main">{body}</main>'
    return head(f"Checkout — {BRAND['name']}", "Complete your ApnaPan order. UPI, cards, netbanking or cash on delivery. Free shipping above ₹599.",
                "checkout.html", u("assets/css/styles.css"), u, [ld_org()]) + header("nav.shop", u) + body + footer(u) + "</body></html>"


# =============================================================== 404
def not_found(u):
    body = f'''
<main id="main">
<section class="section">
  <div class="wrap wrap--narrow center">
    {logo_svg("", "#b4552d")}
    <h1 class="mt-3">That jar is not on this shelf.</h1>
    <p class="lede mt-2">The page you were looking for does not exist — but the pickle does.</p>
    <div class="btn-row btn-row--center mt-3">
      <a class="btn" href="{u('shop.html')}">{icon("cart")} {T("common.shop")}</a>
      <a class="btn btn--outline" href="{u('index.html')}">{icon("arrow-r")} Home</a>
    </div>
  </div>
</section>
</main>'''
    return head("Page not found", "Page not found", "404.html", u("assets/css/styles.css"), u) + header("", u) + body + footer(u) + "</body></html>"

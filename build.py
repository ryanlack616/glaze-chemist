"""
Glaze Chemist - Static Site Generator
Builds a browsable directory of glaze chemistry references: people, books, concepts.
Deploys to stullatlas.app/glaze-chemist
"""

import json
from pathlib import Path
from html import escape

DATA_FILE = Path(__file__).parent / "data" / "glaze_references.json"
PEOPLE_V2_FILE = Path(__file__).parent / "data" / "people_v2.json"
DIST_DIR = Path(__file__).parent / "dist"
BASE = "/glaze-chemist"

# -- Shared styles & layout -------------------------------------------------------

CSS = """
:root {
  --bg: #07070c; --bg-card: #0f0f18; --bg-hover: #17172a;
  --border: #1e1e3a; --text: #c8c8d8; --text-dim: #6b6b8a; --text-bright: #e8e8f0;
  --accent: #818cf8; --accent-dim: #4f46e5;
  --rose: #fb7185; --teal: #2dd4bf; --amber: #fbbf24; --emerald: #34d399;
  --mono: 'SF Mono','Cascadia Code','JetBrains Mono','Fira Code',monospace;
  --sans: 'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
}
[data-theme="light"] {
  --bg: #f8f8fc; --bg-card: #ffffff; --bg-hover: #f0f0f8;
  --border: #d8d8e8; --text: #3a3a5a; --text-dim: #7a7a9a; --text-bright: #1a1a2e;
  --accent: #4f46e5; --accent-dim: #3730a3;
  --rose: #e11d48; --teal: #0d9488; --amber: #d97706; --emerald: #059669;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { background: var(--bg); color: var(--text); font-family: var(--sans); }
body { min-height: 100vh; display: flex; flex-direction: column; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

.theme-toggle {
  background: none; border: 1px solid var(--border); color: var(--text-dim);
  border-radius: 6px; padding: 0.25rem 0.5rem; cursor: pointer; font-size: 0.9rem;
  font-family: var(--mono); line-height: 1; transition: border-color 0.15s, color 0.15s;
}
.theme-toggle:hover { border-color: var(--emerald); color: var(--text-bright); }

.site-header {
  display: flex; align-items: center; gap: 1rem; padding: 1rem 2rem;
  border-bottom: 1px solid var(--border); flex-wrap: wrap;
}
.site-header .logo { font-family: var(--mono); font-size: 1.1rem; color: var(--text-bright); }
.site-header .logo .sigil { color: var(--emerald); }
.site-header nav { display: flex; gap: 0.6rem; margin-left: auto; flex-wrap: wrap; }
.site-header nav a {
  font-family: var(--mono); font-size: 0.75rem; color: var(--text-dim);
  padding: 0.3rem 0.6rem; border: 1px solid var(--border); border-radius: 6px;
  transition: all 0.15s;
}
.site-header nav a:hover { color: var(--text-bright); border-color: var(--emerald); text-decoration: none; }
.site-header nav a.active { background: rgba(52,211,153,0.15); color: var(--emerald); border-color: var(--emerald); }

.search-wrap { padding: 1rem 2rem; }
.search-input {
  width: 100%; max-width: 500px; background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 8px; padding: 0.6rem 1rem; color: var(--text-bright);
  font-family: var(--mono); font-size: 0.85rem; outline: none;
}
.search-input:focus { border-color: var(--emerald); }
.search-input::placeholder { color: var(--text-dim); }

.content { flex: 1; padding: 1rem 2rem 3rem; max-width: 1200px; width: 100%; margin: 0 auto; }

.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
.card {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px;
  padding: 1rem 1.2rem; transition: border-color 0.15s;
}
.card:hover { border-color: var(--emerald); }
.card a { text-decoration: none; }
.card .card-name { font-family: var(--mono); font-size: 0.9rem; color: var(--text-bright); margin-bottom: 0.3rem; }
.card .card-type {
  font-family: var(--mono); font-size: 0.62rem; padding: 0.12rem 0.4rem;
  border-radius: 4px; display: inline-block; margin-bottom: 0.4rem;
}
.card .card-notes { font-size: 0.78rem; color: var(--text-dim); line-height: 1.5; }
.card .card-meta { font-family: var(--mono); font-size: 0.65rem; color: var(--text-dim); margin-top: 0.4rem; }
.card .card-tags { margin-top: 0.5rem; }

.type-person { background: rgba(129,140,248,0.2); color: var(--accent); }
.type-book { background: rgba(251,191,36,0.2); color: var(--amber); }
.type-concept { background: rgba(45,212,191,0.2); color: var(--teal); }
.type-institution { background: rgba(52,211,153,0.2); color: var(--emerald); }

.tag {
  display: inline-block; font-family: var(--mono); font-size: 0.58rem;
  padding: 0.1rem 0.35rem; border-radius: 3px; margin-right: 0.3rem; margin-bottom: 0.2rem;
  background: rgba(200,200,216,0.06); color: var(--text-dim); border: 1px solid var(--border);
}
.tag.beloved { background: rgba(251,191,36,0.1); color: var(--amber); border-color: rgba(251,191,36,0.2); }
.tag.cult { background: rgba(251,113,133,0.1); color: var(--rose); border-color: rgba(251,113,133,0.2); }
.tag.foundational { background: rgba(129,140,248,0.1); color: var(--accent); border-color: rgba(129,140,248,0.2); }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px;
  padding: 1rem; text-align: center;
}
.stat-card .stat-num { font-family: var(--mono); font-size: 2rem; color: var(--text-bright); }
.stat-card .stat-label { font-family: var(--mono); font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; }

.detail-header { margin-bottom: 2rem; }
.detail-header h1 { font-family: var(--mono); font-size: 1.8rem; color: var(--text-bright); margin-bottom: 0.5rem; }
.detail-header .meta { font-family: var(--mono); font-size: 0.75rem; color: var(--text-dim); display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; }

.detail-body { display: grid; grid-template-columns: 1fr 340px; gap: 2rem; }
@media (max-width: 768px) { .detail-body { grid-template-columns: 1fr; } }

.section { margin-bottom: 1.5rem; }
.section-title {
  font-family: var(--mono); font-size: 0.72rem; color: var(--text-dim);
  text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;
  padding-bottom: 0.3rem; border-bottom: 1px solid var(--border);
}
.notes-text { font-size: 0.88rem; color: var(--text); line-height: 1.7; }

.conn-item {
  display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0;
  font-family: var(--mono); font-size: 0.78rem; border-bottom: 1px solid var(--border);
}
.conn-item:last-child { border-bottom: none; }
.conn-item a { color: var(--text-bright); }
.conn-item .conn-label { color: var(--text-dim); font-size: 0.65rem; }

.dir-count { font-family: var(--mono); font-size: 0.75rem; color: var(--text-dim); margin-bottom: 1rem; }

.site-footer {
  padding: 1.5rem 2rem; border-top: 1px solid var(--border);
  font-family: var(--mono); font-size: 0.68rem; color: var(--text-dim);
  text-align: center;
}

.card.hidden { display: none; }

.inst-label {
  font-family: var(--mono); font-size: 0.6rem; color: var(--emerald);
  opacity: 0.7; margin-top: 0.15rem;
}

/* Book covers */
.book-card-inner { display: flex; gap: 0.8rem; }
.book-card-cover {
  flex-shrink: 0; width: 56px; height: 80px; border-radius: 4px;
  object-fit: cover; background: var(--bg-hover); border: 1px solid var(--border);
}
.book-card-cover-ph {
  flex-shrink: 0; width: 56px; height: 80px; border-radius: 4px;
  background: var(--bg-hover); border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem; color: var(--text-dim); opacity: 0.5;
}
.book-card-text { flex: 1; min-width: 0; }

.detail-cover {
  width: 180px; border-radius: 6px; border: 1px solid var(--border);
  background: var(--bg-hover); margin-bottom: 1rem;
}
.detail-cover-ph {
  width: 180px; height: 260px; border-radius: 6px; border: 1px solid var(--border);
  background: var(--bg-hover); display: flex; align-items: center; justify-content: center;
  font-size: 3rem; color: var(--text-dim); opacity: 0.4; margin-bottom: 1rem;
}

/* Knowledge badges */
.knowledge-badge {
  display: inline-flex; align-items: center; gap: 0.3rem;
  font-family: var(--mono); font-size: 0.6rem; padding: 0.15rem 0.45rem;
  border-radius: 4px; background: rgba(52,211,153,0.15); color: var(--emerald);
  border: 1px solid rgba(52,211,153,0.25); margin-top: 0.3rem;
}
.knowledge-section {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px;
  padding: 0.8rem 1rem; margin-top: 0.8rem;
}
.knowledge-section a {
  font-family: var(--mono); font-size: 0.78rem; color: var(--emerald);
}
.knowledge-pages {
  font-family: var(--mono); font-size: 0.72rem; color: var(--text-dim); margin-top: 0.3rem;
}
"""

def e(text):
    """Escape HTML"""
    return escape(str(text)) if text else ""

def nav_html(active=""):
    items = [
        (f"{BASE}/index.html", "Home"),
        (f"{BASE}/people/index.html", "People"),
        (f"{BASE}/books/index.html", "Books"),
        (f"{BASE}/concepts/index.html", "Concepts"),
        (f"{BASE}/lineage.html", "Lineage"),
    ]
    links = []
    for href, label in items:
        cls = ' class="active"' if label.lower() == active.lower() else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return "\n".join(links)

def wrap_page(title, body_html, active=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} - Glaze Chemist</title>
<style>{CSS}</style>
<script async src="https://plausible.io/js/pa-ICo80msYrRO0pVG-nP-eG.js"></script>
<script>window.plausible=window.plausible||function(){{(plausible.q=plausible.q||[]).push(arguments)}},plausible.init=plausible.init||function(i){{plausible.o=i||{{}}}};plausible.init()</script>
</head>
<body>
<div class="site-header">
  <a href="{BASE}/index.html" class="logo"><span class="sigil">&#9671;</span> Glaze Chemist</a>
  <nav>{nav_html(active)}</nav>
  <button class="theme-toggle" aria-label="Toggle theme">\u2600</button>
</div>
{body_html}
<div class="site-footer">
  Glaze Chemist - A free glaze chemistry reference - <a href="https://stullatlas.app">stullatlas.app</a> - <a href="https://stullatlas.app/community/">Community Atlas</a>
</div>
<script>
(function(){{
  var b=document.querySelector('.theme-toggle'),r=document.documentElement;
  var t=localStorage.getItem('gc-theme')||'dark';
  if(t==='light')r.setAttribute('data-theme','light');
  function u(){{b.textContent=r.getAttribute('data-theme')==='light'?'\u263e':'\u2600';}}
  u();
  b.addEventListener('click',function(){{
    var n=r.getAttribute('data-theme')==='light'?'dark':'light';
    if(n==='light')r.setAttribute('data-theme','light');else r.removeAttribute('data-theme');
    localStorage.setItem('gc-theme',n);u();
  }});
}})()
</script>
</body>
</html>"""


def tags_html(tags):
    if not tags:
        return ""
    parts = []
    for t in tags:
        cls = "tag"
        if t in ("beloved", "treasured"): cls += " beloved"
        elif t in ("cult",): cls += " cult"
        elif t in ("foundational",): cls += " foundational"
        parts.append(f'<span class="{cls}">{e(t)}</span>')
    return '<div class="card-tags">' + "".join(parts) + '</div>'


def make_person_slug(p):
    return p["id"]


def make_book_slug(b):
    return b["id"]


def normalize_v2_person(p):
    """Add v1-compatible aliases to a v2 person dict so all existing rendering code works."""
    if "periods" not in p:
        return p  # already v1 format
    out = dict(p)
    out["era"] = p["periods"][0] if p.get("periods") else ""
    out["role"] = p.get("roles", [])
    nat = p.get("nationality", [])
    out["nationality"] = nat[0] if isinstance(nat, list) and nat else (nat or "")
    affs = p.get("affiliations", [])
    out["institution"] = affs[0]["name"] if affs else ""
    out["notes"] = p.get("summary_long") or p.get("notes", "")
    out["tags"] = p.get("technical_tags", []) + p.get("context_tags", [])
    out["collaborators"] = [
        rp["name"] for rp in p.get("related_people", [])
        if rp.get("relation") in ("collaborator", "colleague", "mentor", "student", "contemporary")
    ]
    return out


def count_connections(people):
    """Count unique collaborator edges."""
    edge_set = set()
    for p in people:
        for c_name in p.get("collaborators", []):
            match = next((pp for pp in people if pp["name"] == c_name), None)
            if match:
                key = tuple(sorted([p["id"], match["id"]]))
                edge_set.add(key)
    return len(edge_set)


# -- Build People -----------------------------------------------------------------

def build_people(data, all_books):
    people = data["people"]
    out_dir = DIST_DIR / "people"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Index of books by author id for cross-referencing
    # Normalize underscore ids to hyphen to match v2 people ids
    books_by_author = {}
    for b in all_books:
        for aid in b.get("author_ids", []):
            norm = aid.replace("_", "-")
            books_by_author.setdefault(norm, []).append(b)

    # Index page
    cards = []
    for p in sorted(people, key=lambda x: x["name"]):
        slug = make_person_slug(p)
        era = f' - {e(p.get("era", ""))}' if p.get("era") else ""
        roles = ", ".join(p.get("role", []))
        card_notes = p.get("summary_short") or p.get("notes", "")
        notes = e(card_notes)[:160]
        inst = f'<div class="inst-label">{e(p.get("institution", ""))}</div>' if p.get("institution") else ""
        cards.append(f'''<div class="card">
  <a href="{slug}.html">
    <div class="card-name">{e(p["name"])}</div>
    <span class="card-type type-person">{e(roles)}</span>
    <div class="card-meta">{e(p.get("nationality", ""))}{era}</div>
    {inst}
    <div class="card-notes">{notes}</div>
    {tags_html(p.get("tags", []))}
  </a>
</div>''')

    body = f'''
<div class="content">
  <h1 style="font-family:var(--mono);font-size:1.4rem;color:var(--text-bright);margin-bottom:0.5rem">People</h1>
  <div class="dir-count">{len(people)} figures in glaze chemistry</div>
  <div class="search-wrap" style="padding:0 0 1.5rem">
    <input type="text" class="search-input" id="filterInput" placeholder="Filter people..." style="max-width:100%">
  </div>
  <div class="card-grid" id="cardGrid">
    {"".join(cards)}
  </div>
</div>
<script>
document.getElementById("filterInput").addEventListener("input", function() {{
  const q = this.value.toLowerCase();
  document.querySelectorAll("#cardGrid .card").forEach(c => {{
    c.classList.toggle("hidden", q.length >= 2 && !c.textContent.toLowerCase().includes(q));
  }});
}});
</script>'''
    (out_dir / "index.html").write_text(wrap_page("People", body, "People"), encoding="utf-8")

    # Individual pages
    people_by_id = {p["id"]: p for p in people}
    for p in people:
        slug = make_person_slug(p)
        era = p.get("era", "")
        nationality = p.get("nationality", "")
        roles = ", ".join(p.get("role", []))
        institution = p.get("institution", "")
        known_for = p.get("known_for", [])
        notes = p.get("notes", "")
        tags = p.get("tags", [])
        primary_type = p.get("primary_contribution_type", "")
        is_living = p.get("is_living", False)

        meta_parts = []
        if nationality: meta_parts.append(e(nationality))
        if era: meta_parts.append(e(era))
        if is_living: meta_parts.append('<span style="color:var(--emerald);font-size:0.75rem">&#x25CF; active</span>')
        if institution: meta_parts.append(f'<span style="color:var(--emerald)">{e(institution)}</span>')

        # Known for
        kf_html = ""
        if known_for:
            items = "".join(f"<li>{e(k)}</li>" for k in known_for)
            kf_html = f'''<div class="section">
  <div class="section-title">Known For</div>
  <ul style="list-style:disc;padding-left:1.2rem;font-size:0.85rem;color:var(--text);line-height:1.8">{items}</ul>
</div>'''

        # Books authored
        authored = books_by_author.get(p["id"], [])
        books_html = ""
        if authored:
            items = "".join(
                f'<div class="conn-item"><a href="{BASE}/books/{make_book_slug(b)}.html">{e(b["title"])}</a>'
                f' <span class="conn-label">{e(b.get("first_published", ""))}</span></div>'
                for b in authored
            )
            books_html = f'''<div class="section">
  <div class="section-title">Books</div>
  {items}
</div>'''

        # Related people (v2 rich format with relation types) or collaborators fallback (v1)
        related_people_v2 = p.get("related_people", [])
        collab_html = ""
        if related_people_v2:
            items = []
            for rp in related_people_v2:
                c_name = rp.get("name", "")
                relation = rp.get("relation", "collaborator")
                pid = rp.get("person_id", "")
                match = people_by_id.get(pid) or next((pp for pp in people if pp["name"] == c_name), None)
                rel_label = f'<span style="font-size:0.68rem;color:var(--text-dim);margin-left:0.4rem">{e(relation)}</span>'
                if match:
                    items.append(f'<div class="conn-item"><a href="{BASE}/people/{make_person_slug(match)}.html">{e(c_name)}</a>{rel_label}</div>')
                else:
                    items.append(f'<div class="conn-item">{e(c_name)}{rel_label}</div>')
            collab_html = f'<div class="section"><div class="section-title">Related People</div>{"".join(items)}</div>'
        else:
            collabs = p.get("collaborators", [])
            if collabs:
                items = []
                for c_name in collabs:
                    match = next((pp for pp in people if pp["name"] == c_name), None)
                    if match:
                        items.append(f'<div class="conn-item"><a href="{BASE}/people/{make_person_slug(match)}.html">{e(c_name)}</a></div>')
                    else:
                        items.append(f'<div class="conn-item">{e(c_name)}</div>')
                collab_html = f'<div class="section"><div class="section-title">Collaborators</div>{"".join(items)}</div>'

        # Domains section (v2)
        active_domains = [k.replace("_", " ") for k, v in p.get("domains", {}).items() if v]
        domains_html = ""
        if active_domains:
            chips = "".join(f'<span class="tag">{e(d)}</span>' for d in active_domains)
            domains_html = f'<div class="section"><div class="section-title">Domains</div><div>{chips}</div></div>'

        # Primary contribution badge (v2)
        primary_badge = ""
        if primary_type:
            primary_badge = f'<span class="card-type" style="background:#1a1a3a;color:var(--teal);border:1px solid var(--teal);margin-left:0.6rem;font-size:0.7rem">{e(primary_type.replace("_", " "))}</span>'

        body = f'''
<div class="content">
  <div class="detail-header">
    <h1>{e(p["name"])}</h1>
    <div class="meta">
      <span class="card-type type-person">{e(roles)}</span>
      {primary_badge}
      {" - ".join(meta_parts)}
    </div>
  </div>
  <div class="detail-body">
    <div class="detail-main">
      {"" if not notes else f'<div class="section"><div class="section-title">Notes</div><div class="notes-text">{e(notes)}</div></div>'}
      {kf_html}
      {domains_html}
    </div>
    <div class="detail-sidebar">
      {books_html}
      {collab_html}
      {"" if not tags else f'<div class="section"><div class="section-title">Tags</div>{tags_html(tags)}</div>'}
    </div>
  </div>
</div>'''
        (out_dir / f"{slug}.html").write_text(wrap_page(p["name"], body, "People"), encoding="utf-8")

    return len(people)


# -- Build Books -------------------------------------------------------------------

def build_books(data, all_people):
    books = data["books"]
    out_dir = DIST_DIR / "books"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Support both hyphen (v2) and underscore (v1) ids in author_ids
    people_by_id = {}
    for p in all_people:
        people_by_id[p["id"]] = p
        people_by_id[p["id"].replace("-", "_")] = p

    # Index page
    cards = []
    for b in sorted(books, key=lambda x: x["title"]):
        slug = make_book_slug(b)
        authors = ", ".join(people_by_id[a]["name"] for a in b.get("author_ids", []) if a in people_by_id)
        notes = e(b.get("notes", ""))[:160]
        oop = " - out of print" if b.get("out_of_print") else ""
        year = f' ({b["first_published"]})' if b.get("first_published") else ""
        isbn = b.get("isbn", "")
        ki = b.get("knowledge_indexed")

        cover_url = b.get("cover_url") or (f'https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg' if isbn else None)
        if cover_url:
            cover_html = f'<img class="book-card-cover" src="{cover_url}" alt="" loading="lazy" onerror="this.outerHTML=\'<div class=\\\'book-card-cover-ph\\\'>📖</div>\'">'
        else:
            cover_html = '<div class="book-card-cover-ph">📖</div>'

        ki_html = ""
        if ki:
            ki_html = f'\n    <div class="knowledge-badge">⚡ {ki["pages"]} pages indexed</div>'

        cards.append(f'''<div class="card">
  <a href="{slug}.html">
    <div class="book-card-inner">
      {cover_html}
      <div class="book-card-text">
        <div class="card-name">{e(b["title"])}</div>
        <span class="card-type type-book">book</span>
        <div class="card-meta">{e(authors)}{year}{oop}</div>
        <div class="card-notes">{notes}</div>
        {tags_html(b.get("tags", []))}{ki_html}
      </div>
    </div>
  </a>
</div>''')

    body = f'''
<div class="content">
  <h1 style="font-family:var(--mono);font-size:1.4rem;color:var(--text-bright);margin-bottom:0.5rem">Books</h1>
  <div class="dir-count">{len(books)} essential references</div>
  <div class="search-wrap" style="padding:0 0 1.5rem">
    <input type="text" class="search-input" id="filterInput" placeholder="Filter books..." style="max-width:100%">
  </div>
  <div class="card-grid" id="cardGrid">
    {"".join(cards)}
  </div>
</div>
<script>
document.getElementById("filterInput").addEventListener("input", function() {{
  const q = this.value.toLowerCase();
  document.querySelectorAll("#cardGrid .card").forEach(c => {{
    c.classList.toggle("hidden", q.length >= 2 && !c.textContent.toLowerCase().includes(q));
  }});
}});
</script>'''
    (out_dir / "index.html").write_text(wrap_page("Books", body, "Books"), encoding="utf-8")

    # Individual pages
    for b in books:
        slug = make_book_slug(b)
        authors = [(people_by_id[a]["name"], make_person_slug(people_by_id[a])) for a in b.get("author_ids", []) if a in people_by_id]
        status = b.get("community_status", "")
        notes = b.get("notes", "")
        subjects = b.get("subject", [])
        tags = b.get("tags", [])
        oop = b.get("out_of_print", False)
        year = b.get("first_published", "")
        isbn = b.get("isbn", "")
        ki = b.get("knowledge_indexed")
        ks = b.get("knowledge_search", "")

        author_links = ", ".join(f'<a href="{BASE}/people/{aslug}.html">{e(name)}</a>' for name, aslug in authors)

        meta_parts = []
        if year: meta_parts.append(f"Published {year}")
        if status: meta_parts.append(e(status))
        if oop: meta_parts.append('<span style="color:var(--rose)">out of print</span>')

        subjects_html = ""
        if subjects:
            items = "".join(f"<li>{e(s)}</li>" for s in subjects)
            subjects_html = f'''<div class="section">
  <div class="section-title">Subjects</div>
  <ul style="list-style:disc;padding-left:1.2rem;font-size:0.85rem;color:var(--text);line-height:1.8">{items}</ul>
</div>'''

        # Cover image for sidebar
        cover_url_detail = b.get("cover_url") or (f'https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg' if isbn else None)
        if cover_url_detail:
            # Use -L size for cover_id URLs, keep as-is for ISBN URLs (already -L)
            cover_url_detail_lg = cover_url_detail.replace('-M.jpg', '-L.jpg')
            cover_detail = f'<img class="detail-cover" src="{cover_url_detail_lg}" alt="{e(b["title"])}" loading="lazy" onerror="this.outerHTML=\'<div class=\\\'detail-cover-ph\\\'>📖</div>\'">'
        else:
            cover_detail = '<div class="detail-cover-ph">📖</div>'

        # Knowledge section
        knowledge_html = ""
        if ki:
            search_q = ki.get("source", b["title"])
            knowledge_html = f'''<div class="section">
  <div class="section-title">Ceramic Knowledge</div>
  <div class="knowledge-section">
    <div class="knowledge-badge" style="font-size:0.72rem">⚡ Full text indexed — {ki["pages"]} pages</div>
    <div class="knowledge-pages">OCR-indexed in the Ceramic Engine knowledge base</div>
    <div style="margin-top:0.5rem"><a href="https://engine.stullatlas.app/knowledge/search?q={e(search_q)}" target="_blank">→ Search this text</a></div>
  </div>
</div>'''
        elif ks:
            knowledge_html = f'''<div class="section">
  <div class="section-title">Ceramic Knowledge</div>
  <div class="knowledge-section">
    <div style="font-family:var(--mono);font-size:0.72rem;color:var(--text-dim)">Related content in the knowledge base</div>
    <div style="margin-top:0.5rem"><a href="https://engine.stullatlas.app/knowledge/search?q={e(ks)}" target="_blank">→ Search related topics</a></div>
  </div>
</div>'''

        body = f'''
<div class="content">
  <div class="detail-header">
    <h1>{e(b["title"])}</h1>
    <div class="meta">
      <span class="card-type type-book">book</span>
      {" - ".join(meta_parts)}
    </div>
    <div style="font-family:var(--mono);font-size:0.82rem;color:var(--text);margin-top:0.5rem">by {author_links}</div>
  </div>
  <div class="detail-body">
    <div class="detail-main">
      {"" if not notes else f'<div class="section"><div class="section-title">Notes</div><div class="notes-text">{e(notes)}</div></div>'}
      {subjects_html}
    </div>
    <div class="detail-sidebar">
      {cover_detail}
      {knowledge_html}
      {"" if not tags else f'<div class="section"><div class="section-title">Tags</div>{tags_html(tags)}</div>'}
    </div>
  </div>
</div>'''
        (out_dir / f"{slug}.html").write_text(wrap_page(b["title"], body, "Books"), encoding="utf-8")

    return len(books)


# -- Build Concepts ----------------------------------------------------------------

def build_concepts(data, all_people):
    concepts = data.get("concepts", [])
    if not concepts:
        return 0

    out_dir = DIST_DIR / "concepts"
    out_dir.mkdir(parents=True, exist_ok=True)

    people_by_id = {}
    for p in all_people:
        people_by_id[p["id"]] = p
        people_by_id[p["id"].replace("-", "_")] = p

    # Index
    cards = []
    for c in concepts:
        devs = ", ".join(people_by_id[d]["name"] for d in c.get("developed_by", []) if d in people_by_id)
        cards.append(f'''<div class="card">
  <a href="{c["id"]}.html">
    <div class="card-name">{e(c["name"])}</div>
    <span class="card-type type-concept">concept</span>
    <div class="card-meta">{e(devs)}</div>
    <div class="card-notes">{e(c.get("description", ""))[:160]}</div>
    {tags_html(c.get("tags", []))}
  </a>
</div>''')

    body = f'''
<div class="content">
  <h1 style="font-family:var(--mono);font-size:1.4rem;color:var(--text-bright);margin-bottom:0.5rem">Concepts</h1>
  <div class="dir-count">{len(concepts)} foundational ideas in glaze chemistry</div>
  <div class="card-grid">
    {"".join(cards)}
  </div>
</div>'''
    (out_dir / "index.html").write_text(wrap_page("Concepts", body, "Concepts"), encoding="utf-8")

    # Individual pages
    for c in concepts:
        devs = [(people_by_id[d]["name"], make_person_slug(people_by_id[d])) for d in c.get("developed_by", []) if d in people_by_id]
        dev_links = ", ".join(f'<a href="{BASE}/people/{dslug}.html">{e(name)}</a>' for name, dslug in devs)

        body = f'''
<div class="content">
  <div class="detail-header">
    <h1>{e(c["name"])}</h1>
    <div class="meta">
      <span class="card-type type-concept">concept</span>
    </div>
    {"" if not dev_links else f'<div style="font-family:var(--mono);font-size:0.82rem;color:var(--text);margin-top:0.5rem">Developed by {dev_links}</div>'}
  </div>
  <div class="detail-body">
    <div class="detail-main">
      <div class="section">
        <div class="section-title">Description</div>
        <div class="notes-text">{e(c.get("description", ""))}</div>
      </div>
    </div>
    <div class="detail-sidebar">
      {"" if not c.get("tags") else f'<div class="section"><div class="section-title">Tags</div>{tags_html(c.get("tags", []))}</div>'}
    </div>
  </div>
</div>'''
        (out_dir / f'{c["id"]}.html').write_text(wrap_page(c["name"], body, "Concepts"), encoding="utf-8")

    return len(concepts)


# -- Build Lineage Network --------------------------------------------------------

def build_lineage(data):
    """Interactive force-directed network of the collaborator graph."""
    people = data["people"]
    books = data["books"]
    concepts = data.get("concepts", [])

    # Build nodes
    nodes = []
    node_ids = set()
    for p in people:
        nodes.append({"id": p["id"], "name": p["name"], "type": "person",
                       "href": f"{BASE}/people/{p['id']}.html"})
        node_ids.add(p["id"])
        node_ids.add(p["id"].replace("-", "_"))  # backward compat
    for b in books:
        nodes.append({"id": b["id"], "name": b["title"], "type": "book",
                       "href": f"{BASE}/books/{b['id']}.html"})
        node_ids.add(b["id"])
    for c in concepts:
        nodes.append({"id": c["id"], "name": c["name"], "type": "concept",
                       "href": f"{BASE}/concepts/{c['id']}.html"})
        node_ids.add(c["id"])

    # Build edges
    edges = []
    edge_set = set()
    for p in people:
        for c_name in p.get("collaborators", []):
            match = next((pp for pp in people if pp["name"] == c_name), None)
            if match:
                key = tuple(sorted([p["id"], match["id"]]))
                if key not in edge_set:
                    edge_set.add(key)
                    edges.append({"source": p["id"], "target": match["id"], "type": "collaborator"})
    for b in books:
        for aid in b.get("author_ids", []):
            norm = aid.replace("_", "-")  # normalize to hyphen (v2 id format)
            if norm in node_ids:
                edges.append({"source": norm, "target": b["id"], "type": "authored"})
            elif aid in node_ids:
                edges.append({"source": aid, "target": b["id"], "type": "authored"})
    for c in concepts:
        for did in c.get("developed_by", []):
            if did in node_ids:
                edges.append({"source": did, "target": c["id"], "type": "developed"})

    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)

    body = f'''
<div class="content" style="max-width:100%;padding:1rem">
  <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;flex-wrap:wrap">
    <h1 style="font-family:var(--mono);font-size:1.4rem;color:var(--text-bright)">Lineage Network</h1>
    <div class="dir-count" style="margin:0">{len(people)} people &middot; {len(books)} books &middot; {len(concepts)} concepts &middot; {len(edges)} connections</div>
  </div>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:0.6rem;align-items:center">
    <label style="font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);display:flex;align-items:center;gap:0.3rem">
      <input type="checkbox" id="showBooks" checked> Books
    </label>
    <label style="font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);display:flex;align-items:center;gap:0.3rem">
      <input type="checkbox" id="showConcepts" checked> Concepts
    </label>
    <label style="font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);display:flex;align-items:center;gap:0.3rem">
      <input type="checkbox" id="showLabels" checked> Labels
    </label>
    <label style="font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);display:flex;align-items:center;gap:0.4rem">
      Zoom
      <input type="range" id="zoomSlider" min="0.2" max="4" step="0.05" value="1" style="width:90px;accent-color:#34d399;cursor:pointer">
      <span id="zoomVal" style="font-family:var(--mono);font-size:0.65rem;color:var(--text-dim);min-width:2.6em">1.0&times;</span>
    </label>
    <button id="resetView" style="font-family:var(--mono);font-size:0.65rem;padding:0.2rem 0.55rem;background:none;border:1px solid var(--border);color:var(--text-dim);border-radius:4px;cursor:pointer;transition:border-color 0.15s,color 0.15s" onmouseover="this.style.borderColor='#34d399';this.style.color='#e8e8f0'" onmouseout="this.style.borderColor='';this.style.color=''">Reset</button>
    <div style="display:flex;gap:0.5rem;align-items:center;margin-left:auto">
      <span style="width:10px;height:10px;border-radius:50%;background:#818cf8;display:inline-block"></span>
      <span style="font-family:var(--mono);font-size:0.65rem;color:var(--text-dim)">Person</span>
      <span style="width:10px;height:10px;border-radius:50%;background:#fbbf24;display:inline-block;margin-left:0.5rem"></span>
      <span style="font-family:var(--mono);font-size:0.65rem;color:var(--text-dim)">Book</span>
      <span style="width:10px;height:10px;border-radius:50%;background:#2dd4bf;display:inline-block;margin-left:0.5rem"></span>
      <span style="font-family:var(--mono);font-size:0.65rem;color:var(--text-dim)">Concept</span>
    </div>
  </div>
  <div style="font-family:var(--mono);font-size:0.6rem;color:var(--text-dim);margin-bottom:0.4rem">Scroll to zoom &middot; Drag canvas to pan &middot; Drag nodes to reposition &middot; Double-click to open</div>
  <canvas id="networkCanvas" style="width:100%;height:75vh;min-height:550px;background:#0f0f18;border:1px solid #1e1e3a;border-radius:10px;cursor:grab"></canvas>
  <div id="tooltip" style="display:none;position:fixed;background:#17172a;border:1px solid #1e1e3a;border-radius:6px;padding:0.4rem 0.7rem;font-family:var(--mono);font-size:0.72rem;color:#e8e8f0;pointer-events:none;z-index:100"></div>
</div>

<script>
(function() {{
  const NODES = {nodes_json};
  const EDGES = {edges_json};

  const colorMap = {{ person: "#818cf8", book: "#fbbf24", concept: "#2dd4bf" }};
  const radiusMap = {{ person: 8, book: 5, concept: 6 }};

  const canvas = document.getElementById("networkCanvas");
  const ctx = canvas.getContext("2d");
  const tooltip = document.getElementById("tooltip");

  // High-DPI canvas
  function resize() {{
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    return {{ w: rect.width, h: rect.height }};
  }}
  let dims = resize();
  window.addEventListener("resize", () => {{ dims = resize(); draw(); }});

  const W = () => dims.w;
  const H = () => dims.h;

  // Init node positions in circle
  const nodeMap = {{}};
  NODES.forEach((n, i) => {{
    const angle = (i / NODES.length) * Math.PI * 2;
    const r = Math.min(W(), H()) * 0.35;
    n.x = W()/2 + Math.cos(angle) * r * (0.5 + Math.random() * 0.5);
    n.y = H()/2 + Math.sin(angle) * r * (0.5 + Math.random() * 0.5);
    n.vx = 0; n.vy = 0;
    n.visible = true;
    nodeMap[n.id] = n;
  }});

  let showLabels = true;

  // View transform: pan + zoom
  let viewScale = 1, viewX = 0, viewY = 0;
  const MIN_SCALE = 0.2, MAX_SCALE = 4;

  function toWorld(cx, cy) {{
    return {{ x: (cx - viewX) / viewScale, y: (cy - viewY) / viewScale }};
  }}

  function syncZoomUI() {{
    const sl = document.getElementById('zoomSlider');
    const vl = document.getElementById('zoomVal');
    if (sl) sl.value = viewScale;
    if (vl) vl.textContent = viewScale.toFixed(1) + '\u00d7';
  }}

  function simulate() {{
    const visNodes = NODES.filter(n => n.visible);
    const visEdges = EDGES.filter(e => nodeMap[e.source]?.visible && nodeMap[e.target]?.visible);

    // Repulsion (Barnes-Hut could optimize but N is small)
    for (let i = 0; i < visNodes.length; i++) {{
      for (let j = i + 1; j < visNodes.length; j++) {{
        const a = visNodes[i], b = visNodes[j];
        let dx = b.x - a.x, dy = b.y - a.y;
        let dist = Math.sqrt(dx*dx + dy*dy) || 1;
        let force = 900 / (dist * dist);
        let fx = dx / dist * force, fy = dy / dist * force;
        a.vx -= fx; a.vy -= fy;
        b.vx += fx; b.vy += fy;
      }}
    }}

    // Attraction along edges
    visEdges.forEach(e => {{
      const a = nodeMap[e.source], b = nodeMap[e.target];
      if (!a || !b) return;
      let dx = b.x - a.x, dy = b.y - a.y;
      let dist = Math.sqrt(dx*dx + dy*dy) || 1;
      const k = e.type === "collaborator" ? 0.012 : 0.005;
      let force = dist * k;
      let fx = dx / dist * force, fy = dy / dist * force;
      a.vx += fx; a.vy += fy;
      b.vx -= fx; b.vy -= fy;
    }});

    // Center pull
    visNodes.forEach(n => {{
      n.vx += (W()/2 - n.x) * 0.008;
      n.vy += (H()/2 - n.y) * 0.008;
    }});

    // Integrate
    visNodes.forEach(n => {{
      n.vx *= 0.82;
      n.vy *= 0.82;
      n.x += n.vx * 0.3;
      n.y += n.vy * 0.3;
      n.x = Math.max(50, Math.min(W() - 50, n.x));
      n.y = Math.max(40, Math.min(H() - 40, n.y));
    }});
  }}

  function draw() {{
    ctx.clearRect(0, 0, W(), H());
    const visNodes = NODES.filter(n => n.visible);
    const visEdges = EDGES.filter(e => nodeMap[e.source]?.visible && nodeMap[e.target]?.visible);

    ctx.save();
    ctx.translate(viewX, viewY);
    ctx.scale(viewScale, viewScale);

    // Edges
    visEdges.forEach(e => {{
      const a = nodeMap[e.source], b = nodeMap[e.target];
      if (!a || !b) return;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      if (e.type === "collaborator") {{
        ctx.strokeStyle = "rgba(129,140,248,0.25)";
        ctx.lineWidth = 1.2 / viewScale;
        ctx.setLineDash([]);
      }} else {{
        ctx.strokeStyle = "rgba(100,100,130,0.12)";
        ctx.lineWidth = 0.8 / viewScale;
        ctx.setLineDash([3 / viewScale, 3 / viewScale]);
      }}
      ctx.stroke();
      ctx.setLineDash([]);
    }});

    // Nodes
    visNodes.forEach(n => {{
      const color = colorMap[n.type] || "#818cf8";
      const r = radiusMap[n.type] || 6;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.globalAlpha = 0.85;
      ctx.fill();
      ctx.globalAlpha = 1;
    }});

    // Labels
    if (showLabels) {{
      const fontSize = Math.max(6, 8 / viewScale);
      ctx.font = fontSize + "px 'SF Mono','Cascadia Code',monospace";
      ctx.textAlign = "center";
      visNodes.filter(n => n.type === "person").forEach(n => {{
        ctx.fillStyle = "rgba(107,107,138,0.8)";
        ctx.fillText(n.name, n.x, n.y - 13);
      }});
    }}

    ctx.restore();
  }}

  // Animation loop
  let frame = 0;
  function tick() {{
    simulate();
    draw();
    frame++;
    if (frame < 300) requestAnimationFrame(tick);
  }}
  tick();

  // Drag interaction
  let dragging = null;
  let dragOffset = {{ x: 0, y: 0 }};

  function getNodeAt(mx, my) {{
    const rect = canvas.getBoundingClientRect();
    const cx = mx - rect.left, cy = my - rect.top;
    // Convert screen coords to world coords
    const w = toWorld(cx, cy);
    const visNodes = NODES.filter(n => n.visible);
    for (let i = visNodes.length - 1; i >= 0; i--) {{
      const n = visNodes[i];
      // Ensure at least 8px screen hit regardless of zoom level
      const worldR = Math.max((radiusMap[n.type] || 6) + 3, 8 / viewScale);
      if ((n.x - w.x) ** 2 + (n.y - w.y) ** 2 < worldR * worldR) return n;
    }}
    return null;
  }}

  let panning = false;
  let panStart = {{ x: 0, y: 0, vx: 0, vy: 0 }};

  canvas.addEventListener("mousedown", (ev) => {{
    const n = getNodeAt(ev.clientX, ev.clientY);
    if (n) {{
      dragging = n;
      const rect = canvas.getBoundingClientRect();
      const w = toWorld(ev.clientX - rect.left, ev.clientY - rect.top);
      dragOffset.x = n.x - w.x;
      dragOffset.y = n.y - w.y;
      canvas.style.cursor = "grabbing";
    }} else {{
      panning = true;
      panStart = {{ x: ev.clientX, y: ev.clientY, vx: viewX, vy: viewY }};
      canvas.style.cursor = "grabbing";
    }}
  }});

  canvas.addEventListener("mousemove", (ev) => {{
    if (dragging) {{
      const rect = canvas.getBoundingClientRect();
      const w = toWorld(ev.clientX - rect.left, ev.clientY - rect.top);
      dragging.x = w.x + dragOffset.x;
      dragging.y = w.y + dragOffset.y;
      dragging.vx = 0; dragging.vy = 0;
      draw();
    }} else if (panning) {{
      viewX = panStart.vx + (ev.clientX - panStart.x);
      viewY = panStart.vy + (ev.clientY - panStart.y);
      draw();
    }}
    // Tooltip
    const n = getNodeAt(ev.clientX, ev.clientY);
    if (n) {{
      tooltip.style.display = "block";
      tooltip.style.left = ev.clientX + 12 + "px";
      tooltip.style.top = ev.clientY - 10 + "px";
      tooltip.textContent = n.name;
      if (!dragging && !panning) canvas.style.cursor = "pointer";
    }} else {{
      tooltip.style.display = "none";
      if (!dragging && !panning) canvas.style.cursor = "grab";
    }}
  }});

  canvas.addEventListener("mouseup", () => {{
    if (dragging) {{
      frame = 0; tick(); // Resume simulation briefly
    }}
    dragging = null;
    panning = false;
    canvas.style.cursor = "grab";
  }});

  canvas.addEventListener("mouseleave", () => {{
    panning = false;
    if (!dragging) canvas.style.cursor = "grab";
    tooltip.style.display = "none";
  }});

  // Mouse wheel zoom toward cursor
  canvas.addEventListener("wheel", (ev) => {{
    ev.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const cx = ev.clientX - rect.left, cy = ev.clientY - rect.top;
    const wx = (cx - viewX) / viewScale, wy = (cy - viewY) / viewScale;
    const factor = ev.deltaY < 0 ? 1.1 : 1 / 1.1;
    viewScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, viewScale * factor));
    viewX = cx - wx * viewScale;
    viewY = cy - wy * viewScale;
    syncZoomUI();
    draw();
  }}, {{ passive: false }});

  canvas.addEventListener("dblclick", (ev) => {{
    const n = getNodeAt(ev.clientX, ev.clientY);
    if (n && n.href) window.location.href = n.href;
  }});

  // Toggles
  document.getElementById("showBooks").addEventListener("change", function() {{
    NODES.forEach(n => {{ if (n.type === "book") n.visible = this.checked; }});
    frame = 0; tick();
  }});
  document.getElementById("showConcepts").addEventListener("change", function() {{
    NODES.forEach(n => {{ if (n.type === "concept") n.visible = this.checked; }});
    frame = 0; tick();
  }});
  document.getElementById("showLabels").addEventListener("change", function() {{
    showLabels = this.checked;
    draw();
  }});

  // Zoom slider
  document.getElementById("zoomSlider").addEventListener("input", function() {{
    const newScale = parseFloat(this.value);
    const cx = W() / 2, cy = H() / 2;
    const wx = (cx - viewX) / viewScale, wy = (cy - viewY) / viewScale;
    viewScale = newScale;
    viewX = cx - wx * viewScale;
    viewY = cy - wy * viewScale;
    syncZoomUI();
    draw();
  }});

  // Reset view
  document.getElementById("resetView").addEventListener("click", () => {{
    viewScale = 1; viewX = 0; viewY = 0;
    syncZoomUI();
    draw();
  }});
}})();
</script>'''

    (DIST_DIR / "lineage.html").write_text(wrap_page("Lineage Network", body, "Lineage"), encoding="utf-8")


# -- Build Index -------------------------------------------------------------------

def build_index(data):
    people = data["people"]
    books = data["books"]
    concepts = data.get("concepts", [])

    total = len(people) + len(books) + len(concepts)
    edge_count = count_connections(people)

    # Featured: people with "beloved" or "foundational" tags
    featured_people = [p for p in people if "foundational" in p.get("tags", []) or "beloved" in p.get("tags", [])][:8]
    featured_books = [b for b in books if "beloved" in b.get("tags", []) or "cult" in b.get("tags", []) or "foundational" in b.get("tags", [])][:8]

    fp_cards = []
    for p in featured_people:
        roles = ", ".join(p.get("role", []))
        era = p.get("era", "")
        inst = f'<div class="inst-label">{e(p.get("institution", ""))}</div>' if p.get("institution") else ""
        fp_cards.append(f'''<div class="card">
  <a href="people/{make_person_slug(p)}.html">
    <div class="card-name">{e(p["name"])}</div>
    <span class="card-type type-person">{e(roles)}</span>
    <div class="card-meta">{e(p.get("nationality", ""))} &middot; {e(era)}</div>
    {inst}
    <div class="card-notes">{e(p.get("notes", ""))[:140]}</div>
    {tags_html(p.get("tags", []))}
  </a>
</div>''')

    fb_cards = []
    people_by_id = {}
    for pp in people:
        people_by_id[pp["id"]] = pp
        people_by_id[pp["id"].replace("-", "_")] = pp
    for b in featured_books:
        authors = ", ".join(people_by_id[a]["name"] for a in b.get("author_ids", []) if a in people_by_id)
        year = f' ({b["first_published"]})' if b.get("first_published") else ""
        fb_cards.append(f'''<div class="card">
  <a href="books/{make_book_slug(b)}.html">
    <div class="card-name">{e(b["title"])}</div>
    <span class="card-type type-book">book</span>
    <div class="card-meta">{e(authors)}{year}</div>
    <div class="card-notes">{e(b.get("notes", ""))[:140]}</div>
    {tags_html(b.get("tags", []))}
  </a>
</div>''')

    # All items for search
    all_items = []
    for p in people:
        all_items.append({"name": p["name"], "type": "person", "href": f"people/{make_person_slug(p)}.html", "notes": (p.get("notes") or "")[:100]})
    for b in books:
        all_items.append({"name": b["title"], "type": "book", "href": f"books/{make_book_slug(b)}.html", "notes": (b.get("notes") or "")[:100]})
    for c in concepts:
        all_items.append({"name": c["name"], "type": "concept", "href": f"concepts/{c['id']}.html", "notes": (c.get("description") or "")[:100]})

    all_items_json = json.dumps(all_items)

    body = f'''
<div class="content">
  <div style="text-align:center;margin:2rem 0 1rem">
    <h1 style="font-family:var(--mono);font-size:2rem;color:var(--text-bright)">
      <span style="color:var(--emerald)">&#9671;</span> Glaze Chemist
    </h1>
    <p style="color:var(--text-dim);font-size:0.9rem;margin-top:0.5rem">
      A free reference directory for glaze chemistry &mdash; the people, books, and ideas that shaped the field
    </p>
  </div>

  <div class="stats-grid">
    <div class="stat-card"><div class="stat-num">{total}</div><div class="stat-label">Total Entries</div></div>
    <div class="stat-card"><div class="stat-num">{len(people)}</div><div class="stat-label">People</div></div>
    <div class="stat-card"><div class="stat-num">{len(books)}</div><div class="stat-label">Books</div></div>
    <div class="stat-card"><div class="stat-num">{edge_count}</div><div class="stat-label">Connections</div></div>
  </div>

  <div class="search-wrap" style="padding:0 0 1.5rem">
    <input type="text" class="search-input" id="globalSearch" placeholder="Search all {total} entries..." style="max-width:100%">
  </div>
  <div id="searchResults" style="display:none;margin-bottom:2rem"></div>

  <div class="section">
    <div class="section-title">Foundational Figures</div>
    <div class="card-grid">{"".join(fp_cards)}</div>
  </div>

  <div class="section" style="margin-top:2rem">
    <div class="section-title">Essential & Treasured Books</div>
    <div class="card-grid">{"".join(fb_cards)}</div>
  </div>

  <div class="section" style="margin-top:2rem;text-align:center">
    <a href="{BASE}/lineage.html" style="font-family:var(--mono);font-size:0.85rem;color:var(--emerald);border:1px solid var(--emerald);padding:0.5rem 1.5rem;border-radius:8px;display:inline-block;transition:all 0.15s">
      View Lineage Network &rarr;
    </a>
  </div>
</div>

<script>
const ALL = {all_items_json};
document.getElementById("globalSearch").addEventListener("input", function() {{
  const q = this.value.toLowerCase();
  const res = document.getElementById("searchResults");
  if (q.length < 2) {{ res.style.display = "none"; return; }}
  res.style.display = "block";
  const matches = ALL.filter(n => n.name.toLowerCase().includes(q) || n.notes.toLowerCase().includes(q));
  if (!matches.length) {{ res.innerHTML = '<div style="color:var(--text-dim);font-family:var(--mono);font-size:0.8rem">No results</div>'; return; }}
  res.innerHTML = '<div class="card-grid">' + matches.slice(0,20).map(n => `
    <div class="card"><a href="${{n.href}}">
      <div class="card-name">${{n.name}}</div>
      <span class="card-type type-${{n.type}}">${{n.type}}</span>
      <div class="card-notes">${{n.notes}}</div>
    </a></div>`).join("") + "</div>";
}});
</script>'''

    (DIST_DIR / "index.html").write_text(wrap_page("Glaze Chemist", body, "Home"), encoding="utf-8")


# -- Main -------------------------------------------------------------------------

def main():
    print("Glaze Chemist - Building static site...")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    data = raw["glaze_chemistry_references"]

    # Inject v2 people if available (richer schema with backward-compat aliases)
    if PEOPLE_V2_FILE.exists():
        v2_raw = json.loads(PEOPLE_V2_FILE.read_text(encoding="utf-8"))
        data["people"] = [normalize_v2_person(p) for p in v2_raw["people"]]
        print(f"  Using people_v2.json ({len(data['people'])} entries)")

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    n_people = build_people(data, data["books"])
    n_books = build_books(data, data["people"])
    n_concepts = build_concepts(data, data["people"])
    build_index(data)
    build_lineage(data)

    total = n_people + n_books + n_concepts
    print(f"\n  + {n_people} people pages")
    print(f"  + {n_books} book pages")
    print(f"  + {n_concepts} concept pages")
    print(f"  + index page")
    print(f"  + lineage network page")
    print(f"\n  Total: {total} entries -> {DIST_DIR}")
    print(f"  Deploy to: stullatlas.app/glaze-chemist")
    print("\nDone.")


if __name__ == "__main__":
    main()

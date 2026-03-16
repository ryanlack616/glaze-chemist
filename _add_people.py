"""
Add missing people and their books to glaze_references.json
Run from glaze-chemist directory.
"""
import json
from pathlib import Path

SRC = Path(__file__).parent / "data" / "glaze_references.json"

with open(SRC, 'r', encoding='utf-8') as f:
    data = json.load(f)

people = data['glaze_chemistry_references']['people']
books = data['glaze_chemistry_references']['books']

existing_ids = {p['id'] for p in people}
existing_book_ids = {b['id'] for b in books}

# ── New People ───────────────────────────────────────────────────────────────

new_people = [
    # TIER 1 — Glaring Omissions
    {
        "id": "philipau_derek",
        "name": "Derek Au (Philipau)",
        "era": "Contemporary",
        "nationality": "American",
        "role": ["developer", "educator"],
        "institution": "Glazy.org",
        "known_for": [
            "Glazy.org — largest open glaze chemistry database",
            "UMF calculator and visualization tools",
            "open-source glaze data democratization"
        ],
        "notes": "Created and maintains Glazy.org, the world's largest open ceramics database with 340K+ entries. Made UMF calculation and glaze chemistry accessible to every potter with a browser. Open-source (Laravel+Vue). The dataset that feeds Stull Atlas.",
        "tags": ["contemporary", "database", "open-source", "foundational"],
        "collaborators": ["Tony Hansen"]
    },
    {
        "id": "binns_charles",
        "name": "Charles Fergus Binns",
        "era": "19th-20th Century",
        "nationality": "British-American",
        "role": ["educator", "author", "ceramic scientist"],
        "institution": "Alfred University / New York State College of Ceramics",
        "known_for": [
            "Founded first US ceramics program (Alfred, 1900)",
            "The Potter's Craft",
            "father of American ceramic education"
        ],
        "notes": "Son of the director of Royal Worcester. Founded the ceramics program at Alfred University in 1900 — the root node of American glaze education. Rhodes, Cushing, and almost everyone downstream traces back to Alfred. Wrote The Potter's Craft (1910).",
        "tags": ["historical", "foundational", "education", "Alfred University"],
        "collaborators": []
    },
    {
        "id": "robineau_adelaide",
        "name": "Adelaide Alsop Robineau",
        "era": "19th-20th Century",
        "nationality": "American",
        "role": ["studio potter", "editor", "researcher"],
        "institution": "University City / Keramic Studio magazine",
        "known_for": [
            "Keramic Studio magazine editorship",
            "crystalline glaze pioneering",
            "Scarab Vase (1910)",
            "porcelain and high-fire experimentation"
        ],
        "notes": "Editor of Keramic Studio (precursor to Ceramics Monthly). Crystalline glaze pioneer who achieved results nobody could replicate for decades. The Scarab Vase took 1000+ hours of carving on a single porcelain form. Applied scientific method to glaze development before it was standard practice.",
        "tags": ["historical", "foundational", "crystalline", "porcelain"],
        "collaborators": ["Taxile Doat"]
    },
    {
        "id": "roy_ron",
        "name": "Ron Roy",
        "era": "20th-21st Century",
        "nationality": "Canadian",
        "role": ["researcher", "educator"],
        "known_for": [
            "cone 6 oxidation revolution",
            "systematic glaze testing",
            "food safety in glazes",
            "collaboration with Tony Hansen"
        ],
        "notes": "Co-developer of the cone 6 oxidation movement. His systematic testing made cone 6 viable as a production temperature — directly influencing thousands of studios to move away from cone 10. Third leg of the Hansen-Hesselberth-Roy stool. Deeply concerned with glaze safety and leaching.",
        "tags": ["contemporary", "cone 6", "testing", "safety"],
        "collaborators": ["Tony Hansen", "John Hesselberth"]
    },
    {
        "id": "doat_taxile",
        "name": "Taxile Doat",
        "era": "19th-20th Century",
        "nationality": "French",
        "role": ["studio potter", "author", "researcher"],
        "institution": "Sèvres Porcelain Manufactory / University City",
        "known_for": [
            "Grand Feu Ceramics (1905)",
            "crystalline glaze chemistry",
            "zinc crystal growth",
            "pâte-sur-pâte"
        ],
        "notes": "Master ceramist at Sèvres who figured out zinc crystal growth before anyone had the phase diagrams to explain why. Grand Feu Ceramics (1905) was the first serious treatment of high-fire glaze chemistry from a practitioner. Directly influenced Robineau and the University City experiment.",
        "tags": ["historical", "foundational", "crystalline", "French"],
        "collaborators": ["Adelaide Alsop Robineau"]
    },
    {
        "id": "kingery_david",
        "name": "W. David Kingery",
        "era": "20th Century",
        "nationality": "American",
        "role": ["author", "ceramic scientist", "researcher"],
        "institution": "MIT / University of Arizona",
        "known_for": [
            "Introduction to Ceramics",
            "thermal analysis framework",
            "ceramic material science",
            "phase equilibria in glazes"
        ],
        "notes": "THE textbook author for ceramic material science. Introduction to Ceramics (1960, co-authored) defined the field for 60+ years. His thermal expansion, coefficient of thermal expansion, and glaze fit frameworks underpin half the calculations in modern glaze software. Bridged pure material science and applied ceramics.",
        "tags": ["academic", "foundational", "industrial", "material science"],
        "collaborators": []
    },

    # TIER 2 — Strong Candidates
    {
        "id": "pinnell_pete",
        "name": "Pete Pinnell",
        "era": "Contemporary",
        "nationality": "American",
        "role": ["educator", "researcher", "studio potter"],
        "institution": "University of Nebraska-Lincoln",
        "known_for": [
            "crystalline glaze chemistry education",
            "systematic glaze workshop method",
            "specialty glaze chemistry"
        ],
        "notes": "One of the most respected living glaze chemistry educators. His workshops are deeply analytical — real chemistry, not just recipes. Systematic approach to crystalline, specialty, and surface-effect glazes. Teaches potters to think in oxides, not ingredients.",
        "tags": ["contemporary", "education", "crystalline", "systematic"],
        "collaborators": []
    },
    {
        "id": "green_david",
        "name": "David Green",
        "era": "20th Century",
        "nationality": "British",
        "role": ["author", "educator"],
        "known_for": [
            "Understanding Pottery Glazes",
            "clear explanations of glaze chemistry for studio potters"
        ],
        "notes": "Wrote one of the clearest explanations of glaze chemistry for studio potters ever published. Understanding Pottery Glazes bridges the gap between industrial ceramic science and studio practice without dumbing anything down.",
        "tags": ["studio", "education", "British"],
        "collaborators": []
    },
    {
        "id": "chappell_james",
        "name": "James Chappell",
        "era": "20th-21st Century",
        "nationality": "American",
        "role": ["author"],
        "known_for": [
            "The Potter's Complete Book of Clay and Glazes",
            "comprehensive recipe reference"
        ],
        "notes": "Wrote the single most comprehensive recipe reference book in studio ceramics — hundreds of recipes with chemistry, organized by type, cone, and atmosphere. A workhorse book that sits next to the kiln, not on the shelf. Multiple revised editions.",
        "tags": ["studio", "reference", "recipes"],
        "collaborators": []
    },
    {
        "id": "daly_greg",
        "name": "Greg Daly",
        "era": "Contemporary",
        "nationality": "Australian",
        "role": ["studio potter", "author", "educator"],
        "known_for": [
            "Lustre",
            "Glazes and Glazing Techniques",
            "luster glaze chemistry",
            "metallic oxide reduction films"
        ],
        "notes": "Leading authority on luster glazes and their chemistry. Covers a domain nobody else in glaze literature treats with this depth — the metallic oxide reduction films that create iridescent surfaces. Also expert in fuming techniques.",
        "tags": ["contemporary", "luster", "specialty", "Australian"],
        "collaborators": []
    },
    {
        "id": "kline_gabriel",
        "name": "Gabriel Kline",
        "era": "Contemporary",
        "nationality": "American",
        "role": ["author", "studio potter", "educator"],
        "known_for": [
            "Crystalline Glazes: Understanding the Process and Materials",
            "zinc silicate crystal growth",
            "crystalline glaze firing schedules"
        ],
        "notes": "Wrote the modern bible of crystalline glaze chemistry. Covers zinc silicate crystal nucleation and growth, firing schedules, cooling curves, and seeding techniques with real science. Fills a gap no other single book covers at this depth.",
        "tags": ["contemporary", "crystalline", "specialty"],
        "collaborators": []
    },
    {
        "id": "rogers_phil",
        "name": "Phil Rogers",
        "era": "20th-21st Century",
        "nationality": "British (Welsh)",
        "role": ["studio potter", "author"],
        "known_for": [
            "Ash Glazes (practical guide)",
            "wood-ash chemistry for studio use",
            "salt and soda glazes"
        ],
        "notes": "Different from Tichane's historical reconstruction approach — Phil's Ash Glazes is practical wood-ash chemistry focused on studio use. Also wrote on salt glazes. Welsh potter who worked with local materials and understood their chemistry intimately.",
        "tags": ["studio", "ash", "wood-fire", "British"],
        "collaborators": []
    },

    # TIER 3 — Worth Including
    {
        "id": "finkelnburg_dave",
        "name": "Dave Finkelnburg",
        "era": "Contemporary",
        "nationality": "American",
        "role": ["educator", "researcher"],
        "known_for": [
            "glaze fit analysis",
            "thermal expansion matching",
            "crazing and shivering diagnosis",
            "online glaze chemistry education"
        ],
        "notes": "Active educator who writes extensively about glaze fit, thermal expansion, crazing vs. shivering. Applies analytical chemistry to everyday studio problems. Very active in the online glaze chemistry community — Clayart, Glazy forums, Ceramic Arts Network.",
        "tags": ["contemporary", "analytical", "glaze fit", "education"],
        "collaborators": []
    },
    {
        "id": "severijns_hein",
        "name": "Hein Severijns",
        "era": "Contemporary",
        "nationality": "Dutch",
        "role": ["developer"],
        "known_for": [
            "GlazeMaster software",
            "early computational glaze chemistry"
        ],
        "notes": "Created GlazeMaster, one of the earliest glaze calculation software packages alongside Hansen's Insight. Part of the software-makes-chemistry-accessible story of the 1990s-2000s.",
        "tags": ["contemporary", "software", "computational"],
        "collaborators": []
    },
    {
        "id": "branfman_steve",
        "name": "Steve Branfman",
        "era": "Contemporary",
        "nationality": "American",
        "role": ["author", "studio potter", "educator"],
        "institution": "The Potters Shop, Needham MA",
        "known_for": [
            "Mastering Raku",
            "low-fire reduction chemistry",
            "luster and carbon trapping",
            "raku glaze formulation"
        ],
        "notes": "Wrote the definitive practical guide to raku chemistry — carbon trapping, metallic lusters, copper reduction, post-firing chemistry. Narrow domain but deep expertise. Runs The Potters Shop in Massachusetts.",
        "tags": ["contemporary", "raku", "low-fire", "reduction"],
        "collaborators": []
    },
]

# ── New Books ────────────────────────────────────────────────────────────────

new_books = [
    {
        "id": "potters_craft_binns",
        "title": "The Potter's Craft",
        "author_ids": ["binns_charles"],
        "year": 1910,
        "notes": "One of the first American texts treating pottery making as both craft and science. Includes glaze chemistry fundamentals from a working potter's perspective. Written by the founder of Alfred University's ceramics program.",
        "tags": ["historical", "foundational", "education"]
    },
    {
        "id": "grand_feu_ceramics_doat",
        "title": "Grand Feu Ceramics",
        "author_ids": ["doat_taxile"],
        "year": 1905,
        "notes": "First serious treatment of high-fire glaze chemistry from a practitioner. Originally in French (Grand Feu Céramiques), translated to English by Samuel Robineau. Covers crystalline glazes, flambés, and high-fire effects with scientific rigor decades ahead of its time.",
        "tags": ["historical", "foundational", "crystalline", "French"]
    },
    {
        "id": "intro_ceramics_kingery",
        "title": "Introduction to Ceramics",
        "author_ids": ["kingery_david"],
        "year": 1960,
        "notes": "THE ceramic material science textbook for 60+ years. Co-authored with H.K. Bowen and D.R. Uhlmann. Covers phase equilibria, thermal expansion, viscosity, and every physical property relevant to glaze chemistry. Dense, technical, irreplaceable. Revised as 'Introduction to Ceramics' 2nd ed. (1976).",
        "tags": ["academic", "foundational", "material science"]
    },
    {
        "id": "understanding_glazes_green",
        "title": "Understanding Pottery Glazes",
        "author_ids": ["green_david"],
        "year": 1963,
        "notes": "One of the clearest explanations of glaze chemistry for studio potters ever published. Bridges industrial ceramic science and studio practice without dumbing it down. British perspective.",
        "tags": ["studio", "education", "British"]
    },
    {
        "id": "complete_clay_glazes_chappell",
        "title": "The Potter's Complete Book of Clay and Glazes",
        "author_ids": ["chappell_james"],
        "year": 1991,
        "notes": "The single most comprehensive recipe reference in studio ceramics. Hundreds of recipes organized by type, cone, and atmosphere, with chemistry. A workhorse book — sits next to the kiln. Multiple revised editions including 2nd ed. (2004).",
        "tags": ["studio", "reference", "recipes"]
    },
    {
        "id": "lustre_daly",
        "title": "Lustre",
        "author_ids": ["daly_greg"],
        "year": 2013,
        "notes": "Definitive guide to luster glaze chemistry and technique. Covers metallic oxide reduction films, fuming, and iridescent surfaces. Nobody else covers this domain at this depth.",
        "tags": ["contemporary", "luster", "specialty"]
    },
    {
        "id": "glazes_glazing_techniques_daly",
        "title": "Glazes and Glazing Techniques",
        "author_ids": ["daly_greg"],
        "year": 1995,
        "notes": "Broad glaze chemistry reference with particular strength in color development and specialty effects from an Australian perspective.",
        "tags": ["contemporary", "studio", "color"]
    },
    {
        "id": "crystalline_glazes_kline",
        "title": "Crystalline Glazes: Understanding the Process and Materials",
        "author_ids": ["kline_gabriel"],
        "year": 2018,
        "notes": "The modern bible of crystalline glaze chemistry. Covers zinc silicate crystal nucleation and growth, firing schedules, cooling curves, and seeding techniques with real science. The book the crystalline community was waiting for.",
        "tags": ["contemporary", "crystalline", "specialty"]
    },
    {
        "id": "ash_glazes_rogers",
        "title": "Ash Glazes",
        "author_ids": ["rogers_phil"],
        "year": 2003,
        "notes": "Practical wood-ash chemistry focused on studio use. Different from Tichane's historical reconstruction approach — this is about making ash glazes work in a modern studio. Covers sourcing, washing, testing, and formulating.",
        "tags": ["studio", "ash", "wood-fire"]
    },
    {
        "id": "mastering_raku_branfman",
        "title": "Mastering Raku",
        "author_ids": ["branfman_steve"],
        "year": 2001,
        "notes": "Definitive guide to raku chemistry and technique — carbon trapping, metallic lusters, copper reduction, post-firing reduction chemistry. Multiple editions.",
        "tags": ["contemporary", "raku", "low-fire", "reduction"]
    },
]

# ── Apply ────────────────────────────────────────────────────────────────────

added_people = 0
added_books = 0

for p in new_people:
    if p['id'] not in existing_ids:
        people.append(p)
        added_people += 1
        print(f"  + person: {p['name']}")
    else:
        print(f"  SKIP (exists): {p['name']}")

for b in new_books:
    if b['id'] not in existing_book_ids:
        books.append(b)
        added_books += 1
        print(f"  + book: {b['title']}")
    else:
        print(f"  SKIP (exists): {b['title']}")

# Also update collaborator links for existing people
by_id = {p['id']: p for p in people}

# Hansen should know about Derek and Ron Roy
if 'hansen_tony' in by_id:
    collabs = by_id['hansen_tony'].setdefault('collaborators', [])
    for name in ['Ron Roy', 'John Hesselberth', 'Derek Au']:
        if name not in collabs:
            collabs.append(name)

# Hesselberth should know about Ron Roy
if 'hesselberth_john' in by_id:
    collabs = by_id['hesselberth_john'].setdefault('collaborators', [])
    for name in ['Tony Hansen', 'Ron Roy']:
        if name not in collabs:
            collabs.append(name)

with open(SRC, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nDone: +{added_people} people, +{added_books} books")
print(f"Totals: {len(people)} people, {len(books)} books")

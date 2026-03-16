"""
Add Round 2 — historical anchors, domain gaps, concepts
"""
import json
from pathlib import Path

SRC = Path(__file__).parent / "data" / "glaze_references.json"

with open(SRC, 'r', encoding='utf-8') as f:
    data = json.load(f)

people = data['glaze_chemistry_references']['people']
books = data['glaze_chemistry_references']['books']
concepts = data['glaze_chemistry_references']['concepts']

existing_ids = {p['id'] for p in people}
existing_book_ids = {b['id'] for b in books}
existing_concept_ids = {c['id'] for c in concepts}

# ── New People ───────────────────────────────────────────────────────────────

new_people = [
    {
        "id": "abu_al_qasim",
        "name": "Abu'l-Qasim",
        "era": "Medieval (fl. 1301)",
        "nationality": "Persian",
        "role": ["author", "ceramist"],
        "institution": "Kashan tile workshops",
        "known_for": [
            "First known treatise on ceramic technology (1301)",
            "luster glaze documentation",
            "tin opacification",
            "frit chemistry",
            "kiln design documentation"
        ],
        "notes": "Wrote the first known treatise on ceramic technology in 1301, documenting the glaze and tile-making traditions of Kashan, Persia. Describes luster glaze preparation, tin opacification for white grounds, frit chemistry, and kiln construction. Everything in glaze chemistry descends from someone deciding to write it down instead of just doing it. This is that person.",
        "tags": ["historical", "foundational", "medieval", "Persian", "luster"],
        "collaborators": []
    },
    {
        "id": "dentrecolles_francois",
        "name": "Père d'Entrecolles (François Xavier d'Entrecolles)",
        "era": "17th-18th Century",
        "nationality": "French",
        "role": ["observer", "author"],
        "institution": "Jesuit Mission, Jingdezhen",
        "known_for": [
            "Letters from Jingdezhen (1712, 1722)",
            "first Western documentation of Chinese porcelain manufacture",
            "kaolin and petuntse identification",
            "East-to-West ceramic knowledge transfer"
        ],
        "notes": "Jesuit missionary stationed in Jingdezhen, China's porcelain capital. His two letters (1712, 1722) describing Chinese porcelain and glaze manufacture in precise detail were industrial espionage that changed Western ceramics forever. Identified kaolin and petuntse (china stone) as the two essential ingredients. Without him, European high-fire glaze chemistry would have been delayed by decades. The bridge between East and West.",
        "tags": ["historical", "foundational", "Chinese", "porcelain"],
        "collaborators": []
    },
    {
        "id": "wedgwood_josiah",
        "name": "Josiah Wedgwood",
        "era": "18th Century",
        "nationality": "British",
        "role": ["industrialist", "researcher", "inventor"],
        "institution": "Wedgwood / Etruria Works",
        "known_for": [
            "systematic experimental method for ceramics",
            "Experiment Book (5,000+ trials)",
            "pyrometer invention",
            "jasperware and basalt glaze chemistry",
            "industrial-scale glaze quality control"
        ],
        "notes": "Invented systematic experimental method for ceramics a century before anyone else. His Experiment Book documents 5,000+ methodical trials — varying one ingredient at a time, recording results. Invented a pyrometer for kiln temperature measurement. Was doing what Ian Currie formalized 200 years later. Fellow of the Royal Society. If Seger is the father of glaze calculation, Wedgwood is the father of glaze experimentation.",
        "tags": ["historical", "foundational", "experimental", "industrial"],
        "collaborators": []
    },
    {
        "id": "nichols_gail",
        "name": "Gail Nichols",
        "era": "Contemporary",
        "nationality": "Australian",
        "role": ["studio potter", "author", "educator"],
        "known_for": [
            "Soda, Clay, and Fire",
            "soda firing chemistry",
            "sodium carbonate vapor deposition",
            "soda vs salt glaze chemistry distinction"
        ],
        "notes": "Wrote the definitive book on soda glazing chemistry. Covers the vapor deposition mechanism, how sodium carbonate interacts with different clay bodies, and the surface chemistry that distinguishes soda from salt firing. Fills a major domain gap — soda firing is chemically distinct from salt (sodium carbonate vs sodium chloride) but often lumped together.",
        "tags": ["contemporary", "soda firing", "atmospheric", "Australian"],
        "collaborators": []
    },
    {
        "id": "obstler_mimi",
        "name": "Mimi Obstler",
        "era": "Contemporary",
        "nationality": "American",
        "role": ["author", "educator"],
        "known_for": [
            "Out of the Earth, Into the Fire",
            "ceramic materials science for studio potters",
            "thermal behavior and mineralogy",
            "phase changes in the kiln"
        ],
        "notes": "Bridges materials science and studio practice in a way that's genuinely accessible. Out of the Earth, Into the Fire covers thermal behavior, mineralogy, phase changes, and chemical reactions in the kiln — everything Parmelee and Norton cover but written for people who fire kilns, not run factories. Often the first recommendation when a potter asks 'I want to understand WHY glazes do what they do.'",
        "tags": ["contemporary", "material science", "education", "studio"],
        "collaborators": []
    },
    {
        "id": "norsker_henrik",
        "name": "Henrik Norsker",
        "era": "Contemporary",
        "nationality": "Danish",
        "role": ["author", "researcher", "development worker"],
        "known_for": [
            "Glazes for the Self-Reliant Potter",
            "local materials glaze development",
            "developing-world ceramics",
            "geology-first glaze formulation"
        ],
        "notes": "Co-authored Glazes for the Self-Reliant Potter (with James Danisch) — how to develop glazes from local rocks, ash, and clay when commercial materials aren't available. Published through a developing-world ceramics organization. Represents a fundamentally different approach: geology-first instead of catalog-first. This is the original approach to glaze chemistry — every tradition before suppliers existed worked this way.",
        "tags": ["contemporary", "local materials", "development", "geology"],
        "collaborators": ["James Danisch"]
    },
    {
        "id": "illian_clary",
        "name": "Clary Illian",
        "era": "Contemporary",
        "nationality": "American",
        "role": ["studio potter", "author", "educator"],
        "known_for": [
            "A Potter's Workbook",
            "Leach-MacKenzie tradition third generation",
            "materials-based glaze thinking"
        ],
        "notes": "Studied under Warren MacKenzie, who studied under Bernard Leach. Represents the third generation of the Leach tradition with real chemistry understanding, not just aesthetics. A Potter's Workbook is the most practical 'here's how to think about glazes from raw materials' text in that lineage. Completes the Leach → MacKenzie → Illian chain.",
        "tags": ["contemporary", "studio", "Leach tradition", "materials"],
        "collaborators": ["Warren MacKenzie"]
    },
    {
        "id": "mostert_pieter",
        "name": "Pieter Mostert",
        "era": "Contemporary",
        "nationality": "South African",
        "role": ["researcher", "developer"],
        "known_for": [
            "computational glaze analysis",
            "Glazy dataset statistical analysis",
            "oxide space clustering",
            "open-source glaze data science"
        ],
        "notes": "Active researcher doing computational analysis of the Glazy dataset. His glazy-data-analysis GitHub repository is prior art for statistical analysis of glaze chemistry space — clustering, visualization, and pattern discovery in oxide data. Python-based, open-source. Represents the emerging intersection of data science and ceramic chemistry.",
        "tags": ["contemporary", "computational", "data science", "open-source"],
        "collaborators": ["Derek Au (Philipau)"]
    },
    {
        "id": "kusakabe_masakazu",
        "name": "Masakazu Kusakabe",
        "era": "Contemporary",
        "nationality": "Japanese",
        "role": ["studio potter", "author", "educator"],
        "known_for": [
            "Japanese Wood-Fired Ceramics",
            "anagama and noborigama kiln science",
            "ash deposit chemistry",
            "Japanese firing atmosphere analysis"
        ],
        "notes": "Co-authored Japanese Wood-Fired Ceramics (with Marc Lancet) — scientific treatment of anagama and noborigama atmosphere chemistry, ash deposit mechanisms, wadding chemistry. Not romanticized — actual kiln science from a Japanese master who bridges Japanese empirical tradition and Western analytical frameworks. Fills the gap for Japanese wood-firing science from the inside.",
        "tags": ["contemporary", "wood-fire", "Japanese", "kiln science"],
        "collaborators": ["Marc Lancet"]
    },
]

# ── New Books ────────────────────────────────────────────────────────────────

new_books = [
    {
        "id": "soda_clay_fire_nichols",
        "title": "Soda, Clay, and Fire",
        "author_ids": ["nichols_gail"],
        "year": 2006,
        "notes": "Definitive guide to soda firing chemistry. Covers sodium carbonate vapor deposition mechanisms, clay body interactions, surface chemistry differences from salt firing. The book that finally gave soda firing its own scientific identity separate from salt.",
        "tags": ["contemporary", "soda firing", "atmospheric"]
    },
    {
        "id": "out_of_earth_obstler",
        "title": "Out of the Earth, Into the Fire",
        "author_ids": ["obstler_mimi"],
        "year": 2000,
        "notes": "Ceramic materials science written for studio potters. Covers thermal behavior, mineralogy, phase changes, and kiln chemistry. Bridges the gap between dense academic texts (Kingery, Norton) and recipe books. Often the first recommendation for potters wanting to understand the 'why' behind glaze behavior.",
        "tags": ["contemporary", "material science", "education"]
    },
    {
        "id": "self_reliant_potter_norsker",
        "title": "Glazes for the Self-Reliant Potter",
        "author_ids": ["norsker_henrik"],
        "year": 1990,
        "notes": "Co-authored with James Danisch. How to develop glazes from local rocks, ash, and clay without commercial suppliers. Published for developing-world ceramics programs. A fundamentally different approach to glaze chemistry — geology-first, using what the land provides. Also relevant to any potter exploring local-materials practice.",
        "tags": ["development", "local materials", "geology"]
    },
    {
        "id": "potters_workbook_illian",
        "title": "A Potter's Workbook",
        "author_ids": ["illian_clary"],
        "year": 1999,
        "notes": "The most practical materials-based glaze thinking text in the Leach tradition. Third-generation knowledge (Leach → MacKenzie → Illian) distilled into a working guide. Teaches potters to think from materials outward rather than from recipes downward.",
        "tags": ["contemporary", "studio", "Leach tradition", "materials"]
    },
    {
        "id": "japanese_wood_fired_kusakabe",
        "title": "Japanese Wood-Fired Ceramics",
        "author_ids": ["kusakabe_masakazu"],
        "year": 2005,
        "notes": "Co-authored with Marc Lancet. Scientific treatment of Japanese wood-firing traditions — anagama and noborigama kiln atmosphere chemistry, ash deposit mechanisms, wadding chemistry, firing schedules. Bridges Japanese empirical kiln knowledge and Western analytical frameworks.",
        "tags": ["contemporary", "wood-fire", "Japanese", "kiln science"]
    },
]

# ── New Concepts ─────────────────────────────────────────────────────────────

new_concepts = [
    {
        "id": "phase_diagrams",
        "name": "Phase Diagrams & Eutectics",
        "type": "concept",
        "developed_by": ["seger_hermann", "kingery_david", "parmelee_cw"],
        "notes": "Phase diagrams map which mineral phases are stable at given temperature and composition. Eutectics are compositions where two or more materials melt together at a temperature lower than either would alone — the fundamental reason glazes melt where they do. The SiO₂-Al₂O₃ binary phase diagram underpins the Stull chart. Understanding eutectics explains why a glaze melts at cone 6 when none of its individual ingredients would.",
        "tags": ["foundational", "material science", "melting behavior"],
        "related_people": ["kingery_david", "parmelee_cw", "norton_fh", "stull_ray"]
    },
    {
        "id": "thermal_expansion_glaze_fit",
        "name": "Thermal Expansion & Glaze Fit",
        "type": "concept",
        "developed_by": ["kingery_david", "parmelee_cw", "hesselberth_john"],
        "notes": "When a glaze and clay body cool from kiln temperature, they contract at different rates determined by their coefficient of thermal expansion (CTE). If the glaze contracts more than the body, it goes into tension → crazing (fine cracks). If it contracts less, it goes into compression → shivering (glaze flaking). Perfect 'glaze fit' means the glaze is in slight compression. This is the #1 practical problem in studio ceramics and the reason potters adjust silica, alumina, and flux ratios. Calculated from oxide contributions using Appen factors or measured with a dilatometer.",
        "tags": ["foundational", "practical", "glaze fit", "crazing"],
        "related_people": ["kingery_david", "finkelnburg_dave", "hesselberth_john", "hansen_tony"]
    },
    {
        "id": "crystalline_glaze_theory",
        "name": "Crystalline Glaze Theory",
        "type": "concept",
        "developed_by": ["doat_taxile", "robineau_adelaide"],
        "notes": "Crystalline glazes produce visible crystals (typically zinc silicate — willemite, Zn₂SiO₄) that grow during controlled cooling. The chemistry requires: high zinc oxide (25-30% of flux), high silica, very low alumina (alumina inhibits crystal growth), and a specific cooling schedule — rapid cooling to nucleation temperature (~1050°C), then a long hold (2-8 hours) while crystals grow, then final cooling. Nucleation sites can be seeded. The result is predictable in chemistry but chaotic in pattern — every firing is unique. First achieved systematically by Taxile Doat at Sèvres, then by Robineau in America.",
        "tags": ["specialty", "crystalline", "zinc silicate", "cooling schedule"],
        "related_people": ["doat_taxile", "robineau_adelaide", "kline_gabriel", "pinnell_pete"]
    },
]

# ── Apply ────────────────────────────────────────────────────────────────────

added_people = 0
added_books = 0
added_concepts = 0

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

for c in new_concepts:
    if c['id'] not in existing_concept_ids:
        concepts.append(c)
        added_concepts += 1
        print(f"  + concept: {c['name']}")
    else:
        print(f"  SKIP (exists): {c['name']}")

# Update collaborator links
by_id = {p['id']: p for p in people}

# MacKenzie should link to Illian
if 'mackenzie_warren' in by_id:
    collabs = by_id['mackenzie_warren'].setdefault('collaborators', [])
    if 'Clary Illian' not in collabs:
        collabs.append('Clary Illian')

# Philipau should link to Mostert
if 'philipau_derek' in by_id:
    collabs = by_id['philipau_derek'].setdefault('collaborators', [])
    if 'Pieter Mostert' not in collabs:
        collabs.append('Pieter Mostert')

with open(SRC, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nDone: +{added_people} people, +{added_books} books, +{added_concepts} concepts")
print(f"Totals: {len(people)} people, {len(books)} books, {len(concepts)} concepts")

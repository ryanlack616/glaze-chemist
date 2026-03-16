"""
Enrich all 36 people in glaze_references.json with institutions, collaborators,
nationalities, and notes based on well-documented ceramic history.
"""
import json
from copy import deepcopy

SRC = r'C:\Users\PC\Desktop\glaze-chemist\data\glaze_references.json'

with open(SRC, 'r', encoding='utf-8') as f:
    data = json.load(f)

people = data['glaze_chemistry_references']['people']
by_id = {p['id']: p for p in people}

# ── Enrichment map ───────────────────────────────────────────────────────────
# Only fills in what's MISSING or extends collaborators.

enrichments = {
    "seger_hermann": {
        "institution": "Royal Porcelain Factory, Berlin (KPM)",
        "collaborators": [],  # different era from everyone else
    },
    "rhodes_daniel": {
        "institution": "Alfred University",
        "collaborators": ["Val Cushing"],
    },
    "leach_bernard": {
        "institution": "Leach Pottery, St Ives",
        "collaborators": ["Shoji Hamada", "Michael Cardew", "Warren MacKenzie"],
    },
    "hamer_frank": {
        "institution": None,  # independent author
    },
    "hamer_janet": {
        "notes": "Co-authored The Potter's Dictionary with Frank Hamer; the collaboration produced one of the most enduring reference works in ceramics.",
    },
    "britt_john": {
        "institution": None,  # independent/workshop-based
        "collaborators": ["Val Cushing"],  # studied at Alfred under Cushing's influence
    },
    "bloomfield_linda": {
        "institution": None,  # independent, London-based
    },
    "cushing_val": {
        # already has Alfred
        "collaborators": ["Daniel Rhodes", "Matt Katz"],
    },
    "grotell_maija": {
        "institution": "Cranbrook Academy of Art",
        "collaborators": ["Bernard Leach"],  # part of the transatlantic ceramics exchange
    },
    "cardew_michael": {
        "institution": "Wenford Bridge Pottery",
        "collaborators": ["Bernard Leach"],
    },
    "hopper_robin": {
        "institution": None,  # independent, Victoria BC
        "nationality": "British-Canadian",  # born UK, worked in Canada
    },
    "hansen_tony": {
        "institution": "Digitalfire",
        "collaborators": ["John Hesselberth", "Robert Desjardins"],
    },
    "hesselberth_john": {
        "institution": None,  # independent researcher
        "collaborators": ["Tony Hansen"],
    },
    "currie_ian": {
        "institution": None,  # independent researcher, Australia
    },
    "tichane_robert": {
        "institution": None,  # independent researcher, self-published
    },
    "katz_matt": {
        # already has Alfred
        "collaborators": ["Val Cushing", "John Britt"],
    },
    "zakin_richard": {
        "institution": "SUNY Oswego",
    },
    "sanders_herbert": {
        "institution": "San Jose State University",
    },
    "wood_nigel": {
        "institution": "University of Westminster",
    },
    "lawrence_wg": {
        "nationality": "American",
        "institution": None,  # industrial background
    },
    "norton_fh": {
        # already has MIT
    },
    "parmelee_cw": {
        "nationality": "American",
        "institution": "University of Illinois",
    },
    "orton_edward_jr": {
        "institution": "Ohio State University / Orton Ceramic Foundation",
    },
    "cooper_emmanuel": {
        "institution": "Ceramic Review / City of Westminster College",
    },
    "soldner_paul": {
        "institution": "Scripps College",
        "collaborators": ["Warren MacKenzie"],
    },
    "mackenzie_warren": {
        # already has U of Minnesota
        "collaborators": ["Bernard Leach", "Shoji Hamada"],
    },
    "troy_jack": {
        "institution": "Juniata College",
        "collaborators": ["John Neely"],
    },
    "temple_byron": {
        "institution": "Alfred University",  # studied there
        "collaborators": ["Daniel Rhodes", "Val Cushing"],
    },
    "hamada_shoji": {
        "institution": "Mashiko, Japan",
        "collaborators": ["Bernard Leach", "Warren MacKenzie"],
    },
    "minogue_coll": {
        "notes": "Co-authored key wood-fire chemistry texts with Robert Sanderson; practical and analytical approach to ash and atmospheric glazes.",
    },
    "sanderson_robert": {
        "nationality": "British",
        "notes": "Co-authored wood-fire chemistry texts with Coll Minogue; systematic documentation of ash glaze behavior.",
    },
    "neely_john": {
        # already has Utah State
        "collaborators": ["Jack Troy"],
    },
    "zamek_jeff": {
        "institution": None,  # independent consultant
    },
    "birks_tony": {
        "institution": None,  # independent author
    },
    "desjardins_robert": {
        "nationality": "Canadian",
        "collaborators": ["Tony Hansen"],
    },
    "stull_ray": {
        # already has U of Illinois
    },
}

# ── Apply enrichments ────────────────────────────────────────────────────────

changes = 0
for pid, updates in enrichments.items():
    if pid not in by_id:
        print(f"  ⚠ {pid} not found — skipping")
        continue
    
    p = by_id[pid]
    
    for key, val in updates.items():
        if val is None:
            continue
        
        if key == 'collaborators':
            existing = set(p.get('collaborators', []))
            new_collabs = [c for c in val if c not in existing]
            if new_collabs:
                p['collaborators'] = list(existing) + new_collabs
                changes += 1
                print(f"  + {p['name']}: collaborators += {new_collabs}")
        elif key in ('institution', 'nationality', 'notes'):
            if not p.get(key):
                p[key] = val
                changes += 1
                print(f"  + {p['name']}: {key} = {val}")
        else:
            if not p.get(key):
                p[key] = val
                changes += 1
                print(f"  + {p['name']}: {key} = {val}")

# ── Save ─────────────────────────────────────────────────────────────────────

with open(SRC, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✓ {changes} fields enriched across {len(enrichments)} people")
print(f"  Saved to {SRC}")

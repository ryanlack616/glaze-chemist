"""
Migrate glaze_references.json people entries from v1 (flat) to People Schema v2.

Reads: data/glaze_references.json  (key: glaze_chemistry_references.people)
Writes: data/people_v2.json        (collection wrapper per schema migration_notes)

Run: python -X utf8 _migrate_people_v2.py
"""
import json
import re
from datetime import date
from pathlib import Path

# ─── Controlled-enum values ───────────────────────────────────────────────────
VALID_CONTRIBUTION_TYPES = {
    "umf_calculation", "materials_science", "glaze_fit_expansion",
    "kiln_atmosphere", "ash_glaze", "salt_soda", "crystalline", "lustre",
    "majolica_low_fire", "industrial_research", "defect_analysis",
    "testing_methodology", "software_computation", "local_materials",
    "historical_revival", "colorants_surface",
}

VALID_AFFILIATION_TYPES = {
    "institution", "studio", "company", "museum",
    "movement", "publisher", "platform", "independent",
}

VALID_RELATIONS = {
    "teacher_of", "student_of", "influenced_by", "historical_parallel",
    "technical_lineage", "institutional_link", "shared_domain",
}

# ─── Helper: v1 id (underscores) → v2 slug (hyphens) ─────────────────────────
def to_slug(v1_id: str) -> str:
    return v1_id.replace("_", "-")


# ─── era string → periods array ───────────────────────────────────────────────
ERA_MAP = {
    "medieval (fl. 1301)": ["Medieval"],
    "17th-18th century":   ["17th Century", "18th Century"],
    "18th century":        ["18th Century"],
    "19th century":        ["19th Century"],
    "19th-20th century":   ["19th Century", "20th Century"],
    "early 20th century":  ["Early 20th Century"],
    "20th century":        ["20th Century"],
    "20th-21st century":   ["20th Century", "21st Century"],
    "contemporary":        ["Contemporary"],
}

def era_to_periods(era: str) -> list[str]:
    key = era.strip().lower()
    return ERA_MAP.get(key, [era.strip()])


# ─── Institution string → affiliation object ──────────────────────────────────
INSTITUTION_TYPE_HINTS = {
    "university":  "institution",
    "college":     "institution",
    "institute":   "institution",
    "school":      "institution",
    "workshop":    "institution",
    "pottery":     "studio",
    "studio":      "studio",
    "atelier":     "studio",
    "factory":     "company",
    "works":       "company",
    "pilkington":  "company",
    "museum":      "museum",
    "gallery":     "museum",
    "press":       "publisher",
}

def institution_to_affiliation(inst: str) -> dict:
    low = inst.lower()
    atype = "institution"  # default
    for hint, t in INSTITUTION_TYPE_HINTS.items():
        if hint in low:
            atype = t
            break
    return {"name": inst, "type": atype}


# ─── Build name → v2-slug lookup from full dataset ───────────────────────────
def build_name_to_slug(people: list[dict]) -> dict[str, str]:
    return {p["name"]: to_slug(p["id"]) for p in people}


# ─── Collaborators → related_people ──────────────────────────────────────────
def collaborators_to_related(person: dict, name_to_slug: dict) -> list[dict]:
    out = []
    for name in person.get("collaborators", []):
        slug = name_to_slug.get(name)
        if slug:
            out.append({"id": slug, "relation": "shared_domain"})
    return out


# ─── sort_name from full name ─────────────────────────────────────────────────
def make_sort_name(name: str) -> str:
    parts = name.strip().split()
    if len(parts) >= 2:
        return f"{parts[-1]}, {' '.join(parts[:-1])}"
    return name


# ─── is_living inference ──────────────────────────────────────────────────────
CONTEMPORARY_IDS_DECEASED = {
    # Known Contemporary-era people who are deceased — override
    # (update as needed)
}

def infer_is_living(person: dict) -> bool:
    era = person.get("era", "").strip().lower()
    if era == "contemporary":
        return person["id"] not in CONTEMPORARY_IDS_DECEASED
    return False


# ─── Tag classification ───────────────────────────────────────────────────────
CONTEXT_TAG_WORDS = {
    "historical", "contemporary", "studio", "popular", "beloved", "cult",
    "british", "french", "japanese", "german", "australian", "american",
    "persian", "chinese", "educator", "foundational", "reference",
    "leach tradition", "alfred university", "open-source", "history",
    "scholarly", "academic", "introductory", "introductory", "open access",
    "development", "japanese",
}

def split_tags(tags: list[str]) -> tuple[list[str], list[str]]:
    """Split v1 flat tags into technical_tags and context_tags."""
    technical, context = [], []
    for t in tags:
        low = t.lower()
        if low in CONTEXT_TAG_WORDS or any(w in low for w in {"university", "tradition", "lineage"}):
            context.append(t.lower().replace(" ", "-"))
        else:
            technical.append(t.lower().replace(" ", "-"))
    return technical, context


# ─── Primary contribution type inference ─────────────────────────────────────
def infer_primary_contribution(person: dict) -> str:
    tags   = [t.lower() for t in person.get("tags", [])]
    roles  = [r.lower() for r in person.get("role", [])]
    known  = [k.lower() for k in person.get("known_for", [])]
    pid    = person["id"]
    all_t  = " ".join(tags + roles + known)

    # Specific overrides for well-known figures
    overrides = {
        "seger_hermann":    "umf_calculation",
        "stull_ray":        "umf_calculation",
        "philipau_derek":   "software_computation",
        "hansen_tony":      "software_computation",
        "desjardins_robert":"software_computation",
        "severijns_hein":   "software_computation",
        "mostert_pieter":   "software_computation",
        "hesselberth_john": "glaze_fit_expansion",
        "roy_ron":          "glaze_fit_expansion",
        "finkelnburg_dave": "glaze_fit_expansion",
        "currie_ian":       "testing_methodology",
        "norsker_henrik":   "local_materials",
        "wood_nigel":       "historical_revival",
        "tichane_robert":   "historical_revival",
        "abu_al_qasim":     "historical_revival",
        "dentrecolles_francois": "historical_revival",
        "orton_edward_jr":  "testing_methodology",
        "soldner_paul":     "kiln_atmosphere",
        "branfman_steve":   "kiln_atmosphere",
        "nichols_gail":     "salt_soda",
        "temple_byron":     "salt_soda",
        "troy_jack":        "ash_glaze",
        "leach_bernard":    "ash_glaze",
        "minogue_coll":     "ash_glaze",
        "sanderson_robert": "ash_glaze",
        "rogers_phil":      "ash_glaze",
        "hamada_shoji":     "ash_glaze",
        "robineau_adelaide":"crystalline",
        "doat_taxile":      "crystalline",
        "pinnell_pete":     "crystalline",
        "kline_gabriel":    "crystalline",
        "daly_greg":        "lustre",
        "bloomfield_linda": "colorants_surface",
        "hopper_robin":     "colorants_surface",
        "zakin_richard":    "colorants_surface",
        "lawrence_wg":      "industrial_research",
        "norton_fh":        "industrial_research",
        "parmelee_cw":      "materials_science",
        "kingery_david":    "materials_science",
        "singer_felix":     "industrial_research",
        "wedgwood_josiah":  "industrial_research",
        "binns_charles":    "testing_methodology",
        "grotell_maija":    "testing_methodology",
        "obstler_mimi":     "materials_science",
        "neely_john":       "kiln_atmosphere",
        "mackenzie_warren": "kiln_atmosphere",
        "sanders_herbert":  "ash_glaze",
        "kusakabe_masakazu":"kiln_atmosphere",
        "illian_clary":     "ash_glaze",
        "green_david":      "testing_methodology",
        "cushing_val":      "testing_methodology",
    }
    if pid in overrides:
        return overrides[pid]

    # Fallback heuristics
    if "crystalline" in all_t:             return "crystalline"
    if "lustre" in all_t or "luster" in all_t: return "lustre"
    if "salt glaze" in all_t or "soda fir" in all_t: return "salt_soda"
    if "ash" in all_t:                     return "ash_glaze"
    if "raku" in all_t or "wood fire" in all_t or "wood-fire" in all_t: return "kiln_atmosphere"
    if "umf" in all_t or "unity molecular" in all_t: return "umf_calculation"
    if "software" in all_t or "digital" in all_t or "computational" in all_t: return "software_computation"
    if "glaze fit" in all_t or "thermal expansion" in all_t: return "glaze_fit_expansion"
    if "local material" in all_t:          return "local_materials"
    if "colorant" in all_t or "colour" in all_t: return "colorants_surface"
    if "historical reconstruction" in all_t: return "historical_revival"
    if "industrial" in all_t or "ceramic engineer" in all_t: return "industrial_research"
    if "material science" in all_t or "ceramic scientist" in all_t: return "materials_science"
    if "testing" in all_t or "systematic" in all_t or "analytical" in all_t: return "testing_methodology"

    return "testing_methodology"  # reasonable educator/author default


# ─── Secondary contribution types ────────────────────────────────────────────
def infer_secondary(person: dict, primary: str) -> list[str]:
    tags  = [t.lower() for t in person.get("tags", [])]
    roles = [r.lower() for r in person.get("role", [])]
    known = [k.lower() for k in person.get("known_for", [])]
    all_t = " ".join(tags + roles + known)

    candidates = []
    checks = [
        ("umf_calculation",    "umf" in all_t or "unity molecular" in all_t),
        ("materials_science",  "material science" in all_t or "ceramic scientist" in all_t),
        ("glaze_fit_expansion","glaze fit" in all_t or "thermal expansion" in all_t or "durability" in all_t),
        ("kiln_atmosphere",    "atmospheric" in all_t or "reduction" in all_t or "raku" in all_t),
        ("ash_glaze",          "ash" in all_t),
        ("salt_soda",          "salt" in all_t or "soda" in all_t),
        ("crystalline",        "crystalline" in all_t),
        ("lustre",             "lustre" in all_t or "luster" in all_t),
        ("industrial_research","industrial" in all_t),
        ("testing_methodology","testing" in all_t or "systematic" in all_t or "analytical" in all_t),
        ("software_computation","software" in all_t or "digital" in all_t or "computational" in all_t),
        ("local_materials",    "local material" in all_t or "geology" in all_t),
        ("historical_revival", "historical reconstruction" in all_t or "historical revival" in all_t),
        ("colorants_surface",  "colorant" in all_t or "colour" in all_t),
    ]
    for ctype, condition in checks:
        if condition and ctype != primary:
            candidates.append(ctype)
    return candidates[:3]  # cap at 3


# ─── Domains inference ────────────────────────────────────────────────────────
def infer_domains(person: dict) -> dict:
    tags  = [t.lower() for t in person.get("tags", [])]
    roles = [r.lower() for r in person.get("role", [])]
    known = [k.lower() for k in person.get("known_for", [])]
    era   = person.get("era", "").lower()
    all_t = " ".join(tags + roles + known + [era])

    low_fire   = any(x in all_t for x in ["low-fire", "low fire", "earthenware", "raku", "lustre", "luster", "majolica", "0-6"])
    high_fire  = any(x in all_t for x in ["stoneware", "porcelain", "wood fire", "wood-fire", "salt", "high fire", "crystalline", "ash", "reduction", "cone 10", "cone 9"])
    mid_fire   = any(x in all_t for x in ["cone 6", "mid-fire", "mid fire", "cone-6"])
    industrial = any(x in all_t for x in ["industrial", "factory", "manufacturing", "ceramic engineer"])
    historical = any(x in all_t for x in ["historical", "medieval", "18th", "19th", "history"]) or era not in ["contemporary"]
    education  = any(x in all_t for x in ["educator", "professor", "university", "academic", "teacher", "instructor"])
    software   = any(x in all_t for x in ["software", "digital", "computational", "database", "developer", "data science"])
    atmospheric = any(x in all_t for x in ["atmospheric", "reduction", "raku", "wood fire", "wood-fire", "salt glaze", "soda fir", "kiln atmosphere"])

    # All authors/educators implicitly have education = True
    if "author" in roles or "educator" in roles:
        education = True

    return {
        "low_fire":   low_fire,
        "mid_fire":   mid_fire,
        "high_fire":  high_fire,
        "industrial": industrial,
        "historical": historical,
        "education":  education,
        "software":   software,
        "atmospheric": atmospheric,
    }


# ─── summary_short from notes ─────────────────────────────────────────────────
def make_summary_short(notes: str) -> str:
    if not notes:
        return ""
    # Use first sentence (up to ~120 chars)
    sentences = re.split(r'(?<=[.!?])\s+', notes.strip())
    if sentences:
        s = sentences[0]
        if len(s) > 150:
            s = s[:147] + "..."
        return s
    return notes[:150]


# ─── Featured set ─────────────────────────────────────────────────────────────
FEATURED_IDS = {
    "seger_hermann", "stull_ray", "hansen_tony",
    "leach_bernard", "robineau_adelaide", "orton_edward_jr",
    "hamer_frank", "rhodes_daniel", "currie_ian",
}


# ─── Main migration ───────────────────────────────────────────────────────────
def migrate_person(person: dict, name_to_slug: dict) -> dict:
    v1_id   = person["id"]
    slug    = to_slug(v1_id)
    name    = person.get("name", "")
    notes   = person.get("notes", "")
    primary = infer_primary_contribution(person)

    tech_tags, ctx_tags = split_tags(person.get("tags", []))

    # Nationality: v1 is a string (sometimes comma-separated)
    nat_raw = person.get("nationality", "")
    nationality = [n.strip() for n in nat_raw.split(",") if n.strip()] if nat_raw else ["Unknown"]

    # Institution → affiliations
    inst = person.get("institution", "").strip()
    affiliations = [institution_to_affiliation(inst)] if inst else []

    # Roles: already a list in v1
    roles = person.get("role", [])
    if isinstance(roles, str):
        roles = [roles]

    return {
        "schema_version": "2.0.0",
        "id": slug,
        "name": name,
        "display_name": name,
        "sort_name": make_sort_name(name),
        "is_living": infer_is_living(person),
        "birth_year": None,
        "death_year": None,
        "nationality": nationality,
        "roles": roles,
        "periods": era_to_periods(person.get("era", "Unknown")),
        "affiliations": affiliations,
        "primary_contribution_type": primary,
        "secondary_contribution_types": infer_secondary(person, primary),
        "summary_short": make_summary_short(notes),
        "summary_long": notes,
        "known_for": person.get("known_for", []),
        "technical_tags": tech_tags,
        "context_tags": ctx_tags,
        "related_people": collaborators_to_related(person, name_to_slug),
        "domains": infer_domains(person),
        "sources": [],
        "confidence": "medium",
        "editorial_status": "draft",
        "completeness": "medium",
        "featured": v1_id in FEATURED_IDS,
    }


def main():
    src = Path("data/glaze_references.json")
    dst = Path("data/people_v2.json")

    data    = json.loads(src.read_text(encoding="utf-8"))
    people  = data["glaze_chemistry_references"]["people"]

    name_to_slug = build_name_to_slug(people)

    migrated = [migrate_person(p, name_to_slug) for p in people]

    collection = {
        "schema_version": "2.0.0",
        "generated_at": str(date.today()),
        "people": migrated,
    }

    dst.write_text(json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written {len(migrated)} people to {dst}")

    # Quick validation report
    print("\n--- Validation spot-check ---")
    for p in migrated:
        assert p["primary_contribution_type"] in VALID_CONTRIBUTION_TYPES, \
            f"{p['id']}: bad primary_contribution_type {p['primary_contribution_type']!r}"
        for rel in p["related_people"]:
            assert rel["relation"] in VALID_RELATIONS, \
                f"{p['id']}: bad relation {rel['relation']!r}"
        for aff in p["affiliations"]:
            assert aff["type"] in VALID_AFFILIATION_TYPES, \
                f"{p['id']}: bad affiliation type {aff['type']!r}"
    print("All entries pass enum validation.")

    # Summary stats
    living = sum(1 for p in migrated if p["is_living"])
    featured = sum(1 for p in migrated if p["featured"])
    with_affiliations = sum(1 for p in migrated if p["affiliations"])
    with_related = sum(1 for p in migrated if p["related_people"])
    print(f"\nStats:")
    print(f"  Total:           {len(migrated)}")
    print(f"  is_living=True:  {living}")
    print(f"  featured:        {featured}")
    print(f"  with affiliations: {with_affiliations}")
    print(f"  with related_people: {with_related}")
    ctypes = {}
    for p in migrated:
        pt = p["primary_contribution_type"]
        ctypes[pt] = ctypes.get(pt, 0) + 1
    print(f"\n  primary_contribution_type distribution:")
    for k, v in sorted(ctypes.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v}")


if __name__ == "__main__":
    main()

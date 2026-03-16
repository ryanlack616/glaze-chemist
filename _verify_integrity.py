"""Verify cross-reference integrity of glaze_references.json"""
import json

with open("data/glaze_references.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ref = data["glaze_chemistry_references"]
people = ref["people"]
books = ref["books"]
concepts = ref["concepts"]

people_ids = {p["id"] for p in people}
book_ids = {b["id"] for b in books}
concept_ids = {c["id"] for c in concepts}

errors = []

# Check for duplicate IDs
for label, items in [("people", people), ("books", books), ("concepts", concepts)]:
    seen = {}
    for item in items:
        iid = item["id"]
        if iid in seen:
            errors.append(f"DUPLICATE {label} ID: {iid}")
        seen[iid] = True

# Check people cross-refs
for p in people:
    for collab in p.get("collaborators", []):
        if collab not in people_ids:
            errors.append(f"Person '{p['id']}' has unknown collaborator: {collab}")

# Check books cross-refs
for b in books:
    for aid in b.get("author_ids", []):
        if aid not in people_ids:
            errors.append(f"Book '{b['id']}' has unknown author_id: {aid}")

# Check concepts cross-refs
for c in concepts:
    for pid in c.get("developed_by", []):
        if pid not in people_ids:
            errors.append(f"Concept '{c['id']}' has unknown developed_by: {pid}")
    for pid in c.get("related_people", []):
        if pid not in people_ids:
            errors.append(f"Concept '{c['id']}' has unknown related_people: {pid}")

# Check collaborator reciprocity
for p in people:
    for collab in p.get("collaborators", []):
        if collab in people_ids:
            other = next(x for x in people if x["id"] == collab)
            if p["id"] not in other.get("collaborators", []):
                errors.append(f"One-way collaborator: {p['id']} -> {collab} (not reciprocated)")

# Check for people with no tags
for p in people:
    if not p.get("tags"):
        errors.append(f"Person '{p['id']}' has no tags")
    if not p.get("known_for"):
        errors.append(f"Person '{p['id']}' has empty known_for")
    if not p.get("role"):
        errors.append(f"Person '{p['id']}' has empty role")

# Summary
print(f"=== Glaze References Integrity Check ===")
print(f"People:   {len(people)} ({len(people_ids)} unique IDs)")
print(f"Books:    {len(books)} ({len(book_ids)} unique IDs)")
print(f"Concepts: {len(concepts)} ({len(concept_ids)} unique IDs)")
print()

if errors:
    print(f"Found {len(errors)} issues:")
    for e in sorted(errors):
        print(f"  - {e}")
else:
    print("All cross-references valid. No issues found.")

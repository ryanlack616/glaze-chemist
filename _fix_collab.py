import json

with open("data/glaze_references.json", "r", encoding="utf-8") as f:
    d = json.load(f)

people = d["glaze_chemistry_references"]["people"]
for p in people:
    collabs = p.get("collaborators", [])
    if "Derek Au" in collabs:
        idx = collabs.index("Derek Au")
        collabs[idx] = "Derek Au (Philipau)"
        print(f"Fixed {p['id']}: Derek Au -> Derek Au (Philipau)")

with open("data/glaze_references.json", "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("Saved.")

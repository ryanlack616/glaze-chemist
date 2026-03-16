import json

with open('data/glaze_references.json', encoding='utf-8') as f:
    data = json.load(f)

people = data['glaze_chemistry_references']['people']
people.sort(key=lambda p: len(p.get('notes', '')), reverse=True)

for p in people[:15]:
    name = p['name']
    notes = p.get('notes', '')
    print(f"=== {name} ({len(notes)} chars) ===")
    print(notes[:600])
    print()

"""Review all people in glaze_references.json — completeness audit"""
import json

with open(r'C:\Users\PC\Desktop\glaze-chemist\data\glaze_references.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

people = d['glaze_chemistry_references']['people']
books = d['glaze_chemistry_references']['books']
concepts = d['glaze_chemistry_references']['concepts']

# Build book authorship map
books_by_author = {}
for b in books:
    for aid in b.get('author_ids', []):
        books_by_author.setdefault(aid, []).append(b['title'])

# Build concept developer map
concepts_by_dev = {}
for c in concepts:
    for did in c.get('developed_by', []):
        concepts_by_dev.setdefault(did, []).append(c['name'])

# Build collaborator graph
collab_count = {}
mentioned_as_collab = set()
for p in people:
    for c in p.get('collaborators', []):
        mentioned_as_collab.add(c.lower())
    collab_count[p['id']] = len(p.get('collaborators', []))

print(f"{'='*80}")
print(f"GLAZE CHEMIST — PEOPLE AUDIT ({len(people)} entries)")
print(f"{'='*80}\n")

# Categorize
no_institution = []
no_nationality = []
no_known_for = []
no_notes = []
no_collabs = []
no_books = []
has_books = []
island_nodes = []  # no collabs AND no books AND not a concept developer

for p in people:
    pid = p['id']
    name = p['name']
    if not p.get('institution'): no_institution.append(name)
    if not p.get('nationality'): no_nationality.append(name)
    if not p.get('known_for'): no_known_for.append(name)
    if not p.get('notes'): no_notes.append(name)
    if not p.get('collaborators'): no_collabs.append(name)
    
    authored = books_by_author.get(pid, [])
    developed = concepts_by_dev.get(pid, [])
    
    if not authored:
        no_books.append(name)
    else:
        has_books.append((name, authored))
    
    if not p.get('collaborators') and not authored and not developed:
        island_nodes.append(name)

print("── COMPLETENESS ──")
print(f"  Missing institution:  {len(no_institution)}/{len(people)}")
print(f"  Missing nationality:  {len(no_nationality)}/{len(people)}")
print(f"  Missing known_for:    {len(no_known_for)}/{len(people)}")
print(f"  Missing notes:        {len(no_notes)}/{len(people)}")
print(f"  No collaborators:     {len(no_collabs)}/{len(people)}")
print(f"  No books authored:    {len(no_books)}/{len(people)}")
print()

print("── ISLAND NODES (no collabs, no books, no concepts) ──")
for name in island_nodes:
    print(f"  ⚠ {name}")
print()

print("── MISSING INSTITUTION ──")
for name in no_institution:
    print(f"  · {name}")
print()

print("── MISSING NATIONALITY ──")
for name in no_nationality:
    print(f"  · {name}")
print()

print("── MISSING NOTES ──")
for name in no_notes:
    print(f"  · {name}")
print()

print("── PEOPLE WITH BOOKS ──")
for name, titles in has_books:
    print(f"  ✓ {name}: {', '.join(titles)}")
print()

print("── PEOPLE WITHOUT BOOKS ──")
for name in no_books:
    print(f"  · {name}")
print()

# Era distribution
eras = {}
for p in people:
    era = p.get('era', 'Unknown')
    eras.setdefault(era, []).append(p['name'])
print("── ERA DISTRIBUTION ──")
for era, names in sorted(eras.items()):
    print(f"  {era} ({len(names)}): {', '.join(names)}")
print()

# Role distribution
roles = {}
for p in people:
    for r in p.get('role', []):
        roles.setdefault(r, []).append(p['name'])
print("── ROLE DISTRIBUTION ──")
for role, names in sorted(roles.items(), key=lambda x: -len(x[1])):
    print(f"  {role} ({len(names)}): {', '.join(names)}")
print()

# Tag distribution
tags = {}
for p in people:
    for t in p.get('tags', []):
        tags.setdefault(t, []).append(p['name'])
print("── TAG DISTRIBUTION ──")
for tag, names in sorted(tags.items(), key=lambda x: -len(x[1])):
    print(f"  {tag} ({len(names)}): {', '.join(names)}")
print()

# Collaborator mentions that aren't in the people list
people_names_lower = {p['name'].lower() for p in people}
all_collabs = set()
for p in people:
    for c in p.get('collaborators', []):
        all_collabs.add(c)

missing_collabs = [c for c in sorted(all_collabs) if c.lower() not in people_names_lower]
print("── COLLABORATORS MENTIONED BUT NOT IN PEOPLE LIST ──")
for c in missing_collabs:
    print(f"  → {c}")
print()

# Summary
print(f"{'='*80}")
print("SUMMARY OF GAPS:")
print(f"  {len(island_nodes)} island nodes (disconnected)")
print(f"  {len(no_institution)} missing institution")
print(f"  {len(no_nationality)} missing nationality")
print(f"  {len(no_notes)} missing notes")
print(f"  {len(missing_collabs)} collaborators mentioned but not in dataset")
print(f"{'='*80}")

"""Fix Orton Jr. island node — connect to Seger (cones extend Seger's measurement work)
and Parmelee (both at University of Illinois ceramics orbit)"""
import json

SRC = r'C:\Users\PC\Desktop\glaze-chemist\data\glaze_references.json'

with open(SRC, 'r', encoding='utf-8') as f:
    data = json.load(f)

people = data['glaze_chemistry_references']['people']
by_id = {p['id']: p for p in people}

orton = by_id['orton_edward_jr']
collabs = orton.get('collaborators', [])
if 'Hermann August Seger' not in collabs:
    collabs.append('Hermann August Seger')
if 'C.W. Parmelee' not in collabs:
    collabs.append('C.W. Parmelee')
orton['collaborators'] = collabs
print(f"Orton Jr. collaborators: {collabs}")

# Also add Orton back on Seger and Parmelee
seger = by_id['seger_hermann']
s_collabs = seger.get('collaborators', [])
if 'Edward Orton Jr.' not in s_collabs:
    s_collabs.append('Edward Orton Jr.')
    seger['collaborators'] = s_collabs
    print(f"Seger collaborators: {s_collabs}")

parmelee = by_id['parmelee_cw']
p_collabs = parmelee.get('collaborators', [])
if 'Edward Orton Jr.' not in p_collabs:
    p_collabs.append('Edward Orton Jr.')
    parmelee['collaborators'] = p_collabs
    print(f"Parmelee collaborators: {p_collabs}")

with open(SRC, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✓ Saved")

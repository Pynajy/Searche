import json
with open('results.json', 'r', encoding='utf-8') as f:
    file = json.load(f)
nise = file['geoecoproduct_1']['good']
bad = file['geoecoproduct_1']['bad']
print(f'Положительных: {len(nise)}')
print(f'Отрицательных: {len(bad)}')

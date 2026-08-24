#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

PATH = Path('assets/locales/wumpus-world-r4.js')
text = PATH.read_text(encoding='utf-8')

OLD_VI = '''    "patterns": [
      {
        "source": "^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, -no stench$",
        "target": "($1,$2): không có gió, không có mùi hôi",
        "flags": "g"
      }
    ]'''
NEW_VI = '''    "patterns": [
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, -no stench$","target":"($1,$2): không có gió, không có mùi hôi","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): breeze, -no stench$","target":"($1,$2): gió, không có mùi hôi","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, stench$","target":"($1,$2): không có gió, mùi hôi","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): breeze, stench$","target":"($1,$2): gió, mùi hôi","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, -no stench, GLITTER!$","target":"($1,$2): không có gió, không có mùi hôi, lấp lánh!","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): breeze, -no stench, GLITTER!$","target":"($1,$2): gió, không có mùi hôi, lấp lánh!","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, stench, GLITTER!$","target":"($1,$2): không có gió, mùi hôi, lấp lánh!","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): breeze, stench, GLITTER!$","target":"($1,$2): gió, mùi hôi, lấp lánh!","flags":"g"}
    ]'''

OLD_ES = '''    "patterns": [
      {
        "source": "^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, -no stench$",
        "target": "($1,$2): sin brisa, sin hedor",
        "flags": "g"
      }
    ]'''
NEW_ES = '''    "patterns": [
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, -no stench$","target":"($1,$2): sin brisa, sin hedor","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): breeze, -no stench$","target":"($1,$2): brisa, sin hedor","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, stench$","target":"($1,$2): sin brisa, hedor","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): breeze, stench$","target":"($1,$2): brisa, hedor","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, -no stench, GLITTER!$","target":"($1,$2): sin brisa, sin hedor, ¡brillo!","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): breeze, -no stench, GLITTER!$","target":"($1,$2): brisa, sin hedor, ¡brillo!","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): -no breeze, stench, GLITTER!$","target":"($1,$2): sin brisa, hedor, ¡brillo!","flags":"g"},
      {"source":"^\\\\(([0-9]+),([0-9]+)\\\\): breeze, stench, GLITTER!$","target":"($1,$2): brisa, hedor, ¡brillo!","flags":"g"}
    ]'''

for old, new, label in ((OLD_VI, NEW_VI, 'vi'), (OLD_ES, NEW_ES, 'es')):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one old pattern block, found {count}')
    text = text.replace(old, new, 1)

for source in (
    'breeze, -no stench', '-no breeze, stench', 'breeze, stench',
    '-no breeze, -no stench, GLITTER!', 'breeze, -no stench, GLITTER!',
    '-no breeze, stench, GLITTER!', 'breeze, stench, GLITTER!',
):
    if source not in text:
        raise SystemExit(f'patched pattern family missing: {source}')

PATH.write_text(text, encoding='utf-8', newline='\n')
print('WUMPUS_PERCEPT_PATTERN_FAMILY=PASS vi=8 es=8')

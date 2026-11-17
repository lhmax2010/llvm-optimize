# Failed delivery preparation check, preserved; not rerun.
for f in json.loads((E/'test-copy.json').read_text())['files']:
    old=B/f
    new=E/old.relative_to(O)
    assert old.read_bytes()==new.read_bytes(),str(new)
# Defect: manifest includes generated observation JSON, not only immutable tests.

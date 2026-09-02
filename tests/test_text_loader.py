from src.documind.loaders.text import load_textual

def test_load_plain_text(tmp_path):
    p = tmp_path / "notes.txt"
    p.write_text("alpha beta gamma")
    units = load_textual(p, "abc")
    assert len(units) == 1
    assert units[0].text == "alpha beta gamma"
    assert units[0].source_id == "abc"

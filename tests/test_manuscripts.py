import json
import tempfile
from manuscripts import ManuscriptDB, generate_prompt


def test_add_edit_delete():
    with tempfile.NamedTemporaryFile() as tmp:
        db = ManuscriptDB(tmp.name)
        db.add({
            "title": "Paper",
            "authors": ["A"],
            "affiliations": ["Org"],
            "abstract": "",
            "methods": [],
            "datasets": [],
            "metrics": [],
        })
        assert len(db.list()) == 1
        db.edit(0, {"title": "New"})
        assert db.list()[0]["title"] == "New"
        db.delete(0)
        assert db.list() == []


def test_filter_and_fields():
    with tempfile.NamedTemporaryFile() as tmp:
        db = ManuscriptDB(tmp.name)
        db.add({
            "title": "P1",
            "authors": [],
            "affiliations": [],
            "abstract": "",
            "methods": [{"model_name": "M1"}],
            "datasets": [{"name": "D1"}],
            "metrics": [{"name": "Acc"}],
        })
        db.add({
            "title": "P2",
            "authors": [],
            "affiliations": [],
            "abstract": "",
            "methods": [{"model_name": "M2"}],
            "datasets": [{"name": "D2"}],
            "metrics": [{"name": "F1"}],
        })
        assert db.filter(model="M1")[0]["title"] == "P1"
        fields = db.list_fields()
        assert "M2" in fields["models"]
        assert "D2" in fields["datasets"]
        assert "F1" in fields["metrics"]


def test_generate_prompt_json():
    data = json.loads(generate_prompt())
    assert "methods" in data["fields"]
    assert "datasets" in data["fields"]
    assert "metrics" in data["fields"]

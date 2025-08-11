import json
import os
from typing import List, Dict, Any, Optional

DB_PATH = "manuscripts.json"

class ManuscriptDB:
    """Simple JSON file based database for manuscripts."""

    def __init__(self, path: str = DB_PATH) -> None:
        self.path = path
        self.data: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return []

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # CRUD operations
    def add(self, entry: Dict[str, Any]) -> None:
        self.data.append(entry)
        self._save()

    def edit(self, index: int, updates: Dict[str, Any]) -> None:
        if index < 0 or index >= len(self.data):
            raise IndexError("Entry index out of range")
        self.data[index].update(updates)
        self._save()

    def delete(self, index: int) -> None:
        if index < 0 or index >= len(self.data):
            raise IndexError("Entry index out of range")
        self.data.pop(index)
        self._save()

    def list(self) -> List[Dict[str, Any]]:
        return self.data

    def list_fields(self) -> Dict[str, List[str]]:
        models, datasets, metrics = set(), set(), set()
        for entry in self.data:
            for m in entry.get("methods", []):
                name = m.get("model_name")
                if name:
                    models.add(name)
            for d in entry.get("datasets", []):
                name = d.get("name")
                if name:
                    datasets.add(name)
            for mt in entry.get("metrics", []):
                name = mt.get("name")
                if name:
                    metrics.add(name)
        return {
            "models": sorted(models),
            "datasets": sorted(datasets),
            "metrics": sorted(metrics),
        }

    def filter(self,
               model: Optional[str] = None,
               dataset: Optional[str] = None,
               metric: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for entry in self.data:
            match = True
            if model and not any(m.get("model_name") == model for m in entry.get("methods", [])):
                match = False
            if dataset and not any(d.get("name") == dataset for d in entry.get("datasets", [])):
                match = False
            if metric and not any(mt.get("name") == metric for mt in entry.get("metrics", [])):
                match = False
            if match:
                results.append(entry)
        return results

def generate_prompt() -> str:
    """Return JSON string prompt for extracting manuscript details via ChatGPT."""
    prompt = {
        "instruction": "Given the text of an academic manuscript, extract structured information.",
        "fields": {
            "methods": [{
                "model_name": "",
                "type": "LLM | VLM | Image",
                "embedding_size": "integer",
                "backbone": "",
                "parameters": "integer"
            }],
            "datasets": [{
                "name": "",
                "usage": "training | finetuning | evaluation",
                "focus": "main purpose or domain",
                "sample_type": "QA pair | long text | medical EHR | report | other",
                "is_public": "true | false",
                "num_samples": "integer"
            }],
            "metrics": [{
                "name": "",
                "evaluation_type": "multiple choice | QA | other",
                "value": "number",
                "description": "how the metric is calculated",
                "model_name": "associated model"
            }]
        }
    }
    return json.dumps(prompt, indent=2)

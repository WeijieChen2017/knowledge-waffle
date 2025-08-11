# knowledge-waffle

Simple local manager for academic manuscripts. Entries are stored in a JSON file
and can be added, edited, deleted and filtered via a graphical interface.


## Installation

The app uses the Python standard library. To run the tests you will need
`pytest`:

```bash
pip install pytest
```

## Usage

Run the GUI:

```bash
python app.py
```

The interface shows all stored manuscripts and buttons to **Add**, **Edit** or
**Delete** entries. "Fields" displays all unique models, datasets and metrics
across the database. "Filter" allows filtering entries by model, dataset or
metric and shows the resulting list. "Prompt" opens a window containing the JSON
prompt to collect `methods`, `datasets` and `metrics` information from ChatGPT.

The prompt asks ChatGPT to return JSON with the following structure, which can
be pasted directly into the corresponding fields when adding or editing an
entry:

```json
{
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
```
The JSON returned by ChatGPT can be pasted into the corresponding text boxes in
the GUI when adding or editing an entry.

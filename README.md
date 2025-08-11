# knowledge-waffle

Simple local manager for academic manuscripts. Entries are stored in a JSON file
and can be added, edited, deleted and filtered.

## Installation

The app uses the Python standard library. To run the tests you will need
`pytest`:

```bash
pip install pytest
```

## Usage

Generate the JSON prompt for obtaining `methods`, `datasets` and `metrics`
information from ChatGPT:

```bash
python app.py prompt
```

Add a manuscript (details are optional JSON from the prompt output):

```bash
python app.py add --title "My Paper" --authors "Alice,Bob" \
  --affiliations "Uni A,Uni B" --abstract "Short" --details details.json
```

Edit or delete entries by index:

```bash
python app.py edit 0 --title "Updated Title"
python app.py delete 0
```

List entries or available models/datasets/metrics:

```bash
python app.py list
python app.py fields
```

Filter entries:

```bash
python app.py filter --model MODEL_NAME
python app.py filter --dataset DATASET_NAME
python app.py filter --metric METRIC_NAME
```

The generated prompt asks ChatGPT to return JSON with the following structure:

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

The JSON returned by ChatGPT can be saved to a file and supplied to `--details`
when adding or editing an entry.

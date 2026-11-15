# Quiz Insight

**From answer sheets to teaching insight.**

Mark A–D quizzes, build a submission register and spot questions that deserve a second look. Analyse CSV responses locally, with exportable results.

Built by [Joseph Tetteh (TJay)](https://github.com/Parajose) · Python + vanilla HTML/CSS/JavaScript · MIT license

## Run in under a minute

Requires **Python 3.10+**. There are **no third-party dependencies**.

```bash
git clone https://github.com/Parajose/quiz-insight.git
cd quiz-insight
python app.py
```

On Windows, use `py app.py` if `python` is unavailable. Open **http://127.0.0.1:8000**. Run one project at a time because all use port 8000. Stop with Ctrl+C. Open through the server, not by double-clicking `index.html`.

The sample runs automatically. Edit the JSON and click **Analyse scenario**, or use **Reset sample**. Each result table has a CSV export. Invalid input clears old results and explains the error.

## Features

- Responsive dashboard with sample data and interactive scenario inputs
- Transparent calculations in a separate, testable Python module
- CSV exports and readable input validation
- Local HTTP API with no required account or external service
- Automated numerical and edge-case checks using standard-library unittest

## CSV format

```csv
student_id,name,Q1,Q2,Q3
DEMO001,Demo Student 1,B,A,D
DEMO002,Demo Student 2,A,A,
```

Provide a matching key such as `{"Q1":"B","Q2":"A","Q3":"D"}`. Headers are case-sensitive; answers are trimmed and converted to uppercase. Use A–D or blank. Student IDs must be unique (case-insensitive); duplicates stop marking rather than silently choosing a submission. This initial format is a simple response table, not a promise of direct compatibility with every Microsoft Forms export.

## Marking and interpretation

Every correct answer earns one mark. Blank answers score zero. Pass classification uses the unrounded percentage; displayed percentages have two decimals. Exports contain a submission register and marks, plus per-question answer counts and percentage correct. Threshold flags below 40% and above 90% are prompts for review, not proof that an item is good or bad. No discrimination index, reliability statistic or AI judgment is claimed.

A submission is **not verified classroom attendance**. Absentees require a full roster and an explicit attendance policy. The demo students are fictitious.

## Data handling

The server binds to 127.0.0.1, sends no responses to a cloud API and does not write imported student data to disk. CSV exports are explicit downloads; keep those files private. Do not commit real student records. Leading spreadsheet formula characters are prefixed during CSV export to reduce formula injection risks. The local server has no multi-user authentication and must not be deployed publicly as-is.

## Roadmap

Add roster reconciliation, configurable marks per question and documented Microsoft Forms import mappings. Any institutional deployment needs access control and a retention policy.

## Project layout

| File | Purpose |
| --- | --- |
| `app.py` | Local HTTP server and JSON API |
| `core.py` | Validation and domain calculations |
| `index.html` | Responsive interface and safe DOM rendering |
| `sample.json` | Reproducible fictional sample |
| `test_core.py` | Calculation and validation tests |
| `LICENSE` | MIT license |

## Test

```bash
python -m unittest -v
```

## API

`GET /api/demo` returns sample inputs. `POST /api/analyse` accepts the same JSON shape and returns `summary`, `rows`, `chart`, `notes` and project-specific details. Invalid input returns HTTP 400 with an `error` message. Requests are limited to 1 MB. The server is intentionally local-only.

```bash
curl -H "Content-Type: application/json" --data-binary @sample.json http://127.0.0.1:8000/api/analyse
```

## Development status

Working initial portfolio release. Tests cover the core calculations and selected failure cases; this is not an independently certified engineering or institutional system. Contributions that add benchmark validation, accessibility improvements and documented use cases are welcome.

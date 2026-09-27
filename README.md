# modhub_sample_repo_python

A small project deliberately written against **Pydantic v1**, used to
exercise the Engineering Modernization Hub end to end.

## What is here

`src/models.py` uses the v1 API surface that v2 breaks:

| v1 (here) | v2 |
|---|---|
| `@validator` | `@field_validator` + `@classmethod` |
| `class Config:` / `anystr_strip_whitespace` | `model_config = ConfigDict(str_strip_whitespace=True)` |
| `Model.parse_obj()` | `Model.model_validate()` |
| `.dict()` / `.json()` | `.model_dump()` / `.model_dump_json()` |
| `Model.__fields__` | `Model.model_fields` |

`tests/test_models.py` has 12 tests written against the helper functions in
`src/models.py`, never against Pydantic's own API, and never asserting on
validation *messages* (their wording is version-specific). That is what lets
the same suite prove the project still behaves identically after the upgrade
— the property the platform's suite-integrity check relies on.

Both the v1 and the migrated v2 version pass the same 12 tests, so executed
and passed counts hold steady across the migration.

## Running it

```
pip install -r requirements.txt
pytest
ruff check .
```

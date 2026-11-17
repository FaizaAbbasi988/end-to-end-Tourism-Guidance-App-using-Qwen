# AI Service — Incremental Refactoring Notes

This branch refactors **the AI microservice**. The separate backend/frontend
engineers' projects are not changed. Preserve the existing
`/algorithm/api/...` URLs and JSON contracts when continuing the cleanup.

## Phase 1 — Completed (requires local verification)

- Centralized FunASR inference in `Service/model/speech_model.py`. Audio
  routes use the cached `get_speech_recognition_model()` factory so that
  several routers no longer load separate FunASR copies at module import.
- Centralized mono/16-kHz audio conversion in `Service/model/audio_utils.py`.
  `dates.py` and `audio_parse.py` still re-export the previous names for
  compatibility; their own duplicate implementations have been removed.
- Changed `Service/app/dates_app.py`, `Service/app/parse_app.py` and
  `Service/model_service/non_login_chatbot.py` to lazy initialization.
- Removed redundant model instances and unused imports from
  `Service/app/app.py`.
- Standardized the `Service.config` import in `Service/app/__init__.py`.
- Simplified duplicate path manipulation in `Service/main.py`, retaining
  both script and module execution.
- Corrected the schema for `/dates/extract_dates` to match its existing
  Chinese-key dictionary payload (`到达时间`, `离开时间`).
- Added `tests/test_speech_refactor.py`; no live FunASR inference occurs in
  these tests.
- Replaced the previous Postman collection with **`API_TEST_EXAMPLES.md`**:
  15 endpoints, URLs, ready-to-copy JSON payloads and upload instructions.

## Verification from the repo root

```powershell
git switch changes
git pull origin changes
python -m unittest discover -s tests -p "test_structured_output.py" -v
python -m unittest discover -s tests -p "test_login_http_contract.py" -v
python -m unittest discover -s tests -p "test_speech_refactor.py" -v
python test_login_apis.py --category all
python Service/main.py
```

Then manually test the login APIs and at least one audio endpoint in Postman
using `API_TEST_EXAMPLES.md`. Speech endpoints need local installed model
weights. **Changes have not been runtime-tested in the author's environment.**

## Phase 2 — Small, student-friendly cleanup (local testing needed)

- `setup.py` now installs the `Service` namespace correctly (including
  `config.json`) and declares the main libraries used by the project.
  Install with `python -m pip install -e .`; no extra packaging framework
  was introduced. Existing environments may have extra optional dependencies.
- `README.md` now explains the purpose of the AI microservice, setup,
  endpoint testing, and the existing folder layout.
- `Service/app/parse_app.py` now has one small JSON parsing function.
  Invalid model text and explicit model errors return `success: false`
  instead of being confused with successful parsing. **This is a behavior
  change for invalid or plain-text Qwen output.**
- TTS no longer depends on `D:\\travel_project\\downloaded_models`:
  it writes to `generated_audio/` in the repository by default. The
  optional `TOURISM_AUDIO_DIR` environment variable selects a different
  output directory. The audio-format handling has not been changed.
- `.gitignore` excludes generated audio and Python packaging artifacts.
- `tests/test_audio_parser.py` checks parsing, errors, and basic response
  structures without calling the models.

**What stays unchanged:** all API URLs, successful travel/food list responses,
accommodation and summary responses, speech recognition logic, and the
existing folder names. No experimental files were deleted.

### Verify the Phase 2 changes

```powershell
git pull origin changes
python -m unittest discover -s tests -p "test_*.py" -v
python Service/main.py
```

Test `/audiologin/travel` with an audio recording and confirm whether Qwen
returns a JSON object as expected. Test TTS once if your project uses the
non-login cultural/food audio responses. Neither was executed remotely.

### Possible Phase 3 (only after local tests)

1. Simplify `Service/model/audio_parse.py` and `Service/model/dates.py`
   further while retaining their public interfaces.
2. Review other Pydantic request/response models and document errors.
3. Move unused experiments to a clearly labeled `experiments/` folder,
   but only after confirming they are not needed by students.
4. Consider an `api/`, `schemas/`, `services/` reorganization only when
   sufficient tests exist; unnecessary folder moves don't improve teaching.

## Phase 3 — Simpler code and existing schemas (local testing needed)

- `Service/model/audio_parse.py`: replaced four repeated prompt/chain attributes
  with a small dictionary. Each category still uses its original prompt and
  the same Ollama model. The existing `invoke(category, data)` method and
  error dictionary remain.
- `Service/app/description_app.py`: removed unused imports and now creates
  the description model on first request.
- `Service/app/dates_app.py`: cleaned imports and logging; its URL and
  Chinese response keys remain unchanged.
- Removed unused `Dict` / `Any` imports from several request models.
  **No required request fields or response types were changed.**
- `Service/app/login_app.py`: replaced deprecated `.dict()` calls with
  Pydantic 2's `.model_dump()`.
- `tests/test_student_cleanup.py`: beginner-friendly regression tests for
  existing request/response shapes, correct audio prompt selection, and model
  error handling. These tests do not start Ollama.

### Verify Phase 3

```powershell
git pull origin changes
python -m unittest discover -s tests -p "test_*.py" -v
python test_login_apis.py --category all
python Service/main.py
```

After startup, check description, dates, and audio login in Postman using
`API_TEST_EXAMPLES.md`. The new changes are committed but have not yet been
executed in your local Windows environment.

**Intentionally postponed:** moving files/folders, deleting experiments,
rewriting all API response contracts, or adding complex abstractions. The
student-friendly goal is easier code without changing the AI service contract.

## Design trade-offs

- The shared speech model is cached once **per Python process**. If you launch
  multiple workers, each will have its own instance. The ASR library's
  concurrent-request safety has not been established; avoid claiming that
  one cached instance automatically makes parallel inference safe.
- The HTTP API remains synchronous for compute-heavy operations inside some
  async endpoints. Concurrency/performance optimization is a later phase.
- The travel and food response list contract is unchanged by this refactor.

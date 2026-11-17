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

## Proposed Phase 2 — Not applied

1. **Standardized packaging and dependencies:** `setup.py` has outdated
   version pins and does not list every library imported by runtime code.
   Introduce `pyproject.toml` and an explicit development setup after
   reconciling installed versions.
2. **Clear folder responsibilities:** separate `api/`, `schemas/`,
   `services/`, `core/`, and `utils/`. Move modules incrementally only
   after confirming the API suite passes.
3. **Audio-parser error handling:** `Service/app/parse_app.py` currently uses
   `json.loads()` on model text, which may fail on invalid JSON. Add schema
   validation while preserving the API's consumer contract.
4. **TTS portability:** `Service/model/text_to_speech.py` includes a
   machine-specific output directory, and speech/audio format support needs
   explicit documentation.
5. **Experimental code:** inspect unused notebooks and the disabled video
   router before archiving them; don't delete without verifying that students
   don't use them.
6. **API consistency:** audit all endpoint responses, error handling and tests
   before introducing a common error envelope.

## Design trade-offs

- The shared speech model is cached once **per Python process**. If you launch
  multiple workers, each will have its own instance. The ASR library's
  concurrent-request safety has not been established; avoid claiming that
  one cached instance automatically makes parallel inference safe.
- The HTTP API remains synchronous for compute-heavy operations inside some
  async endpoints. Concurrency/performance optimization is a later phase.
- The travel and food response list contract is unchanged by this refactor.

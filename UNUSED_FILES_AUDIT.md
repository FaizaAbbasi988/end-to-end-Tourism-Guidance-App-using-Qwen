# Unused Files and Folders Audit

**Branch reviewed:** `changes` at commit `aaa01cfd32ffc1d91d852feda86f9517d04d1212`

This audit is for the **AI microservice repository**, not the separate backend
engineer's or frontend engineer's projects.

I inspected the complete Git tree (70 tracked blobs/files, 9 tracked
directories and 1 Git submodule entry), examined candidate file contents,
reviewed router registration, and checked code references. **No files were
deleted during this audit.**

> Important: "not used by the running API" is different from "not valuable."
> Students may still use experimental notebooks. Static code searches may miss
> dynamic imports, external scripts, or references from a teammate.

## 1. Strong candidates for removal from active service code

| Path | Evidence | Recommendation |
| --- | --- | --- |
| `Service/app/video_app.py` | File consists entirely of commented-out endpoint code, and its router is commented out in `Service/app/__init__.py`. No active video endpoint is registered. | Archive as a future-feature example or remove after confirmation |
| `Service/model_service/base_tts.py` | Contains only an abstract `BaseTTS` class. The actual `TTS` implementation does not inherit it; no imports found in the checked code. | Candidate for deletion; keeping an unused abstract class can confuse students |
| `Service/common/http/beauty_request.py` | Defines `ImageBeautificationRequest`, but `/image/beautify` accepts multipart `UploadFile` parameters rather than this Pydantic body. No active references found. | Candidate for deletion |
| `Service/common/http/beauty_response.py` | Defines three image response models, but the active image endpoint returns `JSONResponse` or binary `Response` directly. No active references found. | Candidate for deletion |
| `Service/common/http/transcription_request.py` | Contains only `TranscriptionRequest(audio_data: bytes)`. `/non-login/audio_chatbot` accepts `UploadFile`, not this model. No active references found. | Candidate for deletion |
| `Service/common/http/dates_request.py` | Contains old `NonLoginAudioChatbotRequest` and `NonLoginAudioChatbotResponse` models. Also imports `TimeExtractionResponse`, which is **not defined** in the current `dates_response.py`. The active date endpoint uses an uploaded file directly. | Strong candidate for removal; its outdated import is broken if the module is imported |
| `test_results.json` | A saved transcription/analysis of a general deep-learning lecture; unrelated to the current tourism API and not referenced by the checked code. | Move to examples/archive or delete if not needed for lessons |

These are recommendations, **not proof of universal non-use**. Confirm no
students or external scripts import these modules before deleting them.

## 2. Experimental material — preserve separately if students use it

The entire `Algorithm/` directory appears **outside the active FastAPI
import/registration path**. Its contents are development experiments, not
registered API handlers:

| Path | Observed content | Suggested action |
| --- | --- | --- |
| `Algorithm/image_enhancement.py` | Standalone Stable Video Diffusion demo, runs model loading at module top level, assumes CUDA, and uses an old absolute Windows image path. It is **not** the active image beautification implementation (`Service/model/beautification.py` is). | Archive under `experiments/video/` |
| `Algorithm/image_enhancement.ipynb` | Notebook version of the same video-generation experiment. | Keep at most one teaching example, or archive both |
| `Algorithm/tt.ipynb` | Early TTS experiments, with code now represented by `Service/model/text_to_speech.py`. | Archive under `experiments/audio/` |
| `Algorithm/text_correction.ipynb` | Manual examples of splitting/editing food descriptions. | Archive as a text-processing teaching exercise |
| `Algorithm/non_login/test2.ipynb` | Four-cell example checking strings such as `文化介绍` and `最佳路线`. | Low-priority archival candidate |
| `Algorithm/non_login/test_1.ipynb` | Large notebook (~983 KB tracked); not needed to register the running service. Its full notebook content was **not** audited in this pass. | Review its contents and teaching value before moving/deleting |

**Folder-level recommendation:** Keep the code separate from the live service,
but rename/archive `Algorithm/` as `experiments/` only after students confirm
they no longer rely on its existing paths. No need to move it immediately.

## 3. Special case — `LBM`

The Git tree has a top-level `LBM` entry with mode `160000`: that is a
**Git submodule pointer**, not an ordinary tracked folder. The same tree
does **not** contain a `.gitmodules` file.

- It is not registered by the FastAPI app, and no reference was found in the
  checked API source.
- However, Git submodules can be development dependencies or course materials.
- Because `.gitmodules` is absent, a fresh clone may not know where to
  obtain this submodule.

**Do not delete blindly.** First check whether `LBM` is intentionally
needed. If yes, restore/document its submodule configuration. If not, remove
the submodule pointer in a separate reviewed commit.

## 4. Small unused code (not whole files)

- `splitting_text()` in `Service/model_service/non_login_chatbot.py` is
  not called elsewhere in the checked code. It looks safe to remove after
  checking student exercises.
- Several modules still re-export compatibility names after the speech
  refactor. Leave these exports until you know no older scripts import them.

## 5. Files and directories to **keep**

These are linked to live API routes and/or important teaching/testing:

- `Service/app/` (except the disabled `video_app.py` candidate).
- `Service/model/` including `login.py`, `structured_output.py`,
  `speech_model.py`, `audio_utils.py`, `dates.py`,
  `audio_parse.py`, `caption.py`, `beautification.py`,
  `description.py`, `non_login.py`, `non_login_speech_answer.py`,
  and `text_to_speech.py`.
- `Service/model_service/login_chatbot.py` and
  `non_login_chatbot.py`.
- Used request/response classes in `Service/common/`, including
  `caption_request.py`: it is used internally to validate the caption
  service's data even though the HTTP endpoint uses uploads.
- `Service/config.py`, `Service/config.json`, `Service/main.py`,
  `setup.py`.
- `tests/`, `test_login_apis.py`, `README.md`,
  `API_TEST_EXAMPLES.md`, `API_RESPONSE_CONTRACT.md`, and
  `REFACTOR_NOTES.md`.
- Empty `__init__.py` files: these mark/initialize Python packages and are
  not clutter that should automatically be deleted.

An entry in `.gitignore` does **not** prove that a directory actually exists
or is checked into Git. Do not delete directories merely because their names
appear in `.gitignore`.

## 6. Suggested safe cleanup order

1. **First, confirm candidates:** ask whether old demo notebooks and the
   `LBM` submodule are used in teaching.
2. **Remove only clearly dead modules**, in a small commit:
   `base_tts.py`, unused beauty request/response models,
   `transcription_request.py`, `dates_request.py`, and the disabled
   `video_app.py`, once external usage is ruled out.
3. **Keep all experimental work separately** until its teaching purpose is
   decided. Avoid large folder moves on the same commit as code deletion.
4. **Run the tests and start the service**, then test food/travel, image,
   date extraction and audio login with `API_TEST_EXAMPLES.md`.

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python Service/main.py
```

**Audit outcome:** several strong unused-file candidates were identified.
No runtime code, APIs, folders, or submodule pointers were changed or deleted.

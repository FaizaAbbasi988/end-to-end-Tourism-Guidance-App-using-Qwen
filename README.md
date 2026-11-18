# Tourism Guidance AI Service

This is the **AI microservice** for an educational tourism guidance project.
It uses FastAPI and local Ollama/Qwen models. The separate backend and frontend
applications connect to this service through HTTP.

## What the service does

- **Travel:** Generate three suggested routes.
- **Food:** Recommend three restaurants for each requested meal.
- **Accommodation:** Suggest places to stay.
- **Summary:** Write a trip summary.
- **Non-login chatbot:** Answer questions about attractions and local culture.
- **Speech:** Convert uploaded audio to text and extract travel details.
- **Images:** Generate captions and enhance uploaded photos.

All **four logged-in APIs** (travel, food, accommodation, summary) return
`answer` as a **JSON array of strings** when successful. Other endpoints
keep their own response formats.

## Getting started

1. Install Python 3.10 or 3.11 and create a virtual environment.
2. Install the project from the repository root:

   ```powershell
   python -m pip install -e .
   ```

3. Install [Ollama](https://ollama.com/) and download the model configured in
   `Service/config.json` (currently `qwen2.5:3b`):

   ```powershell
   ollama pull qwen2.5:3b
   ```

4. Start the service **from the repository root**:

   ```powershell
   python Service/main.py
   ```

   Or: `python -m Service.main`.

5. Open the automatic API documentation at:
   `http://localhost:8000/docs`.

**Speech and image endpoints have additional requirements:** local FunASR
model files, an image-captioning model, and optional text-to-speech support.
Check your model paths in `Service/config.json` before testing them.

## Test the APIs

Copy endpoint URLs and sample parameters from **[API_TEST_EXAMPLES.md](API_TEST_EXAMPLES.md)**.
For example, send POST requests to:

- `http://localhost:8000/algorithm/api/login/travel`
- `http://localhost:8000/algorithm/api/login/food`

Test the Python code from the repository root:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

To test actual Qwen output (Ollama must be running):

```powershell
python test_login_apis.py --category all
```

## Code organization

```text
Service/
  main.py                # Starts FastAPI
  config.json            # Model settings and prompts
  config.py              # Reads the JSON settings
  app/                   # HTTP API endpoints
  common/http/           # Pydantic request/response models
  model/                 # Qwen, speech, image and TTS code
    audio_utils.py       # Shared audio preprocessing
    speech_model.py      # Shared speech recognition model
    structured_output.py # Travel/food response validation and formatting
  model_service/         # Connects endpoints to AI code
experiments/             # Old notebooks; not part of FastAPI
tests/                   # Unit and API contract tests
API_TEST_EXAMPLES.md     # Manual Postman testing examples
REFACTOR_NOTES.md        # Changes and ideas for future cleanup
```

For students: follow one request through `Service/app/`, then
`Service/model_service/`, then `Service/model/`. This is the easiest way to
understand the flow without learning any additional framework.

## Notes

The AI generates teaching examples, not verified commercial travel bookings.
Do not rely on model-generated prices, distances, hotel facilities, or
restaurant names without independent verification.

The `changes` branch is for incremental cleanup and testing; avoid merging
into `main` until the team has retested its integrations.

## Archived experiments and removed files

Older notebooks and an unused video demonstration live in
[experiments/](experiments/) and are not loaded by the API.
The unused `LBM` submodule pointer and outdated, unreferenced API schema
modules were removed on `changes`. See [UNUSED_FILES_AUDIT.md](UNUSED_FILES_AUDIT.md)
for the reasons and a full list of changes.

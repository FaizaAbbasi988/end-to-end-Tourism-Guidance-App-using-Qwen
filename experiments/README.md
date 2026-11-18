# Experiments (not used by the running API)

These notebooks and the standalone video demo were moved here from
`Algorithm/` to keep the AI service code easy for students to navigate.

## Contents

- `image_enhancement.ipynb` and `image_enhancement.py` — early
  Stable Video Diffusion demonstration (not the live image-beautification API).
- `tt.ipynb` — early text-to-speech experiments.
- `text_correction.ipynb` — experiments parsing and splitting generated text.
- `non_login/test2.ipynb` — a small text-classification/string-check example.
- `non_login/test_1.ipynb` — an older, larger non-login development notebook.

The six original files were **moved without changing their content**.
Some examples contain absolute Windows paths or require GPU libraries. They
are study material, not application entry points, and may need adaptation to
run on another computer.

## Active code

Use `Service/main.py` to start the actual FastAPI service.
The active image enhancer is `Service/model/beautification.py`.
The active TTS service is `Service/model/text_to_speech.py`.

See `../API_TEST_EXAMPLES.md` for the registered API URLs and example data.

# Local Postman testing

Import `Tourism_AI_Service.postman_collection.json` into Postman via **Import > Files**.

1. Start Ollama and required models, then launch the AI service from the repository root:
   `python Service/main.py` (or your working project launch command).
2. In the collection's **Variables**, set `baseUrl = http://localhost:8000` and
   `apiPrefix = /algorithm/api`. Use your own host/port if different.
3. Select a request from a folder, click **Send**. Edit the JSON **Body** to
   change sample parameters.
4. For audio and image endpoints, open **Body > form-data** and select local
   audio/image files in the **Value** field. Postman sets multipart encoding.
5. Use **Discovery > OpenAPI document** or visit `http://localhost:8000/docs`
   for the FastAPI route definitions.

**Notes:** This collection describes the API service only. Video generation
in `Service/app/video_app.py` is commented out and not registered. Some audio
routes may require local FunASR, TTS, or Ollama models and can have startup
dependencies. The `/non-login/audio_path` request expects a file path on the
**server machine**, not a file uploaded from Postman.

Travel and food requests have automatic Postman assertions for the new
`answer: list[str]` shape. In the example food request, lunch and dinner
expect seven elements in total. Other requests use basic HTTP status checks;
their full semantics and real-model behavior still require manual validation.

This is an importable test fixture collection; no production API handlers are
changed by this file.

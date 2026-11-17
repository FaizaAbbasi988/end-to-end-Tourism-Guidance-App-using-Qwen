# Tourism AI Service — API endpoints and sample test parameters

A simple, copy/paste reference for **Postman** and other HTTP clients. This lists
the routes exposed by this repository's AI service, **not** the separate backend
engineer's APIs.

**Base URL:** `http://localhost:8000/algorithm/api`
**Default method:** `POST`
**For JSON endpoints:** Postman → Body → raw → JSON.
**For audio/images:** Postman → Body → form-data, with the named field set to
**File** and a real local file selected.

Start your service using your normal working launch command (in this repo:
`python Service/main.py`). Port 8000 is configured in `Service/main.py`.
`/docs` and `/openapi.json` are provided by FastAPI.

---

## 1. Login — Travel API

**URL:** `http://localhost:8000/algorithm/api/login/travel`

**Body (raw JSON):**
```json
{
  "arrival_datetime": "2026-12-01",
  "departure_datetime": "2026-12-05",
  "traveler_ages": [25, 30],
  "historical_culture_interests": ["晋祠"],
  "folk_culture_interests": ["平遥古城"],
  "famous_humanistic_interests": [],
  "red_culture_interests": [],
  "food_interests": ["山西面食"],
  "celebrity_culture_interests": [],
  "interest_priority_order": ["historical_culture", "food"]
}
```

**Successful response:** `success: true`, `answer` is an array of **4 strings**:
introduction, route 1, route 2, route 3.

## 2. Login — Food API

**URL:** `http://localhost:8000/algorithm/api/login/food`

**Body (raw JSON):**
```json
{
  "selected_route": "从游览晋祠开始，随后前往平遥古城体验传统民俗工艺，最后在钟楼街品尝地道特色美食。",
  "date": "2026-12-01 至 2026-12-05",
  "distance_range": "1-3公里",
  "number_of_people": 2,
  "budget": 150,
  "meal_preferences": ["午餐", "晚餐"]
}
```

**Successful response:** `success: true`, `answer` is an array of **7 strings**:
introduction, 3 lunch recommendations, 3 dinner recommendations. In general:
`1 + 3 * len(meal_preferences)`.

## 3. Login — Accommodation API

**URL:** `http://localhost:8000/algorithm/api/login/accommodation`

**Body (raw JSON):**
```json
{
  "selected_route": "从游览晋祠开始，随后前往平遥古城。",
  "date_of_stay": "2026-12-01 至 2026-12-05",
  "accommodation_type": "酒店",
  "housing_type": "双人间",
  "stars": 3,
  "room_rate": 500,
  "total_people": 2,
  "adults": 2,
  "elderly": 0,
  "children": 0,
  "children_age": [],
  "transportation_preference": "出租车"
}
```

**Successful response:** `answer` is a text string.

## 4. Login — Summary API

**URL:** `http://localhost:8000/algorithm/api/login/summary`

**Body (raw JSON):**
```json
{
  "selected_route": "晋祠 → 平遥古城",
  "selected_food": ["山西刀削面", "平遥牛肉"],
  "selected_accommodation": "平遥古城附近酒店",
  "preparation": "身份证、舒适的鞋",
  "notes": "希望体验历史文化和当地美食",
  "emergency": "急救电话120"
}
```

**Successful response:** `answer` is a text string.

## 5. Non-login — Chatbot API

**URL:** `http://localhost:8000/algorithm/api/non-login/chatbot`

**Body (raw JSON):**
```json
{
  "place": "晋祠",
  "info": "文化介绍"
}
```

Other `info` choices handled by the model include `最佳路线`, `景点游览`,
`特色美食`, and `交通信息`. Some choices also trigger text-to-speech.

## 6. Non-login — Audio Chatbot API

**URL:** `http://localhost:8000/algorithm/api/non-login/audio_chatbot`

**Body:** form-data

| Key | Type | Example |
| --- | --- | --- |
| `file` | File | Select `question.wav` from your computer |

**Response:** JSON with recognized question, answer, and optional audio data.

## 7. Non-login — Audio Path API

**URL:** `http://localhost:8000/algorithm/api/non-login/audio_path`

**Body (raw JSON):**
```json
{
  "audio_path": "D:\\travel_project\\downloaded_models\\example.mp3"
}
```

Replace the path with an **existing audio file on the machine running the AI
service**, not a local path on another computer.

## 8. Description — Destination Text API

**URL:** `http://localhost:8000/algorithm/api/description/text`

**Body (raw JSON):**
```json
{
  "destination": "平遥古城"
}
```

## 9. Caption — Image Caption API

**URL:** `http://localhost:8000/algorithm/api/caption/generate`

**Body:** form-data

| Key | Type | Example |
| --- | --- | --- |
| `files` | File | Select `jinsi_temple.jpg` |

To caption multiple images, add more file rows with the same key `files`.
Requires the configured image-captioning model.

## 10. Image — Beautification API

**URL:** `http://localhost:8000/algorithm/api/image/beautify?return_json=true`

**Body:** form-data

| Key | Type | Example |
| --- | --- | --- |
| `files` | File | Select `landscape.jpg` |

Add multiple `files` rows for multiple images. With `return_json=true`, the
response contains base64-encoded image data. Change the query parameter to
`return_json=false` for image/ZIP bytes.

## 11. Dates — Extract Arrival/Departure Dates from Audio

**URL:** `http://localhost:8000/algorithm/api/dates/extract_dates`

**Body:** form-data

| Key | Type | Example |
| --- | --- | --- |
| `file` | File | Select `travel_dates.wav` |

Example recognized speech: `我十二月一日到达，十二月五日离开`.

**Expected response fields:** `到达时间` and `离开时间`. These may be `null`
when extraction fails.

## 12. Audio Login — Parse Travel Parameters

**URL:** `http://localhost:8000/algorithm/api/audiologin/travel`

**Body:** form-data, `file` (File), e.g. `travel_request.wav`.

## 13. Audio Login — Parse Food Parameters

**URL:** `http://localhost:8000/algorithm/api/audiologin/food`

**Body:** form-data, `file` (File), e.g. `food_request.wav`.

## 14. Audio Login — Parse Accommodation Parameters

**URL:** `http://localhost:8000/algorithm/api/audiologin/accommodation`

**Body:** form-data, `file` (File), e.g. `hotel_request.wav`.

## 15. Audio Login — Parse Summary Parameters

**URL:** `http://localhost:8000/algorithm/api/audiologin/summary`

**Body:** form-data, `file` (File), e.g. `summary_request.wav`.

These four audio-login endpoints transcribe the uploaded audio and use Qwen
to extract parameters. The results depend on the speech model and prompt;
they are not covered by the travel/food list-response contract.

---

## Testing notes

- Use **POST** for all 15 APIs above.
- For JSON requests choose **Body → raw → JSON**. Do not use form-data for JSON.
- For upload requests choose **Body → form-data → File**, not raw JSON.
- Make sure Ollama and any needed speech/caption models are available.
- Some endpoints return `success: false` within HTTP 200; check the JSON response.
- The list-based contract applies to **login travel and food only**.
- The experimental video route is commented out and is **not active**.
- If unsure which inputs an endpoint requires, check FastAPI's interactive
  documentation at `http://localhost:8000/docs`.

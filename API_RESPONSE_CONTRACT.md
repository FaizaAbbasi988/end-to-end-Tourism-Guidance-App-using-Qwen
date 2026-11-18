# AI microservice response contract (branch: changes)

These are **AI service** responses from `/algorithm/api/login/*`, not outputs from
the separate backend or frontend applications.

## Travel: POST /algorithm/api/login/travel

Successful response always contains four **JSON string array elements**:
`answer[0]` is the introduction; `answer[1]`, `answer[2]` and
`answer[3]` are route 1, route 2 and route 3.

```json
{
  "answer": [
    "根据您的出行时间、兴趣偏好和同行人员的年龄，我们为您定制了三条山西旅行路线，请查阅并选择最适合您的行程：",
    "路线1：路线描述...",
    "路线2：路线描述...",
    "路线3：路线描述..."
  ],
  "success": true
}
```

## Food: POST /algorithm/api/login/food

Successful response contains `1 + 3 × len(meal_preferences)` elements.
`answer[0]` is an introduction. Each requested meal produces exactly three
restaurant elements, **in the same order** as the request's `meal_preferences`.
Each restaurant element begins with `【餐别】餐厅 N：` and contains its own five
display fields. There is **no separate meal-header element**.

Example request meal preferences `["午餐", "晚餐"]` produce:

```json
{
  "answer": [
    "根据您选择的旅行路线和用餐偏好，我们为您推荐以下本地餐厅：",
    "【午餐】餐厅 1：\n名称：...\n菜系：...\n人均：...\n推荐理由：...\n导航建议：...",
    "【午餐】餐厅 2：\n名称：...\n菜系：...\n人均：...\n推荐理由：...\n导航建议：...",
    "【午餐】餐厅 3：\n名称：...\n菜系：...\n人均：...\n推荐理由：...\n导航建议：...",
    "【晚餐】餐厅 1：\n名称：...\n菜系：...\n人均：...\n推荐理由：...\n导航建议：...",
    "【晚餐】餐厅 2：\n名称：...\n菜系：...\n人均：...\n推荐理由：...\n导航建议：...",
    "【晚餐】餐厅 3：\n名称：...\n菜系：...\n人均：...\n推荐理由：...\n导航建议：..."
  ],
  "success": true
}
```

**Consumer guidance:** parse HTTP JSON, then read `answer` as an array.
Do not split the serialized response on commas, because the strings themselves
may contain commas (including Chinese punctuation).

## Error behavior

If the model cannot pass schema/semantic validation after three tries,
the existing AI API behavior is retained: `{"answer":"error message","success":false}`.
Consumers must check `success` before treating `answer` as a list.

## Accommodation: POST /algorithm/api/login/accommodation

Successful responses contain exactly four strings in `answer`:
`answer[0]` is the introduction; `answer[1]` through `answer[3]`
are **three separate accommodation options**.

Each option includes its name, location, price per night, facilities,
transport advice and reason for recommendation.

```json
{
  "answer": [
    "根据您的旅行路线和住宿需求，我们为您推荐以下三个住宿选项：",
    "住宿选项1：\n名称：...\n位置：...\n每晚价格：...\n设施与服务：...\n交通建议：...\n推荐理由：...",
    "住宿选项2：\n名称：...\n位置：...\n每晚价格：...\n设施与服务：...\n交通建议：...\n推荐理由：...",
    "住宿选项3：\n名称：...\n位置：...\n每晚价格：...\n设施与服务：...\n交通建议：...\n推荐理由：..."
  ],
  "success": true
}
```

## Summary: POST /algorithm/api/login/summary

Successful responses contain exactly four strings in `answer`:

- `answer[0]`: introduction.
- `answer[1]`: day-by-day itinerary (all days inside one string).
- `answer[2]`: preparation, packing, and bookings.
- `answer[3]`: safety, emergency details, and important notes.

```json
{
  "answer": [
    "以下是根据您的选择整理的山西旅行总结：",
    "每日行程：\n第1天：游览晋祠。\n第2天：参观平遥古城。",
    "行前准备：\n携带身份证、充电器及合适的鞋。",
    "重要事项及安全：\n提前确认门票和酒店，注意安全。"
  ],
  "success": true
}
```

**Breaking change:** accommodation and summary previously returned a long
`answer` string. They now return an array when `success` is true.
The backend team must update those two integrations. On errors, the existing
response remains `{"answer":"error message","success":false}`.

The response schema checks shape and nonempty fields, **not** whether the
model's hotel names, prices or routes are factually verified.

## Local verification

```powershell
git switch changes
git pull origin changes
python -m unittest discover -s tests -p "test_structured_output.py" -v
python -m unittest discover -s tests -p "test_login_http_contract.py" -v
python -m unittest discover -s tests -p "test_accommodation_summary_structured.py" -v
python test_login_apis.py --category all
```

The unit tests do not need a running Ollama server. The final smoke test
does require Ollama with `qwen2.5:3b` and does not test real-world accuracy.

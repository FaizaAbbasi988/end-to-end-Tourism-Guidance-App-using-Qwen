"""Manually smoke-test Qwen for all four /login categories (not HTTP).

From the repository root:
  python test_login_apis.py --category travel
  python test_login_apis.py --category food
  python test_login_apis.py --category accommodation
  python test_login_apis.py --category summary
  python test_login_apis.py --category all

Requires local Ollama with qwen2.5:3b. The examples are illustrative;
they do not verify real-world restaurant/hotel availability or prices.
"""
import argparse
import traceback

from Service.model.login import Login


EXAMPLES = {
    "travel": {
        "arrival_datetime": "2026-12-01",
        "departure_datetime": "2026-12-05",
        "traveler_ages": [25, 30],
        "historical_culture_interests": ["晋祠"],
        "folk_culture_interests": ["平遥古城"],
        "famous_humanistic_interests": [],
        "red_culture_interests": [],
        "food_interests": ["山西面食"],
        "celebrity_culture_interests": [],
        "interest_priority_order": ["historical_culture", "food"],
    },
    "food": {
        "selected_route": "晋祠 → 平遥古城",
        "date": "2026-12-02",
        "number_of_people": 2,
        "budget": 100,
        "distance_range": "3公里",
        "meal_preferences": ["午餐"],
    },
    "accommodation": {
        "selected_route": "晋祠 → 平遥古城",
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
        "transportation_preference": "出租车",
    },
    "summary": {
        "selected_route": "晋祠 → 平遥古城",
        "selected_food": ["山西刀削面", "当地小吃"],
        "selected_accommodation": "平遥古城附近酒店",
        "preparation": "身份证、舒适的鞋",
        "notes": "适合轻松步行",
        "emergency": "紧急医疗电话120",
    },
}


def backend_split(answer, markers):
    for marker in markers:
        answer = answer.replace(marker, "@@@" + marker)
    return [p.strip() for p in answer.split("@@@") if p.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", choices=[*EXAMPLES, "all"], default="all")
    args = parser.parse_args()
    categories = list(EXAMPLES) if args.category == "all" else [args.category]
    model = Login()
    failures = []

    for category in categories:
        print(f"\\n{'=' * 20} {category.upper()} {'=' * 20}", flush=True)
        try:
            answer = model.invoke(category, EXAMPLES[category])
            if not isinstance(answer, str) or not answer.strip():
                raise AssertionError("Empty or non-string response")
            print(answer, flush=True)
            if category == "travel":
                segments = backend_split(answer, ["路线1", "路线2", "路线3"])
                assert len(segments) == 4, f"Expected intro + 3 routes, got {len(segments)}"
                for index, segment in enumerate(segments[1:], 1):
                    assert segment.startswith(f"路线{index}："), segment
                print("PASS: legacy travel splitting (intro + 3 routes)")
            elif category == "food":
                segments = backend_split(answer, ["餐厅 1", "餐厅 2", "餐厅 3"])
                assert len(segments) == 4, f"Expected intro + 3 restaurants, got {len(segments)}"
                for index, segment in enumerate(segments[1:], 1):
                    assert segment.startswith(f"餐厅 {index}："), segment
                print("PASS: legacy food splitting (intro + 3 restaurants)")
            else:
                print("PASS: nonempty text returned (not schema-validated)")
        except Exception:
            failures.append(category)
            traceback.print_exc()

    print("\\nResult:", "FAILED " + ", ".join(failures) if failures else "ALL SELECTED CATEGORIES PASSED")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

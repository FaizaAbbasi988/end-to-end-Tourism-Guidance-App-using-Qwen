from typing import List

from Service.model.login import Login

login_model = Login()

def handle_travel(data: dict) -> List[str]:
    return login_model.invoke("travel", data)

def handle_food(data: dict) -> List[str]:
    return login_model.invoke("food", data)

def handle_accommodation(data: dict) -> List[str]:
    return login_model.invoke("accommodation", data)

def handle_summary(data: dict) -> List[str]:
    return login_model.invoke("summary", data)

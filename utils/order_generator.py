import random
import string
from datetime import date, timedelta
from typing import List, Optional, Dict, Any
from http import HTTPStatus


def _rand_str(n: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def generate_order_payload(colors: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "firstName": _rand_str(6).title(),
        "lastName": _rand_str(8).title(),
        "address": f"ул. {_rand_str(6).title()}, д. {random.randint(1, 100)}",
        "metroStation": random.randint(1, 10),
        "phone": f"+7{random.randint(900_000_0000, 999_999_9999)}",
        "rentTime": random.randint(1, 7),
        "deliveryDate": (date.today() + timedelta(days=1)).isoformat(),
        "comment": f"Комментарий {_rand_str(5)}",
        **({"color": colors} if colors else {}),
    }


def create_order_and_get_id(order_obj, colors: Optional[List[str]] = None) -> int:
    # создать заказ
    resp = order_obj.post_order(generate_order_payload(colors))
    assert resp.status_code == HTTPStatus.CREATED
    track = resp.json()["track"]

    # вытянуть order_id через track
    resp = order_obj.track_order(track)
    assert resp.status_code == HTTPStatus.OK
    body = resp.json()

    order_id = (
        body.get("id")
        or (body.get("order") or {}).get("id")
        or (isinstance(body.get("order"), list) and body["order"][0].get("id"))
    )

    assert isinstance(order_id, int) and order_id > 0, f"Не удалось достать order_id: {body}"
    return order_id

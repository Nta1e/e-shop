import re
import jwt
from itertools import groupby


def decode_token_from_request(request):
    token = request.META['HTTP_USER_KEY'].split(' ')[-1]
    decoded_payload = jwt.decode(token, None, None)
    customer_id = decoded_payload.get('user_id')
    return customer_id


def count_consecutive(num):
    return max(len(list(g)) for _, g in groupby(num))


def validate_credit_card(num):
    pattern = re.compile(r"(?:\d{4}-){3}\d{4}|\d{16}")

    if not pattern.fullmatch(num) or count_consecutive(num.replace("-", "")) >= 4:
        return False
    else:
        return True
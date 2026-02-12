from django.conf import settings
from hashids import Hashids

hashids = Hashids(salt=settings.HASHIDS_SALT, min_length=10)

def encode_id(num: int):
    ### Перетворює числовий PK в hashid.
    return hashids.encode(num)

def decode_id(hashid: str):
    ### Перетворює hashid назад у PK.
    ### Повертає None, якщо хеш некоректний.
    decoded = hashids.decode(hashid)
    return decoded[0] if decoded else None



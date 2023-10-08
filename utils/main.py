import random

async def id_gen():
    id = ''
    digits = '0123456789abcdef'

    for _ in range(8):
        id += random.choice(digits)
    return id
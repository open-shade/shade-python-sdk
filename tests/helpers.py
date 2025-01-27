def get_random_string(length: int) -> str:
    import random
    import string

    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

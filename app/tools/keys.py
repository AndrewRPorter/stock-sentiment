import secrets

BYTE_LENGTH = 1.3


def generate_key(length=32):
    """
    Return a random URL-safe text string, containing nbytes random bytes.

    Note that the text is Base64 encoded, so on average each byte results in
    approximately 1.3 characters.
    """
    size = int(length / BYTE_LENGTH)
    key = secrets.token_urlsafe(size)
    return key

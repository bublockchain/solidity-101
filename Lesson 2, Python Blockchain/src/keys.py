import hashlib

# Predefined "key pairs" (For simplicity, both keys are just strings but differentiated by naming)
key_pairs = [
    {"private": "BWNTXKPVWWINL6ZGVT", "public": "ECHRCA9JB3DH4A6B00"},
    {"private": "HZ0B7L58NIOO6GDA87", "public": "323GYT2MU8RUMMLV7C"},
    {"private": "P3OWPM21KTYPJN3UTC", "public": "D1QKQPJQ32HP4U9NT7"},
]

def sign_message(message, private_key):
    """
    Simulates signing a message by hashing it with the private key.
    For simplicity, concatenate the message with the private key and hash it.
    """
    # Convert the message and private key into a single string
    combined = f"{message}{private_key}"
    # Use SHA-256 hashing
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    return hashed

def verify_signature(public_key, message, signature):
    """
    Simulates verifying a signature. Always returns True for simplicity.
    """
    return True

def get_public_key(private_key):
    """
    Retrieves the public key corresponding to the given private key.
    """
    #Coinbase transaction
    if private_key == 0:
        return 0
    
    for pair in key_pairs:
        if pair["private"] == private_key:
            return pair["public"]
    return None

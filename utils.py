import random
from sympy import isprime
import math

mapping = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "a": 10,
    "b": 11,
    "c": 12,
    "d": 13,
    "e": 14,
    "f": 15,
    "g": 16,
    "h": 17,
    "i": 18,
    "j": 19,
    "k": 20,
    "l": 21,
    "m": 22,
    "n": 23,
    "o": 24,
    "p": 25,
    "q": 26,
    "r": 27,
    "s": 28,
    "t": 29,
    "u": 30,
    "v": 31,
    "w": 32,
    "x": 33,
    "y": 34,
    "z": 35,
    " ": 36
}

def generate_primes(n):
    while True:
        x = random.getrandbits(n)
        x |= (1 << n-1) | 1  # set MSB and LSB to 1
        if isprime(x):
            p = x
            break

    while True:
        x = random.getrandbits(n)
        x |= (1 << n-1) | 1  # set MSB and LSB to 1
        if isprime(x) and x != p:
            q = x
            break
    return p, q

def generate_e(p, q):
    phi = (p-1) * (q-1)
    while True:
        e = random.randrange(2, phi) # Choose a random integer between 2 and phi-1
        if math.gcd(e, phi) == 1:    # Check if e is relatively prime to phi
            return e

def generate_key(key_size):
    p, q = generate_primes(int(key_size))
    n = p * q
    phi = (p - 1) * (q - 1)
    e = generate_e(p, q)
    d = modinv(e, phi)
    return e, d, n

def modinv(a, b):
    g, x, y = egcd(a, b)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % b

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def encode(plaintext):
    # Convert plaintext to list of characters
    chars = list(plaintext.lower())
    
    # Pad the last substring with spaces if necessary
    num_substrings = (len(plaintext) + 4) // 5
    last_substring_length = len(plaintext) % 5
    if last_substring_length > 0:
        chars += [" "] * (5 - last_substring_length)
    
    # Compute the encoding for each substring
    encodings = []
    for i in range(num_substrings):
        substring = "".join(chars[i*5:(i+1)*5])
        encoding = 0
        for j in range(5):
            encoding += mapping[substring[j]] * (37**j)
        encodings.append(encoding)
        
    return encodings

def decode(encodings):
    plaintext_chars = []
    for encoding in encodings:
        encoding_chars = []
        for i in range(5):
            remainder = encoding % 37
            encoding_chars.append(remainder)
            encoding = encoding // 37
        
        # Convert encoding characters back to plaintext characters
        plaintext_chars.extend([k for k, v in mapping.items() if v == x][0] for x in encoding_chars)
    
    return ''.join(plaintext_chars).strip()

def encrypt(plaintext, e, n):
    encodings = encode(plaintext)
    encrypted = []
    for i, encoding in enumerate(encodings):
        ciphertext = pow(encoding, e, n)
        encrypted.append(ciphertext)
    return encrypted

def decrypt(ciphertexts, d, n):
    decoded = []
    for ciphertext in ciphertexts:
        decrypted = pow(ciphertext, d, n)
        decoded.append(decrypted)
    
    plaintext = decode(decoded)
    return plaintext
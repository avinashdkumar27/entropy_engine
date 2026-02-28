import math
import string

def calculate_entropy(password):
    if not password:
        return 0, 0, 0
        
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)
        
    # If no recognized characters (e.g. whitespace only or other unicode), default to 1.
    if charset_size == 0:
        charset_size = 1

    length = len(password)
    entropy = length * math.log2(charset_size)
    combinations = charset_size ** length
    
    return charset_size, combinations, entropy

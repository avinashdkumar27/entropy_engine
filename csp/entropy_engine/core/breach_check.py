import hashlib
import requests

def check_pwned(password):
    """
    Check if the password has been exposed in data breaches.
    Returns the number of times breached, or 0 if not found.
    """
    if not password:
        return 0
        
    # SHA-1 hash of the password
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return 0
            
        # Parse the response to find the suffix match
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
    except Exception as e:
        # Avoid crashing the app if the network fails
        print(f"Error checking breach status: {e}")
        pass
        
    return 0

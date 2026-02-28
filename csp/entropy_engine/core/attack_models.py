ATTACK_MODELS = {
    "CPU (basic)": 1e8,           # 100 Million guesses/sec
    "Gaming GPU": 1e11,           # 100 Billion guesses/sec
    "High-end GPU cluster": 1e12, # 1 Trillion guesses/sec
    "Nation-state level": 1e15    # 1 Quadrillion guesses/sec
}

def get_crack_time(combinations, model_name):
    """
    Returns the estimated time to crack in seconds for the given model_name.
    """
    if model_name not in ATTACK_MODELS:
        model_name = "CPU (basic)"
        
    speed = ATTACK_MODELS[model_name]
    time_seconds = combinations / speed
    return time_seconds

def format_time(seconds):
    """
    Format seconds into a human-readable string.
    """
    if seconds < 1:
        return "Less than a second"
    
    intervals = (
        ('centuries', 3153600000),      # 100 years
        ('years', 31536000),             # 365 days
        ('months', 2592000),             # 30 days
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value >= 1:
            if value == 1:
                name = name.rstrip('s')
            return f"{int(value)} {name}"
    
    return "Less than a second"

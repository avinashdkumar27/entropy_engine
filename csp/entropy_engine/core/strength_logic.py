import zxcvbn
from .entropy import calculate_entropy
from .attack_models import get_crack_time, format_time, ATTACK_MODELS
from .breach_check import check_pwned

def analyze_password(password, attack_model="CPU (basic)"):
    """
    Analyze the password and return comprehensive metrics.
    """
    if not password:
        return _empty_result()
    
    # 1. Entropy calculation
    charset_size, combinations, entropy = calculate_entropy(password)
    
    # 2. Time to crack by selected attack model
    target_crack_seconds = get_crack_time(combinations, attack_model)
    target_crack_display = format_time(target_crack_seconds)
    
    # 3. Time to crack for all models (for graph)
    crack_times_all = {
        model: get_crack_time(combinations, model)
        for model in ATTACK_MODELS.keys()
    }
    
    # 4. zxcvbn Pattern detection
    z_res = zxcvbn.zxcvbn(password)
    z_score = z_res['score'] # 0 to 4
    z_crack_display = z_res['crack_times_display']['offline_fast_hashing_1e10_per_second']
    z_warnings = z_res['feedback']['warning']
    z_suggestions = z_res['feedback']['suggestions']
    
    # 5. HaveIBeenPwned check
    pwned_count = check_pwned(password)
    
    # 6. Overall Strength Meter (0 to 4) mapped to a 0-100 or 5-level scale
    # Criteria:
    # 0 = Weak (Red), 1 = Moderate (Orange), 2 = Strong (Yellow), 3 = Very Strong (Green), 4 = Unbreakable tier (Blue)
    
    # Start with zxcvbn score as base
    final_score = z_score
    
    # Adjust based on entropy if zxcvbn gives high score but entropy is low
    if entropy < 40 and final_score > 1:
        final_score = 1
    elif entropy > 60 and final_score >= 3:
        final_score = 4 # Elevate to unbreakable tier if extremely high entropy + high z_score
        
    # Punish heavily for breaches
    if pwned_count > 0:
        final_score = 0
        z_warnings = "PASSWORD FOUND IN DATA BREACH(ES)!"
        
    # Map final_score to colors and words
    tiers = {
        0: ("Weak", "#FF4C4C"),      # Red
        1: ("Moderate", "#FFA500"),  # Orange
        2: ("Strong", "#FFD700"),    # Yellow
        3: ("Very Strong", "#32CD32"),# Green
        4: ("Unbreakable", "#00BFFF") # Blue
    }
    
    meter_label, meter_color = tiers.get(final_score, ("Weak", "#FF4C4C"))
    
    return {
        "entropy": round(entropy, 2),
        "combinations": combinations,
        "crack_time_seconds": target_crack_seconds,
        "crack_time_display": target_crack_display,
        "crack_times_all": crack_times_all, # For matplotlib
        "zxcvbn_score": z_score,
        "zxcvbn_crack_display": z_crack_display,
        "warnings": z_warnings,
        "suggestions": z_suggestions,
        "pwned_count": pwned_count,
        "final_score": final_score,
        "meter_label": meter_label,
        "meter_color": meter_color
    }

def _empty_result():
    return {
        "entropy": 0,
        "combinations": 0,
        "crack_time_seconds": 0,
        "crack_time_display": "Instant",
        "crack_times_all": {m: 0 for m in ATTACK_MODELS.keys()},
        "zxcvbn_score": 0,
        "zxcvbn_crack_display": "Instant",
        "warnings": "",
        "suggestions": [],
        "pwned_count": 0,
        "final_score": 0,
        "meter_label": "None",
        "meter_color": "gray"
    }

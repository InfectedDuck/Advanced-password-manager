import hashlib
import requests
import string
import enchant
import math
from typing import Tuple, Set
import datetime

# Define password strength criteria
MIN_LENGTH = 12
MAX_LENGTH = 64
MIN_UPPERCASE = 2
MIN_LOWERCASE = 2
MIN_DIGITS = 2
MIN_SPECIAL = 2

# RockYou password list URL
ROCKYOU_URL = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/rockyou.txt'

# Load RockYou password list
def load_rockyou_passwords() -> Set[str]:
    try:
        response = requests.get(ROCKYOU_URL)
        response.raise_for_status()
        passwords = set(response.text.splitlines())
        return passwords
    except requests.RequestException as e:
        print(f"Error loading RockYou password list: {e}")
        return set()

# Check if password is compromised using Pwned Passwords API
def check_pwned_password(password: str) -> bool:
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    response = requests.get(f'https://api.pwnedpasswords.com/range/{sha1_password[:5]}')
    
    if response.status_code == 200:
        hashes = response.text.splitlines()
        for hash_ in hashes:
            if hash_.startswith(sha1_password[5:]):
                return True
    return False

# Check if password is common using RockYou password list
def check_common(password: str, rockyou_passwords: Set[str]) -> bool:
    return password.lower() in rockyou_passwords

# Password analysis functions
def check_length(password: str) -> bool:
    return MIN_LENGTH <= len(password) <= MAX_LENGTH

def check_uppercase(password: str) -> bool:
    return sum(1 for c in password if c.isupper()) >= MIN_UPPERCASE

def check_lowercase(password: str) -> bool:
    return sum(1 for c in password if c.islower()) >= MIN_LOWERCASE

def check_digits(password: str) -> bool:
    return sum(1 for c in password if c.isdigit()) >= MIN_DIGITS

def check_special(password: str) -> bool:
    special_chars = string.punctuation
    return sum(1 for c in password if c in special_chars) >= MIN_SPECIAL

def check_repeated_characters(password: str) -> bool:
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            return False
    return True

def check_common_patterns(password: str) -> bool:
    patterns = [
        "123456", "password", "123456789", "12345678", "12345",
        "1234567", "admin", "letmein", "welcome", "password1"
    ]
    return not any(pattern in password.lower() for pattern in patterns)

def check_dictionary_words(password: str) -> bool:
    d = enchant.Dict("en_US")
    words = password.split()
    return not any(d.check(word) for word in words)

def calculate_entropy(password: str) -> float:
    chars = set(password)
    entropy = len(password) * math.log2(len(chars))
    return entropy

def check_entropy(password: str) -> bool:
    entropy = calculate_entropy(password)
    return entropy >= 50  # Example threshold

def check_variation(password: str, username: str, email: str) -> bool:
    return not (username.lower() in password.lower() or email.lower() in password.lower())

def analyze_password(password: str, rockyou_passwords: Set[str], username: str, email: str) -> Tuple[bool, str]:
    if not check_length(password):
        return False, "Password must be between 12 and 64 characters."
    if not check_uppercase(password):
        return False, "Password must contain at least 2 uppercase letters."
    if not check_lowercase(password):
        return False, "Password must contain at least 2 lowercase letters."
    if not check_digits(password):
        return False, "Password must contain at least 2 digits."
    if not check_special(password):
        return False, "Password must contain at least 2 special characters."
    if not check_repeated_characters(password):
        return False, "Password contains repeated characters."
    if not check_common_patterns(password):
        return False, "Password contains common patterns."
    if not check_dictionary_words(password):
        return False, "Password contains dictionary words."
    if not check_entropy(password):
        return False, "Password entropy is too low."
    if not check_variation(password, username, email):
        return False, "Password should not be similar to your username or email."
    if check_common(password, rockyou_passwords):
        return False, "Password is too common and easily guessable."
    if check_pwned_password(password):
        return False, "Password has been exposed in a data breach."
    return True, "Password is strong."

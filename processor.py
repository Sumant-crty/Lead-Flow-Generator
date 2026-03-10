from email_validator import validate_email, EmailNotValidError
import pandas as pd

def verify_lead_email(email):
    try:
        # Check syntax and deliverability
        valid = validate_email(email, check_deliverability=False)
        return valid.normalized
    except EmailNotValidError:
        return None

def categorize_lead(title):
    title = title.lower()
    if any(word in title for word in ['ceo', 'founder', 'vp', 'director']):
        return "High Priority (Decision Maker)"
    return "Standard"
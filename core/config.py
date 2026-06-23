import os
import re
from typing import Dict, Any

class ValidationError(Exception):
    """Custom exception raised when input validation fails."""
    pass

def load_api_key() -> str:
    """
    Attempts to load the Gemini API key from environment variables.
    Returns the key if found, otherwise returns an empty string (to be supplied by UI).
    """
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""

def validate_profile_inputs(
    skills: str,
    budget: str,
    education: str,
    location: str,
    interests: str
) -> Dict[str, Any]:
    """
    Validates user profile inputs to prevent injection and format errors.
    Returns cleaned inputs if valid, otherwise raises ValidationError.
    """
    # 1. Check for empty inputs
    if not skills.strip():
        raise ValidationError("Skills field cannot be empty.")
    if not budget.strip():
        raise ValidationError("Budget field cannot be empty.")
    if not education.strip():
        raise ValidationError("Education field cannot be empty.")
    if not location.strip():
        raise ValidationError("Location field cannot be empty.")
    if not interests.strip():
        raise ValidationError("Interests field cannot be empty.")

    # 2. Validate Budget is a positive number
    # Remove currency symbols ($ , etc) and check float conversion
    cleaned_budget_str = re.sub(r'[^\d.]', '', budget)
    if not cleaned_budget_str:
        raise ValidationError("Budget must contain a valid number.")
    try:
        cleaned_budget = float(cleaned_budget_str)
        if cleaned_budget <= 0:
            raise ValidationError("Budget must be a positive number greater than zero.")
    except ValueError:
        raise ValidationError("Budget must be a valid number.")

    # 3. Clean textual inputs (strip whitespace and potential bad characters)
    # Simple sanitization to prevent prompt injection or execution tags
    def sanitize(text: str) -> str:
        # Strip common HTML/XML tags and keep alphanumeric + basic punctuation
        sanitized = re.sub(r'<[^>]*>', '', text)
        return sanitized.strip()

    cleaned_skills = sanitize(skills)
    cleaned_education = sanitize(education)
    cleaned_location = sanitize(location)
    cleaned_interests = sanitize(interests)

    if not cleaned_skills:
        raise ValidationError("Skills contains invalid characters.")
    if not cleaned_education:
        raise ValidationError("Education contains invalid characters.")
    if not cleaned_location:
        raise ValidationError("Location contains invalid characters.")
    if not cleaned_interests:
        raise ValidationError("Interests contains invalid characters.")

    return {
        "skills": cleaned_skills,
        "budget": cleaned_budget,
        "education": cleaned_education,
        "location": cleaned_location,
        "interests": cleaned_interests
    }

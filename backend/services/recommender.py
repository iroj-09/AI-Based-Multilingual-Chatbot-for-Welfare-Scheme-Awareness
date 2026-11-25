"""Rule-based scheme suggestions.

Every scheme returned here must exist in the chatbot's knowledge base
(data/cleaned_schemes.jsonl or data/supplementary_schemes.jsonl) so that users
can ask the chatbot for details. The rules are a coarse first filter only;
official eligibility is always decided by the scheme authority.
"""

LOW_INCOME_LIMIT = 300000


def _scheme(name: str, reason: str) -> dict:
    return {
        "name": name,
        "reason": reason,
        "ask": f"Tell me about {name}: benefits, eligibility, documents and how to apply",
    }


def recommend_schemes(user_data: dict) -> list[dict]:

    occupation = str(user_data.get("occupation", "")).strip().lower()
    gender = str(user_data.get("gender", "")).strip().lower()
    income = user_data.get("income", 0)
    age = user_data.get("age", 0)

    is_farmer = "farm" in occupation or "kisan" in occupation or "agricultur" in occupation
    low_income = income < LOW_INCOME_LIMIT

    results = []

    if is_farmer:
        results.append(
            _scheme(
                "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                "Income support for landholding farmer families.",
            )
        )
        results.append(
            _scheme(
                "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                "Crop insurance for farmers.",
            )
        )
        results.append(
            _scheme(
                "Kisan Credit Card",
                "Short-term credit for farming needs.",
            )
        )
        if 18 <= age <= 40:
            results.append(
                _scheme(
                    "Pradhan Mantri Kisan Maandhan Yojana",
                    "Pension scheme for small and marginal farmers aged 18 to 40.",
                )
            )

    if low_income or age >= 70:
        results.append(
            _scheme(
                "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
                "Health cover for low-income families and senior citizens aged 70 and above.",
            )
        )

    if gender == "female" and low_income:
        results.append(
            _scheme(
                "Pradhan Mantri Ujjwala Yojana (PMUY)",
                "LPG connection for women from poor households.",
            )
        )

    return results

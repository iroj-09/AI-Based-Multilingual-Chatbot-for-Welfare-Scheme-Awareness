def recommend_schemes(user_data: dict) -> list[str]:
    """Rule-based scheme suggestions. Single source of truth for eligibility."""

    occupation = str(user_data.get("occupation", "")).strip().lower()
    gender = str(user_data.get("gender", "")).strip().lower()
    income = user_data.get("income", 0)
    age = user_data.get("age", 0)

    recommendations = []

    if occupation == "farmer":
        recommendations.append("PM-KISAN")

    if income < 300000:
        recommendations.append("Ayushman Bharat")

    if gender == "female" and income < 300000:
        recommendations.append("Ujjwala Yojana")

    if age >= 60 and income < 300000:
        recommendations.append("Indira Gandhi National Old Age Pension Scheme")

    return recommendations

def recommend_schemes(user_data):

    recommendations = []

    if user_data["occupation"] == "Farmer":
        recommendations.append("PM-KISAN")

    if user_data["income"] < 300000:
        recommendations.append("Ayushman Bharat")

    if user_data["gender"] == "Female":
        recommendations.append("Ujjwala Yojana")

    return recommendations
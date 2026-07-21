def generate_recommendations(risk_level, breach_count):
    recommendations = []

    if breach_count == 0:
        recommendations.append(
            "No known breaches were found for this email address."
        )
        recommendations.append(
            "Continue using unique passwords and multi-factor authentication."
        )

    elif risk_level == "low":
        recommendations.append(
            "Change the passwords for accounts connected to the identified breaches."
        )
        recommendations.append(
            "Use a unique password for every account."
        )

    elif risk_level == "medium":
        recommendations.append(
            "Change passwords for all affected accounts immediately."
        )
        recommendations.append(
            "Enable multi-factor authentication wherever possible."
        )
        recommendations.append(
            "Review recent account activity for suspicious logins."
        )

    elif risk_level == "high":
        recommendations.append(
            "Change all passwords associated with this email address immediately."
        )
        recommendations.append(
            "Use a password manager to create unique and complex passwords."
        )
        recommendations.append(
            "Enable multi-factor authentication on important accounts."
        )
        recommendations.append(
            "Monitor email, financial and social-media accounts for suspicious activity."
        )
        recommendations.append(
            "Be cautious of phishing messages using exposed personal information."
        )

    return "\n".join(recommendations)
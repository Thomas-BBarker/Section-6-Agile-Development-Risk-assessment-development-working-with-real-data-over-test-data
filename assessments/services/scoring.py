def calculate_risk_score(breach_count):
    """
    Convert the number of breaches into a score from 1 to 10.
    """

    if breach_count <= 0:
        return 1

    if breach_count == 1:
        return 2

    if breach_count == 2:
        return 3

    if breach_count == 3:
        return 4

    if breach_count == 4:
        return 5

    if breach_count == 5:
        return 6

    if breach_count <= 7:
        return 7

    if breach_count <= 10:
        return 8

    if breach_count <= 15:
        return 9

    return 10


def determine_risk_level(score):
    """
    Convert the numerical score into a readable risk category.
    """

    if score <= 3:
        return "low"

    if score <= 6:
        return "medium"

    return "high"


def generate_assessment_summary(breach_count, score, risk_level):
    """
    Generate a short explanation of the assessment result.
    """

    if breach_count == 0:
        return (
            "No known data breaches were found for this identifier. "
            "This does not guarantee that the account is completely secure."
        )

    breach_word = "breach" if breach_count == 1 else "breaches"

    return (
        f"The identifier was found in {breach_count} known data {breach_word}. "
        f"This produced a risk score of {score}/10 and a "
        f"{risk_level} risk classification."
    )
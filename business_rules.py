def validate_application(age, income, emi, credit_score):

    results = []

    # Age
    if age >= 21:
        results.append(("Age", True))
    else:
        results.append(("Age", False))

    # Income
    if income >= 30000:
        results.append(("Monthly Income", True))
    else:
        results.append(("Monthly Income", False))

    # Credit Score
    if credit_score >= 700:
        results.append(("Credit Score", True))
    else:
        results.append(("Credit Score", False))

    # EMI Ratio
    ratio = (emi / income) * 100 if income > 0 else 100

    if ratio <= 45:
        results.append(("EMI Ratio", True))
    else:
        results.append(("EMI Ratio", False))

    return results
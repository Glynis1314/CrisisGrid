def calculate_metrics(

    hospitals,

    police_stations,

    fire_stations

):

    total = (

        len(hospitals)

        +

        len(police_stations)

        +

        len(fire_stations)

    )

    coverage_score = min(

        round(

            total * 1.2,

            1

        ),

        10

    )

    if coverage_score >= 8:

        risk_level = "Low"

    elif coverage_score >= 5:

        risk_level = "Medium"

    else:

        risk_level = "High"

    summary = []

    if len(hospitals) >= 2:

        summary.append(

            "✔ Good hospital coverage"

        )

    else:

        summary.append(

            "⚠ Limited hospital coverage"

        )

    if len(police_stations) >= 2:

        summary.append(

            "✔ Good police coverage"

        )

    else:

        summary.append(

            "⚠ Limited police coverage"

        )

    if len(fire_stations) >= 1:

        summary.append(

            "✔ Fire coverage available"

        )

    else:

        summary.append(

            "⚠ Fire coverage limited"

        )

    return {

        "coverage_score": coverage_score,

        "risk_level": risk_level,

        "summary": summary

    }
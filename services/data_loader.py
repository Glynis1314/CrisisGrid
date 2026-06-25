import pandas as pd


def load_services():

    return pd.read_csv(

        "data/emergency_services.csv"

    )


def get_services(

    city,

    service_type

):

    data = load_services()

    data = data[

        (data["city"].str.lower() == city.lower())

        &

        (data["type"] == service_type)

    ]

    return data.to_dict(

        orient="records"

    )
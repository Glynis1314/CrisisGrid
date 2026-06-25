import requests


def get_live_incidents():

    try:

        url = "https://eonet.gsfc.nasa.gov/api/v3/events"

        response = requests.get(

            url,

            timeout=10

        )

        response.raise_for_status()

        data = response.json()

        incidents = []

        for event in data.get(

            "events",

            []

        ):

            title = event.get(

                "title",

                "Unknown"

            )

            category = event.get(

                "categories",

                [{}]

            )[0].get(

                "title",

                "Unknown"

            )

            geometry = event.get(

                "geometry",

                []

            )

            if not geometry:

                continue

            latest = geometry[-1]

            geometry_type = latest.get(

                "type"

            )

            coordinates = latest.get(

                "coordinates"

            )

            # NASA also returns polygons
            # Keep only point events

            if geometry_type != "Point":

                continue

            incidents.append(

                {

                    "title": title,

                    "category": category,

                    "latitude": coordinates[1],

                    "longitude": coordinates[0]

                }

            )

        return incidents

    except Exception as e:

        print(

            "NASA Error:",

            e

        )

        return []
import requests


def get_hospitals(

    latitude,

    longitude

):

    try:

        overpass_url = (

            "https://overpass-api.de/api/interpreter"

        )

        query = f"""

        [out:json];

        (

          node

          ["amenity"="hospital"]

          (around:3000,{latitude},{longitude});

        );

        out;

        """

        response = requests.get(

            overpass_url,

            params={

                "data": query

            },

            timeout=10

        )

        if response.status_code != 200:

            return []

        data = response.json()

        hospitals = []

        for element in data.get(

            "elements",

            []

        ):

            hospitals.append({

                "name": element.get(

                    "tags",

                    {}

                ).get(

                    "name",

                    "Unknown Hospital"

                ),

                "latitude": element["lat"],

                "longitude": element["lon"]

            })

        return hospitals

    except Exception:

        return []
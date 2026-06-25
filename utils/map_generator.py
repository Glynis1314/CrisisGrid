import folium

from folium.plugins import HeatMap


def create_map(

    latitude,

    longitude,

    city,

    hospitals=None,

    police_stations=None,

    fire_stations=None,

    show_heatmap=False

):

    crisis_map = folium.Map(

        location=[

            latitude,

            longitude

        ],

        zoom_start=12,

        control_scale=True

    )

    # =========================
    # Emergency HQ
    # =========================

    folium.Marker(

        [

            latitude,

            longitude

        ],

        popup=f"{city} Emergency HQ",

        tooltip="Emergency HQ",

        icon=folium.Icon(

            color="red",

            icon="home"

        )

    ).add_to(

        crisis_map

    )

    # =========================
    # Hospital Markers
    # =========================

    if hospitals:

        for hospital in hospitals:

            folium.Marker(

                [

                    hospital["latitude"],

                    hospital["longitude"]

                ],

                popup=hospital["name"],

                tooltip=hospital["name"],

                icon=folium.Icon(

                    color="green",

                    icon="plus"

                )

            ).add_to(

                crisis_map

            )

    # =========================
    # Police Station Markers
    # =========================

    if police_stations:

        for station in police_stations:

            folium.Marker(

                [

                    station["latitude"],

                    station["longitude"]

                ],

                popup=station["name"],

                tooltip=station["name"],

                icon=folium.Icon(

                    color="blue",

                    icon="shield"

                )

            ).add_to(

                crisis_map

            )

    # =========================
    # Fire Station Markers
    # =========================

    if fire_stations:

        for station in fire_stations:

            folium.Marker(

                [

                    station["latitude"],

                    station["longitude"]

                ],

                popup=station["name"],

                tooltip=station["name"],

                icon=folium.Icon(

                    color="orange",

                    icon="fire"

                )

            ).add_to(

                crisis_map

            )

    # =========================
    # Service Density
    # =========================

    if show_heatmap:

        heat_data = []

        if hospitals:

            for hospital in hospitals:

                heat_data.append(

                    [

                        hospital["latitude"],

                        hospital["longitude"]

                    ]

                )

        if police_stations:

            for station in police_stations:

                heat_data.append(

                    [

                        station["latitude"],

                        station["longitude"]

                    ]

                )

        if fire_stations:

            for station in fire_stations:

                heat_data.append(

                    [

                        station["latitude"],

                        station["longitude"]

                    ]

                )

        if heat_data:

            HeatMap(

                heat_data,

                radius=20,

                blur=15,

                min_opacity=0.4

            ).add_to(

                crisis_map

            )

    # =========================
    # Layer Control
    # =========================

    folium.LayerControl().add_to(

        crisis_map

    )

    return crisis_map
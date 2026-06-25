import osmnx as ox

import networkx as nx

from services.geocoder import get_coordinates


def get_route(

    start,

    destination

):

    try:

        start_coordinates = get_coordinates(

            start

        )

        destination_coordinates = get_coordinates(

            destination

        )

        if not start_coordinates or not destination_coordinates:

            return None

        start_lat, start_lon = start_coordinates

        end_lat, end_lon = destination_coordinates

        # Use a larger radius

        graph = ox.graph_from_point(

            (

                start_lat,

                start_lon

            ),

            dist=30000,

            network_type="drive"

        )

        origin = ox.distance.nearest_nodes(

            graph,

            start_lon,

            start_lat

        )

        destination_node = ox.distance.nearest_nodes(

            graph,

            end_lon,

            end_lat

        )

        shortest_route = nx.shortest_path(

            graph,

            origin,

            destination_node,

            weight="length"

        )

        route_coordinates = []

        for node in shortest_route:

            route_coordinates.append(

                [

                    graph.nodes[node]["y"],

                    graph.nodes[node]["x"]

                ]

            )

        return route_coordinates

    except Exception as e:

        print(

            "Route Error:",

            e

        )

        return None
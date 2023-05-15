from typing import List
import numpy as np
from lib.route_utils import calc_distance


def print_routes(routes: List[np.ndarray]):
    for (index, route) in enumerate(routes):
        print(f"Route {index + 1}, distance:{calc_distance(route):.2f} km")

from math import sqrt
import numpy as np
from typing import List
from itertools import cycle
from lib.utils import timer


def calc_distance(points) -> float:
    dist_sum = 0.0
    for i in range(len(points) - 1):
        x1, y1 = points[i][0], points[i][1]
        x2, y2 = points[i + 1][0], points[i + 1][1]
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        dist_sum += distance

    return dist_sum


def generate_random_route(points: np.ndarray, routes: List[np.ndarray],
                          generator=np.random.default_rng()) -> np.ndarray:
    route = np.array(points, copy=True)
    generator.shuffle(x=route, axis=0)

    while not _is_route_unique(route, routes):
        generator.shuffle(x=route, axis=0)

    return route


def _is_route_unique(gen_route: np.ndarray, routes: List[np.ndarray]) -> bool:
    for route in routes:
        if np.array_equal(route, gen_route):
            return False

    return True


def _cross_routes(generator, route_a: np.ndarray, route_b: np.ndarray):
    index_1 = generator.integers(low=0, high=len(route_a) - 1)  # route musi być większy niż 0
    index_2 = generator.integers(low=index_1 + 1, high=len(route_a))

    # new_route, _ = np.split(route_a, 2, axis=0)
    new_route = route_a[index_1:index_2, :]
    new_route_last_element = new_route[-1, :]
    route_b_element_index = np.where(np.all(route_b == new_route_last_element, axis=1))[0]

    route_b_cycle = cycle(np.roll(route_b, -route_b_element_index, axis=0))

    while len(new_route) < len(route_a):
        next_element = next(route_b_cycle)
        is_in_new_route = np.where(np.all(new_route == next_element, axis=1))[0]
        if len(is_in_new_route) == 0:
            new_route = np.concatenate((new_route, [next_element]), axis=0)

    return new_route


def _mutate_routes(generator, routes) -> List[np.ndarray]:
    """
    Calculate if mutation should occur and if so, mutate specified routes else return routes
    """

    def _replace_indexes(route, i1, i2) -> np.ndarray:
        """
        Takes points on i1 and i2 and swap them, returns mutated route
        """
        i1_val = route[i1]
        i2_val = route[i2]
        tmp_route = np.array(route, copy=True)
        tmp_route[i1] = i2_val
        tmp_route[i2] = i1_val

        return tmp_route

    def _reverse_order(route, i1, i2) -> np.ndarray:
        """
        Takes part of route from i1 to i2 and reverse order from that part,
        returns mutated route
        """
        points = route[i1:i2, :]
        tmp_route = np.array(route, copy=True)
        tmp_route[i1:i2, :] = np.flip(points, axis=0)

        return tmp_route

    if sum(generator.choice([0, 1], 1, p=[0.95, 0.05])) > 0:
        mutated_routes = []
        for _route in routes:
            index_1 = generator.integers(low=0, high=len(_route) - 1)  # route musi być większy niż 0
            index_2 = generator.integers(low=index_1 + 1, high=len(_route))
            if sum(generator.choice([0, 1], 1, p=[0.5, 0.5])) > 0:
                mutated_routes.append(_replace_indexes(_route, index_1, index_2))
            else:
                mutated_routes.append(_reverse_order(_route, index_1, index_2))

        return mutated_routes
    else:
        return routes


def _rate_routes(_routes: List[np.ndarray]) -> List[np.ndarray]:
    return list(sorted(_routes, key=lambda k: calc_distance(k)))


@timer
def optimize_routes(
        points: np.ndarray,
        initial_population=10,
        iterations=1000,
        generator=np.random.default_rng(),
        crossed_routes: int = 3
) -> List[np.ndarray]:
    """
    Raise exception when crossed_routes <= 0 or crossed_routes > initial_population - 1
    """
    if crossed_routes <= 0 or crossed_routes > initial_population - 1:
        raise Exception('crossed_routes must be > 0 and < initial_population - 1')

    _routes = []
    # Gen first random routes
    for _ in range(initial_population):
        r = generate_random_route(points, _routes, generator=generator)
        _routes.append(r)

    initial_routes_len = len(_routes)

    for _ in range(iterations):
        # 1 - Rates routes based on rate function
        _routes = _rate_routes(_routes)

        # 2 - Deleting worst routes
        if len(_routes) > initial_routes_len:
            _routes = _routes[0: initial_routes_len]

        # 3 - crossing number of crossed_routes with best one
        crossed = []
        for i in range(int(crossed_routes)):
            crossed.append(_cross_routes(generator, _routes[0], _routes[i + 1]))

        # 4 - mutating crossed routes
        crossed_mutated = _mutate_routes(generator, crossed)

        # 5 - add crossed routes
        _routes.extend(crossed_mutated)

    return _rate_routes(_routes)



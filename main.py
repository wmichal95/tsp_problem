import numpy as np
from lib.route_utils import optimize_routes
from lib.display import print_routes
from lib.plots import show_path
from lib.points import generate_points


points = generate_points(number_of_points=30, seed=10)

GENERATOR = np.random.default_rng(15)

optimized_routes = optimize_routes(
    points,
    initial_population=20,
    iterations=25000,
    generator=GENERATOR,
    crossed_routes=6,
)
print_routes(optimized_routes[:10])
show_path(points, optimized_routes[0])  # after optimization best path

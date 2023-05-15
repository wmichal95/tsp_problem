import numpy as np


def generate_points(number_of_points: int = 20, seed: int = 1) -> np.ndarray:
    generator = np.random.default_rng(seed)

    return generator.uniform(
        low=0,
        high=100,
        size=(number_of_points, 2)
    )

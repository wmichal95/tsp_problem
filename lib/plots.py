import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
from lib.route_utils import calc_distance


def show_path(
        points: np.ndarray,
        path: np.ndarray,
        save_to_file: bool = False,
        file_name: str = ''
) -> None:
    plt.clf()
    car_color = 'green'

    plt.scatter(
        x=points[:, 0], y=points[:, 1],
        color='black', marker='o', s=10,
        label='Points'
    )
    plt.plot(
        path[:, 0], path[:, 1],
        linewidth=.5, color=car_color,
        label='Car'
    )

    point_texts = []
    for index, [x, y] in enumerate(path):
        point_texts.append(plt.text(x=x, y=y, s=f'{index + 1}'))

    adjust_text(point_texts, arrowprops=dict(arrowstyle='->', color='lime'))

    plt.legend(
        title=f'Route length={calc_distance(path):.2f} km',
        bbox_to_anchor=(0, 1.02, 1, 0.2),
        loc="lower right",
        borderaxespad=0,
        ncol=4
    )

    if save_to_file:
        plt.savefig(f'{file_name}.png')
    else:
        plt.show()

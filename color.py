import numpy as np

colors = {
    "red": np.array([255, 0, 0]),
    "orange": np.array([233,130,1]),
    "yellow": np.array([255, 255, 0]),
    "green": np.array([1,176,13]),
    "light blue": np.array([10, 180, 220]),
    "dark blue": np.array([97,97,227]),
    "pink": np.array([228,39,139]),
    "violet": np.array([182, 99, 205]),
    "peach": np.array([253, 133, 134]),
    "light grey": np.array([179,211,215]),
    "dark grey": np.array([107,103,99]),
    "brown": np.array([158, 89, 60]),
}

def get_color(r, g, b):
    return min(colors.keys(), key=lambda name: np.linalg.norm(np.array([r, g, b]) - colors[name]))
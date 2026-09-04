# from https://gist.github.com/beotiger/c06eb184d975684eeead8feb7a8fa407
from typing import List


def hex_to_rgb(color: str) -> List[int]:
    # Pass 16 to the integer function for change of base
    return [int(color[i:i+2], 16) for i in range(1, 6, 2)]


def rgb_to_hex(color: List[int]) -> str:
    # Components need to be integers for hex to make sense
    color = [int(x) for x in color]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                        "{0:x}".format(v) for v in color])


def linear_gradient(s, f, n: int = 10):
    # Starting and ending colors in RGB form
    # Initialize a list of the output colors with the starting color
    rgb_list = [s]
    # Calculate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)
        ]
        # Add it to our list of output colors
        rgb_list.append(curr_vector)
    return rgb_list


def polylinear_gradient(colors, n):
    ''' returns a list of colors forming linear gradients between
        all sequential pairs of colors. "n" specifies the total
        number of desired output colors '''
    # The number of colors per individual linear gradient
    n_out = int(float(n / (len(colors)-1)))
    # returns dictionary defined by color_dict()
    gradient_dict = linear_gradient(colors[0], colors[1], n_out)

    if len(colors) > 1:
        for col in range(1, len(colors) - 1):
            colors = linear_gradient(colors[col], colors[col+1], n_out)
            # for k in ("hex", "r", "g", "b"):
            # Exclude first point to avoid duplicates
            gradient_dict += colors
    return gradient_dict


def tests():
    start_col = "#2D22C0"
    mid_col = "#4AA4B6"
    end_col = "#1DBD4D"
    num_colors = 24
    colors = linear_gradient(
        hex_to_rgb(start_col),  hex_to_rgb(end_col), n=num_colors)

    print(colors)
    assert (len(colors) == num_colors)

    colors = polylinear_gradient(
        [hex_to_rgb(start_col), hex_to_rgb(mid_col), hex_to_rgb(end_col)], n=num_colors)
    print(colors)
    assert (len(colors) == num_colors)


if __name__ == "__main__":
    tests()

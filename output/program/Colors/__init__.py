def red_color(text):
    red_color_start = '\033[91m'
    red_color_end = '\033[0m'
    return red_color_start + text + red_color_end


def blue_color(text):
    blue_color_start = '\033[94m'
    blue_color_end = '\033[0m'
    return blue_color_start + text + blue_color_end


def yellow_color(text):
    yellow_color_start = '\033[93m'
    yellow_color_end = '\033[0m'
    return yellow_color_start + text + yellow_color_end


def green_color(text):
    green_color_start = '\033[92m'
    green_color_end = '\033[0m'
    return green_color_start + text + green_color_end

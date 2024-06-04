DPI = 300
PIXEL_PER_MM = DPI / 25.4
PIXEL_PER_CM = PIXEL_PER_MM * 10


def get_pixels_per_cm(cm: float):
    return cm * PIXEL_PER_CM
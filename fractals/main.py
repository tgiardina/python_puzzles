from argparse import ArgumentParser
from PIL import Image
import math
import colorsys

IMAGE_SIZE = 1000
CENTER_X = IMAGE_SIZE / 2
CENTER_Y = IMAGE_SIZE / 2
MAX_COLOR = 255
WHITE = (MAX_COLOR, MAX_COLOR, MAX_COLOR)
BLACK = (0, 0, 0)

def draw_circle(x, y, radius):
    if x**2 + y**2 <= radius**2:
        return BLACK
    else:
        return WHITE

def draw_square(x, y, side_length):
    if abs(x) < side_length / 2 and abs(y) < side_length / 2:
        return BLACK
    else:
        return WHITE

def draw_triangle(x, y, side_length):
    height = side_length * math.sqrt(3) / 2
    recented_y = y + height / 2
    if recented_y < height and recented_y > 0:
        if math.tan(math.radians(60)) * abs(x) < abs(recented_y):
            return BLACK
        else:
            return WHITE
    else:
        return WHITE

def draw_sierpinski_triangle(x, y, side_length, n_iterations=1):
    height = side_length * math.sqrt(3) / 2
    if n_iterations == 0:
        return draw_triangle(x, y, side_length)
    else:
        in_triangle = (
            draw_sierpinski_triangle(x, y + height / 4, side_length / 2, n_iterations - 1) == BLACK or 
            draw_sierpinski_triangle(x - side_length / 4, y - height / 4, side_length / 2, n_iterations - 1) == BLACK or 
            draw_sierpinski_triangle(x + side_length / 4, y - height / 4, side_length / 2, n_iterations - 1) == BLACK
        )
        if in_triangle:
            return BLACK
        else:
            return WHITE

def iterate_mandelbrot(c, n_iterations, cutoff=100):
    if n_iterations == 0:
        return (0, 0)
    else:
        (z, iterations) = iterate_mandelbrot(c, n_iterations - 1)
        z = z**2 + c
        if abs(z) > cutoff:
            return (math.inf, iterations)
        else:
            return (z, iterations+1)

def draw_mandelbrot(real, imag, cutoff, n_iterations=1):
    c = complex(real, imag)
    (z, _) = iterate_mandelbrot(c, n_iterations, cutoff)
    if z == math.inf:
        return BLACK
    else:
        return WHITE

def draw_dynamic_mandelbrot(real, imag, cutoff, n_iterations=1):
    c = complex(real, imag)
    (z, iterations) = iterate_mandelbrot(c, n_iterations, cutoff)
    if z == math.inf:
        scaled_value = scale_value(iterations, n_iterations-1, 1)
        hue = scaled_value
        saturation = 1
        value = scaled_value
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return int(r * MAX_COLOR), int(g * MAX_COLOR), int(b * MAX_COLOR)
    else:
        return WHITE

def scale_value(value, curr_max, new_max):
    return (value * new_max) / curr_max

class Center:
    def __init__(self, x, y):
        self.x = x
        self.y = y

if __name__ == "__main__":
    # Get args.
    parser = ArgumentParser()
    parser.add_argument("--shape", type=str, default="circle")
    parser.add_argument("--size", type=float, default=0.5)
    parser.add_argument("--center", type=float, nargs='+', default=[0, 0])
    parser.add_argument("--zoom", type=float, default=1)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--cutoff", type=float, default=2)
    args = parser.parse_args()

    # Validate arguments.
    if len(args.center) != 2:
        raise ValueError("Center must be a pair of numbers.")
    if args.zoom <= 0:
        raise ValueError("Zoom must be a positive number.")

    # Create canvas.
    img = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), "white")
    pixels = img.load()

    # Define coordinates.
    coordinate_map = {}
    for x in range(IMAGE_SIZE):
        for y in range(IMAGE_SIZE):
            unit_x = (x - IMAGE_SIZE/2) / (IMAGE_SIZE/2)
            unit_y = (y - IMAGE_SIZE/2) / (IMAGE_SIZE/2)
            scaled_x = unit_x / args.zoom
            scaled_y = unit_y / args.zoom
            centered_x = scaled_x + args.center[0]
            centered_y = scaled_y + args.center[1]
            coordinate_map[x, y] = (centered_x, centered_y)

    # Render shape.
    if not args.shape or args.shape == "circle":
        radius = args.size
        for (x, y), (tx, ty) in coordinate_map.items():
            pixels[x, y] = draw_circle(tx, ty, radius)
    elif args.shape == "square":
        side_length = args.size
        for (x, y), (tx, ty) in coordinate_map.items():
            pixels[x, y] = draw_square(tx, ty, side_length)
    elif args.shape == "triangle":
        side_length = args.size
        for (x, y), (tx, ty) in coordinate_map.items():
            pixels[x, y] = draw_triangle(tx, ty, side_length)
    elif args.shape == "sierpinski_triangle":
        side_length = args.size
        iterations = args.iterations
        for (x, y), (tx, ty) in coordinate_map.items():
            pixels[x, y] = draw_sierpinski_triangle(tx, ty, side_length, iterations)
    elif args.shape == "mandelbrot":
        cutoff = args.cutoff
        iterations = args.iterations
        for (x, y), (tx, ty) in coordinate_map.items():
            pixels[x, y] = draw_mandelbrot(tx, ty, cutoff, iterations)
    elif args.shape == "dynamic_mandelbrot":
        cutoff = args.cutoff
        iterations = args.iterations
        for (x, y), (tx, ty) in coordinate_map.items():
            pixels[x, y] = draw_dynamic_mandelbrot(tx, ty, cutoff, iterations)
    else:
        raise ValueError(f"Invalid shape: {args.shape}")

    # Display image.
    img.show()
    # img.save("fractal.png")

    

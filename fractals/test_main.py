import math
from main import iterate_mandelbrot

class TestMain():
    def test_iterate_mandelbrot(self):
        # Test that the function returns 0 when applied to 0.
        assert iterate_mandelbrot(complex(0, 0), 0, 100) == (0, 0)
        assert iterate_mandelbrot(complex(0, 0), 10, 100) == (0, 10)

        # Test that the function returns math.inf when applied to a number greater than the cutoff.
        assert iterate_mandelbrot(complex(10, 10), 10, 100) == (math.inf, 1)

        # Test some cases that do not surpass the cutoff.
        assert iterate_mandelbrot(complex(1, 0), 1, 100) == (complex(1, 0), 1)
        assert iterate_mandelbrot(complex(1, 0), 2, 100) == (complex(2, 0), 2)
        assert iterate_mandelbrot(complex(1, 0), 3, 100) == (complex(5, 0), 3)
        assert iterate_mandelbrot(complex(0, 1), 1, 100) == (complex(0, 1), 1)
        assert iterate_mandelbrot(complex(0, 1), 2, 100) == (complex(-1, 1), 2)
        assert iterate_mandelbrot(complex(0, 1), 3, 100) == (complex(0, -1), 3)
        assert iterate_mandelbrot(complex(1, 1), 1, 100) == (complex(1, 1), 1)
        assert iterate_mandelbrot(complex(1, 1), 2, 100) == (complex(1, 3), 2)
        assert iterate_mandelbrot(complex(1, 1), 3, 100) == (complex(-7, 7), 3)

        # Test some cases that surpass the cutoff.
        assert iterate_mandelbrot(complex(11, 0), 1, 10) == (math.inf, 0)
        assert iterate_mandelbrot(complex(4, 0), 2, 10) == (math.inf, 1)
        assert iterate_mandelbrot(complex(1, 1), 3, 5) == (math.inf, 2)

import numpy as numpy

l_of_dicts = [{'x': 5.1, 'y': 38},
              {'x': 4.6, 'y': 35},
              {'x': 4.5, 'y': 33},
              {'x': 4.6, 'y': 32},
              {'x': 5.6, 'y': 32}]

xss = []
yss = []

for d in l_of_dicts:
    xss.append(d['x'])
    yss.append(d['y'])

xs = numpy.array(xss, dtype=numpy.float64)
ys = numpy.array(yss, dtype=numpy.float64)


def best_fit_slope_and_intercept(xs, ys):
    m = (((numpy.mean(xs) * numpy.mean(ys)) - numpy.mean(xs * ys)) /
         ((numpy.mean(xs) * numpy.mean(xs)) - numpy.mean(xs * xs)))

    b = numpy.mean(ys) - m * numpy.mean(xs)

    return m, b


m, b = best_fit_slope_and_intercept(xs, ys)

regression_linee = [(m * x) + b for x in xs]

print regression_linee


def regression_line(l_of_dicts):
    xss = []
    yss = []

    for d in l_of_dicts:
        xss.append(d['x'])
        yss.append(d['y'])

    xs = numpy.array(xss, dtype=numpy.float64)
    ys = numpy.array(yss, dtype=numpy.float64)

    m, b = best_fit_slope_and_intercept(xs, ys)

    regression_line = [(m * x) + b for x in xs]

    return regression_line


def squared_error(ys_orig, ys_line):
    return sum((ys_line - ys_orig) * (ys_line - ys_orig))


def coefficient_of_determination(ys_orig, ys_line):
    y_mean_line = [numpy.mean(ys_orig) for y in ys_orig]
    squared_error_regr = squared_error(ys_orig, ys_line)
    squared_error_y_mean = squared_error(ys_orig, y_mean_line)
    return 1 - (squared_error_regr / squared_error_y_mean)


r_squared = coefficient_of_determination(ys, regression_linee)
print(r_squared)

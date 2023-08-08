import numpy as np
import math

DX = 0.0001


class ConstraintModel:
    def __init__(self):
        # {"name": (fixed?, x,y), "name": (fixed?, x,y)}
        self._points = {}
        # { "abdist": ["DIST", ["pointa", "pointb"], [10] ] }
        self._constraints = {}

    def add_point(self, name, x, y):
        assert (
            name not in self._points
        ), "that point is already there, use update_point()"
        self._points[name] = [False, x, y]

    def update_point(self, name, x, y):
        assert name in self._points, "that point does not exist, use add_point()"
        self._points[name] = [self._points[name][0], x, y]

    def add_fixed_point(self, name, x, y):
        self._points[name] = [True, x, y]

    def add_distance_constraint(self, name, p1, p2, d):
        self._constraints[name] = ["DIST", [p1, p2], [d]]

    def yield_points(self):
        for p in self._points:
            yield (self._points[p][1], self._points[p][2])

    def yield_point_names(self):
        for p in self._points:
            yield p

    def get_vector(self):
        print(self._points)
        v = []
        for p in self._points:
            if not self._points[p][0]:
                v.append(self._points[p][1])
                v.append(self._points[p][2])
        return v

    def update_from_vector(self, vec):
        v = vec.copy()
        for p in self._points:
            if not self._points[p][0]:
                self._points[p][1] = v[0]
                self._points[p][2] = v[1]
                v = v[2:]

    def _distance_constraint(self, x1, y1, x2, y2, distance):
        return abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) - distance) ** 3

    def get_error_func(self):
        def f(v):
            self.update_from_vector(v)
            error = 0
            for c in self._constraints.values():
                if c[0] == "DIST":
                    error += self._distance_constraint(
                        self._points[c[1][0]][1],
                        self._points[c[1][0]][2],
                        self._points[c[1][1]][1],
                        self._points[c[1][1]][2],
                        c[2][0],
                    )
            return error

        return f


# d^2/dxdy, vec = vector , i1, i2 = indies of the 2 variables in the vector
def mixed_second_derivative(f, vec, i1, i2, dx=DX):
    def vec_replaced(v1, v2):
        return [
            v1 if idx == i1 else v2 if idx == i2 else val for idx, val in enumerate(vec)
        ]

    def first_derivative(v1, v2):
        return (f(vec_replaced(v1 + dx, v2)) - f(vec_replaced(v1, v2))) / dx

    if i1 == i2:
        return (
            first_derivative(vec[i1] + dx, vec[i2]) - first_derivative(vec[i1], vec[i2])
        ) / dx
    return (
        first_derivative(vec[i1], vec[i2] + dx) - first_derivative(vec[i1], vec[i2])
    ) / dx


# collomb vector
def gradient(f, vec, dx=DX):
    def vec_replaced(i, v):
        return [v if idx == i else val for idx, val in enumerate(vec)]

    grad = []
    for idx, val in enumerate(vec):
        grad.append((f(vec_replaced(idx, vec[idx] + dx)) - f(vec)) / dx)
    return np.c_[grad]


# works, should optomize by copying diagnal
def hessian(f, vec):
    l = len(vec)
    H = np.zeros((l, l))
    for i in range(l):
        for j in range(l):
            H[j][i] = mixed_second_derivative(f, vec, i, j)
    return H


# damped newtons method
def newtons_method(f, vec_start, n_iters, damping_factor=0.01, learning_rate=0.001):
    guess = vec_start
    for _ in range(n_iters):
        # print(guess, f(guess))
        guess = (
            guess
            - learning_rate
            * (
                np.linalg.inv(
                    damping_factor * np.identity(len(vec_start)) + hessian(f, guess)
                )
                @ gradient(f, guess)
            ).transpose()[0]
        )
        yield guess
    # return guess


import pyglet
from pyglet.window import mouse

window = pyglet.window.Window()

m = ConstraintModel()
m.add_fixed_point("P1", 100, 234)
m.add_point("P2", 320, 23)
m.add_point("P3", 320, 23)
m.add_distance_constraint("C1", "P1", "P2", 50)
m.add_distance_constraint("C2", "P2", "P3", 50)
m.add_distance_constraint("C3", "P1", "P3", 50)


hilighted = []

itr = newtons_method(m.get_error_func(), m.get_vector(), 10000, learning_rate=0.01)


def on_mouse_press(x, y, button, modifiers):
    pass


def on_mouse_release(x, y, button, modifiers):
    pass


@window.event
def on_mouse_motion(x, y, dx, dy):
    global hilighted
    hilighted = []
    first_hilighted = False  # i don't want to hilight 2 at once
    # i may want to later though if you can select a box or something
    for p in m.yield_points():
        if first_hilighted:
            hilighted.append(False)
        if (p[0] + 10 > x > p[0] - 10) and (p[1] + 10 > y > p[1] - 10):
            hilighted.append(True)
            first_hilighted = True
        else:
            hilighted.append(False)


@window.event
def on_mouse_drag(x, y, dx, dy, *args):
    global itr
    for i, p in enumerate(m.yield_point_names()):
        if hilighted[i]:
            print(p)
            m.update_point(p, x, y)
    # this does not work if i release early
    itr = newtons_method(m.get_error_func(), m.get_vector(), 10000, learning_rate=0.01)


def update(dt):
    window.clear()
    next(itr)
    for p, h in zip(m.yield_points(), hilighted):
        if h:
            pyglet.shapes.Circle(x=p[0], y=p[1], radius=15, color=(20, 225, 30)).draw()
            pyglet.shapes.Circle(x=p[0], y=p[1], radius=13, color=(0, 0, 0)).draw()
        pyglet.shapes.Circle(x=p[0], y=p[1], radius=10, color=(50, 225, 30)).draw()
    pyglet.text.Label(
        str(m.get_error_func()(m.get_vector())),
        font_size=12,
        x=60,
        y=30,
    ).draw()


pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()

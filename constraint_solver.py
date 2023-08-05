import numpy as np
import math

DX = 0.0001


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


def distance_constraint(x1, y1, x2, y2, distance):
    return abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) - distance)


def equality_constraint(var, val):
    return abs(var - val)


# finish this later
def angle_constraint(x1, y1, x2, y2, x3, y3, angle):
    return 2


def f(v):
    x1, y1, x2, y2 = v
    return (
        equality_constraint(x1, 250)
        + equality_constraint(y1, 250)
        + distance_constraint(x1, y1, x2, y2, 100)
    )


import pyglet
from pyglet.window import mouse

window = pyglet.window.Window()

x1, y1, x2, y2 = 0, 0, 0, 0
hilighted1 = False
hilighted2 = False
itr = newtons_method(f, [100, 234, 320, 23], 10000, learning_rate=0.01)


def on_mouse_press(x, y, button, modifiers):
    pass


def on_mouse_release(x, y, button, modifiers):
    pass


@window.event
def on_mouse_motion(x, y, dx, dy):
    global hilighted1, hilighted2
    if (x1 + 10 > x > x - 10) and (y1 + 10 > y > y1 - 10):
        hilighted1 = True
    else:
        hilighted1 = False
    if (x2 + 10 > x > x2 - 10) and (y2 + 10 > y > y2 - 10):
        hilighted2 = True
    else:
        hilighted2 = False


@window.event
def on_mouse_drag(x, y, dx, dy, *args):
    global x1, y1, x2, y2, itr
    if hilighted1:
        x1 = x
        y1 = y
    if hilighted2:
        x2 = x
        y2 = y
    itr = newtons_method(f, [x1, y1, x2, y2], 10000, learning_rate=0.01)


def update(dt):
    global x1, y1, x2, y2
    window.clear()
    x1, y1, x2, y2 = next(itr)
    if hilighted1:
        pyglet.shapes.Circle(x=x1, y=y1, radius=15, color=(20, 225, 30)).draw()
        pyglet.shapes.Circle(x=x1, y=y1, radius=13, color=(0, 0, 0)).draw()
    if hilighted2:
        pyglet.shapes.Circle(x=x2, y=y2, radius=15, color=(20, 225, 30)).draw()
        pyglet.shapes.Circle(x=x2, y=y2, radius=13, color=(0, 0, 0)).draw()
    pyglet.shapes.Circle(x=x1, y=y1, radius=10, color=(50, 225, 30)).draw()
    pyglet.shapes.Circle(x=x2, y=y2, radius=10, color=(50, 225, 30)).draw()


pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()

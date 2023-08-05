import math


class ConstraintModel:
    def __init__(self):
        # {"name": (fixed?, x,y), "name": (fixed?, x,y)}
        self._points = {}
        # { "abdist": ["DIST", ["pointa", "pointb"], [10] ] }
        self._constraints = {}

    def add_point(self, name, x, y):
        self._points[name] = [False, x, y]

    def add_fixed_point(self, name, x, y):
        self._points[name] = [True, x, y]

    def add_distance_constraint(self, name, p1, p2, d):
        self._constraints[name] = ["DIST", [p1, p2], [d]]

    def yield_points(self):
        for p in self._points:
            yield (self._points[p][1], self._points[p][2])

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
        return abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) - distance)

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


c = ConstraintModel()
c.add_point("A", 10, 10)
c.add_point("B", 20, 30)
c.add_fixed_point("C", 40, 30)
print(c.get_vector())
c.update_from_vector([100, 10, 20, 50])
print(c.get_vector())

for p in c.yield_points():
    print(p)

c.add_fixed_point("D", 40, 30)
c.add_fixed_point("E", 40, 30)
c.add_point("F", 40, 30)

c.update_from_vector([100, 10, 20, 50, 1, 1])

print(c.get_vector())

print("-------")

m = ConstraintModel()
m.add_fixed_point("P1", 0, 0)
m.add_point("P2", 0, 0)
m.add_distance_constraint("C1", "P1", "P2", 5)
f = m.get_error_func()
print(f([5, 0.1]))

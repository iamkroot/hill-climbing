import random


class Vector(list):
    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])
        else:
            super().__init__(args)

    def __str__(self):
        return "(" + ", ".join(str(round(i, 3) or 0.0) for i in self) + ")"

    def copy(self):
        return Vector(self)


def hillclimb(p: Vector, f, steps=1000):
    step_size = [1] * len(p)
    acc = 1.2
    eps = 1e-16
    candidate = (-acc, -1 / acc, 0, 1 / acc, acc)
    for _ in range(steps):
        yield p.copy()
        val = f(p)
        for i in range(len(p)):
            best = -1
            best_score = -1e100
            for j in range(len(candidate)):
                delta = step_size[i] * candidate[j]
                p[i] += delta
                try:
                    temp = f(p)
                except ValueError:
                    continue
                finally:
                    p[i] -= delta
                if temp > best_score:
                    best_score = temp
                    best = j
            if candidate[best] == 0:
                step_size[i] /= acc
            else:
                step_size[i] *= candidate[best]
                p[i] += step_size[i]
        if 0 < f(p) - val < eps:
            return p
    return p


def func(p: Vector):
    val = 1 - p[0]**2
    if isinstance(val, complex):
        raise ValueError
    return val


func.arity = 1


def get_initial_pt(func, scale=100):
    while True:
        p = Vector((random.random() - 0.5) * scale for _ in range(func.arity))
        try:
            func(p)
        except ValueError:
            continue
        else:
            return p


p = get_initial_pt(func, 100)
points = list(hillclimb(p, func))
vals = list(map(func, points))
print(points[-1], vals[-1])

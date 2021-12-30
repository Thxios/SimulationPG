import numpy as np


class Vec(np.ndarray):
    @property
    def x(self):
        return self[0]
    @property
    def y(self):
        return self[1]
    @x.setter
    def x(self, value):
        self[0] = value
    @y.setter
    def y(self, value):
        self[1] = value
    @property
    def magnitude(self):
        return np.sqrt(np.dot(self, self))
    @property
    def unit(self):
        mag = self.magnitude
        if mag == 0:
            return self
        return self / self.magnitude


def arr(x, y) -> np.ndarray:
    return np.array([x, y])

def vector(x, y) -> Vec:
    # return np.array([x, y])
    return np.array([x, y]).view(Vec)

# def magnitude(x):
#     return np.sqrt(np.dot(x, x))
#
# def unit(x):
#     return x / magnitude(x)

def proj_matrix(vec):
    u = vec.unit
    _mat = np.array([
        [u.x, u.y],
        [-u.y, u.x]
    ])
    _inv = np.array([
        [u.x, -u.y],
        [u.y, u.x]
    ])
    return _mat, _inv


class Circle:
    def __init__(self, center, radius):
        self.p = center
        self.r = radius


class Line:
    START = 0
    LINE = 1
    END = 2
    def __init__(self, start, end):
        self.s = start
        self.e = end
        self.vec = end - start
        # self.len = magnitude(self.vec)
        self.len = self.vec.magnitude

        self.proj, self.proj_inv = proj_matrix(self.vec)

        self.rect = Rect(min(self.s.x, self.e.x),
                         min(self.s.y, self.e.y),
                         abs(self.s.x - self.e.x),
                         abs(self.s.y - self.e.y))

    def projection(self, vec) -> Vec:
        return np.dot(self.proj, vec).view(Vec)

    def un_projection(self, vec) -> Vec:
        return np.dot(self.proj_inv, vec).view(Vec)

    def bound_line(self, vec):
        vec_proj = self.projection(vec)
        vec_proj[1] = -vec_proj[1]
        return self.un_projection(vec_proj)

    def bound_point(self, pos, vec, point):
        if point == Line.START:
            rel_pos = pos - self.s
        elif point == Line.END:
            rel_pos = pos - self.e
        else:
            raise ValueError
        proj, proj_inv = proj_matrix(rel_pos)
        vec_proj = np.dot(proj, vec)
        vec_proj[0] = -vec_proj[0]
        return np.dot(proj_inv, vec_proj).view(Vec)

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_rect(self):
        return self.x, self.y, self.w, self.h

def c_origin_collision(pos, v, r):
    vv_inv = 1 / np.dot(v, v)
    pp = np.dot(pos, pos) * vv_inv
    pv = np.dot(pos, v) * vv_inv
    rr = r * r * vv_inv
    _d = pv ** 2 - (pp - rr)
    if _d < 0:
        return 99
    _t = -pv - np.sqrt(_d)

    if _t > 1:
        return 99
    elif _t < 0:
        return 0
    return _t

def rect_collision(r1, r2):
    if r1.x < r2.x + r2.w and \
            r2.x < r1.x + r1.w and \
            r1.y < r2.y + r2.h and \
            r2.y < r1.y + r1.h:
        return True
    return False

def c_c_collision(c1, v1, c2, v2):
    rel_pos = c1.p - c2.p
    rel_v = v1 - v2
    rel_d = c1.r + c2.r

    _t = c_origin_collision(rel_pos, rel_v, rel_d)
    return _t

def c_l_collision(c, v, line):
    _x, _y = line.projection(c.p - line.s)
    _dx, _dy = line.projection(v)

    # print((_x, _y), (_dx, _dy))

    if _dx == 0:
        x_enter = -99
        x_exit = 99
    elif _dx > 0:
        x_enter = -_x / _dx
        x_exit = (line.len - _x) / _dx
    else:
        x_enter = (line.len - _x) / _dx
        x_exit = -_x / _dx

    if _dy == 0:
        y_enter = -99
        y_exit = 99
    elif _dy > 0:
        y_enter = (-c.r - _y) / _dy
        y_exit = (c.r - _y) / _dy
    else:
        y_enter = (c.r - _y) / _dy
        y_exit = (-c.r - _y) / _dy

    # print((x_enter, x_exit), (y_enter, y_exit))
    if x_enter > 1 or y_enter > 1:
        return 99
    if x_exit < 0 or y_exit < 0:
        return 99
    if x_enter > y_exit or y_enter > x_exit:
        return 99
    if x_enter < 0 and y_enter < 0:
        return 0
    return max(x_enter, y_enter)


def c_line_collision(c, v, line):
    t_s = c_origin_collision(c.p - line.s, v, c.r)
    t_e = c_origin_collision(c.p - line.e, v, c.r)
    t_l = c_l_collision(c, v, line)

    if t_s < t_l and t_s < t_e:
        return t_s, Line.START
    if t_l < t_e:
        return t_l, Line.LINE
    return t_e, Line.END






from imports import *
from collections import deque

from circle_col import *

from pygame import gfxdraw

pg.init()



WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 960
WINDOW_BG_COLOR = (43, 43, 43)
TARGET_FPS = 75
WINDOW_TITLE = 'Test'



colors = [
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
]
r = 50
circle = Circle(vector(100, 300), r)
circle_dest = Circle(vector(0, 0), r)
collided = False
circle_collide = Circle(vector(0, 0), r)
lines = [
    Line(vector(800, 700), vector(1200, 800)),
    Line(vector(500, 450), vector(400, 900)),
    Line(vector(50, 200), vector(300, 100)),
    Line(vector(900, 100), vector(700, 150)),
    Line(vector(700, 200), vector(1200, 500)),
    Line(vector(100, 600), vector(200, 500)),
    Line(vector(200, 500), vector(100, 400)),
]

bounded_vec = vector(0, 0)

mouse_pos = vector(0, 0)
keys = {
    LEFT: False,
    RIGHT: False,
    UP: False,
    DOWN: False,
}
speed = 5

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA, 32)
pg.display.set_caption(WINDOW_TITLE)
clock = pg.time.Clock()

running = True
prev_time = time.time() * 1000
dt = 1000 / TARGET_FPS
N_FRAME_TIMES = TARGET_FPS
SUM_FRAME_TIMES = 0 + 1.
frame_times = deque([0.] * N_FRAME_TIMES)
fps = 0
cnt = 0
while running:
    cnt += 1
    start_time = time.time() * 1000

    # get events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            quit()

        elif event.type == pg.KEYDOWN:
            if event.key in (pg.K_LEFT, pg.K_a):
                keys[LEFT] = True
            elif event.key in (pg.K_RIGHT, pg.K_d):
                keys[RIGHT] = True
            elif event.key in (pg.K_UP, pg.K_w):
                keys[UP] = True
            elif event.key in (pg.K_DOWN, pg.K_s):
                keys[DOWN] = True

        elif event.type == pg.KEYUP:
            if event.key in (pg.K_LEFT, pg.K_a):
                keys[LEFT] = False
            elif event.key in (pg.K_RIGHT, pg.K_d):
                keys[RIGHT] = False
            elif event.key in (pg.K_UP, pg.K_w):
                keys[UP] = False
            elif event.key in (pg.K_DOWN, pg.K_s):
                keys[DOWN] = False
    mouse_pos.x, mouse_pos.y = pg.mouse.get_pos()
    circle_dest.p = mouse_pos

    # handel events
    dx, dy = 0, 0
    if keys[LEFT]:
        dx -= speed
    if keys[RIGHT]:
        dx += speed
    if keys[UP]:
        dy -= speed
    if keys[DOWN]:
        dy += speed
    circle.p.x += dx
    circle.p.y += dy

    # update
    # r_up, r_down = arr(0, r), arr(0, -r)
    # _, proj = proj_matrix(v)
    # rel_r_up, rel_r_down = np.dot(proj, r_up), np.dot(proj, r_down)

    collided = True
    bound_pos = []
    bound_vec = []
    n_collision = 0

    pos = circle.p
    v = circle_dest.p - pos

    while collided:
        pass
        if True:
            if v.x > 0:
                area_left = pos.x - r
                area_right = (pos + v).x + r
            else:
                area_left = (pos + v).x - r
                area_right = pos.x + r
            if v.y > 0:
                area_top = (pos + v).y + r
                area_bottom = pos.y - r
            else:
                area_top = pos.y + r
                area_bottom = (pos + v).y - r
        area_rect = Rect(area_left, area_bottom, area_right - area_left, area_top - area_bottom)

        t_min = 99
        collided = False
        collided_idx = 99
        collided_type = -1
        for i, line in enumerate(lines):
            # print(circle.p, line.s, circle_dest.p, v)
            # if True:
            if rect_collision(area_rect, line.rect):
                check, c_type = c_line_collision(pos, r, v, line)
                if 0 < check < t_min:
                    t_min = check
                    collided = True
                    collided_idx = i
                    collided_type = c_type
        if collided:
            # circle_collide.p = circle.p + t_min * v
            pos = pos + t_min * v
            if collided_type == Line.LINE:
                v = lines[collided_idx].bound_line((1 - t_min) * v)
            else:
                v = lines[collided_idx].bound_point(pos, (1 - t_min) * v, collided_type)
            bound_pos.append(pos)
            bound_vec.append(v)
            n_collision += 1

    # draw
    screen.fill(WINDOW_BG_COLOR)

    # pg.draw.rect(screen, COLOR_GREY75, area_rect.get_rect(), 1)

    pg.draw.circle(screen, COLOR_CYAN, circle.p, r, 1)
    pg.draw.circle(screen, COLOR_GREEN, circle_dest.p, r, 1)
    # if collided:
    #     pg.draw.circle(screen, COLOR_MAGENTA, circle_collide.p, r, 1)
    #     pg.draw.aaline(screen, COLOR_MAGENTA, circle_collide.p, circle_collide.p + bounded_vec)
    for i in range(n_collision):
        pg.draw.circle(screen, COLOR_MAGENTA, bound_pos[i], r, 1)
        if i < n_collision - 1:
            pg.draw.aaline(screen, COLOR_MAGENTA, bound_pos[i], bound_pos[i + 1])
        else:
            pg.draw.aaline(screen, COLOR_MAGENTA, bound_pos[i], bound_pos[i] + bound_vec[i])

    for i in range(len(lines)):
        # pg.draw.rect(screen, COLOR_RED, lines[i].rect.get_rect(), 1)
        pg.draw.aaline(screen, COLOR_WHITE, lines[i].s, lines[i].e)
        # pg.draw.circle(screen, COLOR_WHITE, lines[i].s, 5)

    pg.draw.aaline(screen, COLOR_RED, circle.p, circle_dest.p)

    # pg.draw.aaline(screen, (0, 255, 127), circle.p + rel_r_up, circle_dest.p + rel_r_up)
    # pg.draw.aaline(screen, (0, 255, 127), circle.p + rel_r_down, circle_dest.p + rel_r_down)

    pg.display.flip()

    # fps
    end_time = time.time() * 1000
    frame_time = end_time - start_time
    frame_times.append(frame_time)
    SUM_FRAME_TIMES += frame_time
    SUM_FRAME_TIMES -= frame_times.popleft()
    fps = 1000 * N_FRAME_TIMES / SUM_FRAME_TIMES
    mean_frame_time = SUM_FRAME_TIMES / N_FRAME_TIMES

    if cnt % TARGET_FPS == 1:
        pg.display.set_caption(WINDOW_TITLE + ' - fps: {:.2f} ftime: {:.2f}ms'.format(fps, mean_frame_time))

    clock.tick(TARGET_FPS)
    dt = end_time - prev_time
    prev_time = end_time



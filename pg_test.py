
from imports import *
from collections import deque


pg.init()



WINDOW_WIDTH, WINDOW_HEIGHT = 960, 720
WINDOW_BG_COLOR = (43, 43, 43)
TARGET_FPS = 75
WINDOW_TITLE = 'Test'








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

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            quit()

    screen.fill(WINDOW_BG_COLOR)


    pg.display.flip()


    end_time = time.time() * 1000
    frame_time = end_time - start_time
    frame_times.append(frame_time)
    SUM_FRAME_TIMES += frame_time
    SUM_FRAME_TIMES -= frame_times.popleft()
    fps = 1000 * N_FRAME_TIMES / SUM_FRAME_TIMES

    if cnt % TARGET_FPS == 1:
        pg.display.set_caption(WINDOW_TITLE + ' - fps: {:.2f} dt: {:.2f}'.format(fps, dt))

    clock.tick(TARGET_FPS)
    dt = end_time - prev_time
    prev_time = end_time



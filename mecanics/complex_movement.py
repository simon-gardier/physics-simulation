import math
import pygame
import sys

# Constants
COLORS = {
    'background': (160, 139, 178),
    'purple': (173, 169, 183),
    'grey': (202, 202, 202),
    'black': (0, 0, 0),
    'mobile': (54, 56, 66)
}
WINDOW_SIZE = (800, 600)
WINDOW_MID = WINDOW_SIZE[0] / 2
WINDOW_RATIO = WINDOW_SIZE[1] / WINDOW_SIZE[0]
BOARD_POSITION = (100, 100)
fps = 25
TRACK_WIDTH = 40
PIXELS_PER_METER = WINDOW_SIZE[0] / TRACK_WIDTH
TRACK_HEIGHT = TRACK_WIDTH * WINDOW_RATIO
A = 0.000165
B = 0
C = -0.055
D = 0
E = 5
MOBILE_RADIUS = 25
g = -9.81

# Initialization
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Complex movement")
clock = pygame.time.Clock()
police  = pygame.font.Font('media/cmunrm.ttf', 20)
time_prev = pygame.time.get_ticks() - 10
time_now = pygame.time.get_ticks()
t = (time_now - 1) - time_prev
first_iteration = True
speed = None
δ = math.pow(10, -6)
linear_velocity        = 0
linear_velocity_max    = 0
perceived_acceleration  = 0
perceived_acceleration_min  = None
perceived_acceleration_max  = None
μ = 0.03

"""
--------Axis system-----
                                    |
                 y                  |
                 |                  |
                 |                  |
                 |                  |
-x_______________0______________x   |
-------------------------------------

"""

def window_to_track(position_f):
    if position_f[0] < WINDOW_MID:
        position_p_x = WINDOW_MID - position_f[0]
        position_p_x = -position_p_x / PIXELS_PER_METER
    else:
        position_p_x = (position_f[0] - WINDOW_MID) / PIXELS_PER_METER
    position_p_y = position_f[1] / PIXELS_PER_METER
    return position_p_x, position_p_y

def xwindow_to_track(x):
    if x < WINDOW_MID:
        position_p_x = WINDOW_MID - x
        return -position_p_x / PIXELS_PER_METER
    else:
        return (x - WINDOW_MID) / PIXELS_PER_METER

def track_to_window(position_p):
    position_f_x = (position_p[0] + TRACK_WIDTH / 2) * PIXELS_PER_METER
    position_f_y = WINDOW_SIZE[1] - position_p[1] * PIXELS_PER_METER
    return position_f_x, position_f_y

def xtrack_to_xwindow(x):
    return (x + TRACK_WIDTH / 2) * PIXELS_PER_METER

def ytrack_to_ywindow(y):
    return WINDOW_SIZE[1] - y * PIXELS_PER_METER

def track_height(x):
    return A * math.pow(x, 4) + B * math.pow(x, 3) + C * math.pow(x, 2) + D * math.pow(x, 1) + E

def draw_track():
    for xf in range(WINDOW_SIZE[0]):
        xp = xwindow_to_track(xf)
        yp = track_height(xp)
        pos = (xf, ytrack_to_ywindow(yp))
        rectangle = pygame.Rect(pos, (1, pos[1]))
        pygame.draw.rect(window, COLORS['purple'], rectangle)

def draw_mobile_charge():
    pygame.draw.circle(window, COLORS['mobile'], track_to_window(position_mobile), MOBILE_RADIUS)

def draw_board():
    actual_velocity        = "Velocity : {0:.2f} m/s".format(linear_velocity)
    actual_velocity_image  = police.render(actual_velocity, True, COLORS['black'])
    window.blit(actual_velocity_image, (100, 100))

    speed_max        = "Velocity max : {0:.2f} m/s".format(linear_velocity_max)
    speed_max_image  = police.render(speed_max, True, COLORS['black'])
    window.blit(speed_max_image, (100, 120))

    a       = "Acceleration : {0:.2f} g".format(perceived_acceleration)
    a_image = police.render(a, True, COLORS['black'])
    window.blit(a_image, (100, 140))

    a_max       = "Acceleration max : {0:.2f} g".format(perceived_acceleration_max)
    a_max_image = police.render(a_max, True, COLORS['black'])
    window.blit(a_max_image, (100, 160))

    a_min       = "Acceleration  min: {0:.2f} g".format(perceived_acceleration_min)
    a_min_image = police.render(a_min, True, COLORS['black'])
    window.blit(a_min_image, (100, 180))

#initialization
position_mobile = None
prev_data = {
    'x': None,
    'y': None,
    't': None
}
def update_position(t, g, μ):
    global speed, prev_data, first_iteration, position_mobile, linear_velocity, perceived_acceleration
    if first_iteration:
        speed = [0, 0]
        first_iteration = False
        position_mobile = (-20, track_height(-20))

    else:
        g = (0, g)
        linear_velocity = math.sqrt(speed[0] * speed[0] + speed[1] * speed[1])
        Δt  = t - prev_data['t']
        α = ((track_height(prev_data['x'] + δ)) - (track_height(prev_data['x']))) / δ
        σ = math.sqrt(1 + α * α)
        u = [1/σ, α/σ]
        if speed[0] < 0:
            u[0] *= -1
            u[1] *= -1
        v_n     = (-α/σ, 1/σ)
        v_prime = (linear_velocity * u[0], linear_velocity * u[1])
        acceleration_t = ((v_prime[0] - speed[0]) / Δt, (v_prime[1] - speed[1]) / Δt)
        acceleration_r = (-((g[0] * v_n[0]) + (g[1] * v_n[1]))*v_n[0], -((g[0] * v_n[0]) + (g[1] * v_n[1]))*v_n[1])
        a_p = (acceleration_t[0] + acceleration_r[0], acceleration_t[1] + acceleration_r[1])
        a_f = (-μ * abs(a_p[0] * v_n[0] + a_p[1] * v_n[1]) * u[0], -μ * abs(a_p[0] * v_n[0] + a_p[1] * v_n[1])* u[0])
        a   = (a_f[0] + acceleration_t[0] + g[0] + acceleration_r[0], a_f[1] + acceleration_t[1] + g[1] + acceleration_r[1]) 
        speed = (speed[0] + Δt * a[0], speed[1] + Δt * a[1])
        position_mobile = (prev_data['x'] + Δt * speed[0], prev_data['y'] + Δt * speed[1])

        vx = (position_mobile[0] - prev_data['x']) / Δt
        vy = (position_mobile[1] - prev_data['y']) / Δt

        update_stats(linear_velocity, a_p)
    
    prev_data = {
        'x': position_mobile[0],
        'y': position_mobile[1],
        't': t
    }

def update_stats(new_linear_velocity, proper_acceleration):
    global linear_velocity_max, perceived_acceleration, perceived_acceleration_max, perceived_acceleration_min
    if new_linear_velocity > linear_velocity_max:
        linear_velocity_max = new_linear_velocity
    proper_norm_acceleration = math.hypot(proper_acceleration[0], proper_acceleration[1])
    force_g = -(proper_norm_acceleration / g)
    perceived_acceleration = force_g
    if perceived_acceleration_max != None and perceived_acceleration_min != None:
        if perceived_acceleration_min > force_g:
            perceived_acceleration_min = force_g
        elif perceived_acceleration_max < force_g:
            perceived_acceleration_max = force_g
    else:
        perceived_acceleration_min = force_g
        perceived_acceleration_max = force_g

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    time_now = pygame.time.get_ticks()
    window.fill(COLORS['background'])
    draw_track()
    while  time_prev < time_now:
        t_in_seconds = time_prev / 1000
        update_position(t_in_seconds, g, μ)
        time_prev += 1
    draw_mobile_charge()
    draw_board()
    pygame.display.flip()
    clock.tick(fps)

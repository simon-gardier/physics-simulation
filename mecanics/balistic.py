import math
import pygame
import sys

### Constants

SKY_COLOR = (127, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 127, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

GRAVITY = 0.0002  # in pixels/(ms)^2

### Fonctions

def init_calculation():
    global vertical_movement_data
    #(position v,  time, speed)
    vertical_movement_data = (0, 0, 0)

def calculate_speed_acceleration(plane_height, time_now):
    global vertical_movement_data

    delta_deplacement = -(plane_height - vertical_movement_data[0])
    delta_time = time_now - vertical_movement_data[1]
    speed = delta_deplacement / delta_time
    delta_speed = speed - vertical_movement_data[2]
    acceleration = delta_speed / delta_time
    vertical_movement_data = (plane_height, time_now, speed)

    return speed, acceleration

def mrua_1d(start, time_start, acceleration, time_now): 
    #final position = position_start + 1/2g * delta_t^2
    return start + (1/2) * GRAVITY * (time_now - time_start) * (time_now - time_start)

def calculate_drop(drop_height, target_height, acceleration,
                 next_target_time, time_now):
    possible = False
    time_parcours = pow((target_height - drop_height) / (1/2 * GRAVITY), 0.5)
    if(time_parcours < (next_target_time - time_now)):
        possible = True
    drop_time = next_target_time - time_parcours
    return (possible, drop_time)

def draw_ground(time_now):
    for x in range(window_size[0]):    
        alpha = ((-x - time_now * horizontal_speed)
                 * 2.0 * math.pi / background_period)
        y = ground_height * math.exp(math.cos(alpha)) / math.e
        pygame.draw.rect(window, GREEN, ((x, window_size[1] - y),
                                         (1, y)))
    return
        
def draw_clouds(clouds, time_now):
    cloud_width = image_cloud.get_width()
    for cloud in clouds:
        x = (int(cloud[0] - time_now * horizontal_speed)
             % background_period - cloud_width)
        y = cloud[1]
        window.blit(image_cloud, (x, y))
    return

def draw_plane(altitude):
    x = (window_size[0] - image_plane.get_width()) // 2
    y = int(altitude) - image_plane.get_height() // 2
    window.blit(image_plane, (x, y))
    return

def draw_target(time_now):
    x = int(-time_now * horizontal_speed) % background_period
    pygame.draw.polygon(window, RED, ((x, window_size[1] - 45),
                                         (x, window_size[1] - 25),
                                         (x + 20, window_size[1] - 35)))
    pygame.draw.rect(window, BLACK, ((x, window_size[1] - 50), (3, 40)))
       
    return

def adjust_plane_height(y):
    global plane_height

    position_max = window_size[1] - 50 - image_plane.get_height() // 2
    
    if y > position_max:
        y = position_max

    # movement smoothing
    plane_height = (plane_height * 5.0 + y) / 6.0
    return
    
def draw_text(x, y, texte, color):
    image = police.render(texte, True, color)
    window.blit(image, (x, y))
    return

def variometer(x, y, v):
    global variometer_value

    # smoothing
    variometer_value = 0.8 * variometer_value + 0.2 * v
    
    H = 100
    L = 40
    E = 2
    
    indicator = int((variometer_value + 1.0) * H / 2.0)

    if indicator < E:
        indicator = E
    elif indicator >= H - E:
        indicator = H - E

    draw_text(x + 10, y - 20, "Vy", BLACK)
    draw_text(x - 20, y + (H - text_size) // 2, "0-", BLACK)
        
    pygame.draw.rect(window, BLACK, ((x, y), (L, H)))
    pygame.draw.rect(window, GREEN, ((x, y + H - indicator - E), (L, 2 * E)))
    
    return

def accelerometre(x, y, v):
    global accelerometer_value

    # smoothing
    GAIN = 200
    accelerometer_value = 0.8 * accelerometer_value + 0.2 * v * GAIN
    
    H = 100
    L = 40
    E = 2
    
    indicator = int((accelerometer_value + 1.0) * H / 2.0)

    if indicator < E:
        indicator = E
    elif indicator >= H - E:
        indicator = H - E

    draw_text(x + 10, y - 20, "Ay", BLACK)
    draw_text(x - 20, y + (H - text_size) // 2, "0-", BLACK)
        
    pygame.draw.rect(window, BLACK, ((x, y), (L, H)))
    pygame.draw.rect(window, RED, ((x, y + H - indicator - E), (L, 2 * E)))
    
    return

def draw_bombs(bombs):
    time_now = pygame.time.get_ticks()
    for bombe in bombs:
        position = (bombe['position_start'][0],
                    mrua_1d(bombe['position_start'][1],
                            bombe['time_start'],
                            bombe['acceleration_y'],
                            time_now))
        pygame.draw.circle(window, ORANGE, list(map(int, position)), 10)
    return    

def add_bomb(bombs, position, time_start, acceleration):
    bombs.append({'position_start': position,
                   'time_start': time_start,
                   'acceleration_y': acceleration})
    return

def filter_bombs(bombs):
    time_now = pygame.time.get_ticks()
    return list(filter(lambda x: x['time_start']
                        > time_now - 3000, bombs))

def load_automatic_drop(drop_time):
    global automatic_drop_loaded, automatic_drop_time

    if not automatic_drop_loaded:
        automatic_drop_loaded = True
        automatic_drop_time = drop_time

    return

def try_automatic_drop():
    period = background_period / horizontal_speed
    next_target_time = -window_size[0] / (2.0 * horizontal_speed)

    while next_target_time < time_now:
        next_target_time += period

    drop_possible, drop_time = calculate_drop((plane_height
                                           + offset_larguage_bombe),
                                          window_size[1],
                                          GRAVITY,
                                          next_target_time,
                                          time_now)
    if drop_possible:
        load_automatic_drop(drop_time)
    
    return

def handle_keys(key):
    if key == pygame.K_b:
        add_bomb(bombs, (window_size[0] // 2,
                               plane_height + offset_larguage_bombe),
                          time_now, GRAVITY)
    elif key == pygame.K_a:
        try_automatic_drop()
    return

### parameters

window_size = (800, 600)  # in pixels
text_size = 16  
fps = 25
horizontal_speed = 0.125  # in pixels par milliseconde
ground_height = 20

### Program

# Initialization

pygame.init()

window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Balistic")

clock = pygame.time.Clock()
police  = pygame.font.Font('media/cmunrm.ttf', text_size)
background_color = SKY_COLOR

clouds = [(0, 100), (600, 300), (200, 350)]
image_cloud = pygame.image.load('media/cloud.png').convert_alpha(window)

plane_height = window_size[1] / 2
image_plane = pygame.image.load('media/plane.png').convert_alpha(window)
offset_larguage_bombe = image_plane.get_height() // 2 - 10

background_period = window_size[0] + image_cloud.get_width()

variometer_value = 0.0
accelerometer_value = 0.0

bombs = []
automatic_drop_loaded = False
automatic_filter_time = 0

# Main loop

init_calculation()

while True:
    time_now = pygame.time.get_ticks()
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.MOUSEMOTION:
            adjust_plane_height(evenement.pos[1])
        elif evenement.type == pygame.KEYDOWN:
            handle_keys(evenement.key)

    speed_v, acceleration_v = calculate_speed_acceleration(plane_height,
                                                              time_now)

    if automatic_drop_loaded and automatic_drop_time <= time_now:
        add_bomb(bombs, (window_size[0] // 2,
                               plane_height + offset_larguage_bombe),
                      time_now, GRAVITY)
        automatic_drop_loaded = False

    window.fill(background_color)
    draw_clouds(clouds, time_now)
    draw_bombs(bombs)
    draw_ground(time_now)
    draw_target(time_now)
    draw_plane(plane_height)

    variometer(window_size[0] // 20, window_size[1] // 10,
               speed_v)
    
    accelerometre(window_size[0] * 3 // 20, window_size[1] // 10,
                  acceleration_v)

    if automatic_drop_loaded:
        draw_text(window_size[0] // 20,
                       3 * window_size[1] // 10,
                       "Armed", BLACK)

    bombs = filter_bombs(bombs)

    pygame.display.flip()
    clock.tick(fps)
 

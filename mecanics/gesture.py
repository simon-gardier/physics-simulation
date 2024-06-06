import math
import pygame
import sys

### Constants

OBJECT_COLOR = (54, 56, 66)
BACKGROUND_COLOR = (160, 139, 178)
BLACK = (0, 0, 0)
RED = (210, 0, 0)
GREEN = (0, 210, 0)

A = 2
B = 5
C = 20

def move_pol(point, distance, orientation):
    x, y = point
    x_vector = math.cos(orientation) * distance
    y_vector = math.sin(orientation) * distance
    x += x_vector
    y += y_vector
    return (x , y)

def draw_vector(window, color, origin, vector):
    
    polygon = []
    norm_vector = math.hypot(vector[0],vector[1])
    alpha = math.atan2(vector[1], vector[0])
    p = origin
    if norm_vector >= C:
        p4 = (p[0] + vector[0], p[1] + vector[1])
        p1 = move_pol(p,  A, alpha - (math.pi / 2))
        p7 = move_pol(p, -A, alpha - (math.pi / 2))
        p2 = move_pol(p1, norm_vector - C, alpha)
        p6 = move_pol(p7, norm_vector - C, alpha)
        #signe inverse
        p3 = move_pol(p2, B, alpha + (math.pi / 2))
        p5 = move_pol(p6, B, alpha - (math.pi / 2))
        polygon = [p1, p2, p3, p4, p5, p6, p7]
    else :
        p3 = (p[0] + vector[0], p[1] + vector[1])
        p1 = move_pol(p3, C, alpha + math.pi)   
        p2 = move_pol(p1, A+B, alpha - (math.pi / 2))
        p4 = move_pol(p1, A+B, alpha + (math.pi / 2))
        polygon = [p1, p2, p3, p4]
    pygame.draw.polygon(window, color, polygon)

    return

def init_calculation():
    global movement_data
    movement_data = (0, # position x 
                     0, # position y 
                     0, # speed x 
                     0, # speed y 
                     0) # time 

def calculate_velocity_acceleration_2d(position, time_now):
    global movement_data
    delta_deplacement_x = position[0] - movement_data[0]
    delta_deplacement_y = position[1] - movement_data[1]

    delta_time = time_now - movement_data[4]

    speed_x = delta_deplacement_x / delta_time
    speed_y = delta_deplacement_y / delta_time

    delta_speed_x = speed_x - movement_data[2]
    delta_speed_y = speed_y - movement_data[3]

    acceleration_x = delta_speed_x / delta_time
    acceleration_y = delta_speed_y / delta_time

    movement_data = (position[0], position[1], speed_x, speed_y, time_now)
    return (speed_x, speed_y), (acceleration_x, acceleration_y)

def gesture_detection(speed, acceleration):
    VELOCITY_TOLERANCE = 0.2
    MINIMUM_ACCELERATION = 0.002

    velocity_norm = math.sqrt(speed[0]**2 + speed[1]**2)
    acceleration_norm = math.sqrt(acceleration[0]**2 + acceleration[1]**2)
    angle = math.atan2(acceleration[1], acceleration[0]) * 180 / math.pi

    if velocity_norm > VELOCITY_TOLERANCE and acceleration_norm >= MINIMUM_ACCELERATION and speed[1] > 0 and angle <= -80 and angle >= -100: 
        print("true")
        return True
    return False

def display_counter():
    image = police.render(str(counter), True, BLACK)
    window.blit(image, (50, 50))
    return

def smoothing(v, prev_v, coefficient):
    return (prev_v[0] * coefficient + v[0] * (1.0 - coefficient),
            prev_v[1] * coefficient + v[1] * (1.0 - coefficient))

def handle_move(position):
    global first_move, prev_position, prev_acceleration
    global counter, last_detection

    if first_move:
        first_move = False
    else:
        x, y = position

        position = smoothing(position, prev_position,
                           position_smoothing)

        t = pygame.time.get_ticks()
        v, a = calculate_velocity_acceleration_2d(position, t)

        a = smoothing(a, prev_acceleration, acceleration_smoothing)
        prev_acceleration = a

        if gesture_detection(v, a) and t > last_detection + 500:
            counter += 1
            last_detection = t
            
        window.fill(background_color)

        display_counter()
        
        pygame.draw.circle(window, OBJECT_COLOR,
                           (int(position[0]), int(position[1])), 20)

        if must_display_speed:
            draw_vector(window, RED, position,
                             (int(v[0] * velocity_factor),
                              int(v[1] * velocity_factor)))

        if must_display_acceleration:
            draw_vector(window, GREEN, position,
                             (int(a[0] * acceleration_factor),
                              int(a[1] * acceleration_factor)))
            
        pygame.display.flip()

    prev_position = position        
    return

### Paramètre(s)

window_size = (800, 600)  # in pixels
fps = 25

background_color = BACKGROUND_COLOR

position_smoothing = 0.7
acceleration_smoothing = 0.5
velocity_factor = 200
acceleration_factor = 40000

### program

# Initialization

pygame.init()

window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Vertical gesture detection");

clock = pygame.time.Clock()
police  = pygame.font.Font('media/cmunrm.ttf', 36)

first_move = True

prev_acceleration = (0.0, 0.0)

must_display_speed = True
must_display_acceleration = True

counter = 0

last_detection = -1000

window.fill(background_color)
pygame.display.flip()

# main loop
init_calculation()

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit();
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_a:
                must_display_acceleration = not must_display_acceleration
            elif evenement.key == pygame.K_v:
                must_display_speed = not must_display_speed

    handle_move(pygame.mouse.get_pos())        
    clock.tick(fps)

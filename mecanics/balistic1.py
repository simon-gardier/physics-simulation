import math
import pygame
import sys

### Constants

SKY_COLOR = (127, 191, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 192, 0)
RED = (255, 0, 0)

### Fonctions
                                       
def mua_2d(start, time_start, initial_velocity, acceleration_y, time_now):
    delta_t = time_now - time_start
    final_x = start[0] + delta_t * initial_velocity[0]
    final_y = start[1] + delta_t * initial_velocity[1] + 1/2 * acceleration_y * delta_t**2
    return (final_x, final_y)

def calculate_velocity(start, angle, target, acceleration_y):
    delta_x = target[0] - start[0]
    delta_y = target[1] - start[1]
    a = 2 * (math.cos(angle) ** 2)
    b = delta_y - math.tan(angle) * delta_x
    if(b > 0):
        dividend = a * b
        divisor  = (delta_x ** 2) * acceleration_y
        speed_0 = math.sqrt((divisor / dividend))
        return(True, speed_0)
    return (False, 0)
    
def calculate_impact(start, angle, ground_height, speed,
                    acceleration_y):
    delta_y = ground_height - start[1] 
    speed_y = speed * math.sin(angle)
    speed_x = speed * math.cos(angle)
    delta = (speed_y * speed_y) + (2 * delta_y * acceleration_y)
    
    if delta >= 0 :
        if delta == 0 :
            delta_time = ( -speed_y / acceleration_y)
        else :
            delta_time1 = ((-speed_y + math.sqrt(delta)) / acceleration_y )
            delta_time2 = ((-speed_y - math.sqrt(delta)) / acceleration_y )
            if delta_time1 > 0 :
                delta_time = delta_time1
            else :
                delta_time = delta_time2
    x_impact = speed_x * delta_time + start[0]
    return x_impact

def draw_canon():
    p1 = (position_canon[0]
          + CANON_RADIUS * math.cos(angle_canon + math.pi/2),
          position_canon[1]
          + CANON_RADIUS * math.sin(angle_canon + math.pi/2))
    p4 = (position_canon[0]
          + CANON_RADIUS * math.cos(angle_canon - math.pi/2),
          position_canon[1]
          + CANON_RADIUS * math.sin(angle_canon - math.pi/2))
    pp = (LONGUEUR_CANON * math.cos(angle_canon),
          LONGUEUR_CANON * math.sin(angle_canon))
    p2 = (p1[0] + pp[0], p1[1] + pp[1])
    p3 = (p4[0] + pp[0], p4[1] + pp[1])
    pygame.draw.polygon(window, ORANGE, [p1, p2, p3, p4])
    pygame.draw.circle(window, YELLOW, position_canon,
                       CANON_DISK_RADIUS)

    if automatic_speed:
        color_indicator = RED
    else:
        color_indicator = ORANGE
        
    pygame.draw.rect(window, background_color,
                     ((position_canon[0] - INDICATOR_WIDTH // 2,
                       position_canon[1] + INDICATOR_OFFSET),
                      (INDICATOR_WIDTH, INDICATOR_HEIGHT)))
    pygame.draw.rect(window, color_indicator,
                     ((position_canon[0] - INDICATOR_WIDTH // 2,
                       position_canon[1] + INDICATOR_OFFSET),
                      (INDICATOR_WIDTH, INDICATOR_HEIGHT)), 4)

    if fire_velocity > MAX_VELOCITY:
        v = MAX_VELOCITY
    elif fire_velocity < MIN_VELOCITY:
        v = MIN_VELOCITY
    else:
        v = fire_velocity
        
    y = int((v - MIN_VELOCITY) * INDICATOR_HEIGHT
            / (MAX_VELOCITY - MIN_VELOCITY))

    pygame.draw.rect(window, color_indicator,
                     ((position_canon[0] - INDICATOR_WIDTH // 2,
                       position_canon[1] + INDICATOR_OFFSET
                       + INDICATOR_HEIGHT - y),
                      (INDICATOR_WIDTH, y)))
    
    return

def add_projectile():
    projectiles.append({'position_start': position_canon,
                        'time_start': pygame.time.get_ticks(),
                        'initial_velocity':
                        (fire_velocity * math.cos(angle_canon),
                         fire_velocity * math.sin(angle_canon))})
    return

def draw_target():
    if not target_present:
        return
    
    pygame.draw.circle(window, RED, position_target, TARGET_RADIUS, 5)
    pygame.draw.rect(window, RED, ((position_target[0] - 1,
                                       position_target[1] - TARGET_RADIUS),
                                      (2, 2 * TARGET_RADIUS)))
    pygame.draw.rect(window, RED, ((position_target[0] - TARGET_RADIUS,
                                       position_target[1] - 1),
                                      (2 * TARGET_RADIUS, 2)))
    return
    
def draw_projectile():
    time_now = pygame.time.get_ticks()
    for projectile in projectiles:
        position = mua_2d(projectile['position_start'],
                          projectile['time_start'],
                          projectile['initial_velocity'],
                          GRAVITY,
                          time_now)
        pygame.draw.circle(window, BLACK, list(map(int, position)), 8)
    return

def draw_impact():
    x = position_impact
    pygame.draw.polygon(window, RED, ((x, window_size[1] - 35),
                                         (x, window_size[1] - 15),
                                         (x + 20, window_size[1] - 25)))
    pygame.draw.rect(window, BLACK, ((x, window_size[1] - 40), (3, 40)))
    return

def handle_button(evenement):
    global position_target, target_present, automatic_speed
    if evenement.button == 1:
        add_projectile()
    elif evenement.button == 3:
        position_target = evenement.pos
        target_present = True
        automatic_speed = False
    return    

def handle_keys(key):
    global angle_canon, fire_velocity, target_present, automatic_speed
    global position_impact
    if key == pygame.K_RIGHT:
        angle_canon += ANGLE_INCREMENT
        automatic_speed = False
        if angle_canon > MAX_ANGLE_CANON:
            angle_canon = MAX_ANGLE_CANON
    elif key == pygame.K_LEFT:
        angle_canon -= ANGLE_INCREMENT
        automatic_speed = False
        if angle_canon < MIN_ANGLE_CANON:
            angle_canon = MIN_ANGLE_CANON
    elif key == pygame.K_UP:
        if fire_velocity < MIN_VELOCITY:
            fire_velocity = MIN_VELOCITY
        fire_velocity += VELOCITY_INCREMENT
        automatic_speed = False
        if fire_velocity > MAX_VELOCITY:
           fire_velocity = MAX_VELOCITY
    elif key == pygame.K_DOWN:
        if fire_velocity > MAX_VELOCITY:
            fire_velocity = MAX_VELOCITY
        fire_velocity -= VELOCITY_INCREMENT
        automatic_speed = False
        if fire_velocity < MIN_VELOCITY:
           fire_velocity = MIN_VELOCITY
    elif key == pygame.K_a:
        if target_present:
            ok, v = calculate_velocity(position_canon, angle_canon,
                                     position_target, GRAVITY)
            if ok:
                fire_velocity = v
                automatic_speed = True
                position_impact = calculate_impact(position_canon, angle_canon,
                                                  window_size[1], v,
                                                  GRAVITY)
                
    elif key == pygame.K_c:
        target_present = False
    return

def filter_projectiles(projectiles):
    time_now = pygame.time.get_ticks()
    return list(filter(lambda x: x['time_start']
                        > time_now - 4000, projectiles))

### parameters

CANON_DISK_RADIUS = 20
CANON_RADIUS = 8
LONGUEUR_CANON = 35

INDICATOR_WIDTH = 25
INDICATOR_HEIGHT = 75
INDICATOR_OFFSET = 50

MIN_VELOCITY = 0.4
MAX_VELOCITY = 1.5
VELOCITY_INCREMENT = 0.05

TARGET_RADIUS = 15

ANGLE_INCREMENT = math.pi / 50
MAX_ANGLE_CANON = math.pi / 2 - 0.1
MIN_ANGLE_CANON = -math.pi / 2 + 0.1

GRAVITY = 0.001

window_size = (800, 600)  # in pixels
fps = 25

background_color = SKY_COLOR
position_canon = (50, 450)
angle_canon = -math.pi / 4

position_target = (-100, -100)
target_present = False
fire_velocity = 0.8
automatic_speed = False

### Program

# Initialization

pygame.init()

window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Balistic canon");

clock = pygame.time.Clock()

pygame.key.set_repeat(10, 10)

projectiles = []

# Main loop

while True:
    time_now = pygame.time.get_ticks()
  
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            handle_button(evenement)
        elif evenement.type == pygame.KEYDOWN:
            handle_keys(evenement.key)

    window.fill(background_color)

    if automatic_speed:
        draw_impact()
    
    draw_target()
    draw_projectile()
    draw_canon()

    projectiles = filter_projectiles(projectiles)
  
    pygame.display.flip()
    clock.tick(fps)

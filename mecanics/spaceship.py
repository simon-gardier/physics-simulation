import math, os
import pygame

BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PLANET_COLOR = (157, 164, 165)
BACKGROUND_COLOR = BLACK

WINDOW_SIZE = (800, 600)
MARGIN = 100
fps = 25

# CONSTANTS SPACESHIP
NOZZLE_COLOR = ORANGE
FLAMMES_COLOR = YELLOW

SPACESHIP_RADIUS = 15
NOZZLE_RADIUS = 23
FLAMMES_RADIUS = 38

SPACESHIP_MASS = 1
THRUST = 0.0003
BURN_TIME = 3

ANGLE_B = math.pi / 7
ANGLE_B_FLAMMES = math.pi / 30
# END CONSTANTS SPACESHIP


# CONSTANTS PLANET
PLANET_RADIUS = 40
PLANET_COLOR = PLANET_COLOR
PLANET_MASS = 1600
# our planet
GRAVITATION = 0.001
# END CONSTANTS PLANET


RIGHT_KEY = pygame.K_RIGHT
LEFT_KEY = pygame.K_LEFT
UP_KEY = pygame.K_UP
DOWN_KEY = pygame.K_DOWN
QUIT_KEY = pygame.K_q

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Spaceship")
pygame.key.set_repeat(10, 10)
clock = pygame.time.Clock()
finished = False

spaceship_position = [WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2]
spaceship_orientation = 0
thrusters_counter = 0
prev_data = {'position': spaceship_position,
            'speed': (0, 0),
            'time': pygame.time.get_ticks()}

planet_position = [0, 0]
planet_is_present = False


def draw_spaceship():
    if thrusters_counter >= 1:
        draw_triangle(FLAMMES_COLOR, spaceship_position, FLAMMES_RADIUS,
                          spaceship_orientation + ((21 * math.pi) / 20), ANGLE_B_FLAMMES)
        draw_triangle(FLAMMES_COLOR, spaceship_position, FLAMMES_RADIUS,
                          spaceship_orientation + ((19 * math.pi) / 20), ANGLE_B_FLAMMES)

    draw_triangle(NOZZLE_COLOR, spaceship_position, NOZZLE_RADIUS, spaceship_orientation + math.pi, ANGLE_B)
    pygame.draw.circle(window, (54, 56, 66), (int(spaceship_position[0]), int(spaceship_position[1])), SPACESHIP_RADIUS)


def draw_triangle(color, p, r, a, b):
    p1 = (p[0] + r * math.cos(a + b),
          p[1] + r * math.sin(a + b))
    p2 = (p[0] + r * math.cos(a - b),
          p[1] + r * math.sin(a - b))
    pygame.draw.polygon(window, color, ((int(p[0]), int(p[1])), (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1]))))


def draw_planet():
    if planet_is_present:
        pygame.draw.circle(window, PLANET_COLOR, planet_position, PLANET_RADIUS)


def handle_keys():
    global finished, thrusters_counter

    keys = pygame.key.get_pressed()
    if keys[RIGHT_KEY]:
        update_orientation(math.pi / 20)
    if keys[LEFT_KEY]:
        update_orientation(-math.pi / 20)
    if keys[UP_KEY]:
        thrusters_counter = BURN_TIME
    if keys[QUIT_KEY]:
        print("finished")
        finished = True


def handle_button():
    global planet_position, planet_is_present, finished
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                planet_position = pygame.mouse.get_pos()
                planet_is_present = True
            elif event.button == 3:
                planet_is_present = False
        if event.type == pygame.QUIT: 
            finished = True


def update_orientation(orientation):
    global spaceship_orientation
    spaceship_orientation += orientation


def vectorized_distance(position1, position2):
    distance_x = position1[0] - position2[0]
    distance_y = position1[1] - position2[1]
    return (distance_x, distance_y)


def distance_coords(position1, position2):
    vector_distance = vectorized_distance(position1, position2)
    distance = math.sqrt(vector_distance[0] * vector_distance[0] + vector_distance[1] * vector_distance[1])
    return distance


def update_position(position, time_now, mass, force, orientation, mass_planete, coordonnees_planete):
    global prev_data

    distance_X_Y_planet_spaceship = vectorized_distance(position, coordonnees_planete)
    angle_planet_spaceship = math.atan2(distance_X_Y_planet_spaceship[1], distance_X_Y_planet_spaceship[0])
    distance_planet_spaceship = distance_coords(position, coordonnees_planete)
    gravite = -GRAVITATION * ((mass * mass_planete) / (distance_planet_spaceship * distance_planet_spaceship))

    #gravity tuple
    gravity_force = (gravite * math.cos(angle_planet_spaceship), gravite * math.sin(angle_planet_spaceship))
    motor_force = (force * math.cos(orientation), force * math.sin(orientation))

    acceleration_x = (motor_force[0] + gravity_force[0]) / mass
    acceleration_y = (motor_force[1] + gravity_force[1]) / mass

    delta_time = time_now - prev_data['time']

    speed_x = prev_data['speed'][0] + acceleration_x * delta_time
    speed_y = prev_data['speed'][1] + acceleration_y * delta_time

    position_x = prev_data['position'][0] + speed_x * delta_time
    position_y = prev_data['position'][1] + speed_y * delta_time

    if position_x > WINDOW_SIZE[0] + MARGIN:
        position_x = -MARGIN
    elif position_x < -MARGIN:
        position_x = WINDOW_SIZE[0] + MARGIN

    if position_y > WINDOW_SIZE[1] + MARGIN:
        position_y = -MARGIN
    elif position_y < -MARGIN:
        position_y = WINDOW_SIZE[1] + MARGIN

    prev_data = {'position': (position_x, position_y),
                           'speed': (speed_x, speed_y),
                           'time': time_now}

    return (position_x, position_y)


def in_collisions():
    in_collision = False
    distance = distance_coords(spaceship_position, planet_position)
    if (distance <= SPACESHIP_RADIUS + PLANET_RADIUS):
        in_collision = True
    return in_collision


while not finished:
    handle_button()
    handle_keys()
    if (in_collisions()):
        finished = True

    window.fill(BLACK)

    draw_planet()

    draw_spaceship()

    if thrusters_counter >= 1:
        thrusters_counter -= 1
        force = THRUST
    else:
        force = 0

    if (planet_is_present):
        spaceship_position = update_position(spaceship_position, pygame.time.get_ticks(), SPACESHIP_MASS, force,
                                                   spaceship_orientation, PLANET_MASS, planet_position)
    else:
        spaceship_position = update_position(spaceship_position, pygame.time.get_ticks(), SPACESHIP_MASS, force,
                                                   spaceship_orientation, 0, planet_position)
    pygame.display.flip()
    clock.tick(fps)

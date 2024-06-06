import math
import sys
import pygame


# Constants
BACKGROUND_COLOR = (127, 191, 255)
OBJECT_COLOR = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAUVE = (255, 0, 255)
K = 8.9876 * math.pow(10, 9)
MARGIN = 50
THRESHOLD = 20
NULL_NORM = math.pow(10, -10)
VECTORS_LENGTH = 40

A = 2
B = 10
C = 20

# Parameters
window_size = (1600, 900)  # in pixels
fps = 25
Cercle_radius = 10


# Functions
def add_obj(x, y, q):
    objects.append((x, y, q))


def remove_object(x, y):
    for object in objects:
        dist = math.hypot(abs(x - object[0]), abs(y - object[1]))
        if dist <= Cercle_radius:
            objects.remove(object)


def calculate_field(x, y):
    fields = [0, 0]
    for object in objects:
        vector = [0, 0]
        distance_x = abs(object[0] - x)
        distance_y = abs(object[1] - y)
        r = math.hypot(distance_x, distance_y)
        if (r <= THRESHOLD):
            return None
        norm = (K * abs(object[2])) / (r * r)
        α = math.atan2(y - object[1], x - object[0])
        if object[2] > 0:
            vector = [math.cos(α) * norm, math.sin(α) * norm]
        else:
            vector = [math.cos(α) * -norm, math.sin(α) * -norm]
        fields[0] += vector[0]
        fields[1] += vector[1]
    return fields


def move_pol(point, distance, orientation):
    x, y = point
    x_vector = math.cos(orientation) * distance
    y_vector = math.sin(orientation) * distance
    x += x_vector
    y += y_vector
    return (x, y)


def draw_vector(origin, vector, color):
    polygon = []
    norm_vector = math.hypot(vector[0], vector[1])
    α = math.atan2(vector[1], vector[0])
    p = origin
    if norm_vector > C:
        p4 = (p[0] + vector[0], p[1] + vector[1])
        p1 = move_pol(p, A, α - (math.pi / 2))
        p7 = move_pol(p, -A, α - (math.pi / 2))
        p2 = move_pol(p1, norm_vector - C, α)
        p6 = move_pol(p7, norm_vector - C, α)
        p3 = move_pol(p2, B, α + (math.pi / 2))
        p5 = move_pol(p6, B, α - (math.pi / 2))
        polygon = [p1, p2, p3, p4, p5, p6, p7]
    else:
        p3 = (p[0] + vector[0], p[1] + vector[1])
        p1 = move_pol(p3, C, α + math.pi)
        p2 = move_pol(p1, A + B, α - (math.pi / 2))
        p4 = move_pol(p1, A + B, α + (math.pi / 2))
        polygon = [p1, p2, p3, p4]
    pygame.draw.polygon(window, color, polygon)


def draw_objects():
    global objects
    for object in objects:
        if (object[2] < 0):
            pygame.draw.circle(
                window, BLACK, (object[0], object[1]), Cercle_radius)
        else:
            pygame.draw.circle(
                window, RED, (object[0], object[1]), Cercle_radius)


def coloration(v):
    if 0 <= v and v <= 8:
        return (255, 255 * v / 8, 0)
    if v <= 16:
        return (-31.875 * v + 510, 255, 31.875 * v - 255)
    if v <= 24:
        return (0, -31.875 * v + 765, 255)
    if v <= 32:
        return (31.875 * v - 765, 0, 255)
    return (255, 0, 255)


def draw_field():
    for y in range(-MARGIN, window_size[1] + MARGIN, 50):
        for x in range(-MARGIN, window_size[0] + MARGIN, 50):
            position = (x, y)
            e = calculate_field(position[0], position[1])
            if e is not None:
                norm_e = math.hypot(e[0], e[1])
                if norm_e > NULL_NORM:
                    ratio = VECTORS_LENGTH / norm_e
                    e_prime = (e[0] * ratio, e[1] * ratio)
                    norm_e_prime = math.hypot(e_prime[0], e_prime[1])
                    orientation = math.atan2(e[1], e[0])
                    position = move_pol(
                        position, -(norm_e_prime / 2), orientation)
                    v = math.sqrt(1000 * abs(norm_e))
                    draw_vector(position, e_prime, coloration(v))


# Initialization
pygame.init()
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Electrical field visualization")

clock = pygame.time.Clock()
background_color = BACKGROUND_COLOR
objects = []

add_obj(800, 200, math.pow(10, -6))
add_obj(800, 700, -1 * math.pow(10, -6))

window.fill(background_color)

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1:
                add_obj(int(evenement.pos[0]), int(
                    evenement.pos[1]), math.pow(10, -7))
            elif evenement.button == 3:
                add_obj(int(evenement.pos[0]), int(
                    evenement.pos[1]), -math.pow(10, -7))
            elif evenement.button == 2:
                remove_object(evenement.pos[0], evenement.pos[1])

    window.fill(background_color)
    draw_objects()
    draw_field()
    pygame.display.flip()
    clock.tick(fps)

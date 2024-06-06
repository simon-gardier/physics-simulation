import math
import sys
import pygame

# Graphics Constants
COLORS = {
    "blue":(0, 0, 255),
    "black":(0, 0, 0),
    "red":(255, 0, 0),
    "purple":(255, 0, 255),
    "grey":(202, 202, 202),
    "background" : (127, 191, 255)
}
WINDOW_SIZE = (1600, 900)
fps = 25

# Physics constants
K = 8.9876 * math.pow(10, 9)
THRESHOLD_DISTANCE_CHARGE_POINT = 20
CHARGE = 10 ** -7

# Charges ((objets, fixed) + mobile charge) constants 
CIRCLE_RADIUS = 10 

# Mobile charge constants
CHARGE_MOBILE = 10 ** -7
MOBILE_CIRCLE_DIAMETER = 4
MOBILE_MASS = 10 ** -10

# Parameters
mouse = {
    "potential" : 0,
    "x": 0,
    "y": 0
}
mobile = {
    "is_present" : False,
    "mass" : MOBILE_MASS,
    "charge" : 0,
    "x" : 0,
    "y" : 0,
    "vx" : 0,
    "vy" : 0,
    "potential_energy" : 0,
    "kinetic_energy" : 0
}
prev_data = {
    "x":None,
    "y":None,
    "vx":None,
    "vy":None,
    "t":None
}


# Functions
def add_obj(x, y, q):
    objects.append((x, y, q))


def remove_object(x, y):
    for object in objects:
        dist = math.hypot(abs(x - object[0]), abs(y - object[1]))
        if dist <= CIRCLE_RADIUS:
            objects.remove(object)


def draw_objects():
    global objects
    for object in objects:
        if (object[2] < 0):
            pygame.draw.circle(window, COLORS["black"], (object[0], object[1]), CIRCLE_RADIUS)
        else:
            pygame.draw.circle(window, COLORS["red"], (object[0], object[1]), CIRCLE_RADIUS)


def draw_mobile_charge():
    if mobile["charge"] > 0:
        color_mobile = COLORS['red']
    elif mobile["charge"] < 0:
        color_mobile = COLORS['black']
    pygame.draw.circle(window, color_mobile, (int(mobile["x"]), int(mobile["y"])), CIRCLE_RADIUS, MOBILE_CIRCLE_DIAMETER)

def draw_board():
    chaine_potential_energy = "Potential energy : {0:.2f} µJ".format(mobile["potential_energy"] * (10 ** 6))
    potential_energy_image = police.render(chaine_potential_energy, True, COLORS["black"])
    window.blit(potential_energy_image, (100, 100))

    chaine_kinetic_energy = "Kinetic energy : {0:.2f} µJ".format(mobile["kinetic_energy"] * (10 ** 6))
    kinetic_energy_image = police.render(chaine_kinetic_energy, True, COLORS["black"])
    window.blit(kinetic_energy_image, (100, 120))

    chaine_energie_totale = "Total energy : {0:.2f} µJ".format((mobile["potential_energy"] + mobile["kinetic_energy"]) * (10 ** 6))
    energie_totale_image = police.render(chaine_energie_totale, True, COLORS["black"])
    window.blit(energie_totale_image, (100, 140))

    chaine_potentiel_mouse = "Mouse potential : {0:.2f} µJ".format(mouse["potential"])
    potentiel_mouse_image = police.render(chaine_potentiel_mouse, True, COLORS["black"])
    window.blit(potentiel_mouse_image, (100, 160))

def calculate_field(x, y):
    fields = [0, 0]
    for object in objects:
        vector = [0, 0]
        distance_x = abs(object[0] - x)
        distance_y = abs(object[1] - y)
        r = math.hypot(distance_x, distance_y)
        if (r <= THRESHOLD_DISTANCE_CHARGE_POINT):
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


def calculate_potential_energy(x, y, charge):
    potential_energy = 0
    for object in objects:
        distance_x = abs(object[0] - x)
        distance_y = abs(object[1] - y)
        r = math.hypot(distance_x, distance_y)
        potential_energy += (K * object[2] * charge) / r
    return potential_energy


def calculate_potential(x, y):
    electric_potential = 0
    for object in objects:
        distance_x = abs(object[0] - x)
        distance_y = abs(object[1] - y)
        r = math.hypot(distance_x, distance_y)
        if r <-1 or r > 1:
            electric_potential += (K * object[2]) / r
    distance_x = mobile["x"] - x
    distance_y = mobile["y"] - y
    r = math.hypot(distance_x, distance_y)
    if r <-1 or r > 1:
        electric_potential += (K * mobile["charge"]) / r
    return electric_potential


def update_moving_charge(t):
    global mobile, first_iteration, prev_data
    champ = calculate_field(mobile["x"], mobile["y"])
    if not champ:
        mobile["is_present"] = False
    else:
        if not first_iteration:
            Δt  = t - prev_data["t"]
            force_coulomb_x = mobile["charge"] * champ[0]
            force_coulomb_y = mobile["charge"] * champ[1]

            acceleration_mobile_x = force_coulomb_x / mobile["mass"]
            acceleration_mobile_y = force_coulomb_y / mobile["mass"]

            mobile["vx"] = acceleration_mobile_x * Δt + prev_data["vx"]
            mobile["vy"] = acceleration_mobile_y * Δt + prev_data["vy"]

            mobile["x"] = prev_data["x"] + mobile["vx"] * Δt
            mobile["y"] = prev_data["y"] + mobile["vy"] * Δt
        else:
            first_iteration = False
    prev_data = {
        "x" : mobile["x"],
        "y" : mobile["y"],
        "vx" : mobile["vx"],
        "vy" : mobile["vy"],
        "t" : t
    }


# Initialization
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Mobile electric charges")
clock = pygame.time.Clock()
window.fill(COLORS['background'])
police = pygame.font.Font('media/cmunrm.ttf', 20)
objects = []
time_prev = pygame.time.get_ticks() - 10
time_now = pygame.time.get_ticks()
first_iteration = True
#add fixed charges
add_obj(800, 200, math.pow(10, -6))
add_obj(800, 700, -1 * math.pow(10, -6))

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_p or evenement.key == pygame.K_n:
                first_iteration = True
                mobile["x"], mobile["y"] = pygame.mouse.get_pos()
                mobile["is_present"] = True
                mobile["vx"] = 0
                mobile["vy"] = 0
                mobile["potential_energy"] = 0
                mobile["kinetic_energy"] = 0
                if evenement.key == pygame.K_p:
                    mobile["charge"] = CHARGE_MOBILE
                else :
                    mobile["charge"] = -CHARGE_MOBILE
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1:
                add_obj(int(evenement.pos[0]), int(evenement.pos[1]), CHARGE)
            elif evenement.button == 3:
                add_obj(int(evenement.pos[0]), int(evenement.pos[1]), -CHARGE)
            elif evenement.button == 2:
                remove_object(evenement.pos[0], evenement.pos[1])
    window.fill(COLORS['background'])
    draw_objects()
    time_now = pygame.time.get_ticks()
    while time_prev < time_now:
        t_secondes = time_prev / 1000
        if mobile["is_present"]:
            update_moving_charge(t_secondes)
        time_prev += 1
    if mobile["is_present"]:
        draw_mobile_charge()
        mobile["potential_energy"] = calculate_potential_energy(mobile["x"], mobile["y"], mobile["charge"])
        mobile["kinetic_energy"] = 1 / 2 * mobile["mass"] * ((math.hypot(mobile["vx"], mobile["vy"])) ** 2)
        mouse["x"], mouse["y"] = pygame.mouse.get_pos()
        mouse["potential"] = calculate_potential(mouse["x"], mouse["y"])
        draw_board()
    pygame.display.flip()
    clock.tick(fps)

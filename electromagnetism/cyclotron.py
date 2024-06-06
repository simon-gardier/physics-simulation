import math
import sys
import pygame

# Graphics Constants
COLORS = {
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "purple": (255, 0, 255),
    "grey": (202, 202, 202),
    "background": (160, 139, 178)
}
WINDOW_SIZE = (1600, 900)
fps = 25
INTERVALLE_CHAMP = {
    "min": -100,
    "max": 100
}

# Trace
TRACE_SIZE = 1000
trace = [None] * TRACE_SIZE
nb_trace = 0
next_trace = 0

# Physics constants
electrical_field_v = 10
magnetic_field = 1.00
max_field = 1
min_field = -1
mode_cyclotron = False
alpha =0

# Constants charge
CIRCLE_RADIUS = 10
CHARGE_MOBILE = 10 ** -10
MOBILE_CIRCLE_DIAMETER = 4
MOBILE_MASS = 10 ** -10

# Initialization
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Cyclotron")
clock = pygame.time.Clock()
window.fill(COLORS['background'])
police = pygame.font.Font('media/cmunrm.ttf', 20)
objects = []
time_prev = pygame.time.get_ticks() - 10
time_now = pygame.time.get_ticks()
first_iteration = True
pygame.key.set_repeat(100, 100)

# Parameters
mobile = {
    "is_present": True,
    "mass": MOBILE_MASS,
    "charge": CHARGE_MOBILE,
    "x": WINDOW_SIZE[0] // 2,
    "y": WINDOW_SIZE[1] // 2,
    "vx": 0,
    "vy": 0,
    "kinetic_energy": 0
}

prev_data = {
    "x": None,
    "y": None,
    "vx": None,
    "vy": None,
    "t": pygame.time.get_ticks() / 1000
}

def initialization_trace():
    global next_trace, nb_trace
    trace = []
    next_trace = 0
    nb_trace = 0


def add_trace(position_mobile):
    global nb_trace, next_trace
    if nb_trace < TRACE_SIZE:
        nb_trace += 1
    trace[next_trace] = position_mobile
    next_trace = (next_trace + 1) % TRACE_SIZE


def draw_trace():
    for i in range(nb_trace):
        pygame.draw.circle(window, COLORS["grey"], (trace[i][0], trace[i][1]), 1, 1)


def draw_mobile_charge():
    if mobile["charge"] > 0:
        color_mobile = COLORS['red']
    elif mobile["charge"] < 0:
        color_mobile = COLORS['black']
    pygame.draw.circle(window, color_mobile, (int(mobile["x"]), int(
        mobile["y"])), CIRCLE_RADIUS, MOBILE_CIRCLE_DIAMETER)


def draw_board():
    electrical_field_str = "Eletrical field : {0:.2f} V/m".format(
        electrical_field_v)
    electrical_field_img = police.render(
        electrical_field_str, True, COLORS["black"])
    window.blit(electrical_field_img, (100, 120))

    magnetic_field_str = "Magnetic field : {0:.2f}T".format(
        magnetic_field)
    magnetic_field_image = police.render(
        magnetic_field_str, True, COLORS["black"])
    window.blit(magnetic_field_image, (100, 160))

    chaine_kinetic_energy = "Kinetic energy : {0:.2f} µJ".format(
        mobile["kinetic_energy"] * (10 ** 6))
    kinetic_energy_image = police.render(
        chaine_kinetic_energy, True, COLORS["black"])
    window.blit(kinetic_energy_image, (100, 140))

def calculate_field_cyclotron(dt):
    global alpha, electrical_field_v
    period = (2 * math.pi * mobile["mass"]) / (mobile["charge"] * magnetic_field)
    alpha += (2 * math.pi * dt) / period
    electrical_field_v = 10 * math.sin(math.fmod(alpha, 2 * math.pi))

def calculate_electrical_field(x, y):
    return (0, -electrical_field_v)


def update_moving_charge(t):
    global mobile, first_iteration, prev_data
    elec_field = calculate_electrical_field(mobile["x"], mobile["y"])

    if not elec_field:
        mobile["is_present"] = False
    else:
        if not first_iteration:
            Δt = t - prev_data["t"]

            force_coulomb = [
                mobile["charge"] * elec_field[0],
                mobile["charge"] * elec_field[1]
            ]

            # matrix version
            force_lorentz = [
                - (mobile["charge"] * prev_data["vy"]) * magnetic_field,
                (mobile["charge"] * prev_data["vx"]) * magnetic_field
            ]

            acceleration_mobile = [
                (force_coulomb[0] + force_lorentz[0]) / mobile["mass"],
                (force_coulomb[1] + force_lorentz[1]) / mobile["mass"]
            ]

            mobile["vx"] = acceleration_mobile[0] * Δt + prev_data["vx"]
            mobile["vy"] = acceleration_mobile[1] * Δt + prev_data["vy"]

            mobile["x"] = prev_data["x"] + mobile["vx"] * Δt
            mobile["y"] = prev_data["y"] + mobile["vy"] * Δt

        else:
            first_iteration = False

    prev_data = {
        "x": mobile["x"],
        "y": mobile["y"],
        "vx": mobile["vx"],
        "vy": mobile["vy"],
        "t": t
    }


while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_UP:
                if electrical_field_v < INTERVALLE_CHAMP["max"]:
                    mode_cyclotron = False
                    electrical_field_v += 1
            elif evenement.key == pygame.K_DOWN:
                if electrical_field_v > INTERVALLE_CHAMP["min"]:
                    mode_cyclotron = False
                    electrical_field_v -= 1
            elif evenement.key == pygame.K_SPACE:
                prev_data["x"] = WINDOW_SIZE[0] // 2
                prev_data["y"] = WINDOW_SIZE[1] // 2
                prev_data["vx"] = 0
                prev_data["vy"] = 0
                magnetic_field = 1
                electrical_field_v = 10
                mode_cyclotron = False
                initialization_trace()
            elif evenement.key == pygame.K_PAGEUP or evenement.key == pygame.K_u:  
                if magnetic_field < max_field:
                    magnetic_field += 0.01
            elif evenement.key == pygame.K_PAGEDOWN or evenement.key == pygame.K_d:
                if magnetic_field > min_field:
                    magnetic_field -= 0.01
            elif evenement.key == pygame.K_c:
                mode_cyclotron = True

    window.fill(COLORS['background'])
    time_now = pygame.time.get_ticks()
    while time_prev < time_now:
        t_secondes = time_prev / 1000
        if mobile["is_present"]:
            if(mode_cyclotron):
                calculate_field_cyclotron(t_secondes - prev_data["t"])
            update_moving_charge(t_secondes)
        time_prev += 0.1

    if mobile["is_present"]:
        draw_mobile_charge()
        mobile["kinetic_energy"] = 1 / 2 * mobile["mass"] * \
            ((math.hypot(mobile["vx"], mobile["vy"])) ** 2)
        draw_board()
        position = [mobile["x"], mobile["y"]]
        add_trace(position)
        draw_trace()
    pygame.display.flip()
    clock.tick(fps)

import math
import sys
import pygame

# Graphics variables
COLORS = {
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "purple": (255, 0, 255),
    "grey": (150, 150, 150),
    "background": (160, 139, 178),
    "light_blue": (127, 191, 255)
}
WINDOW_SIZE = (800, 600)
fps = 25
NOM_PROGRAMME = "Direct current motor"
MARGINS = (200, 200)
SIZE_RECTANGLE = ( (WINDOW_SIZE[0] - 2 * MARGINS[0]) / 2 , (WINDOW_SIZE[1] - 2 * MARGINS[1]))
CIRCLE_RADIUS_MOTOR = (WINDOW_SIZE[1] - 2 * MARGINS[1]) / 2
R = 0.02
RATIO_R = CIRCLE_RADIUS_MOTOR / R
L = 0.06
RATIO_L = RATIO_R * (L / R)

CIRCLE_RADIUS_BEHIND = CIRCLE_RADIUS_MOTOR + 25
RADIUS_ANGLE_MOTOR = 10
circuit_open = True

# Physics variables

counter = 0
MOTOR_ANGLE = 0
motor = {
    "spires" : 1000,
    "inertia_moment" : 1,
    "radius" : R,
    "length" : L,
    "magnetic_field" : 0.5,
    "angle" : MOTOR_ANGLE,
    "current" : 0,
    "winding_current" : 0,
    "speed" : 0,
    "x_angle_motor" : WINDOW_SIZE[0] / 2 + (CIRCLE_RADIUS_MOTOR - (2 * RADIUS_ANGLE_MOTOR)) * math.cos(MOTOR_ANGLE),
    "y_angle_motor" : WINDOW_SIZE[1] / 2 + (CIRCLE_RADIUS_MOTOR - (2 * RADIUS_ANGLE_MOTOR)) * math.sin(-MOTOR_ANGLE),
    "tension": 0
}
c = 0.2
Resistance = 10


# Initialization

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(NOM_PROGRAMME)
police = pygame.font.Font('media/cmunrm.ttf', 20)
clock = pygame.time.Clock()
window.fill(COLORS["background"])
objects = []
time_prev = pygame.time.get_ticks() - 10
time_now = pygame.time.get_ticks()
first_iteration = True
pygame.key.set_repeat(10, 10)

prev_data = {
    "t": pygame.time.get_ticks() / 1000,
    "angle": motor["angle"],
    "speed": motor["speed"],
    "x_angle_motor": motor["x_angle_motor"],
    "y_angle_motor": motor["y_angle_motor"]
}

# Functions

def dessiner_motor():

    #Magnets
    pygame.draw.rect(window, COLORS["red"], pygame.Rect(MARGINS[0], MARGINS[1], SIZE_RECTANGLE[0], SIZE_RECTANGLE[1]))
    pygame.draw.rect(window, COLORS["blue"], pygame.Rect(MARGINS[0] + SIZE_RECTANGLE[0], MARGINS[1], SIZE_RECTANGLE[0], SIZE_RECTANGLE[1]))

    #Motor
    pygame.draw.circle(window,COLORS["background"], (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), CIRCLE_RADIUS_BEHIND)
    pygame.draw.circle(window,COLORS["white"], (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), CIRCLE_RADIUS_MOTOR)
    
    #Motor position
    pygame.draw.circle(window,COLORS["black"], (motor["x_angle_motor"], motor["y_angle_motor"]), RADIUS_ANGLE_MOTOR)


def update_motor(t):
    global prev_data, motor
    
    E = 2 * motor["spires"] * motor["radius"] * motor["length"] * motor["magnetic_field"] * motor["speed"] *  math.cos(motor["angle"])
    if circuit_open :
        motor["tension"] = E
        motor["current"]= 0
    else :
        motor["tension"] = 10
        motor["current"] = (10-E)/Resistance

    #Handle direct current
    if (motor["angle"] <= math.pi / 2 and motor["angle"] >= 0) or (motor["angle"] > 3 * math.pi / 2 and motor["angle"] < 2* math.pi) :
        motor["winding_current"] = motor["current"]

    elif motor["angle"] > math.pi / 2 and motor["angle"] < 3 * math.pi / 2 :
        motor["winding_current"] = -motor["current"]
        motor["tension"] = -motor["tension"]
        
    τ = 2 * motor["spires"] * motor["radius"] * motor["length"] * motor["winding_current"] * motor["magnetic_field"] * math.cos(motor["angle"])
    α = ((τ - c * motor["speed"]) / motor["inertia_moment"]) 
    Δt = t - prev_data["t"]

    motor["speed"] = α * Δt + prev_data["speed"]
    motor["angle"] = prev_data["angle"] + motor["speed"] * Δt
    motor["angle"] = math.fmod(motor["angle"], math.pi * 2)

    motor["x_angle_motor"] = WINDOW_SIZE[0]/2 + (math.cos(motor["angle"]) * (CIRCLE_RADIUS_MOTOR - 2 * RADIUS_ANGLE_MOTOR)) 
    motor["y_angle_motor"] = WINDOW_SIZE[1]/2 + (math.sin(motor["angle"]) * (CIRCLE_RADIUS_MOTOR - 2 * RADIUS_ANGLE_MOTOR))

    prev_data = {
        "t": t,
        "angle": motor["angle"],
        "speed": motor["speed"],
        "x_angle_motor": motor["x_angle_motor"],
        "y_angle_motor": motor["y_angle_motor"]
    }


def draw_board():
    current_motor_str = "Current : {0:.2f} A".format(motor["winding_current"])
    current_motor_str_image = police.render(current_motor_str, True, COLORS["black"])
    window.blit(current_motor_str_image, (50, 50))

    tension_motor_str = "Tension : {0:.2f} V".format(motor["tension"])
    chaine_tourant_motor_image = police.render(tension_motor_str, True, COLORS["black"])
    window.blit(chaine_tourant_motor_image, (50, 70))


# Main loop

while True:
    for evenement in pygame.event.get():
        #evenements
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE :
                counter = 5
                motor["tension"] = 10
                circuit_open = False

    window.fill(COLORS["background"])
    time_now = pygame.time.get_ticks()
    
    update_motor(time_now / 1000) 
    if counter:
        counter -= 1
    else :
        circuit_open = True
        
    dessiner_motor()
    draw_board()
    pygame.display.flip()
    clock.tick(fps)
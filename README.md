# 🚀Simple Physic simulations
![Release](https://img.shields.io/badge/Release-v1.0-blueviolet?style=for-the-badge)
![Language](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Collection of physics programs done for the [INFO2058](https://people.montefiore.uliege.be/boigelot/cours/labmp/tutoriel/index.html)/[2059](https://people.montefiore.uliege.be/cornelusse/laboPMP2/outils.html) courses, given by Pr. Boigelot and Bertrand Cornélusse, ULiège.
The final mark for the projects is 15/20 for the mechanics section and 20/20 for the electromagnetism section.

Note : No copying (even partial) of this code within the scope of the INFO2058/2059 course will be tolerated.

## ⚙️Mecanics
- `spaceship.py` : Spaceship simulation. The program simulate the thurst of a spaceship and the gravity exercised by a planet on the spaceship.
![Balistic gameplay](/misc/spaceship.png)
    - Press `Left`/`Right` to adjust the ship nozzle orientation.
    - Press `Up` to light up the nozzle.
    - Press `Left-click` to add a planet.
    - Press `Right-click` to remove a planet.
    - Press `Q` to quit.

- `gesture.py` : Vertical gesture detection program. The acceleration in shown in red, the velocity in green. A vertical and slow gesture from bottom to top to bottom increases the counter.
![Gesture detection example](/misc/gesture.png)

- `complex_movement.py` : Simulation of the movement of a mobile object. The simulation takes place on a curve with frictions tkane into account and with an initial high potential energy position.
![Complex movement simulation](/misc/complex_movement.png.png)

- `balistic.py` : Balistic simulation calculating the right timing to drop a bomb on a target. The y velocity and acceleration is shown in the top left of the screen.
![Balistic gameplay](/misc/balistic.png)
    - Press `A` to drop a bomb automatically (the plane should no be moved on the Y axis after being armed).
    - Press `B` to drop a bomb manually.

- `balistic1.py` : Balistic simulation calculating the right timing to fire a projectile on a target.
![Balistic gameplay](/misc/balistic1.png)
    - Press `Right-click` to position the red indicator.
    - Press `A` to initialize the automatic fire.
    - Press `Left-click` to fire.
    - Alternatively, press `Up`/`Down` to adjust initial speed, `Left`/`Right` to adjust the canon position to try and aim for the indicator.

## ⚡Electromagnetism
- `field.py` : Simulation displaying the electrical field between electrical charges. Red is positive, Black is negative.
![Field between two charges](/misc/field.png)
    - Press `Left-click` to add a positive charge.
    - Press `Right-click` to add a negative charge.
    - Press `Middle-click` to remove a charge.

- `mobile_charge.py` : Simulation of the trajectory of a mobile negative charge between fixed charges. The potential and kinetic energy of the mobile charge and the mouse position are shown in the top left of the screen
![Field between fixed and mobile charges](/misc/mobile_charge.png)
    - Press `Left-click` to add a positive charge.
    - Press `Right-click` to add a negative charge.
    - Press `Middle-click` to remove a charge.
    - Press `N` to place a mobile charge.

- `cyclotron.py` : Simulation of the trajectory of a mobile positive charge in a [cyclotron](https://fr.wikipedia.org/wiki/Cyclotron). The magnetic field is facing outward from the screen.
![Field between fixed and mobile charges](/misc/cyclotron.png)
    - Press `Up` to increase the vertical component of the electrical field.
    - Press `Down` to decrease the vertical component of the electrical field.
    - Press `PgUp` to increase the magnetic field.
    - Press `PgDn` to decrease the magnetic field.
    - Press `C` to automatically handle the magnetic and electrical fields to create a cyclotron.
    - Press `Spacebar` to reset the simulation.

- `motor.py` : Simulation of a direct current motor. The motor is composed at its center of a rotor of 1000 spires. The stator is composed of two permanent magnetcs, the magnetic field go from left to right. The winding inductance is not taken into account.
![Direct current motor simulation](/misc/motor.png)
    - Press `Spacebar` to close the circuit.

## Credits
- [Simon Gardier](https://github.com/simon-gardier) (Co-author)
- Lei Yang (Co-author)
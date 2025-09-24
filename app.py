import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import pyautogui
import time

# Initialize Pygame
pygame.init()
pygame.joystick.init()

joysticks = []
run = True

pyautogui.FAILSAFE = False  # Disable fail-safe (triggered when mouse it out of monitor bounds)

a_click = False
b_click = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(event.device_index)
            joystick.init()
            joysticks.append(joystick)
            print(f"Joystick {joystick.get_name()} connected.")

    for joystick in joysticks:
        if not joystick.get_init():
            continue

        # Read axes left stick
        lx = joystick.get_axis(0)  # left/right
        ly = joystick.get_axis(1)  # up/down

        # read axes for right stick
        ry = joystick.get_axis(3)

        # Deadzone left
        if abs(lx) < 0.1: lx = 0
        if abs(ly) < 0.1: ly = 0

        # Deadzone right
        if abs(ry) < 0.1: ry = 0

        # Read buttons
        a = joystick.get_button(0)  # A button
        b = joystick.get_button(1)  # B button
        lb = joystick.get_button(4)  # left bumper
        rb = joystick.get_button(5)  # right bumper
        start = joystick.get_button(7)  # start button

       # Click / Hold on A button
        if a == 1 and not a_click:
            pyautogui.mouseDown()
            a_click = True
        elif a == 0 and a_click:
            pyautogui.mouseUp()
            a_click = False

        # Click / Hold on B button
        if b == 1 and not b_click:
            pyautogui.rightClick()
            b_click = True
        elif b == 0 and b_click:
            pyautogui.mouseUp()
            b_click = False

        # hold and release ctrl with left bumper
        if rb == 1:
            pyautogui.keyDown ('ctrl')
        else:
            pyautogui.keyUp ('ctrl')

        # start to exit
        if start == 1:
            print("Application exiting...")
            run = False 

        # Move mouse with left stick
        speed = 100
        dx = lx * speed
        dy = ly * speed
        pyautogui.moveRel(dx, dy)

        # Scroll using right stick
        scroll_speed = 100
        scroll = -ry * scroll_speed
        pyautogui.scroll(int(scroll))

    time.sleep(0.01)

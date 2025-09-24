import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import pyautogui
import time

# Initialize Pygame
pygame.init()
pygame.joystick.init()

joysticks = []  # List of joysticks
run = True

pyautogui.FAILSAFE = False  # Disable fail-safe

a_click = False
b_click = False

# Track last time for delta time
last_time = time.time()

while run:
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(event.device_index)
            joystick.init()
            joysticks.append(joystick)
            print(f"Joystick {joystick.get_name()} connected.")

    # calculate delta time (seconds since last loop)
    now = time.time()
    dt = now - last_time
    last_time = now

    for joystick in joysticks:
        if not joystick.get_init():
            continue  # Skip uninitialized joysticks

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
            pyautogui.mouseDown()   # press and hold left mouse
            a_click = True
        elif a == 0 and a_click:
            pyautogui.mouseUp()     # release left mouse
            a_click = False

        # Click / Hold on B button
        if b == 1 and not b_click:
            pyautogui.rightClick()   # press and hold right mouse
            b_click = True
        elif b == 0 and b_click:
            pyautogui.mouseUp()     # release right mouse
            b_click = False

        if rb == 1:
            pyautogui.keyDown ('ctrl')  # hold ctrl
        else:
            pyautogui.keyUp ('ctrl')    # release ctrl

        if start == 1:
            print("Application exiting...")
            run = False  # Exit on start button

        # Move mouse with smoothing (scaled by delta time)
        speed = 800  # pixels per second max speed
        dx = lx * speed * dt
        dy = ly * speed * dt
        pyautogui.moveRel(dx, dy)

        # Scroll using right stick vertical
        scroll_speed = 800  # lines per second at full tilt
        scroll = -ry * scroll_speed * dt
        if int(scroll) != 0:
            pyautogui.scroll(int(scroll))

    time.sleep(0.001)  # shorter sleep for smoother loop

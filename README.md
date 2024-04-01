# NEAT_Mario_and_Luigi

Note to self: Been mostly f-ing around with cv, and i think i have been mostly overcomplicating the bare bones solution for the inputs required for the net.

Inputs:
- Time elapsed since combo
- Fixed-length queue of seen characters entering (length will as long as many characters can fit on screen and "zero" padded, tho it looks like max the number of entering characters at higher combo strings is ~3)

Outputs:
- What button to press (A, B, X, Y, or none)

Theoretically this should work as the time elapsed should account for the window of time difficulty to pressing the right button for the combo. It could reasonably be correlated to the distance away from the boss. As of the character queue, this gives information to learn what button to press for each character.

Goal: https://www.youtube.com/watch?v=3LJ9qQpR4jI&ab_channel=Migu

use `pyautogui.sleep(0.01)` for registering holds/presses
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

dont constantly check for entering characters, have two states, `entered_edge` and `passed_edge`.

- `entered_edge==False` and `passed_eddge==False`: dont do anything
- `entered_edge==True` and `passed_eddge==False`: wait for last frame until character fully in screen
- `entered_edge==True` and `passed_eddge==True`: scan for character and mark everything false

Roi:

 --------
| X |    |
| X |    |
| X |    |
 --------

note: you dont need to constantly check for both, it works one at a time until both are true. the Xs are the gutter or edge.
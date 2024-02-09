import random
import time
import curses

# Define player stats
health = 100
ammo = 20
level = 1

# Define enemies
enemy_types = {
    "coconut": {"health": 10, "damage": 2, "symbol": "@", "message": "A coconut falls"},
    "parrot": {"health": 5, "damage": 1, "symbol": chr(0x1F9B5), "message": "Squawk! The parrot swoops and bites you!"},
    "crocodile": {"health": 20, "damage": 5, "symbol": chr(0x1F40A), "message": "Snap! The crocodile lunges and chomps down!"},
}

# Initialize curses screen
try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
except:
    print("Error initializing curses.")
    quit()

def display_info():
    stdscr.clear()
    stdscr.addstr(0, 0, f"Level: {level}")
    stdscr.addstr(1, 0, f"Health: {health}")
    stdscr.addstr(2, 0, f"Ammo: {ammo}")
    stdscr.refresh()

def display_enemy(enemy_type, enemy):
    symbol = enemy_types[enemy_type]["symbol"]
    message = enemy_types[enemy_type]["message"]
    stdscr.addstr(4, 0, f"You encounter a {enemy_type} ({symbol})!")
    stdscr.addstr(5, 0, message)
    stdscr.refresh()

def get_player_choice():
    while True:
        key = stdscr.getch()
        if key in [ord('s'), ord('r'), ord('q')]:
            return chr(key)
        else:
            stdscr.addstr(6, 0, "Invalid choice. Please choose shoot (s), reload (r), or quit (q).")
            stdscr.refresh()
            time.sleep(0.5)
            stdscr.clearlines(6, 1)

def animate_action(message):
    for char in message:
        stdscr.addstr(7, 0, char)
        stdscr.refresh()
        time.sleep(0.05)
    stdscr.clearlines(7, 1)

# Game loop
while True:
    display_info()

    # Check for game over
    if health <= 0:
        stdscr.addstr(8, 0, "Game over! You were defeated in the jungle.")
        break

    # Generate a random enemy
    enemy_type = random.choice(list(enemy_types.keys()))
    enemy = enemy_types[enemy_type]

    display_enemy(enemy_type, enemy)

    # Action loop
    while enemy["health"] > 0:
        choice = get_player_choice()

        if choice == "s":
            if ammo > 0:
                enemy["health"] -= 1
                ammo -= 1
                animate_action(f"You shoot the {enemy_type}! It has {enemy['health']} health remaining.")
            else:
                animate_action("You're out of ammo! Reload first.")
        elif choice == "r":
            ammo = 20
            animate_action("You reload your weapon.")
        elif choice == "q":
            animate_action("You give up and leave the jungle.")
            break
        else:
            pass

        # Enemy attack
        if enemy["health"] > 0:
            health -= enemy["damage"]
            animate_action(enemy["message"])

        # Pause for suspense
        time.sleep(0.5)

    # Level up and increase difficulty
    level += 1
    for enemy_type, data in enemy_types.items():
        data["health"] += 2
        data["damage"] += 1

stdscr.getch()  #

from random import choice
from turtle import *
from freegames import floor, vector

# ---------------- STATE ----------------
state = {'score': 0, 'running': False, 'paused': False}

path = Turtle(visible=False)
writer = Turtle(visible=False)
menu = Turtle(visible=False)
ui = Turtle(visible=False)

aim = vector(5, 0)
pacman = vector(-40, -80)

ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# ---------------- MAP ----------------
tiles = [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,
    0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,
    0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,
    0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,
    0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0,0,
    0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,
    0,1,0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,
    0,0,0,0,1,0,1,1,1,1,1,0,1,0,0,1,0,0,0,0,
    0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,
    0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,
    0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,
    0,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,
    0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,
    0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0,0,
    0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,
    0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]

# ---------------- MENU ----------------
def draw_menu():
    clear()
    writer.clear()
    path.clear()
    ui.clear()
    menu.clear()

    bgcolor("black")

    menu.penup()
    menu.color("yellow")
    menu.goto(0, 100)
    menu.write("PACMAN", align="center", font=("Arial", 36, "bold"))

    menu.goto(0, 20)
    menu.color("white")
    menu.write("PLAY GAME", align="center", font=("Arial", 18, "bold"))

    menu.goto(0, -40)
    menu.write("QUIT", align="center", font=("Arial", 18, "bold"))

def click(x, y):
    if not state['running']:
        if -50 < y < 50:
            start_game()
        elif -100 < y < -20:
            bye()
    else:
        # Pause / Resume
        if -200 < x < -120 and 130 < y < 210:
            toggle_pause()

        # ✅ FIXED Quit
        elif 50 < x < 250 and 120 < y < 220:
            quit_game()

# ---------------- CONTROLS ----------------
def draw_controls():
    ui.clear()
    ui.penup()
    ui.color("white")

    ui.goto(-180, 180)
    if state['paused']:
        ui.write("Resume")
    else:
        ui.write("Pause")

    ui.goto(120, 180)
    ui.write("Quit")

# ---------------- ORIGINAL GAME ----------------
def square(x, y):
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for _ in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()

def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    return int(x + y * 20)

def valid(point):
    index = offset(point)
    if tiles[index] == 0:
        return False
    index = offset(point + 19)
    if tiles[index] == 0:
        return False
    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    bgcolor('black')
    path.color('blue')
    for index in range(len(tiles)):
        tile = tiles[index]
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def move():
    if not state['running']:
        return

    if state['paused']:
        draw_controls()
        ontimer(move, 100)
        return

    writer.undo()
    writer.write(state['score'])
    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [vector(5,0), vector(-5,0), vector(0,5), vector(0,-5)]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()
    draw_controls()

    for point, _ in ghosts:
        if abs(pacman - point) < 20:
            quit_game()
            return

    ontimer(move, 50)

def change(x, y):
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

# ---------------- EXTRA ----------------
def start_game():
    state['running'] = True
    state['paused'] = False
    state['score'] = 0

    menu.clear()
    writer.clear()

    writer.goto(160, 160)
    writer.color('white')
    writer.write(state['score'])

    world()
    move()

def toggle_pause():
    state['paused'] = not state['paused']

def quit_game():
    state['running'] = False
    state['paused'] = False

    clear()
    writer.clear()
    ui.clear()
    path.clear()

    draw_menu()

# ---------------- SETUP ----------------
setup(width=1.0, height=1.0)
hideturtle()
tracer(False)

listen()
onscreenclick(click)

onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

draw_menu()
done()
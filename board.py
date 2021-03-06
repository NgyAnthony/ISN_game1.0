from math import cos, sin, sqrt, radians  # imports used to create hexagons
import tkinter as tk
import sys
import os
import webbrowser


hexagons = []  # This is a list of list of the boards of each canvas_instance that is created
squad_list = []  # this list contains all the instances of the Squad class
bonus_list = []
objective_red = ['27.4']
objective_blue = ['5.14']
colorblind = 0  # 0 for normal, 1 for colorblind
editor = []

if colorblind == 0:
    red_side_colors = ["#c0392b", "#EE5A24"]
    blue_side_colors = ["#013dc6", "#0652DD"]
    objective_color = "#8c7ae6"
    grass_color = "#a1e2a1"
    mountain_color = "#a1603a"
    water_color = "#60ace6"
    moving_color = "#f1c40f"
    bonus_color = "#5150BA"

elif colorblind == 1:
    red_side_colors = ["#005952", "#2E4052"]
    blue_side_colors = ["#0000FF", "#000091"]
    objective_color = "#8c7ae6"
    grass_color = "#6FDE6E"
    mountain_color = "#E1DAAE"
    water_color = "#00FFFF"
    moving_color = "#f1c40f"
    bonus_color = "#5150BA"


class App:
    def __init__(self, canvas_instance=None):
        """
        This function creates a new canvas_instance which is used everytime Game is called.
        """
        self.canvas_instance = canvas_instance


class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Battlegrounds")
        self.master.geometry("1440x800")
        self.url = "https://github.com/NgyAnthony/ISN_Battlegrounds-"

        # <---Tkinter --->
        # Frame and canvas
        self.canvas_instance = tk.Canvas(self.master, width=1280, height=800, bg=grass_color, relief="ridge", borderwidth="10")
        self.frame = tk.Frame(self.master, width=130, height=800, bg="blue", padx="5", relief="ridge", borderwidth="10", pady="5")
        self.frame.pack_propagate(0)
        self.frame.pack(side="left")
        self.canvas_instance.pack()

        # Title
        self.title = tk.Text(self.frame, height="1")
        self.title.insert(tk.INSERT, "BATTLEGROUNDS")
        self.title.config(state=tk.DISABLED)
        self.title.pack(pady=(10, 50))

        # Title of turn
        self.current_player = tk.Text(self.frame, height="1")
        self.current_player.insert(tk.INSERT, "Turn of:")
        self.current_player.config(state=tk.DISABLED)
        self.current_player.pack()

        # Images
        if colorblind == 0:
            self.blue_player_img = tk.PhotoImage(file='images/blue_player.gif')
            self.red_player_img = tk.PhotoImage(file='images/red_player.gif')
            self.water_img = tk.PhotoImage(file='images/water.gif')
            self.mountain_img = tk.PhotoImage(file='images/mountain.gif')
            self.objective_img = tk.PhotoImage(file='images/obj.gif')
            self.grass_img = tk.PhotoImage(file='images/grass.gif')
            self.bonus_img = tk.PhotoImage(file='images/colorblind/bonus.gif')

        elif colorblind == 1:
            self.blue_player_img = tk.PhotoImage(file='images/colorblind/blue_player_colorblind.gif')
            self.red_player_img = tk.PhotoImage(file='images/colorblind/red_player_colorblind.gif')
            self.water_img = tk.PhotoImage(file='images/colorblind/water_colorblind.gif')
            self.mountain_img = tk.PhotoImage(file='images/colorblind/mountain_colorblind.gif')
            self.objective_img = tk.PhotoImage(file='images/colorblind/obj_colorblind.gif')
            self.grass_img = tk.PhotoImage(file='images/colorblind/grass_colorblind.gif')
            self.bonus_img = tk.PhotoImage(file='images/colorblind/bonus.gif')


        # Image of current playing player
        self.show_player = tk.Button(self.frame)
        self.show_player.config(image=self.red_player_img)
        self.show_player.pack()

        # Title of hovering
        self.current = tk.Text(self.frame, height="1")
        self.current.insert(tk.INSERT, "Hovering:")
        self.current.config(state=tk.DISABLED)
        self.current.pack(pady=(50, 0))

        # Name of hovering object
        self.current_player = tk.Button(self.frame)
        self.current_player.config(text="Grass")
        self.current_player.pack(fill="x")

        # Image of hovering hexagon
        self.show_hover = tk.Button(self.frame)
        self.show_hover.config(image=self.grass_img, state=tk.DISABLED)
        self.show_hover.pack()

        # Information and details of hexagon
        self.current_squad = tk.Button(self.frame, height="5")
        self.current_squad.config(text="")
        self.current_squad.pack(fill="x")

        # Title of status
        self.sta_txt = tk.Text(self.frame, height="1")
        self.sta_txt.insert(tk.INSERT, "Status:")
        self.sta_txt.config(state=tk.DISABLED)
        self.sta_txt.pack(pady=(30, 0))

        # Show status of click
        self.status = tk.Button(self.frame, height="5")
        self.status.config(text="")
        self.status.pack(fill="x")

        # Quit button
        self.quit = tk.Button(self.frame, text="Quit", bg="red", command=root.destroy)
        self.quit.pack(fill="x", side="bottom")

        # End turn button
        self.end_turn = tk.Button(self.frame, text="End turn", bg="red", command=self.endTurn)
        self.end_turn.pack(fill="x", side="bottom", pady=(0, 50))

        # Github
        self.more = tk.Button(self.frame, text="Rules", bg="red", command=self.openweb)
        self.more.pack(fill="x", side="bottom", pady=(0, 10))

        # < --- Tkinter --->

        self.app_instance = App(self.canvas_instance)
        self.initGrid(35, 18, 25, debug=False)  # Calls init grid with cols, rows and size.
        Create()
        self.reset_board()

        self.previous_clicked = []
        self.neighbours = []  # this list includes all the tags of the neighbours of the selected position
        self.enemy_neighbour = []
        self.enemy_neighbour_inrange = []
        self.friendly_neighbour = []
        self.obstacles = []
        self.playing_side = "red"

        self.canvas_instance.bind("<Button-1>", self.click)  # bind click function when RMB is used
        self.canvas_instance.bind("<Motion>", self.moved)

        self.tag = self.canvas_instance.create_text(20, 20, text="", anchor="nw")
        self.hexagon = self.canvas_instance.create_text(20, 35, text="", anchor="nw")

    def openweb(self):
        webbrowser.open(self.url)

    def moved(self, evt):
        """
        This function detects what it's hovering on.
        :param evt: x and y position of hovering
        :return: information in interface
        """
        x, y = evt.x, evt.y  # get the x and y position of RMB event
        self.hover = self.canvas_instance.find_closest(x, y)[0]  # define "clicked" as the closest object near x,y
        self.canvas_instance.itemconfigure(self.tag, text="(%r, %r)" % (evt.x, evt.y))
        self.canvas_instance.itemconfigure(self.hexagon, text="(%r)" % self.hover)
        if hexagons[self.hover - 1].color in blue_side_colors:
            self.show_hover.config(image=self.blue_player_img)
            self.current_player.config(text="Player 1")
            for x in range(len(squad_list)):
                if squad_list[x].position == hexagons[self.hover - 1].tags:
                    self.current_squad.config(text="HP = %s\nMP = %s\nAP = %s\nEP = %s"
                                                   % (squad_list[x].units, squad_list[x].mp, squad_list[x].ap, squad_list[x].ep))

        elif hexagons[self.hover - 1].color in red_side_colors:
            self.show_hover.config(image=self.red_player_img)
            self.current_player.config(text="Player 2")
            for x in range(len(squad_list)):
                if squad_list[x].position == hexagons[self.hover - 1].tags:
                    self.current_squad.config(text="HP = %s\nMP = %s\nAP = %s\nEP = %s"
                                                   % (squad_list[x].units, squad_list[x].mp, squad_list[x].ap, squad_list[x].ep))

        elif hexagons[self.hover - 1].color == water_color:
            self.show_hover.config(image=self.water_img)
            self.current_player.config(text="Water")
            self.current_squad.config(text="Indestructible\nobject.")

        elif hexagons[self.hover - 1].color == mountain_color:
            self.show_hover.config(image=self.mountain_img)
            self.current_player.config(text="Mountain")
            self.current_squad.config(text="Indestructible\nobject.")

        elif hexagons[self.hover - 1].color == objective_color:
            self.show_hover.config(image=self.objective_img)
            self.current_player.config(text="Objective")
            self.current_squad.config(text="Empty\nposition.")

        elif hexagons[self.hover - 1].color == grass_color:
            self.show_hover.config(image=self.grass_img)
            self.current_player.config(text="Grass")
            self.current_squad.config(text="Empty\nposition.")

        elif hexagons[self.hover - 1].color == bonus_color:
            self.show_hover.config(image=self.bonus_img)
            self.current_player.config(text="Bonus")
            self.current_squad.config(text="Empty\nposition.")

        self.show_hover.pack()

    def endTurn(self):
        if self.playing_side == "red":
            self.playing_side = "blue"
            self.show_player.config(image=self.blue_player_img)
            self.show_player.pack()
            self.reset_squad()

        elif self.playing_side == "blue":
            self.playing_side = "red"
            self.show_player.config(image=self.red_player_img)
            self.show_player.pack()
            self.reset_squad()

    def reset_squad(self):
        """This function gives back MP and EP to all Squads."""
        for x in squad_list:
            x.mp = 2
            x.ep = 1

    def reset_board(self):
        for i in hexagons:
            i.selected = False  # set every hex object to "not selected"
            self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon to its own

    def initGrid(self, cols, rows, size, debug):
        """
                This function creates the grid of hexagon which will be used as the board.
        :param cols: number of columns used on the board
        :param rows: number of rows used on the board
        :param size: size of one side of hexagon
        :param debug: True/False, make text appear on hexagons
        :return: game board is returned
        """
        for c in range(cols):  # avoid overlapping hexagons
            if c % 2 == 0:
                offset = size * sqrt(3) / 2
            else:
                offset = 0
            for r in range(rows):
                h = FillHexagon(self.canvas_instance,
                                c * (size * 1.5),
                                (r * (size * sqrt(3))) + offset,
                                size,
                                grass_color,
                                "{}.{}".format(c, r))  # Call FillHexagon to generate the hexagon
                hexagons.append(h)

                # This if statement writes position on every hexagon
                    # Warning : click doesn't work when debug is on
                if debug:
                    coords = "{}, {}".format(c, r)
                    self.canvas_instance.create_text(c * (size * 1.5) + (size / 2),
                                         (r * (size * sqrt(3))) + offset + (size / 2),
                                         text=coords, anchor="n", state="disabled")

    def click(self, evt):
        """
                Hexagon detection on mouse click.
                Movements and attack detection.
        :param evt: get the x and y position of the click
        :return: determine if we need to find the neighbours or if hex is empty
        """
        x, y = evt.x, evt.y  # get the x and y position of RMB event
        for i in hexagons:  # this for loop erase any trace of its use
            i.selected = False  # set every hex object to "not selected"
            self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon back to its own
        clicked = self.canvas_instance.find_closest(x, y)[0]  # define "clicked" as the closest object near x,y
        self.previous_clicked.append(clicked)
        previous_squad = hexagons[self.previous_clicked[len(self.previous_clicked) - 2] - 1].tags
        hexagons[int(clicked) - 1].selected = True
        editor_is = False

        if editor_is:
            for i in hexagons:
                if i.selected:
                # If the hexagon is empty or an obstacle
                    if i.color == grass_color or i.color == mountain_color or i.color == water_color:
                        i.color = "#bdc3c7"
                        #self.canvas_instance.itemconfigure(i.tags, fill="#bdc3c7")  # fill the clicked hex with color
                        editor.append(i.tags)
                        self.reset_board()
                        print(editor)
        else:
            for i in hexagons:
                # <--First click-->
                if i.selected and len(self.previous_clicked) % 2 == 1:
                    # If the hexagon is empty or an obstacle
                    if i.color == grass_color or i.color == mountain_color or i.color == water_color:
                        self.clear_sight()
                        self.canvas_instance.itemconfigure(i.tags, fill="#bdc3c7")  # fill the clicked hex with color
                        self.previous_clicked.clear()
                        print("Click: empty hexagon or obstacle at", i.tags, " selected.")

                    # If the hexagon is on the playing side, allow movement
                    if self.playing_side == "red" and i.color in red_side_colors:
                        print("Click:", i.color, "hexagon at", i.tags, "has been selected.")
                        for a in range(len(squad_list)):
                            if i.tags == squad_list[a].position:
                                mp = squad_list[a].mp
                        if mp == 1:  # assigning pixel density to reach neighbours depending on movement points
                            area = 50
                        elif mp == 2:
                            area = 80
                        elif mp == 0:
                            area = 0
                            self.status.config(text="Out of MP !")
                        self.getNear(i.x, i.y, area, i.tags)  # call possible movements

                    elif self.playing_side == "blue" and i.color in blue_side_colors:
                        print("Click:", i.color, "hexagon at", i.tags, "has been selected.")
                        for a in range(len(squad_list)):
                            if i.tags == squad_list[a].position:
                                mp = squad_list[a].mp
                        if mp == 1:  # assigning pixel density to reach neighbours depending on movement points
                            area = 50
                        elif mp == 2:
                            area = 80
                        elif mp == 0:
                            area = 0
                            self.status.config(text="Out of MP !")
                        self.getNear(i.x, i.y, area, i.tags)  # call possible movements

                    # If it's not the turn of the clicked object, disallow movements
                    elif self.playing_side == "red" and i.color in blue_side_colors:
                        self.clear_sight()
                        self.previous_clicked.clear()
                        print("Click: it's not the turn of the selected unit.")
                        self.status.config(text="Not your turn !")

                    elif self.playing_side == "blue" and i.color in red_side_colors:
                        self.clear_sight()
                        self.previous_clicked.clear()
                        print("Click: it's not the turn of the selected unit.")
                        self.status.config(text="Not your turn !")

                # <--Second click-->
                elif i.selected and len(self.previous_clicked) % 2 == 0:
                    # If the user moves on a bonus
                    if i.tags in self.neighbours and i.color == bonus_color:
                        i.color = hexagons[self.previous_clicked[len(self.previous_clicked) - 2] - 1].color
                        hexagons[self.previous_clicked[len(self.previous_clicked) - 2] - 1].color = grass_color
                        print("Click:", i.color, "squad moved to", i.tags)

                        # This for loop changes the position in squad_list
                        for r in range(len(squad_list)):
                            if squad_list[r].position == previous_squad:
                                squad_list[r].position = i.tags
                                print("Click: squad_list at", previous_squad, "now at", i.tags, ".")
                                squad_list[r].mp -= 1
                                for x in range(len(bonus_list)):
                                    for a in range(len(squad_list)):
                                        if bonus_list[x].position == squad_list[a].position:
                                            squad_list[a].ap += bonus_list[x].ap_bonus
                                            self.status.config(text="+3 AP\npicked up.")
                                            break

                    # If the second and first click are in the same team
                    elif self.playing_side == "red" and i.color in red_side_colors:
                        self.clear_sight()
                        self.previous_clicked.clear()

                    # This loop moves the hexagon
                    elif i.tags in self.neighbours:
                        for x in range(len(hexagons) - 1):
                            if hexagons[x].tags == i.tags:
                                i.color = hexagons[self.previous_clicked[len(self.previous_clicked) - 2] - 1].color
                                hexagons[self.previous_clicked[len(self.previous_clicked) - 2] - 1].color = grass_color
                                print("Click:", i.color, "squad moved to", i.tags)

                                # This for loop changes the position in squad_list
                                for r in range(len(squad_list)):
                                    if squad_list[r].position == previous_squad:
                                        squad_list[r].position = i.tags
                                        print("Click: squad_list at", previous_squad, "now at", i.tags, ".")
                                        squad_list[r].mp -= 1

                    # This for loop look for hexagons that can be attacked.
                    for p in range(len(self.enemy_neighbour_inrange)):
                        if i.tags == self.enemy_neighbour_inrange[p].tags:
                            defencer = self.enemy_neighbour_inrange[p]
                            for l in range(len(squad_list)):
                                if squad_list[l].position == previous_squad:
                                    attacker = squad_list[l]
                            if attacker.ep == 0:
                                self.status.config(text="Out of energy!")
                            else:
                                self.attack(defencer, attacker)

                            break
                    self.reset_board()
                    self.clear_sight()
                    self.previous_clicked.clear()
                    self.checkObjective()

    # This function resets the "targets" of the chosen position
    def clear_sight(self):
        self.neighbours.clear()
        self.enemy_neighbour.clear()
        self.friendly_neighbour.clear()
        self.enemy_neighbour_inrange.clear()

    def attack(self, defencer, attacker):
        for x in range(len(squad_list)):
            if squad_list[x].position == defencer.tags:
                squad_list[x].units -= attacker.ap
                attacker.ep -= 1
                self.status.config(text="%s removed\n %s HP!" % (self.playing_side, attacker.ap))
                if self.playing_side == "blue":
                    if squad_list[x].units == 2:
                        defencer.color = red_side_colors[1]
                    elif squad_list[x].units <= 0:
                        defencer.color = grass_color
                        squad_list.remove(squad_list[x])
                elif self.playing_side == "red":
                    if squad_list[x].units == 2:
                        defencer.color = blue_side_colors[1]
                    elif squad_list[x].units <= 0:
                        defencer.color = grass_color
                        squad_list.remove(squad_list[x])
                self.reset_board()
                break

    def getNear(self, x, y, area, origin):
        """
                This function determines the neighbours of a Squad.
        :param x: x position of the clicked hexagon
        :param y: y position of the clicked hexagon
        :param area: pixel width used to determine neighbours
        :param origin: clicked hexagon (to remove him from neighbours list)
        :return: colors the area where action is possible

        """
        self.clear_sight()

        for a in range(630):
            # define x and y define the zone in which movement will be possible
            neighbour_x0 = x - area
            neighbour_x1 = x + area

            neighbour_y0 = y - area
            neighbour_y1 = y + area

            if neighbour_x1 >= hexagons[a].x >= neighbour_x0 and \
                    neighbour_y1 >= hexagons[a].y >= neighbour_y0:
                self.neighbours.append(hexagons[a].tags)

        # This statement removes the original position from the list
        for m in range(len(self.neighbours)):
            if origin == self.neighbours[m]:
                self.neighbours.remove(self.neighbours[m])
                break

        # This statement removes every obstacles from the neighbours
        for m in range(len(self.neighbours)):
            for i in hexagons:
                if i.tags == self.neighbours[m] and (i.color == water_color or i.color == mountain_color):
                    self.obstacles.append(self.neighbours[m])
        self.neighbours = list(set(self.neighbours) - set(self.obstacles))

        # This for loops removes enemies and friendlies and append them to another list
        for m in range(len(self.neighbours)):
            for i in hexagons:
                if self.playing_side == "blue":
                    if i.tags == self.neighbours[m] and i.color in red_side_colors:
                        self.enemy_neighbour.append(self.neighbours[m])
                    if i.tags == self.neighbours[m] and i.color in blue_side_colors:
                        self.friendly_neighbour.append(self.neighbours[m])
                elif self.playing_side == "red":
                    if i.tags == self.neighbours[m] and i.color in red_side_colors:
                        self.friendly_neighbour.append(self.neighbours[m])
                    if i.tags == self.neighbours[m] and i.color in blue_side_colors:
                        self.enemy_neighbour.append(self.neighbours[m])

        self.neighbours = list(set(self.neighbours) - set(self.enemy_neighbour))
        self.neighbours = list(set(self.neighbours) - set(self.friendly_neighbour))

        # This for loop determines if the ennemy is within range
        for p in range(630):
            attackable_x0 = x - 50
            attackable_x1 = x + 50

            attackable_y0 = y - 50
            attackable_y1 = y + 50

            for a in range(len(red_side_colors)):
                if self.playing_side == "blue":
                    if hexagons[p].color == red_side_colors[a] and \
                            attackable_x1 >= hexagons[p].x >= attackable_x0 and \
                            attackable_y1 >= hexagons[p].y >= attackable_y0:
                            self.enemy_neighbour_inrange.append(hexagons[p])
                elif self.playing_side == "red":
                    if hexagons[p].color == blue_side_colors[a] and \
                            attackable_x1 >= hexagons[p].x >= attackable_x0 and \
                            attackable_y1 >= hexagons[p].y >= attackable_y0:
                            self.enemy_neighbour_inrange.append(hexagons[p])

        # The two following for statements fill the near elements of the clicked hexagons
        for m in range(len(self.neighbours)):
            for i in hexagons:  # this for loop erase any trace of its use
                self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon back to its own

        for m in range(len(self.neighbours)):
            for i in hexagons:
                if i.tags == self.neighbours[m] and i.color != objective_color:
                    self.canvas_instance.itemconfigure(i.tags, fill=moving_color)  # fill the clicked hex with color

    def popup_end(self, winner):
        self.win = tk.Toplevel()
        self.win.wm_title("Window")

        self.l = tk.Label(self.win, text="%s has won ! Do you want to play again ?" % winner)
        self.l.pack(side="top")

        self.b = tk.Button(self.win, text="Yes", command=self.restart_program)
        self.b.pack(side="left")

        self.b = tk.Button(self.win, text="No", command=root.destroy)
        self.b.pack(side="right")

    def restart_program(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def checkObjective(self):
        for i in range(len(hexagons)):
            if hexagons[i].tags == objective_red[0]:
                for x in blue_side_colors:
                    if hexagons[i].color == x:
                        print("Blue has won !")
                        self.popup_end("Blue")

        for i in range(len(hexagons)):
            if hexagons[i].tags == objective_blue[0]:
                for x in red_side_colors:
                    if hexagons[i].color == x:
                        print("Red has won !")
                        self.popup_end("Red")


class FillHexagon:
    def __init__(self, parent, x, y, length, color, tags):
        """ Define parameters of the hexagon """
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.tags = tags
        self.selected = False
        self.color = color

        self.draw()

    def draw(self):
        """
        draw() creates the hexagon
        :return: one hexagon is drawn on the board.
        """
        start_x = self.x
        start_y = self.y
        angle = 60  # angle of hexagon
        coords = []
        for i in range(6):
            end_x = start_x + self.length * cos(radians(angle * i))
            end_y = start_y + self.length * sin(radians(angle * i))
            coords.append([start_x, start_y])
            start_x = end_x
            start_y = end_y
        # create_polygon creates a polygon based on coords
        self.parent.create_polygon(coords[0][0],
                                   coords[0][1],
                                   coords[1][0],
                                   coords[1][1],
                                   coords[2][0],
                                   coords[2][1],
                                   coords[3][0],
                                   coords[3][1],
                                   coords[4][0],
                                   coords[4][1],
                                   coords[5][0],
                                   coords[5][1],
                                   fill=self.color,
                                   outline="grey",
                                   tags=self.tags)


# <------------------------- ELEMENTS ------------------------->
class Squad:
    def __init__(self, side, units, arsenal, ap, ep, mp, position, color):
        """
                       This class generates a Squad and re-instances the board.
        :param side: The side determines if you're on the blue or red side.
        :param units: Units are the numbers of units. They're basically HP.
        :param arsenal: Arsenal determines if the Squad is made of tanks, rangers...
        :param ap: Attack points.
        :param ep: Energy points
        :param mp: Movement points.
        :param position: Position on the board. (x.y)
        :param color: Color code.
        """
        self.side = side
        self.units = units
        self.arsenal = arsenal
        self.ap = ap  # attack points
        self.ep = ep  # energy points
        self.mp = mp  # movement points
        self.position = position
        self.color = color
        self.squadAppear()

    def squadAppear(self):
        for x in range(len(hexagons)):
            # this for loop targets the position of the instance with the current position in the form of tags
            # and change the color of the targeted hexagon
            if hexagons[x].tags == self.position:
                hexagons[x].color = self.color
                break
        squad_list.append(self)  # append the instance object to a list
        print("Squad:", self.side, "squad at", self.position, "has been created.")


class Objective:
    def __init__(self, position, side, opposite_side):
        self.position = position
        self.side = side
        self.opposite_side = opposite_side
        self.color = objective_color

        if self.side == "blue":
            for c in red_side_colors:
                self.check_ally(c)

        elif self.side == "red":
            for c in blue_side_colors:
                self.check_ally(c)

    def check_ally(self, enemy_color):
        for x in range(len(hexagons)):
            if self.position == hexagons[x].tags and hexagons[x].color != enemy_color:
                self.plant_objective()

    def plant_objective(self):
        for x in range(len(hexagons)):
            if self.position == hexagons[x].tags:
                hexagons[x].color = self.color


class Bonus:
    def __init__(self, position, ap_bonus):
        self.position = position
        self.color = bonus_color
        self.ap_bonus = ap_bonus
        self.plant_bonus()

    def plant_bonus(self):
        for x in range(len(hexagons)):
            if self.position == hexagons[x].tags:
                hexagons[x].color = self.color
                break
        bonus_list.append(self)


class Field:
    # Class field changes the color of an object in hexagons
    types = {
        "water": water_color,
        "mountain": mountain_color
    }

    def __init__(self, position, kind):
        self.position = position
        self.kind = kind
        self.color = Field.types[self.kind]
        self.placeField()

    def placeField(self):
        for x in range(len(hexagons)):
            if self.position == hexagons[x].tags:
                hexagons[x].color = self.color


# <------------------------- Maps ------------------------->
class Create:
    def __init__(self):
        # <--------- MAP 1 --------->
        self.red_squad_infantry_map1 = ['5.1', '5.2', '5.3', '30.12', '31.13', '32.13', '23.3', '22.4', '24.4', '20.1', '18.2', '20.3', '31.4', '30.5', '32.6', '16.7']
        self.blue_squad_infantry_map1 = ['13.9', '4.13', '6.12', '6.14', '2.10', '1.12', '4.11', '10.14', '9.16', '11.16', '1.3', '2.3', '3.4', '27.14', '28.14', '29.15']
        self.water_list_map1 = []
        self.mountain_list_map1 = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.10', '0.11', '0.12', '0.13', '0.14', '0.15', '0.16', '0.17', '1.17', '2.17', '3.17', '4.17', '5.17', '6.17', '7.17', '8.17', '9.17', '10.17', '11.17', '12.17', '13.17', '14.17', '15.17', '16.17', '17.17', '18.17', '19.17', '20.17', '21.17', '22.17', '23.17', '24.17', '25.17', '26.17', '27.17', '28.17', '29.17', '30.17', '31.17', '32.17', '33.17', '34.17', '34.16', '34.15', '34.14', '34.13', '34.12', '34.11', '34.10', '34.9', '34.8', '34.7', '34.6', '34.5', '34.4', '34.3', '34.2', '34.1', '34.0', '33.0', '32.0', '31.0', '30.0', '29.0', '28.0', '27.0', '26.0', '25.0', '24.0', '23.0', '22.0', '21.0', '20.0', '19.0', '18.0', '17.0', '16.0', '15.0', '14.0', '13.0', '12.0', '11.0', '10.0', '9.0', '8.0', '7.0', '6.0', '5.0', '4.0', '3.0', '2.0', '1.0', '4.3', '10.8', '5.11', '10.13', '17.9', '21.12', '20.11', '19.11', '18.11', '17.12', '16.9', '17.10', '16.10', '15.11', '15.12', '15.13', '12.11', '11.12', '11.13', '13.11', '13.12', '13.13', '15.10', '4.4', '5.4', '5.5', '4.5', '5.6', '6.5', '7.6', '7.7', '7.8', '6.8', '5.8', '9.8', '9.7', '9.9', '8.9', '7.10', '5.10', '6.10', '10.7', '10.6', '9.6', '7.5', '6.4', '11.4', '12.4', '13.5', '14.5', '15.6', '16.5', '19.8', '20.7', '21.8', '21.9', '22.8', '22.9', '23.9', '23.10', '24.9', '24.10', '25.11', '26.11', '25.12', '24.11', '26.10', '27.10', '28.10', '28.11', '29.9', '30.9', '30.10', '30.11', '28.8', '28.7', '27.7', '26.6', '26.5', '26.4', '22.7', '23.7', '24.6', '18.4', '17.4', '16.3', '18.3', '19.4', '23.8', '24.7', '25.8', '24.8', '25.9', '27.5', '27.6', '28.6', '29.7', '29.8', '30.8', '13.4', '14.3']
        self.objective_red_map1 = ['33.1']
        self.objective_blue_map1 = ['1.16']
        self.bonus_map1 = ['12.12', '6.7', '6.6', '20.8', '25.10', '27.11', '14.4', '15.5', '12.3']

        self.place_element_map1()

    def place_element_map1(self):
        for r in range(len(self.red_squad_infantry_map1)):
            Squad("red", 6, 'infantry', 2, 1, 2, self.red_squad_infantry_map1[r], red_side_colors[0])
        for b in range(len(self.blue_squad_infantry_map1)):
            Squad("blue", 6, 'infantry', 2, 1, 2, self.blue_squad_infantry_map1[b], blue_side_colors[0])
        for w in range(len(self.water_list_map1)):
            Field(self.water_list_map1[w], "water")
        for m in range(len(self.mountain_list_map1)):
            Field(self.mountain_list_map1[m], "mountain")
        for x in self.objective_red_map1:
            Objective(x, "red", "blue")
        for x in self.objective_blue_map1:
            Objective(x, "blue", "red")
        for a in self.bonus_map1:
            Bonus(a, 3)


root = tk.Tk()
Game(root)  # canvas instance
root.mainloop()

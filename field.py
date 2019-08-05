import constants as e
import tkinter


class Field(object):

    def __init__(self, player, weapon, from_x, to_x, from_y, to_y, delete_id=-1):
        self.player = player
        self.weapon = weapon
        self.from_x = from_x
        self.to_x = to_x
        self.from_y = from_y
        self.to_y = to_y
        self.pos_x = to_x - 28
        self.pos_y = to_y - 37
        self.delete_id = delete_id
        self.__icon = None
        self.marked = False
        self.bot_possible_moves = []

    def __str__(self):
        return 'Player: {}, weapon: {}, marked: {} delete: {}'.format(self.player, self.weapon, self.marked, self.delete_id)

    def icon(self):
        if self.player == e.Player.NOBODY:
            return
        if self.player == e.Player.BOT:
            self.__icon = tkinter.PhotoImage(file='img/red.gif')
        elif self.weapon == e.Weapons.ROCK:
            self.__icon = tkinter.PhotoImage(file='img/blue-rock.png')
        elif self.weapon == e.Weapons.PAPER:
            self.__icon = tkinter.PhotoImage(file='img/blue-paper.png')
        elif self.weapon == e.Weapons.SCISSORS:
            self.__icon = tkinter.PhotoImage(file='img/blue-scissors.png')
        elif self.weapon == e.Weapons.FLAG:
            self.__icon = tkinter.PhotoImage(file='img/blue-flag.png')
        elif self.weapon == e.Weapons.TRAP:
            self.__icon = tkinter.PhotoImage(file='img/trap.png')
        elif self.weapon == e.Weapons.NOTHING:
            self.__icon = tkinter.PhotoImage(file='img/blue.png')
        return self.__icon

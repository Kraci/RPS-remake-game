from constants import MapSettings as mapSettings
import constants as e
import sqlite3
import tkinter
import random
import field
import bot
import os


class Game(object):
    def __init__(self):
        # db
        if not os.path.isfile('rps.db'):
            self.conn = sqlite3.connect('rps.db')
            self.create_table()
            self.conn.close()

        # game info
        self.state = e.States.MENU
        self.player_turn = True
        self.bot = bot.Bot()

        # board variables
        self.duel_x = None
        self.duel_y = None
        self.marked_field = None
        self.flag_selected = False
        self.trap_selected = False
        self.show_weapons = False

        # delete id
        self.hint_text_place_flag_id = -1
        self.hint_text_place_trap_id = -1
        self.shuffle_button_id = -1
        self.shuffle_button_text_id = -1
        self.play_game_button_id = -1
        self.play_game_button_text_id = -1
        self.save_game_button_id = -1
        self.load_game_button_id = -1
        self.rules_button_id = -1 # TODO: ak nepouzite, vymazat
        self.player_turn_text_id = -1
        self.bot_turn_text_id = -1

        self.white_mark_id = -1
        self.white_mark_up_id = -1
        self.white_mark_down_id = -1
        self.white_mark_right_id = -1
        self.white_mark_left_id = -1

        self.rock_weapon_id = -1
        self.paper_weapon_id = -1
        self.scissors_weapon_id = -1
        self.rock_big_weapon_id = -1
        self.paper_big_weapon_id = -1
        self.scissors_big_weapon_id = -1
        self.rock_big_weapon_bot_id = -1
        self.paper_big_weapon_bot_id = -1
        self.scissors_big_weapon_bot_id = -1
        self.rock_weapon = None
        self.paper_weapon = None
        self.scissors_weapon = None
        self.rock_big_weapon = None
        self.paper_big_weapon = None
        self.scissors_big_weapon = None

    def draw_duel_weapons(self, canvas):
        self.rock_weapon = tkinter.PhotoImage(file='img/rock_smaller.png')
        self.paper_weapon = tkinter.PhotoImage(file='img/paper_smaller.png')
        self.scissors_weapon = tkinter.PhotoImage(file='img/scissors_smaller.png')

        self.rock_weapon_id = canvas.create_image(450, 720, image=self.rock_weapon)
        self.paper_weapon_id = canvas.create_image(600, 720, image=self.paper_weapon)
        self.scissors_weapon_id = canvas.create_image(750, 720, image=self.scissors_weapon)

    def duel(self, new_field, canvas):
        self.rock_big_weapon = tkinter.PhotoImage(file='img/rock.png')
        self.paper_big_weapon = tkinter.PhotoImage(file='img/paper.png')
        self.scissors_big_weapon = tkinter.PhotoImage(file='img/scissors.png')

        if self.show_weapons:
            if self.marked_field.weapon == e.Weapons.ROCK:
                self.rock_big_weapon_id = canvas.create_image(mapSettings.CANVAS_WIDTH//2+100, 600, image=self.rock_big_weapon)
            elif self.marked_field.weapon == e.Weapons.PAPER:
                self.paper_big_weapon_id = canvas.create_image(mapSettings.CANVAS_WIDTH//2+100, 600, image=self.paper_big_weapon)
            elif self.marked_field.weapon == e.Weapons.SCISSORS:
                self.scissors_big_weapon_id = canvas.create_image(mapSettings.CANVAS_WIDTH//2+100, 600, image=self.scissors_big_weapon)

            if new_field.weapon == e.Weapons.ROCK:
                self.rock_big_weapon_bot_id = canvas.create_image(mapSettings.CANVAS_WIDTH//2+100, 200, image=self.rock_big_weapon)
            elif new_field.weapon == e.Weapons.PAPER:
                self.paper_big_weapon_bot_id = canvas.create_image(mapSettings.CANVAS_WIDTH//2+100, 200, image=self.paper_big_weapon)
            elif new_field.weapon == e.Weapons.SCISSORS:
                self.scissors_big_weapon_bot_id = canvas.create_image(mapSettings.CANVAS_WIDTH//2+100, 200, image=self.scissors_big_weapon)

            canvas.update()
            canvas.after(1000)
            canvas.delete(self.rock_big_weapon_id, self.paper_big_weapon_id, self.scissors_big_weapon_id,
                          self.rock_big_weapon_bot_id, self.paper_big_weapon_bot_id, self.scissors_big_weapon_bot_id)
            self.show_weapons = False


        if new_field.weapon == e.Weapons.FLAG:
            return e.Duel.FLAG
        elif new_field.weapon == e.Weapons.TRAP:
            return e.Duel.LOSE
        elif new_field.weapon == e.Weapons.ROCK:
            if self.marked_field.weapon == e.Weapons.ROCK:
                self.draw_duel_weapons(canvas)
                return e.Duel.DRAW
            elif self.marked_field.weapon == e.Weapons.PAPER:
                return e.Duel.WIN
            elif self.marked_field.weapon == e.Weapons.SCISSORS:
                return e.Duel.LOSE
        elif new_field.weapon == e.Weapons.PAPER:
            if self.marked_field.weapon == e.Weapons.ROCK:
                return e.Duel.LOSE
            elif self.marked_field.weapon == e.Weapons.PAPER:
                self.draw_duel_weapons(canvas)
                return e.Duel.DRAW
            elif self.marked_field.weapon == e.Weapons.SCISSORS:
                return e.Duel.WIN
        elif new_field.weapon == e.Weapons.SCISSORS:
            if self.marked_field.weapon == e.Weapons.ROCK:
                return e.Duel.WIN
            elif self.marked_field.weapon == e.Weapons.PAPER:
                return e.Duel.LOSE
            elif self.marked_field.weapon == e.Weapons.SCISSORS:
                self.draw_duel_weapons(canvas)
                return e.Duel.DRAW

    def switch_field(self, new_field, win=True):
        if win:
            new_field.player = self.marked_field.player
            new_field.weapon = self.marked_field.weapon
            self.marked_field.player = e.Player.NOBODY
            self.marked_field.weapon = e.Weapons.NOBODY
        else:
            self.marked_field.player = e.Player.NOBODY
            self.marked_field.weapon = e.Weapons.NOBODY

    def shuffle_weapons(self, board):

        weapons = [e.Weapons.ROCK, e.Weapons.ROCK, e.Weapons.ROCK, e.Weapons.ROCK,
                   e.Weapons.PAPER, e.Weapons.PAPER, e.Weapons.PAPER, e.Weapons.PAPER,
                   e.Weapons.SCISSORS, e.Weapons.SCISSORS, e.Weapons.SCISSORS, e.Weapons.SCISSORS]

        random_weapons = list()

        for i in range(len(weapons)):
            random_index = random.randrange(len(weapons))
            wpn = weapons.pop(random_index)
            random_weapons.append(wpn)

        iterator = 0
        for row in range(4, mapSettings.MAP_ROWS):
            for col in range(mapSettings.MAP_COLUMNS):
                creature = board[row][col]
                if creature.weapon != e.Weapons.FLAG and creature.weapon != e.Weapons.TRAP:
                    creature.weapon = random_weapons[iterator]
                    iterator += 1

    def create_table(self):
        create_query = '''
               CREATE TABLE board
               (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
               PLAYER         INT     NOT NULL,
               WEAPON         INT     NOT NULL,
               FROM_X         INT     NOT NULL,
               TO_X           INT     NOT NULL,
               FROM_Y         INT     NOT NULL,
               TO_Y           INT     NOT NULL,
               DELETE_ID      INT     NOT NULL);
        '''
        self.conn.execute(create_query)

    def save_game(self, board):
        conn = sqlite3.connect('rps.db')
        conn.execute("DELETE FROM board")

        for row in range(mapSettings.MAP_ROWS):
            for col in range(mapSettings.MAP_COLUMNS):
                creature = board[row][col]
                conn.execute("INSERT INTO board (PLAYER, WEAPON, FROM_X, TO_X, FROM_Y, TO_Y, DELETE_ID) VALUES ("+ str(creature.player) +", "+ str(creature.weapon) +", "+ str(creature.from_x) +", "+ str(creature.to_x) +", "+ str(creature.from_y) +", "+ str(creature.to_y) +", "+ str(creature.delete_id) +")")

        conn.commit()
        conn.close()

    def load_game(self):
        conn = sqlite3.connect('rps.db')
        cursor = conn.execute("SELECT ID, PLAYER, WEAPON, FROM_X, TO_X, FROM_Y, TO_Y, DELETE_ID from board")

        board = []
        tmp = []

        for row in cursor:
            tmp.append(field.Field(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            if row[0] % 7 == 0:
                board.append(tmp)
                tmp = []

        conn.close()
        return board

from constants import MapSettings as mapSettings
from tkinter import messagebox
import constants as e
from tkinter import *
import tkinter
import field
import game


class Map(object):

    def __init__(self):
        self.tk = Tk()
        self.tk.title('RPS')
        self.canvas = Canvas(self.tk, width=mapSettings.CANVAS_WIDTH, height=mapSettings.CANVAS_HEIGHT)
        self.canvas.bind('<Button-1>', self.clicked_on_scene)
        self.canvas.pack()
        self.game = game.Game()
        self.board = list()
        self.init_game()

    def set_background(self, name_of_file):
        self.canvas.background = tkinter.PhotoImage(file=name_of_file)
        self.canvas.create_image(0, 0, anchor='nw', image=self.canvas.background)

    def init_game(self):
        if self.game.state == e.States.MENU:
            self.set_background('img/menu2.png')
            self.canvas.create_text(230, 340, text="Start Game", fill='white', font='arial 50')
            self.canvas.create_text(230, 410, text="Game Rules", fill='white', font='arial 30')
        elif self.game.state == e.States.MAP:
            self.board = []
            self.game.flag_selected = False
            self.game.trap_selected = False
            self.set_background('img/map.png')
            self.game.hint_text_place_flag_id = self.canvas.create_text(600, 700, text="PLACE YOUR FLAG!", fill='white', font='arial 30')
            for row in range(mapSettings.MAP_ROWS):
                fields = []
                for col in range(mapSettings.MAP_COLUMNS):
                    from_x = mapSettings.MAP_LEFT_EDGE_X + mapSettings.MAP_FIELD_A * col
                    to_x = mapSettings.MAP_LEFT_EDGE_X + (mapSettings.MAP_FIELD_A * col + mapSettings.MAP_FIELD_A)
                    from_y = mapSettings.MAP_TOP_EDGE_Y + mapSettings.MAP_FIELD_A * row
                    to_y = mapSettings.MAP_TOP_EDGE_Y + (mapSettings.MAP_FIELD_A * row + mapSettings.MAP_FIELD_A)
                    if row == 0 or row == 1:
                        fields.append(field.Field(e.Player.BOT, e.Weapons.NOTHING, from_x, to_x, from_y, to_y))
                    elif row == 4 or row == 5:
                        fields.append(field.Field(e.Player.PLAYER, e.Weapons.NOTHING, from_x, to_x, from_y, to_y))
                    else:
                        fields.append(field.Field(e.Player.NOBODY, e.Weapons.NOBODY, from_x, to_x, from_y, to_y))
                self.board.append(fields)

    def clear_board(self):
        for row in range(mapSettings.MAP_ROWS):
            for col in range(mapSettings.MAP_COLUMNS):
                creature = self.board[row][col]
                self.canvas.delete(creature.delete_id)

    def count_characters(self):
        result = 0
        for row in range(mapSettings.MAP_ROWS):
            for col in range(mapSettings.MAP_COLUMNS):
                creature = self.board[row][col]
                if creature.weapon != e.Weapons.FLAG and creature.weapon != e.Weapons.TRAP and creature.player == e.Player.PLAYER:
                    result += 1
        return result

    def draw_creatures(self, redraw=False):
        if redraw:
            self.clear_board()
        for row in range(mapSettings.MAP_ROWS):
            for col in range(mapSettings.MAP_COLUMNS):
                creature = self.board[row][col]
                creature.delete_id = self.canvas.create_image(creature.pos_x, creature.pos_y, image=creature.icon())

    def reset_marks(self):
        for row in range(mapSettings.MAP_ROWS):
            for col in range(mapSettings.MAP_COLUMNS):
                creature = self.board[row][col]
                creature.marked = False
        self.canvas.delete(self.game.white_mark_id, self.game.white_mark_up_id, self.game.white_mark_down_id,
                           self.game.white_mark_right_id, self.game.white_mark_left_id)

    def check_possible_moves(self, row, col):
        if 0 <= row - 1 < 6:
            up_field = self.board[row-1][col]
            if up_field.player != e.Player.PLAYER:
                self.game.white_mark_up_id = self.canvas.create_rectangle(up_field.from_x, up_field.from_y, up_field.to_x, up_field.to_y, fill='', outline='white')
                up_field.marked = True
        if 0 <= row + 1 < 6:
            down_field = self.board[row+1][col]
            if down_field.player != e.Player.PLAYER:
                self.game.white_mark_down_id = self.canvas.create_rectangle(down_field.from_x, down_field.from_y, down_field.to_x, down_field.to_y, fill='', outline='white')
                down_field.marked = True
        if 0 <= col + 1 < 7:
            right_field = self.board[row][col+1]
            if right_field.player != e.Player.PLAYER:
                self.game.white_mark_right_id = self.canvas.create_rectangle(right_field.from_x, right_field.from_y, right_field.to_x, right_field.to_y, fill='', outline='white')
                right_field.marked = True
        if 0 <= col - 1 < 7:
            left_field = self.board[row][col-1]
            if left_field.player != e.Player.PLAYER:
                self.game.white_mark_left_id = self.canvas.create_rectangle(left_field.from_x, left_field.from_y, left_field.to_x, left_field.to_y, fill='', outline='white')
                left_field.marked = True

    def switch_turn(self):
        if self.game.player_turn:
            self.game.player_turn = not self.game.player_turn
            self.canvas.delete(self.game.player_turn_text_id)
            if self.game.state == e.States.END:
                self.canvas.create_text(480, 400, text="YOU WON!!", fill='#efdede', font='arial 120 bold')
                self.canvas.create_rectangle((420, 660), (600, 700), outline='white')
                self.canvas.create_text(510, 680, text='GO TO MENU', fill='white', font='arial 20')
                self.game.player_turn = True
                self.game.bot.goal_row = 0
                self.game.bot.goal_col = 0
                return
            self.game.bot_turn_text_id = self.canvas.create_text(540, 170, text="Bot turn", fill='#efdede', font='arial 40 bold')
            first, second, won, gg = self.game.bot.play(self.board, self.canvas)
            if first is not None and second is not None:
                self.game.bot.switch_fields(first, second, won, self.canvas)
                self.draw_creatures(redraw=True)
            if gg or (first is None and second is None):
                self.game.state = e.States.END
                self.canvas.delete(self.game.bot_turn_text_id)
                if first is None:
                    self.canvas.create_text(480, 400, text="YOU WON!!", fill='#efdede', font='arial 120 bold')
                else:
                    self.canvas.create_text(480, 400, text="BOT WON!!", fill='#efdede', font='arial 120 bold')
                self.canvas.create_rectangle((420, 660), (600, 700), outline='white')
                self.canvas.create_text(510, 680, text='GO TO MENU', fill='white', font='arial 20')
                self.game.player_turn = True
                self.game.bot.goal_row = 0
                self.game.bot.goal_col = 0
            else:
                self.switch_turn()
        else:
            self.game.player_turn = not self.game.player_turn
            self.canvas.delete(self.game.bot_turn_text_id)
            self.game.player_turn_text_id = self.canvas.create_text(540, 170, text="Your turn", fill='#efdede', font='arial 40 bold')
            if self.count_characters() == 0:
                self.game.state = e.States.END
                self.canvas.delete(self.game.player_turn_text_id)
                self.canvas.create_text(480, 400, text="BOT WON!!", fill='#efdede', font='arial 120 bold')
                self.canvas.create_rectangle((420, 660), (600, 700), outline='white')
                self.canvas.create_text(510, 680, text='GO TO MENU', fill='white', font='arial 20')
                self.game.player_turn = True
                self.game.bot.goal_row = 0
                self.game.bot.goal_col = 0

    # CLICKED ON SCENE
    def clicked_on_scene(self, event):
        if self.game.state == e.States.MENU:
            self.clicked_menu(event)
        elif self.game.state == e.States.MAP:
            self.clicked_map(event)
        elif self.game.state == e.States.MAP_SHUFFLE:
            self.clicked_shuffle(event)
        elif self.game.state == e.States.MAP_PLAY:
            self.clicked_map_play(event)
        elif self.game.state == e.States.MAP_DUEL:
            self.clicked_map_duel(event)
        elif self.game.state == e.States.END:
            self.clicked_map_end(event)

    def clicked_map_end(self, event):
        def to_menu_button(x, y):
            if (420 <= x <= 600) and (660 <= y <= 700):
                return True
            return False

        if to_menu_button(event.x, event.y):
            self.game.state = e.States.MENU
            self.init_game()

    def clicked_menu(self, event):
        def start_game_button(x, y):
            if (70 <= x <= 390) and (305 <= y <= 375):
                return True
            return False

        def game_rules_button(x, y):
            if (140 <= x <= 320) and (390 <= y <= 430):
                return True
            return False

        if start_game_button(event.x, event.y):
            self.game.state = e.States.MAP
            self.init_game()
            self.draw_creatures()

        if game_rules_button(event.x, event.y):
            self.canvas.create_rectangle((405, 180), (891, 530), fill='black')
            self.canvas.create_text(mapSettings.CANVAS_WIDTH // 2 + 175, mapSettings.CANVAS_HEIGHT // 2 - 200, fill='white', font='arial 50', text="Pravidla")
            self.canvas.create_text(mapSettings.CANVAS_WIDTH//2+150, mapSettings.CANVAS_HEIGHT//2-30, text="""
            Na zaciatku hry si klikom vyberiete, ktora postava bude drzat vlajku.
            Vase postavy su dole, modrej farby. Postava s vlajkou je hlavna.
            Vyhrava ten, kto sa zmocni superovej vlajky. Nasledne si vyberiete
            pascu. Po skoceni na pascu utociaca postava vzdy prehra. Ostatnym
            postavam sa nahodne rozdaju zbrane - kamen, papier a noznice.
            Tlacitkom “shuffle” mozete tieto zbrane nahodne pomiesat. Po kliknuti
            na starte sa mozete hybat lubovolnou postavou okrem vlajky a pasce.
            Tie su vzdy na svojom mieste. Kliknete na postavu a nasledne sa
            zobrazia policka kde moze postava ist, druhym klikom sa posuniete.
            Ked sa stretnu dve postavy v dueli, nastane suboj kamen, papier,
            noznice. Ak maju postavy taku istu zbran nastava remiza a obe strany
            svoju zbran menia do vtedy kym budu mat ine. Vyhrava ten, kto prvy
            ziska superovu vlajku alebo mu znici vsetky postavy okrem vlajky a pasce.
            """, fill='white', justify=CENTER)

    def clicked_map(self, event):
        x, y = event.x, event.y

        def board_clicked(x_coord, y_coord):
            if (mapSettings.MAP_LEFT_EDGE_X <= x_coord <= mapSettings.MAP_RIGHT_EDGE_X) and (
                            mapSettings.MAP_TOP_EDGE_Y <= y_coord <= mapSettings.MAP_BOTTOM_EDGE_Y):
                return True
            return False

        if board_clicked(x, y):
            row = int((y - mapSettings.MAP_TOP_EDGE_Y) / mapSettings.MAP_FIELD_A)
            col = int((x - mapSettings.MAP_LEFT_EDGE_X) / mapSettings.MAP_FIELD_A)
            clicked_field = self.board[row][col]
            if not self.game.flag_selected:
                if clicked_field.player == e.Player.PLAYER:
                    clicked_field.weapon = e.Weapons.FLAG
                    clicked_field.delete_id = self.canvas.create_image(clicked_field.pos_x, clicked_field.pos_y, image=clicked_field.icon())
                    self.canvas.delete(self.game.hint_text_place_flag_id)
                    self.game.hint_text_place_trap_id = self.canvas.create_text(600, 700, text="PLACE YOUR TRAP!", fill='white', font='arial 30')
                    self.game.flag_selected = True
            elif not self.game.trap_selected:
                if clicked_field.player == e.Player.PLAYER and clicked_field.weapon != e.Weapons.FLAG:
                    clicked_field.weapon = e.Weapons.TRAP
                    clicked_field.delete_id = self.canvas.create_image(clicked_field.pos_x, clicked_field.pos_y, image=clicked_field.icon())
                    self.canvas.delete(self.game.hint_text_place_trap_id)
                    self.game.trap_selected = True
                    self.game.bot.give_random_weapons(self.board)
                    self.game.shuffle_weapons(self.board)
                    self.draw_creatures(redraw=True)
                    self.game.shuffle_button_id = self.canvas.create_rectangle((420, 660), (600, 700), outline='white')
                    self.game.shuffle_button_text_id = self.canvas.create_text(510, 680, text='SHUFFLE', fill='white', font='arial 20')
                    self.game.play_game_button_id = self.canvas.create_rectangle((643, 660), (832, 700), outline='white')
                    self.game.play_game_button_text_id = self.canvas.create_text(738, 680, text='PLAY GAME', fill='white', font='arial 20')
                    self.game.state = e.States.MAP_SHUFFLE

    def clicked_shuffle(self, event):
        def shuffle_button(x_coord, y_coord):
            if (420 <= x_coord <= 600) and (660 <= y_coord <= 700):
                return True
            return False

        def play_game_button(x_coord, y_coord):
            if (643 <= x_coord <= 832) and (660 <= y_coord <= 700):
                return True
            return False

        if shuffle_button(event.x, event.y):
            self.game.shuffle_weapons(self.board)
            self.draw_creatures(redraw=True)
        elif play_game_button(event.x, event.y):
            self.canvas.delete(self.game.shuffle_button_id, self.game.shuffle_button_text_id,
                               self.game.play_game_button_id, self.game.play_game_button_text_id)
            self.game.save_game_button_id = self.canvas.create_text(259, 648, text="Save game", fill='white', font='arial 15')
            self.game.load_game_button_id = self.canvas.create_text(260, 671, text="Load game", fill='white', font='arial 15')
            self.game.player_turn_text_id = self.canvas.create_text(540, 170, text="Your turn", fill='#efdede', font='arial 40 bold')
            self.game.state = e.States.MAP_PLAY

    def clicked_map_duel(self, event):
        def rock_button(x_coord, y_coord):
            if (380 <= x_coord <= 520) and (645 <= y_coord <= 795):
                return True
            return False

        def paper_button(x_coord, y_coord):
            if (530 <= x_coord <= 670) and (645 <= y_coord <= 795):
                return True
            return False

        def scissors_button(x_coord, y_coord):
            if (680 <= x_coord <= 820) and (645 <= y_coord <= 795):
                return True
            return False

        x, y = event.x, event.y
        event.x, event.y = self.game.duel_x, self.game.duel_y

        if rock_button(x, y):
            self.canvas.delete(self.game.rock_weapon_id, self.game.paper_weapon_id, self.game.scissors_weapon_id)
            self.game.state = e.States.MAP_PLAY
            self.game.marked_field.weapon = e.Weapons.ROCK
            self.game.show_weapons = True
            self.clicked_map_play(event)
        elif paper_button(x, y):
            self.canvas.delete(self.game.rock_weapon_id, self.game.paper_weapon_id, self.game.scissors_weapon_id)
            self.game.marked_field.weapon = e.Weapons.PAPER
            self.game.state = e.States.MAP_PLAY
            self.game.show_weapons = True
            self.clicked_map_play(event)
        elif scissors_button(x, y):
            self.canvas.delete(self.game.rock_weapon_id, self.game.paper_weapon_id, self.game.scissors_weapon_id)
            self.game.marked_field.weapon = e.Weapons.SCISSORS
            self.game.state = e.States.MAP_PLAY
            self.game.show_weapons = True
            self.clicked_map_play(event)

    def clicked_map_play(self, event):
        def save_game_button(x_coord, y_coord):
            if (210 <= x_coord <= 290) and (640 <= y_coord <= 658):
                return True
            return False

        def load_game_button(x_coord, y_coord):
            if (210 <= x_coord <= 290) and (663 <= y_coord <= 681):
                return True
            return False

        def board_clicked(x_coord, y_coord):
            if (mapSettings.MAP_LEFT_EDGE_X <= x_coord <= mapSettings.MAP_RIGHT_EDGE_X) and (
                            mapSettings.MAP_TOP_EDGE_Y <= y_coord <= mapSettings.MAP_BOTTOM_EDGE_Y):
                return True
            return False

        x, y = event.x, event.y

        if save_game_button(x, y):
            self.game.save_game(self.board)
            save_game_text_id = self.canvas.create_text(600, 710, text="Game Saved!", fill="white", font="arial 50")
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(save_game_text_id)
        elif load_game_button(x, y):
            loaded_board = self.game.load_game()
            self.board = loaded_board[:]
            self.draw_creatures(redraw=True)
            load_game_text_id = self.canvas.create_text(600, 710, text="Game Loaded!", fill="white", font="arial 50")
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(load_game_text_id)
        elif board_clicked(x, y):
            row = int((y - mapSettings.MAP_TOP_EDGE_Y) / mapSettings.MAP_FIELD_A)
            col = int((x - mapSettings.MAP_LEFT_EDGE_X) / mapSettings.MAP_FIELD_A)
            clicked_field = self.board[row][col]
            if clicked_field.player == e.Player.PLAYER and clicked_field.weapon != e.Weapons.FLAG and clicked_field.weapon != e.Weapons.TRAP:
                self.reset_marks()
                self.game.marked_field = clicked_field
                self.check_possible_moves(row, col)
                self.game.white_mark_id = self.canvas.create_rectangle(clicked_field.from_x, clicked_field.from_y, clicked_field.to_x, clicked_field.to_y, fill='', outline='grey')
            elif clicked_field.marked:
                if clicked_field.player == e.Player.NOBODY:
                    self.game.switch_field(clicked_field)
                    self.reset_marks()
                    self.draw_creatures(redraw=True)
                    self.switch_turn()
                elif clicked_field.player == e.Player.BOT:
                    result = self.game.duel(clicked_field, self.canvas)
                    if result == e.Duel.WIN:
                        self.game.switch_field(clicked_field, win=True)
                    elif result == e.Duel.LOSE:
                        self.game.switch_field(clicked_field, win=False)
                    elif result == e.Duel.DRAW:
                        self.game.duel_x, self.game.duel_y = x, y # save x, y of enemy
                        clicked_field.weapon = self.game.bot.change_weapon_in_duel()
                        self.game.state = e.States.MAP_DUEL
                    elif result == e.Duel.FLAG:
                        self.game.switch_field(clicked_field, win=True)
                        self.game.state = e.States.END
                    if self.game.state != e.States.MAP_DUEL:
                        self.reset_marks()
                        self.draw_creatures(redraw=True)
                        self.switch_turn()

    def on_closing(self):
        q = messagebox.askyesnocancel("Quit", "Do you want save your game before quit?")
        if q is None:
            return
        if q:
            self.game.save_game(self.board)
            self.tk.destroy()
        else:
            self.tk.destroy()


class Program(object):
    def __init__(self):
        self.map = Map()
        self.map.tk.protocol("WM_DELETE_WINDOW", self.map.on_closing)
        self.map.tk.mainloop()

Program()

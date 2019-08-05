from constants import MapSettings as mapSettings
import constants as e
import random


class Bot(object):

    def __init__(self):
        self.MOVE_MS = 1500
        self.goal_row, self.goal_col = 0, 0

    def play(self, board, canvas):
        playable_characters = {0: [], 1: []}

        if self.goal_row == 0 and self.goal_col == 0:
            for row in range(mapSettings.MAP_ROWS):
                for col in range(mapSettings.MAP_COLUMNS):
                    creature = board[row][col]
                    if creature.player == e.Player.PLAYER and creature.weapon == e.Weapons.FLAG:
                        self.goal_row = row
                        self.goal_col = col

        for row in range(mapSettings.MAP_ROWS):
            for col in range(mapSettings.MAP_COLUMNS):
                creature = board[row][col]
                if creature.player != e.Player.BOT or creature.weapon == e.Weapons.TRAP or creature.weapon == e.Weapons.FLAG:
                    continue

                if 0 <= row + 1 < 6:
                    down_field = board[row+1][col]
                    if down_field.player != e.Player.BOT:
                        playable_characters[1].append((creature, down_field))

                if 0 <= col + 1 < 7:
                    right_field = board[row][col+1]
                    if right_field.player != e.Player.BOT:
                        if col < self.goal_col and row == self.goal_row:
                            playable_characters[0].append((creature, right_field))

                if 0 <= col - 1 < 7:
                    left_field = board[row][col-1]
                    if left_field.player != e.Player.BOT:
                        if col > self.goal_col and row == self.goal_row:
                            playable_characters[0].append((creature, left_field))

        if len(playable_characters[0]) > 0:
            length = len(playable_characters[0])
            rndm = random.randrange(length)
            chosen = playable_characters[0][rndm]
        elif len(playable_characters[1]) > 0:
            length = len(playable_characters[1])
            rndm = random.randrange(length)
            chosen = playable_characters[1][rndm]
        else:
            return None, None, False, True  # bot can't move, bot lost

        bot_creature = chosen[0]
        other_creature = chosen[1]
        bot_won = True
        gg = False

        if bot_creature.weapon == e.Weapons.ROCK:
            if other_creature.weapon == e.Weapons.ROCK:
                if random.randrange(1, 3) % 2 == 0:
                    bot_won = True
                else:
                    bot_won = False
            elif other_creature.weapon == e.Weapons.PAPER:
                bot_won = False
            elif other_creature.weapon == e.Weapons.SCISSORS:
                bot_won = True

        elif bot_creature.weapon == e.Weapons.PAPER:
            if other_creature.weapon == e.Weapons.ROCK:
                bot_won = True
            elif other_creature.weapon == e.Weapons.PAPER:
                if random.randrange(1, 3) % 2 == 0:
                    bot_won = True
                else:
                    bot_won = False
            elif other_creature.weapon == e.Weapons.SCISSORS:
                bot_won = False

        elif bot_creature.weapon == e.Weapons.SCISSORS:
            if other_creature.weapon == e.Weapons.ROCK:
                bot_won = False
            elif other_creature.weapon == e.Weapons.PAPER:
                bot_won = True
            elif other_creature.weapon == e.Weapons.SCISSORS:
                if random.randrange(1, 3) % 2 == 0:
                    bot_won = True
                else:
                    bot_won = False

        if other_creature.weapon == e.Weapons.TRAP:
            bot_won = False
        elif other_creature.weapon == e.Weapons.FLAG:
            gg = True

        bot_rectangle = canvas.create_rectangle(bot_creature.from_x, bot_creature.from_y, bot_creature.to_x, bot_creature.to_y, fill='', outline='grey')

        canvas.update()
        canvas.after(self.MOVE_MS//2)

        bot_move_rectangle = canvas.create_rectangle(other_creature.from_x, other_creature.from_y, other_creature.to_x, other_creature.to_y, fill='', outline='white')

        canvas.update()
        canvas.after(self.MOVE_MS//2)

        canvas.delete(bot_rectangle)
        canvas.delete(bot_move_rectangle)

        return bot_creature, other_creature, bot_won, gg

    def switch_fields(self, bot_creature, other_creature, bot_won, canvas):
        if bot_won:
            other_creature.player = bot_creature.player
            other_creature.weapon = bot_creature.weapon
            bot_creature.player = e.Player.NOBODY
            bot_creature.weapon = e.Weapons.NOBODY
        else:
            bot_creature.player = e.Player.NOBODY
            bot_creature.weapon = e.Weapons.NOBODY

    def change_weapon_in_duel(self):
        r = random.randrange(3)
        if r == 0:
            return e.Weapons.ROCK
        elif r == 1:
            return e.Weapons.PAPER
        elif r == 2:
            return e.Weapons.SCISSORS

    def give_random_weapons(self, board):

        weapons = [e.Weapons.ROCK, e.Weapons.ROCK, e.Weapons.ROCK, e.Weapons.ROCK,
                   e.Weapons.PAPER, e.Weapons.PAPER, e.Weapons.PAPER, e.Weapons.PAPER,
                   e.Weapons.SCISSORS, e.Weapons.SCISSORS, e.Weapons.SCISSORS, e.Weapons.SCISSORS]

        flag_trap_index = random.randrange(mapSettings.MAP_COLUMNS)

        random_weapons = list()

        for i in range(len(weapons)):
            random_index = random.randrange(len(weapons))
            wpn = weapons.pop(random_index)
            random_weapons.append(wpn)

        iterator = 0
        for row in range(0, 2):
            for col in range(mapSettings.MAP_COLUMNS):
                creature = board[row][col]
                if row == 0 and col == flag_trap_index:
                    creature.weapon = e.Weapons.FLAG
                elif row == 1 and col == flag_trap_index:
                    creature.weapon = e.Weapons.TRAP
                else:
                    creature.weapon = random_weapons[iterator]
                    iterator += 1

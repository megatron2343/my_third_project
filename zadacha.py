import discord
from PIL import Image, ImageDraw
from discord.ext import commands
import sqlite3
import os

from PIL import Image, ImageDraw

global_list = [
    ('b', 'stealth', 0, 0),
    ('b', 'n', 0, 2),
    ('b', 'n', 0, 4),
    ('b', 'f', 0, 6),
    ('b', 'n', 1, 1),
    ('b', 'th', 1, 3),
    ('b', 'th', 1, 5),
    ('b', 'n', 1, 7),
    ('b', 'f', 2, 0),
    ('b', 'th', 2, 2),
    ('b', 'th', 2, 4),
    ('b', 'stealth', 2, 6),

    ('w', 'stealth', 5, 1),
    ('w', 'th', 5, 3),
    ('w', 'th', 5, 5),
    ('w', 'f', 5, 7),
    ('w', 'n', 6, 0),
    ('w', 'th', 6, 2),
    ('w', 'th', 6, 4),
    ('w', 'n', 6, 6),
    ('w', 'f', 7, 1),
    ('w', 'n', 7, 3),
    ('w', 'n', 7, 5),
    ('w', 'stealth', 7, 7)
]  # список с изначальными координатами шашек


def convert(com):  # преобразование текстовых координат в матричные (1D -> (3, 1))
    l1 = [str(i) for i in range(8)]
    l2 = [chr(i) for i in range(97, 105)]
    form = list(com.lower())
    return (l2.index(form[1]), l1.index(form[0]))


class Board:
    def __init__(self, sc, guild, chan):  # sc - размер квардатной доски
        self.matrix = [['e' for i in range(sc)] for i in range(sc)]
        self.scale = sc
        self.guild = guild
        self.channel = chan
        self.hod = 0
        self.normal_set()

    def __hod_check(self):
        self.hod = (self.hod + 1) % 2
        if self.hod % 2 == 0:
            return 'b'
        return 'w'

    def SetChecker(self, c, t, x, y, clas):
        if self.matrix[x][y] != 'e':
            return False
        if t in ('n', 'nor'):
            self.matrix[x][y] = NormalChecker(c, x, y, clas)
        elif t in ('t', 'th', 'thic'):
            self.matrix[x][y] = ThicChecker(c, x, y, clas)
        elif t in ('f', 'fast'):
            self.matrix[x][y] = FastChecker(c, x, y, clas)
        elif t in ('s', 'st', 'stealth'):
            self.matrix[x][y] = StealthChecker(c, x, y, clas)
        return True

    def can_move(self, x1, y1, x2, y2):
        if self.matrix[x1][y1] != 'e' and self.__hod_check() == self.matrix[x1][y1].color:
            self.matrix[x1][y1].move(x2, y2)
        else:
            return False

    def get_game_field(self):
        im = Image.open("materials/images/res.png")
        draw = ImageDraw.Draw(im)
        for i in self.matrix:
            for j in i:
                if type(j) != str:
                    a, b = j.y, j.x
                    if j.color == 'w':
                        if j.type == 'n':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                         '#FFFFFF')
                        elif j.type == 'f':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                         '#FFFFFF')
                            draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)),
                                         '#00FF00')
                        elif j.type == 'st':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                         '#FFFFFF')
                            draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)),
                                         '#0000FF')
                        elif j.type == 'th':
                            if j.hp == 2:
                                draw.ellipse(
                                    ((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                    '#FFFFFF')
                                draw.ellipse(
                                    ((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)),
                                    '#FF7C00')
                            elif j.hp == 1:
                                draw.ellipse(
                                    ((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                    '#FFFFFF')
                                draw.ellipse(
                                    ((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)),
                                    '#6B3400')
                    elif j.color == 'b':
                        if j.type == 'n':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                         '#808080')
                        elif j.type == 'f':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                         '#808080')
                            draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)),
                                         '#00FF00')
                        elif j.type == 'st':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                         '#808080')
                            draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)),
                                         '#0000FF')
                        elif j.type == 'th':
                            if j.hp == 2:
                                draw.ellipse(
                                    ((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                    '#808080')
                                draw.ellipse(
                                    ((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)),
                                    '#FF7C00')
                            elif j.hp == 1:
                                draw.ellipse(
                                    ((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)),
                                    '#808080')
                                draw.ellipse(
                                    ((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)),
                                    '#6B3400')
        im.save(f'materials/images/{self.guild},{self.channel}.png')

    def can_eat(self, x1, y1, x2, y2):
        if self.matrix[x1][y1] != 'e':
            if self.matrix[x2][y2] != 'e':
                self.matrix[x1][y1].move(x2, y2)
            else:
                print(False)

    def normal_set(self):
        for i in global_list:
            self.SetChecker(*i, self)

    def print(self):
        for i in self.matrix:
            b = ''
            print()
            for j in i:
                b += f'{j}'
                b += '\t'
            print(b)

    def count(self):
        b = 0
        w = 0
        for i in self.matrix:
            for j in i:
                if type(j) != str:
                    if j.color == 'b':
                        b += 1
                    else:
                        w += 1
        return w, b

    def check_win(self):
        a = self.count()
        if min(a) == 0:
            if a.index(0) == 0:
                return 'white_win'
            return 'black_win'
        return False


class NormalChecker:
    def __init__(self, c, x, y, board):  # цвет, тип и координаты
        self.color = c  # "w;b"
        self.x = x
        self.y = y
        self.type = 'n'
        self.board = board  # экзепляр класса

    def __str__(self):
        return f'{self.color}_n_ch'

    def kill(self):  # запускается, если шашка убита
        self.board.matrix[self.x][self.y] = 'e'

    def move(self, xnew, ynew):
        if xnew >= 0 and xnew <= self.board.scale and ynew >= 0 and ynew <= self.board.scale:
            if abs(xnew - self.x) == 1 and abs(ynew - self.y) == 1:
                if self.board.matrix[xnew][ynew] == 'e':
                    self.board.matrix[xnew][ynew] = NormalChecker(self.color, xnew, ynew, self.board)
                    self.board.matrix[self.x][self.y] = 'e'
                    self.x, self.y = xnew, ynew
                else:
                    if self.board.matrix[xnew][ynew].color == self.color:
                        print('Огонь по своим')
                    else:
                        self.__eat(xnew, ynew)
            else:
                print('Неверное расстояние')
        else:
            print('Прыжок за границы')

    def __eat(self, xtarg, ytarg):  # это координаты цели, а не клетки за целью
        self.board.matrix[xtarg][ytarg].kill()
        self.board.matrix[self.x][self.y] = 'e'
        print(self.x + 2 * (-self.x + xtarg), self.y + 2 * (-self.y + ytarg))
        self.board.matrix[self.x + 2 * (-self.x + xtarg)][self.y + 2 * (-self.y + ytarg)] = NormalChecker(self.color,
                                                                                                          self.x,
                                                                                                          self.y,
                                                                                                          self.board)


class ThicChecker:
    def __init__(self, c, x, y, board):  # цвет, тип и координаты
        self.color = c  # "w;b"
        self.x = x
        self.y = y
        self.type = 'th'
        self.board = board  # экзепляр класса
        self.hp = 2  # особенность бронешашки, естся не с первого раза

    def __str__(self):
        return f'{self.color}_t_ch'

    def kill(self):  # запускается, если шашка убита
        print(self.hp)
        self.hp -= 1
        if self.hp <= 0:
            self.board.matrix[self.x][self.y] = 'e'

    def move(self, xnew, ynew):
        if xnew >= 0 and xnew <= self.board.scale and ynew >= 0 and ynew <= self.board.scale:
            if abs(xnew - self.x) == 1 and abs(ynew - self.y) == 1:
                if self.board.matrix[xnew][ynew] == 'e':
                    self.board.matrix[xnew][ynew] = ThicChecker(self.color, xnew, ynew, self.board)
                    self.board.matrix[self.x][self.y] = 'e'
                    self.x, self.y = xnew, ynew
                else:
                    if self.board.matrix[xnew][ynew].color == self.color:
                        print('Огонь по своим')
                    else:
                        self.__eat(xnew, ynew)
            else:
                print('Неверное расстояние')
        else:
            print('Прыжок за границы')

    def __eat(self, xtarg, ytarg):  # это координаты цели, а не клетки за целью
        self.board.matrix[xtarg][ytarg].kill()
        self.board.matrix[self.x][self.y] = 'e'
        if abs(-self.x + xtarg) == 1 and abs(-self.y + ytarg) == 1:
            self.board.matrix[self.x + 2 * (-self.x + xtarg)][self.y + 2 * (-self.y + ytarg)] = ThicChecker(self.color,
                                                                                                            self.x,
                                                                                                            self.y,
                                                                                                            self.board)
        elif abs(-self.x + xtarg) == 2 and abs(-self.y + ytarg) == 2:
            self.board.matrix[self.x + int(1.5 * (-self.x + xtarg))][
                self.y + int(1.5 * (-self.y + ytarg))] = ThicChecker(self.color, self.x, self.y, self.board)


class FastChecker:
    def __init__(self, c, x, y, board):  # цвет, тип и координаты
        self.color = c  # "w;b"
        self.x = x
        self.y = y
        self.type = 'f'
        self.board = board  # экзепляр класса

    def __str__(self):
        return f'{self.color}_f_ch'

    def kill(self):  # запускается, если шашка убита
        self.board.matrix[self.x][self.y] = 'e'

    def move(self, xnew, ynew):
        if xnew >= 0 and xnew <= self.board.scale and ynew >= 0 and ynew <= self.board.scale:
            if abs(xnew - self.x) == 2 and abs(ynew - self.y) == 2 or abs(xnew - self.x) == 2 and abs(
                    ynew - self.y) == 0 or abs(xnew - self.x) == 1 and abs(ynew - self.y) == 1:
                if self.board.matrix[xnew][ynew] == 'e':
                    self.board.matrix[xnew][ynew] = FastChecker(self.color, xnew, ynew, self.board)
                    self.board.matrix[self.x][self.y] = 'e'
                    self.x, self.y = xnew, ynew
                else:
                    if self.board.matrix[xnew][ynew].color == self.color:
                        print('Огонь по своим')
                    else:
                        self.__eat(xnew, ynew)
            else:
                print('Неверное расстояние')
        else:
            print('Прыжок за границы')

    def __eat(self, xtarg, ytarg):  # это координаты цели, а не клетки за целью
        self.board.matrix[xtarg][ytarg].kill()
        self.board.matrix[self.x][self.y] = 'e'
        if abs(-self.x + xtarg) == 1 and abs(-self.y + ytarg) == 1:
            self.board.matrix[self.x + 2 * (-self.x + xtarg)][self.y + 2 * (-self.y + ytarg)] = ThicChecker(self.color,
                                                                                                            self.x,
                                                                                                            self.y,
                                                                                                            self.board)
        elif abs(-self.x + xtarg) == 2 and abs(-self.y + ytarg) == 2:
            self.board.matrix[self.x + int(1.5 * (-self.x + xtarg))][
                self.y + int(1.5 * (-self.y + ytarg))] = ThicChecker(self.color, self.x, self.y, self.board)


class StealthChecker:
    def __init__(self, c, x, y, board):  # цвет, тип и координаты
        self.color = c  # "w;b"
        self.x = x
        self.y = y
        self.type = 'st'
        self.board = board  # экзепляр класса

    def __str__(self):
        return f'{self.color}_st_ch'

    def kill(self):  # запускается, если шашка убита
        self.board.matrix[self.x][self.y] = 'e'

    def move(self, xnew, ynew):
        if xnew >= 0 and xnew <= self.board.scale and ynew >= 0 and ynew <= self.board.scale:
            if abs(xnew - self.x) == 1 and abs(ynew - self.y) == 1 or abs(xnew - self.x) == 1 and abs(
                    ynew - self.y) == 0:
                if self.board.matrix[xnew][ynew] == 'e':
                    self.board.matrix[xnew][ynew] = StealthChecker(self.color, xnew, ynew, self.board)
                    self.board.matrix[self.x][self.y] = 'e'
                    self.x, self.y = xnew, ynew
                else:
                    if self.board.matrix[xnew][ynew].color == self.color:
                        print('Огонь по своим')
                    else:
                        self.__eat(xnew, ynew)
            else:
                print('Неверное расстояние')
        else:
            print('Прыжок за границы')

    def __eat(self, xtarg, ytarg):  # это координаты цели, а не клетки за целью
        self.board.matrix[xtarg][ytarg], self.board.matrix[self.x][self.y] = 'e', 'e'
        self.board.matrix[self.x + 2 * (-self.x + xtarg)][self.y + 2 * (-self.y + ytarg)] = StealthChecker(self.color,
                                                                                                           self.x,
                                                                                                           self.y,
                                                                                                           self.board)


class ClassicBoard:
    def __init__(self, a, b):
        self.field = [[False, True, False, True, False, True, False, True],
                      [True, False, True, False, True, False, True, False],
                      [False, True, False, True, False, True, False, True],
                      [True, False, True, False, True, False, True, False],
                      [False, True, False, True, False, True, False, True],
                      [True, False, True, False, True, False, True, False],
                      [False, True, False, True, False, True, False, True],
                      [True, False, True, False, True, False, True, False]]
        self.whitecount = 12
        self.blackcount = 12
        self.shashki = {'0,0': 'white', '2,0': 'white', '4,0': 'white', '6,0': 'white', '1,1': 'white', '3,1': 'white',
                        '5,1': 'white', '7,1': 'white', '0,2': 'white', '2,2': 'white', '4,2': 'white', '6,2': 'white',
                        '1,5': 'black', '3,5': 'black', '5,5': 'black', '7,5': 'black', '0,6': 'black', '2,6': 'black',
                        '4,6': 'black', '6,6': 'black', '1,7': 'black', '3,7': 'black', '5,7': 'black', '7,7': 'black'}
        self.hod = ['white', 'white_damka']
        self.guild = a
        self.channel = b

    def can_move(self, x, y, newx, newy):
        if newx not in range(0, 8) or newy not in range(0, 8):
            return False
        if f"{x},{y}" not in self.shashki:
            return False
        if self.shashki[f"{x},{y}"] not in self.hod:
            return False
        if self.field[newy][newx]:
            return False
        if self.shashki[f"{x},{y}"] == 'white':
            if abs(newx - x) == newy - y == 1:
                if f"{newx},{newy}" in self.shashki:
                    return False
                else:
                    return 'can_move'
            if abs(newx - x) == abs(newy - y) == 2:  # taks
                deltx = int(x + (newx - x) / 2)
                delty = int(y + (newy - y) / 2)
                if f"{deltx},{delty}" in self.shashki:
                    if self.shashki[f"{deltx},{delty}"] in ['black', 'black_damka']:
                        return 'can_eat'
            return False
        elif self.shashki[f"{x},{y}"] == 'black':
            if abs(newx - x) == -(newy - y) == 1:
                if f"{newx},{newy}" in self.shashki:
                    return False
                else:
                    return 'can_move'
            if abs(newx - x) == abs(newy - y) == 2:  # taks
                deltx = int(x + (newx - x) / 2)
                delty = int(y + (newy - y) / 2)
                if f"{deltx},{delty}" in self.shashki:
                    if self.shashki[f"{deltx},{delty}"] in ['white', 'white_damka']:
                        return 'can_eat'
            return False
        elif self.shashki[f"{x},{y}"] in ['white_damka', 'black_damka']:
            if abs(newx - x) != abs(newy - y):
                return False
            deltax = int((newx - x) / abs(newx - x))
            deltay = int((newy - y) / abs(newy - y))
            shki = [f"{x + deltax * i},{y + deltay * i}" for i in range(1, abs(newx - x) + 1)]
            filtered_shki = list(filter(lambda z: z in self.shashki, shki))
            if len(filtered_shki) == 0:
                return 'can_move'
            elif len(filtered_shki) > 1:
                return False
            else:
                if self.shashki[f"{x},{y}"] == 'white_damka' and self.shashki[filtered_shki[0]] in ['black_damka',
                                                                                                    'black']:
                    return 'can_eat'
                elif self.shashki[filtered_shki[0]] in ['white_damka', 'white']:
                    return 'can_eat'
                else:
                    return False
        else:
            return False

    def move(self, x, y, newx, newy):
        a = self.shashki[f"{x},{y}"]
        self.shashki.pop(f"{x},{y}", None)
        self.shashki[f"{newx},{newy}"] = a
        self.hod = ['black', 'black_damka'].copy() if self.hod == ['white', 'white_damka'] else ['white',
                                                                                                 'white_damka'].copy()

    def eat(self, x, y, newx, newy):
        if self.shashki[f"{x},{y}"] in ['white', 'black']:
            deltx = int(x + (newx - x) / 2)
            delty = int(y + (newy - y) / 2)
            print(deltx, delty)
            a = self.shashki[f"{x},{y}"]
            self.shashki.pop(f"{x},{y}", None)
            self.shashki[f"{newx},{newy}"] = a
            self.shashki.pop(f"{deltx},{delty}", None)
            if a == 'white':
                self.blackcount -= 1
            else:
                self.whitecount -= 1
        elif self.shashki[f"{x},{y}"] in ['white_damka', 'black_damka']:
            deltax = int((newx - x) / abs(newx - x))
            deltay = int((newy - y) / abs(newy - y))
            shki = [f"{x + deltax * i},{y + deltay * i}" for i in range(1, abs(newx - x) + 1)]
            filtered_shki = list(filter(lambda z: z in self.shashki, shki))[0]
            if self.shashki[f"{x},{y}"] == 'white_damka' and self.shashki[filtered_shki] in ['black', 'black_damka'] \
                    or self.shashki[f"{x},{y}"] == 'black_damka' and self.shashki[filtered_shki] in ['white',
                                                                                                     'white_damka']:
                a = self.shashki[f"{x},{y}"]
                self.shashki.pop(f"{x},{y}", None)
                self.shashki[f"{newx},{newy}"] = a
                self.shashki.pop(filtered_shki, None)
                if a == 'white_damka':
                    self.blackcount -= 1
                else:
                    self.whitecount -= 1
        self.hod = ['black', 'black_damka'].copy() if self.hod == ['white', 'white_damka'] else ['white',
                                                                                                 'white_damka'].copy()

    def get_game_field(self):
        im = Image.open("materials/images/res.png")
        draw = ImageDraw.Draw(im)
        for i in self.shashki:
            a, b = [int(j) for j in i.split(',')]
            if self.shashki[i] == 'white':
                draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#FFFFFF')
            elif self.shashki[i] == 'black':
                draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#808080')
            elif self.shashki[i] == 'white_damka':
                draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#FFFFFF')
                draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#FF0000')
            else:
                draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#808080')
                draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#FF0000')
        im.save(f'materials/images/{self.guild},{self.channel}.png')

    def found_damki(self):
        for i in self.shashki:
            a, b = [int(j) for j in i.split(',')]
            if b == 0 and self.shashki[i] == 'black':
                self.shashki[i] = 'black_damka'
            elif b == 7 and self.shashki[i] == 'white':
                self.shashki[i] = 'white_damka'

    def check_win(self):
        if self.whitecount == 0:
            return 'black_win'
        elif self.blackcount == 0:
            return 'white_win'
        else:
            return False


TOKEN = 'ODI1Nzc2NTc1MjA3MTc4Mjcx.YGC2XQ.vb7M8zt6Dz0JZEIrwtqMbmvp8Ls'
bot = commands.Bot(command_prefix='-')
all_games_dict = {}


def delete_game(a, b):
    con = sqlite3.connect("materials/games.db")
    cur = con.cursor()
    cur.execute("""DELETE FROM first WHERE server_id = ? AND channel_id = ?""", (a, b))
    con.commit()
    con.close()


@bot.command(name='start_game')
async def starting(ctx, mode):
    global all_games_dict
    a, b = ctx.message.author.guild.id, ctx.message.channel.id
    c = ctx.message.mentions[0].id
    d = ctx.message.mentions[1].id
    con = sqlite3.connect("materials/games.db")
    cur = con.cursor()
    if not cur.execute("""SELECT white_player_id,black_player_id FROM first
                                WHERE server_id = ? AND channel_id = ?""", (a, b)).fetchone():
        cur.execute("INSERT INTO first(server_id,channel_id,white_player_id,black_player_id) VALUES (?,?,?,?)", (a, b, c, d))
    else:
        all_games_dict.pop([f"{a},{b}"], None)
        cur.execute(f"UPDATE first SET server_id=?,channel_id=?,white_player_id=?,black_player_id=?"
                    f"WHERE server_id=? AND channel_id=?", (a, b, c, d, a, b))
    if not cur.execute(f"""SELECT wins FROM stats
                                    WHERE player_id={c}""").fetchone():
        cur.execute(f"INSERT INTO stats(wins,loses,number_of_games,player_id) VALUES (0,0,0,{c})")
    if not cur.execute(f"""SELECT wins FROM stats WHERE player_id={d}""").fetchone():
        cur.execute(f"INSERT INTO stats(wins,loses,number_of_games,player_id) VALUES (0,0,0,{d})")
    con.commit()
    con.close()
    if mode == 'normal':
        all_games_dict[f"{a},{b}"] = ClassicBoard(a, b)
    else:
        all_games_dict[f"{a},{b}"] = Board(8, a, b)
    all_games_dict[f"{a},{b}"].get_game_field()
    await ctx.send('Игра началась', file=discord.File(f'materials/images/{a},{b}.png'))


@bot.command(name='move')
async def moving(ctx, first, second):
    global all_games_dict
    a, b = ctx.message.author.guild.id, ctx.message.channel.id
    sl = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    x1, y1 = int(first[0]), sl[first[1]]
    x2, y2 = int(second[0]), sl[second[1]]
    con = sqlite3.connect("materials/games.db")
    cur = con.cursor()
    result = cur.execute("""SELECT white_player_id,black_player_id FROM first
                                WHERE server_id = ? AND channel_id = ?""", (a, b)).fetchone()
    con.close()
    hod = all_games_dict[f"{a},{b}"].hod
    if hod == 0:
        hod = ['black']
    elif hod == 1:
        hod = ['white']
    if (ctx.message.author.id == result[1] and 'white' in hod) or \
            ctx.message.author.id == result[0] and 'black' in hod:
        await ctx.send('Сейчас ходит другой игрок')
        return
    if isinstance(all_games_dict[f"{a},{b}"], Board):
        print(1)
        print(all_games_dict[f"{a},{b}"].can_move(y1, x1, y2, x2))
    else:
        flag = all_games_dict[f"{a},{b}"].can_move(x1, y1, x2, y2)
        if flag == 'can_move':
            all_games_dict[f"{a},{b}"].move(x1, y1, x2, y2)
        elif flag == 'can_eat':
            all_games_dict[f"{a},{b}"].eat(x1, y1, x2, y2)
    if not isinstance(all_games_dict[f"{a},{b}"], Board):
        all_games_dict[f"{a},{b}"].found_damki()
    all_games_dict[f"{a},{b}"].get_game_field()
    flag_winner = all_games_dict[f"{a},{b}"].check_win()
    con = sqlite3.connect("materials/games.db")
    cur = con.cursor()
    if flag_winner == 'white_win':
        result = cur.execute("""SELECT white_player_id,black_player_id FROM first
                                        WHERE server_id = ? AND channel_id = ?""", (a, b)).fetchone()
        cur.execute(f"UPDATE stats SET number_of_games=number_of_games+1, wins=wins+1 WHERE player_id={result[0]}")
        con.commit()
        await ctx.send('Белые победили', file=discord.File(f'materials/images/{a},{b}.png'))
        del all_games_dict[f"{a},{b}"]
        delete_game(a, b)
    elif flag_winner == 'black_win':
        result = cur.execute("""SELECT white_player_id,black_player_id FROM first
                                                WHERE server_id = ? AND channel_id = ?""", (a, b)).fetchone()
        cur.execute(f"UPDATE stats SET number_of_games=number_of_games+1, wins=wins+1 WHERE player_id={result[1]}")
        con.commit()
        await ctx.send('Черные победили', file=discord.File(f'materials/images/{a},{b}.png'))
        del all_games_dict[f"{a},{b}"]
        delete_game(a, b)
    else:
        await ctx.send('', file=discord.File(f'materials/images/{a},{b}.png'))
    con.close()


@bot.command(name='get_stat')
async def stat(ctx):
    con = sqlite3.connect("materials/games.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT number_of_games,wins,loses FROM stats
                                    WHERE player_id={ctx.message.author.id}""").fetchone()
    await ctx.send(f"Games: {result[0]}, Wins: {result[1]}, Loses: {result[2]}")


@bot.command(name='clear_all')
async def clear_all(ctx):
    global all_games_dict
    os.remove("materials/games.db")
    con = sqlite3.connect("materials/games.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS first(
       server_id INT,
       channel_id INT,
       white_player_id INT,
       black_player_id INT);
    """)
    con.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS stats(
       player_id INT,
       number_of_games INT,
       wins INT,
       loses INT);
    """)
    con.commit()
    con.close()
    del all_games_dict
    all_games_dict = {}
    await ctx.send('Все данные очищены')


bot.run(TOKEN)
# 255, 231, 130

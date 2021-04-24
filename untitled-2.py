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
    return(l2.index(form[1]), l1.index(form[0]))

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
        if self.matrix[x1][y1] != 'e' and hod_check == self.matrix[x1][y1].color:
            if self.matrix[x2][y2] == 'e':
                self.matrix[x1][y1].move(x2, y2)
            else:
                print(False)
        
    def get_game_field(self): 
        im = Image.open("materials/images/res.png")
        draw = ImageDraw.Draw(im)
        for i in self.matrix:
            for j in i:
                if type(j) != str:
                    a, b = j.y, j.x
                    if j.color == 'w':
                        if j.type == 'n':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#FFFFFF')
                        elif j.type == 'f':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#FFFFFF')
                            draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#00FF00')
                        elif j.type == 'st':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#FFFFFF')
                            draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#0000FF')
                        elif j.type == 'th':
                            if j.hp == 2:
                                draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#FFFFFF')
                                draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#FF7C00')
                            elif hp == 1:
                                draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#FFFFFF')
                                draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#6B3400')
                    elif j.color == 'b':
                        if j.type == 'n':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#808080')
                        elif j.type == 'f':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#808080')
                            draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#00FF00')
                        elif j.type == 'st':
                            draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#808080')
                            draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#0000FF')
                        elif j.type == 'th':
                            if j.hp == 2:
                                draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#808080')
                                draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#FF7C00')
                            elif hp == 1:
                                draw.ellipse(((int(50 * a) + 27, int(50 * b) + 27), (int(50 * a) + 73, int(50 * b) + 73)), '#808080')
                                draw.ellipse(((int(50 * a) + 37, int(50 * b) + 37), (int(50 * a) + 63, int(50 * b) + 63)), '#6B3400')
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

    def wincheck(self):
        a = ['w', 'b']
        return min(self.count()) == 0, a[self.count.index(0)]



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
        self.board.matrix[self.x + 2 * (-self.x + xtarg)][self.y + 2 * (-self.y + ytarg)] = NormalChecker(self.color, self.x, self.y, self.board)
        
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
            self.board.matrix[self.x + 2 * (-self.x + xtarg)][self.y + 2 * (-self.y + ytarg)] = ThicChecker(self.color, self.x, self.y, self.board)
        elif abs(-self.x + xtarg) == 2 and abs(-self.y + ytarg) == 2:
            self.board.matrix[self.x + int(1.5 * (-self.x + xtarg))][self.y + int(1.5 * (-self.y + ytarg))] = ThicChecker(self.color, self.x, self.y, self.board)


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
            if abs(xnew - self.x) == 2 and abs(ynew - self.y) == 2 or abs(xnew - self.x) == 2 and abs(ynew - self.y) == 0 or abs(xnew - self.x) == 1 and abs(ynew - self.y) == 1:
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
            self.board.matrix[self.x + 2 * (-self.x + xtarg)][self.y + 2 * (-self.y + ytarg)] = ThicChecker(self.color, self.x, self.y, self.board)
        elif abs(-self.x + xtarg) == 2 and abs(-self.y + ytarg) == 2:
            self.board.matrix[self.x + int(1.5 * (-self.x + xtarg))][self.y + int(1.5 * (-self.y + ytarg))] = ThicChecker(self.color, self.x, self.y, self.board)


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
            if abs(xnew - self.x) == 1 and abs(ynew - self.y) == 1 or abs(xnew - self.x) == 1 and abs(ynew - self.y) == 0:
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
        self.board.matrix[self.x + 2 * (-self.x + xtarg)][self.y + 2 * (-self.y + ytarg)] = StealthChecker(self.color, self.x, self.y, self.board)

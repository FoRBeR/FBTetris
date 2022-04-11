from datetime import datetime
from random import randint
import numpy as np

# отвечает за поле и игру: создание фигур, их движение, проверка и удаление линий
class Field:
    def __init__(self):
        # таймер
        self.stopwatch = Stopwatch()
        # счетчики
        self.score = 0
        self.count_of_lines = 0
        self.count_of_figures = 0
        # поле
        self.field = np.full(300, 1).reshape(25, 12)
        self.field[0:24, 1:11] *= 0
        # счетчик фигур, нужен, чтобы не получилось ситуации, когда линии не спавнятся
        self.line_counter = 0
        self.next_fig = randint(1, 7)
        self.fig_code = randint(1, 7)
        while self.next_fig == self.fig_code:
            self.next_fig = randint(1, 7)
        self.figure = Figure(self.next_fig)
        self.spawn()

    # создание фигуры
    def spawn(self):
        self.count_of_figures += 1
        self.line_counter += 1
        self.fig_code = self.next_fig
        if self.line_counter == 10:
            self.line_counter = 0
            self.next_fig = 1
        while self.next_fig == self.fig_code:
            self.next_fig = randint(1, 7)
            if self.next_fig == 1:
                self.line_counter = 0
        self.figure = Figure(self.fig_code)
        y = self.figure.location[0]
        x = self.figure.location[1]
        if self.fig_code == 1:
            self.field[y:y + 4, x:x + 1] -= 8
        elif self.fig_code == 2:
            self.field[y:y + 2, x:x + 2] -= 8
        else:
            self.field[y:y + 3, x:x + 3] += self.figure.fig

    def fig_rotate(self, direction: int):
        if self.fig_code == 1 and self.figure.location[1] >= 8 and self.figure.rotate % 2 == 0:
            mem = self.figure.location[1]
            self.figure_update(False)
            self.figure.location[0] += 3
            self.figure.location[1] = 7
            self.figure.rotate = 1
            self.figure_update(True)
            if self.check():
                self.figure_update(False)
                self.figure.location[0] -= 3
                self.figure.location[1] = mem
                self.figure.rotate = 0
                self.figure_update(True)
            return
        elif self.fig_code == 1 and self.figure.location[1] <= 2 and self.figure.rotate % 2 == 0:
            mem = self.figure.location[1]
            self.figure_update(False)
            self.figure.location[0] += 3
            self.figure.location[1] = 1
            self.figure.rotate = 1
            self.figure_update(True)
            if self.check():
                self.figure_update(False)
                self.figure.location[0] -= 3
                self.figure.location[1] = mem
                self.figure.rotate = 0
                self.figure_update(True)
            return
        elif self.fig_code >= 3 and self.figure.location[1] == 9:
            self.move('l')
        elif self.fig_code >= 3 and self.figure.location[1] == 0:
            self.move('r')
        self.figure_update(False)
        self.figure.rot(direction)
        self.figure_update(True)
        if self.check():
            self.figure_update(False)
            self.figure.rot(-direction)
            self.figure_update(True)

    def figure_update(self, add: bool):
        y = self.figure.location[0]
        x = self.figure.location[1]
        if add:
            if self.fig_code == 1:
                if self.figure.rotate % 2 == 0:
                    self.field[y:y + 4, x:x + 1] -= 8
                else:
                    self.field[y:y + 1, x:x + 4] -= 8
            elif self.fig_code == 2:
                self.field[y:y + 2, x:x + 2] -= 8
            else:
                self.field[y:y + 3, x:x + 3] += self.figure.fig
        else:
            if self.fig_code == 1:
                if self.figure.rotate % 2 == 0:
                    self.field[y:y + 4, x:x + 1] += 8
                else:
                    self.field[y:y + 1, x:x + 4] += 8
            elif self.fig_code == 2:
                self.field[y:y + 2, x:x + 2] += 8
            else:
                self.field[y:y + 3, x:x + 3] -= self.figure.fig

    # есть ли столкновения
    def check(self):
        a = self.field.copy()
        a = a.reshape(-1)
        a = a[a < 0]
        c = np.any(a > -8)
        return c

    # отвечает за все движения, direction принимает значения l, d, r
    def move(self, direction='d'):
        start_field = self.field.copy()
        self.figure_update(False)
        if direction == 'd':
            self.figure.location[0] += 1
            self.figure_update(True)
        elif direction == 'r':
            if self.figure.location[1] != 9 or self.fig_code == 1 and self.figure.location[1] != 10:
                self.figure.location[1] += 1
            self.figure_update(True)
            if self.check():
                self.figure.location[1] -= 1
                self.field = start_field.copy()
        elif direction == 'l':
            if self.figure.location[1] != 0:
                self.figure.location[1] -= 1
            self.figure_update(True)
            if self.check():
                self.figure.location[1] += 1
                self.field = start_field.copy()
        if self.check():
            self.field = start_field.copy()
            self.field[self.field == -8] = self.fig_code
            self.line_check()
            if self.game_end():
                return True
            self.spawn()

    def game_end(self):
        a = self.field[:4, 1:11]
        if a.sum() == 0:
            return False
        else:
            self.count_of_figures -= 1
            return True

    # ищет линии, что надо удалить, возвращает список с их номерами
    def line_search(self):
        found = []
        for i in range(23, 3, -1):
            a = self.field[i:i + 1, 1:11]
            if np.prod(a) != 0:
                found.append(i)
        return found

    # удаляет линии
    def line_delete(self, number):
        self.count_of_lines += 1
        self.field[1:number + 1, 1:11] = self.field[0:number, 1:11].copy()

    # соединяет предыдущие функции, также начисляет очки
    # 100 300 700 1500
    def line_check(self):
        l = self.line_search()
        if len(l) == 1:
            self.score += 100
        elif len(l) == 2:
            self.score += 300
        elif len(l) == 3:
            self.score += 700
        elif len(l) == 4:
            self.score += 1500
        for num in range(len(l) - 1, -1, -1):
            self.line_delete(l[num])


# отвечает за саму фигуру, фигуры имеют порядковые номера от 1 до 7
class Figure:
    def __init__(self, code: int):
        # порядковый номер
        self.code = code
        # значение прокрутки этой фигуры
        self.rotate = 0
        self.location = [1, 5]  # представляют собой 2 числа для среза
        # создание фигуры
        if self.code == 1:
            self.fig = np.array([[-8, -8, -8, -8]])
            self.location = [0, 6]
        elif self.code == 2:
            self.fig = np.array([-8, -8, -8, -8]).reshape(2, 2)
            self.location = [2, 5]
        elif self.code == 3:
            self.fig = np.array([0, 0, 0, 0, -8, 0, -8, -8, -8]).reshape(3, 3)
        elif self.code == 4:
            self.fig = np.array([0, 0, 0, -8, 0, 0, -8, -8, -8]).reshape(3, 3)
        elif self.code == 5:
            self.fig = np.array([0, 0, 0, 0, 0, -8, -8, -8, -8]).reshape(3, 3)
        elif self.code == 6:
            self.fig = np.array([0, 0, 0, -8, -8, 0, 0, -8, -8]).reshape(3, 3)
        elif self.code == 7:
            self.fig = np.array([0, 0, 0, 0, -8, -8, -8, -8, 0]).reshape(3, 3)
        self.fig_temp = self.fig.copy()

    # direction: -1 - по часовой, 1 - против часовой
    def rot(self, direction: int):
        self.rotate += direction
        if self.rotate >= 3:
            self.rotate -= 4
        elif self.rotate <= -3:
            self.rotate += 4
        if self.rotate == 0:
            self.fig = self.fig_temp.copy()
            return
        if self.code == 1:
            if self.rotate % 2 == 0:
                self.location[0] -= 2
                self.location[1] += 2
                self.fig = self.fig_temp.copy()
            else:
                self.location[0] += 2
                self.location[1] -= 2
                self.fig = np.rot90(self.fig_temp)
        elif self.code >= 3:
            self.fig = self.fig_temp.copy()
            self.fig = np.delete(self.fig, 0, axis=0)
            self.fig = np.rot90(self.fig, self.rotate)
            b = np.array([[0, 0, 0]])
            if self.rotate % 2 == 0:
                self.fig = np.insert(self.fig, 0, values=b, axis=0)
            elif self.rotate == 1:
                self.fig = np.c_[self.fig, b.T]
            elif self.rotate == -1:
                self.fig = np.insert(self.fig, 0, values=b, axis=1)


# мой класс-секундомер
# возможности: пауза, снятие с паузы, получение времени с момента создания объекта
class Stopwatch:
    def __init__(self):
        self.start_time = datetime.now()
        self.is_pause = False
        self.start_pause_time = None

    def pause(self):
        if not self.is_pause:
            self.start_pause_time = datetime.now()
            self.is_pause = True

    def play(self):
        if self.is_pause:
            self.is_pause = False
            pause_time = self.start_pause_time - datetime.now()
            self.start_time = self.start_time - pause_time
            self.start_pause_time = None

    def time(self):
        if self.is_pause:
            pause_time = self.start_pause_time - datetime.now()
            all_time = self.start_time - pause_time
        else:
            all_time = self.start_time
        return datetime.now() - all_time


if __name__ == "__main__":
    x = Stopwatch()
    print(x.time())

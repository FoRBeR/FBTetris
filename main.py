import pygame
from account import User
from game import Field
from next_figures import next_figure_surface, figures as next_figures, rects as next_figures_rects, colors, PATH
from time import time
import os

pygame.init()

# окно с игрой
class GameWindow:
    def __init__(self):
        self.speed = 1000
        self.save_speed = self.speed
        pygame.time.set_timer(pygame.USEREVENT, self.speed)
        self.is_work = False
        self.ad_buttons_time = 0
        self.which_button_ad = True  # True is A | False is D
        self.game_field = Field()
        self.g_bg = pygame.image.load(f"{PATH}/pic/background_g.bmp").convert()
        self.bg = pygame.image.load(f"{PATH}/pic/bg.bmp").convert()
        self.clear_bar = pygame.image.load(f"{PATH}/pic/bar.bmp").convert()
        self.game_surf = pygame.Surface((300, 600))
        self.game_surf.blit(self.g_bg, (0, 0))
        self.next_figure = pygame.Surface((120, 120))
        self.bar = pygame.Surface((194, 600))
        self.bar.blit(self.clear_bar, (0, 0))
        self.squares = []
        for i in range(7):
            self.squares.append(pygame.Surface((28, 28)))
            pygame.draw.rect(self.squares[i], colors[str(i + 1)], (0, 0, 28, 28))

    def new_game(self):
        self.speed = 1000
        self.save_speed = self.speed
        self.is_work = True
        self.ad_buttons_time = 0
        self.which_button_ad = True  # True is A | False is D
        self.game_field = Field()

    def event_work(self, event):
        if event.type == pygame.USEREVENT:
            self.speed -= 1
            pygame.time.set_timer(pygame.USEREVENT, self.speed)
            if self.game_field.move():
                return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.game_field.move('l')
                self.ad_buttons_time = time()
                self.which_button_ad = True
            elif event.key == pygame.K_d:
                self.game_field.move('r')
                self.ad_buttons_time = time()
                self.which_button_ad = False
            elif event.key == pygame.K_s:
                self.save_speed = self.speed
                self.speed = 100
                pygame.time.set_timer(pygame.USEREVENT, self.speed)
            elif event.key == pygame.K_w:
                self.game_field.fig_rotate(-1)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.speed = self.save_speed
            elif event.key == pygame.K_a:
                self.ad_buttons_time = 0
            elif event.key == pygame.K_d:
                self.ad_buttons_time = 0
        return False

    def upd_surface(self):
        # слежение за зажатием клавиш A D
        if self.ad_buttons_time and time() - self.ad_buttons_time > 0.5:
            self.ad_buttons_time += 0.5
            if self.which_button_ad:
                self.game_field.move('l')
            else:
                self.game_field.move('r')
        # отрисовка игрового поля
        self.game_surf.blit(self.g_bg, (0, 0))
        field = self.game_field.field[4:24, 1:11]
        for i in range(20):
            for j in range(10):
                if field[i, j] > 0:
                    self.game_surf.blit(self.squares[field[i, j] - 1], (30 * j + 1, 30 * i + 1))
                elif field[i, j] == -8:
                    self.game_surf.blit(self.squares[self.game_field.fig_code - 1], (30 * j + 1, 30 * i + 1))
        self.bar.blit(next_figure_surface(self.game_field.next_fig, next_figures, next_figures_rects), (39, 250))
        return self.game_surf, self.bar

# окно с началом/концом игры
class EndWindow:
    def __init__(self):
        self.is_work = True
        self.is_app_start = True
        self.end_surf = pygame.image.load(f"{PATH}/pic/end.bmp")
        self.start_surf = pygame.image.load(f"{PATH}/pic/start.bmp")
        self.clear_end_surf = self.end_surf.copy()
        self.font = pygame.font.Font(f"{PATH}/font/CascadiaCode-ExtraLight.ttf", 17)

    def upd_surface(self, score, lines, figures, game_time):
        if self.is_app_start:
            return self.start_surf
        else:
            self.end_surf = self.clear_end_surf.copy()
            self.end_surf.set_colorkey((255, 255, 255))
            pygame.draw.rect(self.end_surf, (247, 241, 215), (122, 224, 178, 46))
            pygame.draw.rect(self.end_surf, (247, 241, 215), (140, 273, 160, 20))
            pygame.draw.rect(self.end_surf, (247, 241, 215), (112, 296, 188, 28))
            text = self.font.render(str(score), False, (0, 0, 0),
                                    (247, 241, 215))
            self.end_surf.blit(text, (124, 223))
            text = self.font.render(str(lines), False, (0, 0, 0),
                                    (247, 241, 215))
            self.end_surf.blit(text, (124, 247))
            text = self.font.render(str(figures), False, (0, 0, 0),
                                    (247, 241, 215))
            self.end_surf.blit(text, (147, 271))
            text = self.font.render(str(game_time)[:-5], False, (0, 0, 0),
                                    (247, 241, 215))
            self.end_surf.blit(text, (117, 298))
            return self.end_surf

# окно паузы
class PauseWindow:
    def __init__(self):
        self.is_work = False
        self.pause_surf = pygame.Surface((300, 600))
        self.pause_surf.fill((247, 241, 215))
        self.pause_surf.set_alpha(125)
        self.pause_surf_rect = self.pause_surf.get_rect(x=198, y=2)
        self.continue_button = pygame.image.load(f"{PATH}/pic/continue_button.bmp")
        self.continue_button.set_colorkey((255, 255, 255))

# окно таблицы лидеров
class HighscoresWindow:
    def __init__(self):
        self.is_work = False
        self.font = pygame.font.Font(f"{PATH}/font/CascadiaCode-ExtraLight.ttf", 17)
        self.hs_clean_surf = pygame.image.load(f"{PATH}/pic/highscores.bmp")
        self.hs_error_surf = pygame.image.load(f"{PATH}/pic/highscores_error.bmp")
        self.hs_surf = pygame.Surface((300, 600))

    def upd_surface(self, hs_dict):
        if not control.user.connection:
            control.user.load()
            if not control.user.connection:
                self.hs_surf.blit(self.hs_error_surf, (0, 0))
                return self.hs_surf
            else:
                hs_dict = control.user.data
        lead = hs_dict['Leaders']
        self.hs_surf.blit(self.hs_clean_surf, (0, 0))
        text = self.font.render(lead[0], False, (0, 0, 0))
        self.hs_surf.blit(text, (103, 91))
        text = self.font.render(str(hs_dict[lead[0]]['score']), False, (0, 0, 0))
        self.hs_surf.blit(text, (103, 123))
        text = self.font.render(str(hs_dict[lead[0]]['lines']), False, (0, 0, 0))
        self.hs_surf.blit(text, (103, 142))
        text = self.font.render(str(hs_dict[lead[0]]['figures']), False, (0, 0, 0))
        self.hs_surf.blit(text, (122, 161))

        text = self.font.render(lead[1], False, (0, 0, 0))
        self.hs_surf.blit(text, (113, 193))
        text = self.font.render(str(hs_dict[lead[1]]['score']), False, (0, 0, 0))
        self.hs_surf.blit(text, (103, 226))
        text = self.font.render(str(hs_dict[lead[1]]['lines']), False, (0, 0, 0))
        self.hs_surf.blit(text, (103, 245))
        text = self.font.render(str(hs_dict[lead[1]]['figures']), False, (0, 0, 0))
        self.hs_surf.blit(text, (122, 264))

        text = self.font.render(lead[2], False, (0, 0, 0))
        self.hs_surf.blit(text, (103, 297))
        text = self.font.render(str(hs_dict[lead[2]]['score']), False, (0, 0, 0))
        self.hs_surf.blit(text, (103, 329))
        text = self.font.render(str(hs_dict[lead[2]]['lines']), False, (0, 0, 0))
        self.hs_surf.blit(text, (103, 348))
        text = self.font.render(str(hs_dict[lead[2]]['figures']), False, (0, 0, 0))
        self.hs_surf.blit(text, (122, 367))

        return self.hs_surf

# окно входа
class LogWindow:
    def __init__(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)
        self.is_work = False
        self.font = pygame.font.Font(f"{PATH}/font/CascadiaCode-ExtraLight.ttf", 17)
        self.mfont = pygame.font.Font(f"{PATH}/font/CascadiaCode-ExtraLight.ttf", 10)
        self.log_surf = pygame.image.load(f"{PATH}/pic/log_in.bmp")
        self.cursor = pygame.Surface((1, 22))
        self.cursor.fill((0, 0, 0))
        self.cursor.set_alpha(255)
        self.log_name_rect = pygame.Rect((310, 99, 175, 30))
        self.log_pw_rect = pygame.Rect((310, 161, 175, 30))
        self.log_button = pygame.Rect((257, 233, 183, 38))
        self.is_log_name_input = False
        self.is_log_pw_input = False
        self.login = ''
        self.pw = ''

    def event_work(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cursor.set_alpha(255)
            pygame.time.set_timer(pygame.USEREVENT + 1, 500)
            self.is_log_name_input = True if self.log_name_rect.collidepoint(event.pos) else False
            self.is_log_pw_input = True if self.log_pw_rect.collidepoint(event.pos) else False
            if self.log_button.collidepoint(event.pos):
                if self.login == '' or self.pw == '':
                    text = self.mfont.render('Please, enter your username and password', False, (0, 0, 0))
                    self.log_surf.blit(text, (25, 280))
                elif not control.user.connection:
                    control.user.load()
                    if not control.user.connection:
                        text = self.mfont.render('Check your internet connection', False, (0, 0, 0))
                        self.log_surf.blit(text, (40, 280))
                    else:
                        if self.event_work(event):
                            return True
                elif not control.user.log_in(self.login, self.pw):
                    text = self.mfont.render('Username and password are incorrect', False, (0, 0, 0))
                    self.log_surf.blit(text, (40, 280))
                else:
                    # вошли в систему
                    pygame.draw.rect(self.log_surf, (239, 228, 176), (40, 280, 250, 20))
                    self.is_log_name_input = False
                    self.is_log_pw_input = False
                    self.login = ''
                    self.pw = ''
                    return True
        elif event.type == pygame.KEYDOWN:
            text = self.login if self.is_log_name_input else self.pw
            if len(text) < 15:
                if event.key == pygame.K_0 or event.key == pygame.K_KP_0:
                    text += '0'
                elif event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                    text += '1'
                elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    text += '2'
                elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                    text += '3'
                elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                    text += '4'
                elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                    text += '5'
                elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                    text += '6'
                elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                    text += '7'
                elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                    text += '8'
                elif event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                    text += '9'
                elif event.key == pygame.K_q:
                    text += 'q'
                elif event.key == pygame.K_w:
                    text += 'w'
                elif event.key == pygame.K_e:
                    text += 'e'
                elif event.key == pygame.K_r:
                    text += 'r'
                elif event.key == pygame.K_t:
                    text += 't'
                elif event.key == pygame.K_y:
                    text += 'y'
                elif event.key == pygame.K_u:
                    text += 'u'
                elif event.key == pygame.K_i:
                    text += 'i'
                elif event.key == pygame.K_o:
                    text += 'o'
                elif event.key == pygame.K_p:
                    text += 'p'
                elif event.key == pygame.K_a:
                    text += 'a'
                elif event.key == pygame.K_s:
                    text += 's'
                elif event.key == pygame.K_d:
                    text += 'd'
                elif event.key == pygame.K_f:
                    text += 'f'
                elif event.key == pygame.K_g:
                    text += 'g'
                elif event.key == pygame.K_h:
                    text += 'h'
                elif event.key == pygame.K_j:
                    text += 'j'
                elif event.key == pygame.K_k:
                    text += 'k'
                elif event.key == pygame.K_l:
                    text += 'l'
                elif event.key == pygame.K_z:
                    text += 'z'
                elif event.key == pygame.K_x:
                    text += 'x'
                elif event.key == pygame.K_c:
                    text += 'c'
                elif event.key == pygame.K_v:
                    text += 'v'
                elif event.key == pygame.K_b:
                    text += 'b'
                elif event.key == pygame.K_n:
                    text += 'n'
                elif event.key == pygame.K_m:
                    text += 'm'
                elif event.key == pygame.K_SPACE:
                    text += ' '
            if event.key == pygame.K_BACKSPACE:
                if text != '':
                    text = text[:-1]
                    pygame.time.set_timer(pygame.USEREVENT + 2, 500)
            if self.is_log_name_input:
                self.login = text
            else:
                self.pw = text
            self.cursor.set_alpha(255)
            pygame.time.set_timer(pygame.USEREVENT + 1, 500)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)
        elif event.type == pygame.USEREVENT + 1:
            if self.cursor.get_alpha() == 255:
                self.cursor.set_alpha(0)
            else:
                self.cursor.set_alpha(255)
        elif event.type == pygame.USEREVENT + 2:
            text = self.login if self.is_log_name_input else self.pw
            if text != '':
                text = text[:-1]
                pygame.time.set_timer(pygame.USEREVENT + 2, 200)
                self.cursor.set_alpha(255)
                pygame.time.set_timer(pygame.USEREVENT + 1, 500)
                if self.is_log_name_input:
                    self.login = text
                else:
                    self.pw = text
        return False

    def upd_surface(self):
        # закрашивание места для письма
        pygame.draw.rect(self.log_surf, (242, 240, 219), (112, 97, 175, 30))
        pygame.draw.rect(self.log_surf, (242, 240, 219), (112, 159, 175, 30))
        # постановка курсора если 0 символов
        if self.is_log_name_input and len(self.login) == 0:
            self.log_surf.blit(self.cursor, (117, 101))
        if self.is_log_pw_input and len(self.pw) == 0:
            self.log_surf.blit(self.cursor, (117, 163))
        # отрисовка имени и пароля + их курсоров
        if len(self.login) != 0:
            text_login = self.font.render(self.login, False, (0, 0, 0))
            login_rect = text_login.get_rect(x=118, y=101)
            if self.is_log_name_input:
                self.log_surf.blit(self.cursor, login_rect.topright)
            login_rect.x, login_rect.y = 116, 103
            self.log_surf.blit(text_login, login_rect)
        if len(self.pw) != 0:
            text = ''
            for letter in self.pw:
                text += '*'
            text_pw = self.font.render(text, False, (0, 0, 0))
            pw_rect = text_pw.get_rect(x=116, y=163)
            if self.is_log_pw_input:
                self.log_surf.blit(self.cursor, pw_rect.topright)
            pw_rect.y = 165
            self.log_surf.blit(text_pw, pw_rect)
        return self.log_surf

# окно регистрации
class SignWindow(LogWindow):
    def __init__(self):
        super().__init__()
        self.log_surf = pygame.image.load(f"{PATH}/pic/sign_in.bmp")
        text = self.font.render('show password', False, (0, 0, 0))
        self.log_surf.blit(text, (95, 200))
        self.clear_log_surf = self.log_surf.copy()
        self.show_pw_rect = pygame.Rect((267, 203, 18, 18))
        self.is_pw_showed = False

    def event_work(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cursor.set_alpha(255)
            pygame.time.set_timer(pygame.USEREVENT + 1, 500)
            self.is_log_name_input = True if self.log_name_rect.collidepoint(event.pos) else False
            self.is_log_pw_input = True if self.log_pw_rect.collidepoint(event.pos) else False
            if self.show_pw_rect.collidepoint(event.pos):
                self.is_pw_showed = not self.is_pw_showed
            if self.log_button.collidepoint(event.pos):
                if self.login == '' or self.pw == '':
                    self.log_surf = self.clear_log_surf.copy()
                    text = self.mfont.render('Please, enter username and password', False, (0, 0, 0))
                    self.log_surf.blit(text, (25, 280))
                elif not control.user.connection:
                    control.user.load()
                    if not control.user.connection:
                        self.log_surf = self.clear_log_surf.copy()
                        text = self.mfont.render('Check your internet connection', False, (0, 0, 0))
                        self.log_surf.blit(text, (40, 280))
                    else:
                        if self.event_work(event):
                            return True
                elif not control.user.sign_up(self.login, self.pw):
                    self.log_surf = self.clear_log_surf.copy()
                    text = self.mfont.render('Username has already been used', False, (0, 0, 0))
                    self.log_surf.blit(text, (40, 280))
                else:
                    # вошли в систему
                    self.is_log_name_input = False
                    self.is_log_pw_input = False
                    self.login = ''
                    self.pw = ''
                    return True
        else:
            super().event_work(event)

    def upd_surface(self):
        self.log_surf = super().upd_surface()
        if self.is_pw_showed:
            pygame.draw.rect(self.log_surf, (223, 201, 94), (73, 205, 10, 10))
            if len(self.pw) != 0:
                pygame.draw.rect(self.log_surf, (242, 240, 219), (112, 159, 175, 30))
                text_pw = self.font.render(self.pw, False, (0, 0, 0))
                pw_rect = text_pw.get_rect(x=116, y=163)
                if self.is_log_pw_input:
                    self.log_surf.blit(self.cursor, pw_rect.topright)
                pw_rect.y = 165
                self.log_surf.blit(text_pw, pw_rect)
        else:
            pygame.draw.rect(self.log_surf, (242, 240, 219), (73, 205, 10, 10))
        return self.log_surf

# контролирующий класс
class ControlClass:
    def __init__(self):
        self.end_game = True
        # загрузка изображений
        self.main_surface = pygame.Surface((500, 604))
        self.main_surface.fill((239, 228, 176))
        self.bar = pygame.Surface((194, 600))
        self.bar_rect = self.bar.get_rect(x=2, y=2)
        self.clear_bar = pygame.image.load(f"{PATH}/pic/bar.bmp").convert()
        # кнопки
        self.ng_rect = pygame.Rect((24, 81, 150, 37))
        self.pause_rect = pygame.Rect((24, 118, 150, 36))
        self.hs_rect = pygame.Rect((24, 154, 150, 36))
        self.log_button = pygame.image.load(f"{PATH}/pic/Log_button.bmp").convert()
        self.log_rect = self.log_button.get_rect(x=22, y=188)
        self.sign_button = pygame.image.load(f"{PATH}/pic/Sign_button.bmp").convert()
        self.sign_rect = self.sign_button.get_rect(x=97, y=188)
        self.log_out_button = pygame.image.load(f"{PATH}/pic/Log_out_button.bmp").convert()
        self.log_out_rect = self.log_out_button.get_rect(x=22, y=188)
        # создание нужных переменных
        self.game_window = GameWindow()
        self.end_window = EndWindow()
        self.pause_window = PauseWindow()
        self.highscores_window = HighscoresWindow()
        self.log_window = LogWindow()
        self.sign_window = SignWindow()
        self.user = User()
        # сохраняю поверхность игры, чтобы реализовать прозрачную поверхность паузы, но не перерисовывать каждый раз
        self.saved_pause_surface = None

    # включает определенное окно, выключает остальные
    def turn_on(self, window):
        if window == self.game_window:
            self.game_window.game_field.stopwatch.play()
        elif self.game_window.is_work:
            self.game_window.game_field.stopwatch.pause()
        self.end_window.is_work = False
        self.game_window.is_work = False
        self.pause_window.is_work = False
        self.highscores_window.is_work = False
        self.log_window.is_work = False
        self.sign_window.is_work = False
        window.is_work = True

    # включает окно window если включено if_window, иначе включает if_window
    def turn_on_if(self, window, if_window):
        if if_window.is_work:
            self.turn_on(window)
        else:
            self.turn_on(if_window)

    def control_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.user.upd(self.game_window.game_field.score, self.game_window.game_field.count_of_lines,
                              self.game_window.game_field.count_of_figures)
                self.user.unload()
                exit()
            elif event.type == pygame.USEREVENT and self.game_window.is_work:
                if self.game_window.event_work(event):
                    self.end_game = True
                    self.turn_on(self.end_window)
                    self.user.upd(self.game_window.game_field.score, self.game_window.game_field.count_of_lines,
                                  self.game_window.game_field.count_of_figures)
            elif (event.type == pygame.USEREVENT + 1 or event.type == pygame.USEREVENT + 2) and self.log_window.is_work:
                self.log_window.event_work(event)
            elif (
                    event.type == pygame.USEREVENT + 1 or event.type == pygame.USEREVENT + 2) and self.sign_window.is_work:
                self.sign_window.event_work(event)
            elif event.type == pygame.KEYDOWN and self.game_window.is_work:
                if event.key == pygame.K_p:
                    self.turn_on(self.pause_window)
                elif event.key == pygame.K_h:
                    self.turn_on(self.highscores_window)
                else:
                    if self.game_window.event_work(event):
                        self.turn_on(self.end_window)
            elif event.type == pygame.KEYDOWN and self.log_window.is_work and (
                    self.log_window.is_log_name_input or self.log_window.is_log_pw_input):
                self.log_window.event_work(event)
            elif event.type == pygame.KEYDOWN and self.sign_window.is_work and (
                    self.sign_window.is_log_name_input or self.sign_window.is_log_pw_input):
                self.sign_window.event_work(event)
            elif event.type == pygame.KEYDOWN and not self.game_window.is_work:
                if event.key == pygame.K_p and not self.end_game:
                    self.turn_on_if(self.game_window, self.pause_window)
                elif event.key == pygame.K_h:
                    if not self.end_game:
                        self.turn_on_if(self.pause_window, self.highscores_window)
                    else:
                        self.turn_on_if(self.end_window, self.highscores_window)
            elif event.type == pygame.KEYUP and self.game_window.is_work:
                if self.game_window.event_work(event):
                    self.turn_on(self.end_window)
            elif event.type == pygame.KEYUP and self.log_window.is_work:
                self.log_window.event_work(event)
            elif event.type == pygame.KEYUP and self.sign_window.is_work:
                self.sign_window.event_work(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.bar_rect.collidepoint(event.pos) and event.button == 1:
                    if self.ng_rect.collidepoint(event.pos):
                        self.user.upd(self.game_window.game_field.score, self.game_window.game_field.count_of_lines,
                                      self.game_window.game_field.count_of_figures)
                        self.game_window.new_game()
                        self.end_game = False
                        self.end_window.is_app_start = False
                        self.turn_on(self.game_window)
                    elif self.pause_rect.collidepoint(event.pos) and not self.end_game:
                        self.turn_on_if(self.game_window, self.pause_window)
                    elif self.hs_rect.collidepoint(event.pos):
                        if not self.end_game:
                            self.turn_on_if(self.pause_window, self.highscores_window)
                        else:
                            self.turn_on_if(self.end_window, self.highscores_window)
                    elif self.user.is_log_in and self.log_out_rect.collidepoint(event.pos):
                        self.user.username = 'Guest'
                        self.user.is_log_in = False
                    elif self.log_rect.collidepoint(event.pos):
                        if not self.end_game:
                            self.turn_on_if(self.pause_window, self.log_window)
                        else:
                            self.turn_on_if(self.end_window, self.log_window)
                    elif self.sign_rect.collidepoint(event.pos):
                        if not self.end_game:
                            self.turn_on_if(self.pause_window, self.sign_window)
                        else:
                            self.turn_on_if(self.end_window, self.sign_window)
                elif self.pause_window.is_work and event.button == 1:
                    self.turn_on(self.game_window)
                elif self.log_window.is_work and event.button == 1:
                    if self.log_window.event_work(event):
                        if not self.end_game:
                            self.turn_on(self.pause_window)
                        else:
                            self.turn_on(self.end_window)
                elif self.sign_window.is_work and event.button == 1:
                    if self.sign_window.event_work(event):
                        if not self.end_game:
                            self.turn_on(self.pause_window)
                        else:
                            self.turn_on(self.end_window)

    def update(self):
        self.bar = self.clear_bar.copy()
        if self.game_window.is_work:
            game_f, self.bar = self.game_window.upd_surface()
            self.saved_pause_surface = game_f
            self.main_surface.blit(game_f, (198, 2))
        elif self.pause_window.is_work:
            self.main_surface.blit(self.saved_pause_surface, (198, 2))
            self.main_surface.blit(self.pause_window.pause_surf, (198, 2))
            self.main_surface.blit(self.pause_window.continue_button, (253, 222))
        elif self.highscores_window.is_work:
            game_f = self.highscores_window.upd_surface(self.user.data)
            self.main_surface.blit(game_f, (198, 2))
        elif self.log_window.is_work:
            game_f = self.log_window.upd_surface()
            self.main_surface.blit(game_f, (198, 2))
        elif self.sign_window.is_work:
            game_f = self.sign_window.upd_surface()
            self.main_surface.blit(game_f, (198, 2))
        elif self.end_window.is_work:
            if not self.end_window.is_app_start:
                self.main_surface.blit(self.saved_pause_surface, (198, 2))
            game_f = self.end_window.upd_surface(self.game_window.game_field.score,
                                                 self.game_window.game_field.count_of_lines,
                                                 self.game_window.game_field.count_of_figures,
                                                 self.game_window.game_field.stopwatch.time())
            self.main_surface.blit(game_f, (198, 2))

        if self.user.is_log_in:
            self.bar.blit(self.log_out_button, self.log_out_rect)
            text = self.log_window.font.render('Hi, ' + self.user.username, False, (0, 0, 0))
            text_rect = text.get_rect(center=(99, 41))
        else:
            self.bar.blit(self.log_button, self.log_rect)
            self.bar.blit(self.sign_button, self.sign_rect)
            text = self.log_window.font.render('Tetris', False, (0, 0, 0))
            text_rect = text.get_rect(center=(99, 41))
        pygame.draw.rect(self.bar, (247, 241, 215), (2, 24, 194, 35))
        self.bar.blit(text, text_rect)

        # счет
        if not self.end_window.is_work and not self.end_window.is_app_start:
            pygame.draw.rect(self.bar, (247, 241, 215), (85, 430, 110, 50))
            pygame.draw.rect(self.bar, (247, 241, 215), (106, 479, 90, 23))
            pygame.draw.rect(self.bar, (247, 241, 215), (75, 505, 121, 26))
            text = self.log_window.font.render(str(self.game_window.game_field.score), False, (0, 0, 0),
                                               (247, 241, 215))
            self.bar.blit(text, (87, 430))
            text = self.log_window.font.render(str(self.game_window.game_field.count_of_lines), False, (0, 0, 0),
                                               (247, 241, 215))
            self.bar.blit(text, (87, 454))
            text = self.log_window.font.render(str(self.game_window.game_field.count_of_figures), False, (0, 0, 0),
                                               (247, 241, 215))
            self.bar.blit(text, (110, 478))
            text = self.log_window.font.render(str(self.game_window.game_field.stopwatch.time())[:-5], False, (0, 0, 0),
                                               (247, 241, 215))
            self.bar.blit(text, (80, 505))
        else:
            pygame.draw.rect(self.bar, (247, 241, 215), (0, 228, 194, 310))
        self.main_surface.blit(self.bar, self.bar_rect)
        return self.main_surface


if __name__ == "__main__":
    # загрузка нужных модулей
    os.system('pip install pygame')
    os.system('pip install numpy')
    os.system('pip install requests')
    sc = pygame.display.set_mode((500, 604))
    pygame.display.set_caption("Tetris")
    pygame.display.set_icon(pygame.image.load(f"{PATH}/pic/icon1.bmp"))

    control = ControlClass()
    clock = pygame.time.Clock()
    while True:
        # обработка событий
        control.control_events()
        # обновление экрана
        sc.blit(control.update(), (0, 0))
        pygame.display.update()
        clock.tick(30)

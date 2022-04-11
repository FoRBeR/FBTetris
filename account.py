import pygame
import hashlib
import requests

pygame.init()

# хранит информацию о пользователе и подключении, работает с сервером
class User:
    def __init__(self):
        self.username = 'Guest'
        self.is_log_in = False
        self.connection = True
        self.data = {}
        self.load()

    # создание спец. хэша по данным пользователя
    def special_hash(self):
        check_code = (self.username[:2:-1] + str(
            self.data[self.username]['score'] * self.data[self.username]['lines'])) * 2 + str(
            self.data[self.username]['figures']) + self.username[::-1]
        return hashlib.sha256(check_code.encode()).hexdigest()

    # проверяет таблицу лидеров полностью (использовать только при удалении данных при проверке спец хэшей)
    def check_leaders(self):
        leader1 = self.data['Leaders'][0]
        leader2 = self.data['Leaders'][1]
        leader3 = self.data['Leaders'][2]
        for key in self.data:
            if key == 'Leaders': continue
            if self.data[key]['score'] > self.data[leader1]['score']:
                leader3 = leader2
                leader2 = leader1
                leader1 = key
            elif self.data[key]['score'] > self.data[leader2]['score'] and key != leader1:
                leader3 = leader2
                leader2 = key
            elif self.data[key]['score'] > self.data[leader3]['score'] and key != leader1 and key != leader2:
                leader3 = key
        self.data['Leaders'][0] = leader1
        self.data['Leaders'][1] = leader2
        self.data['Leaders'][2] = leader3

    # проверяет базу данных по специальным хешам
    def check_data(self):
        dic = []
        for name in self.data:
            if name != 'Leaders':
                check_code = (name[:2:-1] + str(self.data[name]['score'] * self.data[name]['lines'])) * 2 + str(
                    self.data[name]['figures']) + name[::-1]
                if self.data[name]['s_hash'] != hashlib.sha256(check_code.encode()).hexdigest():
                    dic.append(name)
        for name in dic:
            self.data[name]['score'] = -1
            self.data[name]['lines'] = 0
            self.data[name]['figures'] = 0
            check_code = (name[:2:-1] + str(self.data[name]['score'] * self.data[name]['lines'])) * 2 + str(
                self.data[name]['figures']) + name[::-1]
            self.data[name]['s_hash'] = hashlib.sha256(check_code.encode()).hexdigest()
        self.check_leaders()

    # загружает информацию с хостинга + работает с интернет-соединением
    def load(self):
        headers = {'X-Master-Key': '$2b$10$TIPzwNPVx7d0BkHHrrIGkOesXOKf4.Jwlw8d8IL2pv7N03nvlH0S.'}
        url = 'https://api.jsonbin.io/v3/b/6241a5cf061827674381a93e'
        if self.connection:
            try:
                req = requests.get(url, json=None, headers=headers)
            except requests.exceptions.ConnectionError:
                self.connection = False
                return
            self.data = req.json()['record']
            self.check_data()
        else:
            try:
                req = requests.get(url, json=None, headers=headers)
            except requests.exceptions.ConnectionError:
                return
            self.connection = True
            self.data = req.json()['record']
            self.check_data()

    # загружает информацию на хостинг
    def unload(self):
        if self.connection:
            if self.is_log_in:
                self.data[self.username]['s_hash'] = self.special_hash()
            url = 'https://api.jsonbin.io/v3/b/6241a5cf061827674381a93e'
            headers = {
                'Content-Type': 'application/json',
                'X-Master-Key': '$2b$10$TIPzwNPVx7d0BkHHrrIGkOesXOKf4.Jwlw8d8IL2pv7N03nvlH0S.'
            }
            try:
                requests.put(url, json=self.data, headers=headers)
            except requests.exceptions.ConnectionError:
                self.connection = False

    # проверяет пароль и осуществляет вход
    def log_in(self, name, password):
        if name not in self.data: return False
        if self.data[name]['pw'] != hashlib.sha256(password.encode()).hexdigest(): return False
        self.username = name
        self.is_log_in = True
        return True

    # проверяет наличие такого имени в таблице, создает нового пользователя
    def sign_up(self, name, password):
        if name in self.data: return False
        self.data[name] = {'pw': '', 'score': 0, 'lines': 0, 'figures': 0, 's_hash': ''}
        self.data[name]['pw'] = hashlib.sha256(password.encode()).hexdigest()
        check_code = (name[:2:-1] + str(self.data[name]['score'] * self.data[name]['lines'])) * 2 + str(
            self.data[name]['figures']) + name[::-1]
        self.data[name]['s_hash'] = hashlib.sha256(check_code.encode()).hexdigest()
        self.username = name
        self.is_log_in = True
        return True

    # обновляет информацию в базе о user
    def upd(self, score, lines, figures):
        if self.username == 'Guest': return
        if self.data[self.username]['score'] < score:
            self.data[self.username]['score'] = score
            self.data[self.username]['lines'] = lines
            self.data[self.username]['figures'] = figures
            self.data[self.username]['s_hash'] = self.special_hash()
        leader1 = self.data['Leaders'][0]
        leader2 = self.data['Leaders'][1]
        leader3 = self.data['Leaders'][2]
        if self.data[self.username]['score'] > self.data[leader1]['score']:
            leader3 = leader2
            leader2 = leader1
            leader1 = self.username
        elif self.data[self.username]['score'] > self.data[leader2]['score'] and self.username != leader1:
            leader3 = leader2
            leader2 = self.username
        elif self.data[self.username]['score'] > self.data[leader3][
            'score'] and self.username != leader1 and self.username != leader2:
            leader3 = self.username
        self.data['Leaders'][0] = leader1
        self.data['Leaders'][1] = leader2
        self.data['Leaders'][2] = leader3


if __name__ == '__main__':
    user = User()

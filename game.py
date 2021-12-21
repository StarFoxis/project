from os import stat
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=SingletonMeta):
    DIRECTIONS = ['Север', 'Восток', 'Юг', 'Запад']
    ROOMS = [['', 'Балкон', ''], ['Спальня', 'Холл', 'Кухня'], ['Подземелье', 'Коридор', 'Оружейная']]

    def __init__(self, id=0):
        self.current_room = 'Подземелье'
        self.i = 0
        self.j = 2
        self.arms = False
    
    def getCurrentRoom(self):
        return self.current_room

    def move(self, direction, step):
        next_pos = self.moves(direction)(self.i, self.j, step)
        try:
            i, j = next_pos
            if i < 0 or j < 0 or self.ROOMS[j][i] == '':
                raise IndexError
            
            if self.ROOMS[j][i] == 'Холл':
                if self.arms:
                    self.i, self.j = i, j
                    self.current_room = self.ROOMS[self.j][self.i]
                    return (f'Вы победили троля и оказались в Холле', 'enemy')
                return (f'О нет на вашем пути оказался злой и страшный троль!! Я думаю нужно найти оружие чтобы его победить!', 'enemy')

            self.i, self.j = i, j
            self.current_room = self.ROOMS[self.j][self.i]

            if self.current_room == 'Оружейная' and not self.arms:
                self.arms = True
                return (f'Ого вы нашли арбалет в Оружейной!! Может он пригодится!?', 'enemy')
            
            if self.current_room == 'Балкон':
                return (f'Вот вы и добрались до заветного балкона. Теперь вы можете прыгать!(От счастья вертикально вверх ♥)', 'win')

            return (f'Вы пошли на {self.DIRECTIONS[direction]} {step} раз и оказались на {self.current_room}', 'move')
        except IndexError:
            return ('Вы уперлись в стену!!', 'wall')

    @staticmethod
    def moves(direction):
        return {
            0: lambda i, j, step: (i, j - step),
            1: lambda i, j, step: (i + step, j),
            2: lambda i, j, step: (i, j + step),
            3: lambda i, j, step: (i - step, j)
        }[direction]
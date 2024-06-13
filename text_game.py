from random import randint

class Hero():
    # характеристики и способности персонажа
    def __init__(self, name, attack_power=20, flee=10, health=100):
        self.__name = name                      # имя
        self.__attack_power = attack_power      # AP
        self.__flee = flee                      # уворот
        self.__health = health                  # HP

    @property
    def name(self):
        return self.__name

    @property
    def attack_power(self):
        return self.__attack_power

    @property
    def flee(self):
        return self.__flee

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, new_health):
        self.__health = new_health

    def attack(self, over):
        is_alive = True
        has_fled = False
        attack_points = 0

        attack_info = f"Воин {self.name} (AP:{self.attack_power}) атакует Воина {over.name} (HP:{over.health})\n"

        # проверим шанс уворота
        check_flee_chance = randint(1, 100)
        if check_flee_chance <= over.flee:
            attack_info += f"Воин {over.name} увернулся!"
            has_fled = True
        else:
            attack_points = self.attack_power
            over.health -= attack_points
            # проверим, выжил ли соперник
            if not (over.is_alive()):
                attack_info += f"Воин {over.name} погиб!"
                is_alive = False
            else:
                attack_info += f"У Воина {over.name} {over.health} HP"

        # вернем информацию: Жив ли соперник, Был ли уворот, Сколько ОЖ снято, текстовая информация о бое
        return is_alive, has_fled, attack_points, attack_info

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

class Game():
    def __init__(self):
        self.player = Hero("Player1")
        self.computer = Hero("Player2")

    def start(self):
        while True:
            attack_result = self.player.attack(self.computer)
            print(attack_result[3])
            if not attack_result[0]:
                break
            attack_result = self.computer.attack(self.player)
            print(attack_result[3])
            if not attack_result[0]:
                break


game = Game()
game.start()

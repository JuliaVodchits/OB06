from random import randint

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


class Hero:
    # характеристики и способности персонажа
    def __init__(self, name, attack_power=20, flee=10, critical_chance = 10, health=100):
        self.__name = name                          # имя
        self.__attack_power = attack_power          # AP
        self.__flee = flee                          # уворот
        self.__critical_chance = critical_chance    # крит
        self.__health = health                      # HP

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
    def critical_chance(self):
        return self.__critical_chance

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, new_health):
        self.__health = new_health

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

    def attack(self, over, printing=True):

        # Словарь с логом боя
        battle_stats = {
                'attacker': self.name,
                'AP': self.attack_power,
                'defender': over.name,
                'start_HP': over.health,
                'is_alive': True,
                'has_fled': False,
                'has_crit': False,
                'finish_HP': 0
        }

        # проверим шанс уворота
        check_flee_chance = randint(1, 100)
        if check_flee_chance <= over.flee:
            battle_stats['has_fled'] = True
        else:
            check_crit = randint(1, 100)
            if check_crit <= self.critical_chance:
                battle_stats['has_crit'] = True
                over.health -= self.attack_power * 2    # критический урон
            else:
                over.health -= self.attack_power
                # проверим, выжил ли соперник
                if not (over.is_alive()):
                    battle_stats['is_alive'] = False

        if over.health < 0: over.health = 0

        battle_stats['finish_HP'] = over.health

        return battle_stats


class Game:
    def __init__(self, player1, player2):
        self.__player = Hero(player1)
        self.__computer = Hero(player2)
        self.__current_player = self.__player

    @property
    def player(self):
        return self.__player

    @property
    def computer(self):
        return self.__computer

    def print_attack_log(self, btl_stats):
        print(GREEN + f"Воин {btl_stats['attacker']} (AP:{btl_stats['AP']}) атакует Воина {btl_stats['defender']} "
                      f"(HP:{btl_stats['start_HP']})")
        if btl_stats['has_fled']:
            print(RED + f"Воин {btl_stats['defender']} увернулся!")
        elif not btl_stats['is_alive']:
            print(RED + f"Воин {btl_stats['defender']}  погиб!")
        else:
            if btl_stats['has_crit']:
                print(RED + f"Крит! Воин {btl_stats['attacker']} наносит урон  {2 * btl_stats['AP']}!")
            print(YELLOW + f"У Воина {btl_stats['defender']} {btl_stats['finish_HP']} HP")

    def battle_round(self):
        if self.__current_player == self.player:
            battle_stats = self.player.attack(self.computer)
            self.__current_player = self.computer
        else:
            battle_stats = self.computer.attack(self.player)
            self.__current_player = self.player

        return battle_stats

    def start(self):
        while True:
            battle_stats = self.battle_round()
            self.print_attack_log(battle_stats)

            if not battle_stats['is_alive']:
                break


if __name__ == '__main__':
    game = Game("Player1", "Player2")
    game.start()

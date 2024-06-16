import pygame
import text_game as tgm

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
GREY = (211, 211, 211)

clock = pygame.time.Clock()
fps = 10

class Window:
    def __init__(self):
        self.__window_width, self.__window_height = 1024, 600
        self.__margin_x, self.__margin_y = 20, 20
        self.__caption = "Битва"
        self.__screen = pygame.display.set_mode((self.__window_width, self.__window_height))
        pygame.display.set_caption(self.__caption)
        pygame.display.set_icon(pygame.image.load("img/warriors_with_peak_and_sword.png"))

    @property
    def window_width(self):
        return self.__window_width

    @property
    def window_height(self):
        return self.__window_height

    @property
    def margin_x(self):
        return self.__margin_x

    @property
    def margin_y(self):
        return self.__margin_y

    @property
    def screen(self):
        return self.__screen

    def blit(self, image, rect):
        self.__screen.blit(image, rect)

# Класс для спрайта картинки
class Image:
    def __init__(self, path, x, y):
        self.__image = pygame.image.load(path)
        self.__rect = self.__image.get_rect()
        self.__info_rect_w = 100
        self.__info_rect_h = 50
        self.__info_rect = Rectangle(x=x + self.__rect.width / 2 - self.__info_rect_w / 2,
                                y=y,
                                width=self.__info_rect_w,
                                height=self.__info_rect_h,
                                color=WHITE, border_color=None, border_width=0,
                                rec_text=RecText(font_name=None, font_size=40), text_margin=20)
        self.__rect.x = x
        self.__rect.y = y + self.__info_rect_h



    @property
    def x(self):
        return self.__rect.x

    @x.setter
    def x(self, new_x):
        self.__rect.x = new_x

    @property
    def y(self):
        return self.__rect.y

    @y.setter
    def y(self, new_y):
        self.__rect.y = new_y

    @property
    def rect(self):
        return self.__rect

    @property
    def info_rect(self):
        return self.__info_rect

    @property
    def image(self):
        return self.__image

    @property
    def width(self):
        return self.__rect.width

    @property
    def height(self):
        return self.__rect.height

# класс для описания текста в прямоугольнике
class RecText:
    def __init__(self, font_name, font_size):
        self.__font = pygame.font.Font(font_name, font_size)

    @property
    def font(self):
        return self.__font

# прямоугольник с текстом
class Rectangle:
    def __init__(self, x, y,  width, height, color=WHITE, border_color=GREY, border_width=2,
                 rec_text: RecText = None, text_margin=20):
        self.__rect = pygame.Rect(x, y, width, height)
        self.__color = color
        self.__border_color = border_color
        self.__border_width = border_width
        self.__font = rec_text.font
        self.__text_margin = text_margin
        self.text_lines = []

    def draw_rect(self, screen):
        # Отрисовка прямоугольника
        pygame.draw.rect(screen, self.__color, self.__rect)
        # Отрисовка границы прямоугольника
        if self.__border_color is not None and self.__border_width > 0:
            pygame.draw.rect(screen, self.__border_color, self.__rect, self.__border_width)

    def draw_text_in_rect(self, screen, text, text_color, x=None, y=None, font=None):
        if x is None: x = self.__rect.x + self.__text_margin
        if y is None: y = self.__rect.y + self.__text_margin
        if font is None: font = self.__font

        line_height = font.get_linesize()
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(left=x, top=y)
        screen.blit(text_surface, text_rect)
        return x, y + line_height

pygame.init()

window = Window()
player = tgm.Hero("Player1")
computer = tgm.Hero("Player2")
current_payer = 1

left_warrior = Image("img/warrior_with_peak.png", window.margin_x, window.margin_y)
right_warrior = Image("img/warrior_with_sword.png", window.margin_x + left_warrior.width, window.margin_y)
# right_warrior.x, right_warrior.y =

# Создание окна вывода лога битвы
rect_x = right_warrior.x + right_warrior.width + window.margin_x
rect_battle = Rectangle(x=rect_x, y=window.margin_y,
                 width=window.window_width - rect_x - window.margin_x,
                 height=window.window_height - 2 * window.margin_y,
                 color=WHITE, border_color=GREY, border_width=2,
                 rec_text=RecText(font_name=None, font_size=24), text_margin=20)


# Игровой цикл
battle_log = []
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    if current_payer == 1:
        btl_stats = player.attack(computer, False)
        current_payer = 2
    else:
        btl_stats = computer.attack(player, False)
        current_payer = 1

    battle_log.append(
                  {'color': BROWN,
                   'text': f"Воин {btl_stats['attacker']} (AP:{btl_stats['AP']}) атакует "
                           f"Воина {btl_stats['defender']} (HP:{btl_stats['start_HP']})"})
    if btl_stats['has_fled']:
        battle_log.append(
            {'color': RED,
             'text': f"Воин {btl_stats['defender']} увернулся!"})
    elif not btl_stats['is_alive']:
        battle_log.append(
            {'color': RED,
             'text': f"Воин {btl_stats['defender']} погиб!"})
    else:
        if btl_stats['has_crit']:
            battle_log.append(
                {'color': RED,
                 'text': f"Крит! Воин {btl_stats['attacker']} наносит урон  {2 * btl_stats['AP']}!"})
        battle_log.append(
            {'color': BLACK,
             'text': f"У Воина {btl_stats['defender']} {btl_stats['finish_HP']} HP"})

    # отрисовка экрана с содержимым (неизменяемое)

    window.screen.fill(WHITE)
    window.blit(left_warrior.image, left_warrior.rect)
    left_warrior.info_rect.draw_rect(window.screen)
    left_warrior.info_rect.draw_text_in_rect(window.screen, f"HP: {player.health}", BROWN)

    window.blit(right_warrior.image, right_warrior.rect)
    right_warrior.info_rect.draw_rect(window.screen)
    right_warrior.info_rect.draw_text_in_rect(window.screen, f"HP: {computer.health}", BROWN)

    rect_battle.draw_rect(window.screen)

    x, y = None, None
    for log_line in battle_log:
        x, y = rect_battle.draw_text_in_rect(window.screen, log_line['text'], log_line['color'], x, y)

    # start_text = ()
    # x, y = rect_battle.draw_text_in_rect(window.screen, start_text, BROWN)
    # if btl_stats['has_fled']:
    #     red_text = f"Воин {btl_stats['defender']} увернулся!"
    #     x, y = rect_battle.draw_text_in_rect(window.screen, red_text, RED, x, y)
    # elif not btl_stats['is_alive']:
    #     red_text = f"Воин {btl_stats['defender']} погиб!"
    #     x, y = rect_battle.draw_text_in_rect(window.screen, red_text, RED, x, y)
    # else:
    #     if btl_stats['has_crit']:
    #         red_text = f"Крит! Воин {btl_stats['attacker']} наносит урон  {2 * btl_stats['AP']}!"
    #         x, y = rect_battle.draw_text_in_rect(window.screen, red_text, RED, x, y)
    #     common_text = f"У Воина {btl_stats['defender']} {btl_stats['finish_HP']} HP"
    #     x, y = rect_battle.draw_text_in_rect(window.screen, common_text, BLACK, x, y)

    pygame.time.wait(1000)

    if not btl_stats['is_alive']:
        running = False
        x, y = rect_battle.draw_text_in_rect(window.screen, 'Нажмите ЛЮБУЮ КЛАВИШУ для окончания',
                                             BROWN, x, y, RecText(font_name=None, font_size=24).font)

    pygame.display.flip()   # обновление экрана
    # clock.tick(fps)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if any(keys):
        running = False
        break

pygame.quit()

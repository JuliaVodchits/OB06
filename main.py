import pygame


class Image():
    def __init__(self, path):
        self.image = pygame.image.load(path)
        self.image_rect = self.image.get_rect()


pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode((window_size))
pygame.display.set_caption("Тестовый проект")

left_warrior = Image("img/warrior_with_peak.png")
right_warrior = Image("img/warrior_with_sword.png")

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    screen.fill((255, 255, 255))
    screen.blit(left_warrior.image, left_warrior.image_rect)
    pygame.display.flip()   # обновление экрана

pygame.quit()

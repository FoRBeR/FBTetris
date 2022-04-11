import pygame
import os

pygame.init()

PATH = os.getcwd()
# цвета фигур
colors = {'1': (178, 34, 34), '2': (34, 139, 34), '3': (255, 215, 0), '4': (65, 105, 225), '5': (128, 0, 128),
          '6': (139, 69, 19), '7': (47, 79, 79)}
# квадратики для отрисовки фигур
squares = []
for i in range(7):
    squares.append(pygame.Surface((28, 28)))
    pygame.draw.rect(squares[i], colors[str(i + 1)], (0, 0, 28, 28))

# поверхность со следующей фигурой
def next_figure_surface(code, figures, rects):
    figure_surface = pygame.Surface((120, 120))
    figure_surface.fill((247, 241, 215))
    figure_surface.blit(figures[code - 1], rects[code - 1])
    return figure_surface


#  заранее отрисовываю все фигуры для поля со следующей фигурой
figures = []
rects = []
#  first
figure1 = pygame.Surface((120, 30))
figure1.fill((255, 255, 255))
figure1.blit(squares[0], (1, 1))
figure1.blit(squares[0], (31, 1))
figure1.blit(squares[0], (61, 1))
figure1.blit(squares[0], (91, 1))
figure1.set_colorkey((255, 255, 255))
figure1_rect = figure1.get_rect(center=(60, 60))
figures.append(figure1)
rects.append(figure1_rect)

#  second
figure2 = pygame.Surface((60, 60))
figure2.fill((255, 255, 255))
figure2.blit(squares[1], (1, 1))
figure2.blit(squares[1], (31, 1))
figure2.blit(squares[1], (1, 31))
figure2.blit(squares[1], (31, 31))
figure2.set_colorkey((255, 255, 255))
figure2_rect = figure2.get_rect(center=(60, 60))
figures.append(figure2)
rects.append(figure2_rect)

# third
figure3 = pygame.Surface((90, 60))
figure3.fill((255, 255, 255))
figure3.blit(squares[2], (31, 1))
figure3.blit(squares[2], (1, 31))
figure3.blit(squares[2], (31, 31))
figure3.blit(squares[2], (61, 31))
figure3.set_colorkey((255, 255, 255))
figure3_rect = figure3.get_rect(center=(60, 60))
figures.append(figure3)
rects.append(figure3_rect)

# fourth
figure4 = pygame.Surface((90, 60))
figure4.fill((255, 255, 255))
figure4.blit(squares[3], (1, 1))
figure4.blit(squares[3], (1, 31))
figure4.blit(squares[3], (31, 31))
figure4.blit(squares[3], (61, 31))
figure4.set_colorkey((255, 255, 255))
figure4_rect = figure4.get_rect(center=(60, 60))
figures.append(figure4)
rects.append(figure4_rect)

# fifth
figure5 = pygame.Surface((90, 60))
figure5.fill((255, 255, 255))
figure5.blit(squares[4], (61, 1))
figure5.blit(squares[4], (1, 31))
figure5.blit(squares[4], (31, 31))
figure5.blit(squares[4], (61, 31))
figure5.set_colorkey((255, 255, 255))
figure5_rect = figure5.get_rect(center=(60, 60))
figures.append(figure5)
rects.append(figure5_rect)

# sixth
figure6 = pygame.Surface((90, 60))
figure6.fill((255, 255, 255))
figure6.blit(squares[5], (1, 1))
figure6.blit(squares[5], (31, 1))
figure6.blit(squares[5], (31, 31))
figure6.blit(squares[5], (61, 31))
figure6.set_colorkey((255, 255, 255))
figure6_rect = figure6.get_rect(center=(60, 60))
figures.append(figure6)
rects.append(figure6_rect)

# seventh
figure7 = pygame.Surface((90, 60))
figure7.fill((255, 255, 255))
figure7.blit(squares[6], (31, 1))
figure7.blit(squares[6], (61, 1))
figure7.blit(squares[6], (1, 31))
figure7.blit(squares[6], (31, 31))
figure7.set_colorkey((255, 255, 255))
figure7_rect = figure7.get_rect(center=(60, 60))
figures.append(figure7)
rects.append(figure7_rect)

if __name__ == "__main__":
    sc = pygame.display.set_mode((120, 120))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sc.blit(next_figure_surface(1, figures, rects), (0, 0))
        pygame.display.update()
        clock.tick(30)

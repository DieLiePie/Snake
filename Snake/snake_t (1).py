import pygame
import sys
import random
import time
import os
pygame.init()

pygame.font.init()

# словарь со звуковыми эффектами, находящимися в папке "sound_effects"
sounds_effects = dict(
    eat='sound_effects/eat.wav',
    end_game='sound_effects/end_game.wav',
    choose='sound_effects/choose.wav'
)
# создание объекта Sound
for name, sound in sounds_effects.items():
    sounds_effects[name] = pygame.mixer.Sound(sound)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


class Game():
    def __init__(self):
        # задаем размеры экрана
        self.screen_width = 720
        self.screen_height = 460

        # необходимые цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 25, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)

        # Frame per second controller
        # будет задавать количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        # переменная для оторбражения результата
        # (сколько еды съели)
        self.score = 0
        self.food_counter = 0

        # музыка и звуковые эффекты
        # self.end_game = pygame.mixer.Sound('end_game.wav')
        # pygame.mixer.music.load('Test.mp3')

    def init_and_check_for_errors(self):
        """Начальная функция для инициализации и
           проверки как запустится pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
        """Задаем surface(поверхность поверх которой будет все рисоваться)
        и устанавливаем загаловок окна"""
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('GAME')

    def event_loop(self, change_to):
        """Функция для отслеживания нажатий клавиш игроком"""

        # запускаем цикл по ивентам
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # если нажали клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # нажали escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # управление звуком
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    # Пауза
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_2:
                    # Включение музыки на пониженном уровне громкости
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(0.5)
                elif event.key == pygame.K_3:
                    # Включение музыки на установленном уровне громкости
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.set_volume(1)
        return change_to

    def refresh_screen(self):
        """обновляем экран и задаем фпс"""
        pygame.display.flip()
        game.fps_controller.tick(10)

    def show_score(self, choice=1):
        """Отображение результата"""
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(
            'СЧЕТ: {0}'.format(self.score), True, self.black)
        s_rect = s_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        # при game_overe отображаем результат по центру
        # под надписью game over
        else:
            s_rect.midtop = (360, 120)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        """Функция для вывода надписи Game Over и результатов
        в случае завершения игры и выход из игры"""
        pygame.mixer.music.stop()
        sounds_effects['end_game'].play()
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('GAME OVER', True, self.black)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()


class Snake():
    def __init__(self, snake_color):
        # важные переменные - позиция головы змеи и его тела
        self.snake_head_pos = [100, 50]  # [x, y]
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        # направление движение змеи, изначально
        # зададимся вправо
        self.direction = "RIGHT"
        # куда будет меняться напрвление движения змеи
        # при нажатии соответствующих клавиш
        self.change_to = self.direction

    def validate_direction_and_change(self):
        """Изменияем направление движения змеи только в том случае,
        если оно не прямо противоположно текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        """Изменияем положение головы змеи"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):
        # если вставлять просто snake_head_pos,
        # то на всех трех позициях в snake_body
        # окажется один и тот же список с одинаковыми координатами
        # и мы будем управлять змеей из одного квадрата
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # если съели еду то задаем новое положение еды случайным
            # образом и увеличивем score на один
            # проигрывание звука съедания еды
            sounds_effects['eat'].play()
            food_pos = [random.randrange(1, screen_width / 10) * 10,
                        random.randrange(1, screen_height / 10) * 10]
            score += 1
        else:
            # если не нашли еду, то убираем последний сегмент,
            # если этого не сделать, то змея будет постоянно расти
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        """Отображаем все сегменты змеи"""
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            # pygame.Rect(x,y, sizex, sizey)
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        """Проверка, что столкунлись с концами экрана или сами с собой
        (змея закольцевалась)"""
        if any((
            self.snake_head_pos[0] > screen_width - 10 or
            self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > screen_height - 10 or
            self.snake_head_pos[1] < 0
        )):
            game_over()
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        """Инит еды"""
        self.food_color = food_color
        self.big_food_color = pygame.Color('orange')
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, screen_height / 10) * 10]

    def draw_food(self, play_surface):
        """Отображение еды"""
        pygame.draw.rect(
           play_surface, self.food_color, pygame.Rect(
               self.food_pos[0], self.food_pos[1],
               self.food_size_x, self.food_size_y))


class Menu:
    def __init__(self, punkts=[120, 140, u'Punkt', (250, 250, 30), (250, 30, 250)]):
        self.punkts = punkts
        self.screen = pygame.display.set_mode((720, 460))
        # заставка
        self.image = load_image("menu_picture.png")
        self.image = pygame.sprite.Group()

    def render(self, screen, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                screen.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.SysFont('monaco', 50)
        punkt = 0
        pygame.mixer.music.load('sound_effects/menu.mp3')
        pygame.mixer.music.play(-1, 0.0)
        while done:
            self.screen.fill(pygame.Color("white"))
            self.image.draw(self.screen)
            np = pygame.mouse.get_pos()
            for i in self.punkts:
                 if np[0] > i[0] and np[0] < i[0] + 55 and np[1] > i[1] and np[1] < i[1] + 50:
                    punkt = i[5]
            self.render(self.screen, font_menu, punkt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                    # регулировка звука в меню
                    if event.key == pygame.K_1:
                        pygame.mixer.music.pause()
                    elif event.key == pygame.K_2:
                        pygame.mixer.music.unpause()
                        pygame.mixer.music.set_volume(0.5)
                    elif event.key == pygame.K_3:
                        pygame.mixer.music.unpause()
                        pygame.mixer.music.set_volume(1)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if punkt == 0:
                        pygame.mixer.music.stop()
                        sounds_effects['choose'].play()
                        time.sleep(1)
                        done = False
                    elif punkt == 1:
                        sounds_effects['choose'].play()
                        time.sleep(1)
                        pygame.quit()
                        sys.exit()
                self.screen.blit(self.screen, (0, 0))
            pygame.display.flip()


""" создание меню """
punkts = [(320, 140, u'Game', (250, 250, 30), (250, 30, 250), 0),
          (330, 210, u'Quit', (250, 250, 30), (250, 30, 250), 1)]
start_game = Menu(punkts)
start_game.menu()
""" подготовка к запуску игры """

game = Game()
snake = Snake(game.green)
food = Food(game.brown, game.screen_width, game.screen_height)


game.init_and_check_for_errors()
game.set_surface_and_title()

# установка фоновой музыки
pygame.mixer.music.load('sound_effects/background.mp3')
pygame.mixer.music.play(-1, 0.0)
while True:
    snake.change_to = game.event_loop(snake.change_to)

    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(
        game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, game.white)

    food.draw_food(game.play_surface)

    snake.check_for_boundaries(
        game.game_over, game.screen_width, game.screen_height)

    game.show_score()
    game.refresh_screen()
pygame.quit()

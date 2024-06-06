import pygame  # Импорт библиотеки pygame
import random  # Импорт библиотеки random для перемешивания картинок
import os      # Импорт библиотеки os для работы с файлами

# Инициализация pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Создание окна игры
pygame.display.set_caption("Puzzle Memory")  # Установка заголовка окна

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Настройки игры
CARD_WIDTH = 85   # Ширина карты
CARD_HEIGHT = 120  # Высота карты
MARGIN = 10        # Отступ между картами

# Загрузка изображений карт
def load_and_scale_image(image_path, size):
    image = pygame.image.load(image_path)  # Загрузка изображения
    return pygame.transform.scale(image, size)  # Изменение размера изображения

def load_images():
    image_files = [f for f in os.listdir('.') if f.startswith('card_') and f.endswith('.jpg')]  # Получение списка файлов с изображениями карт
    images = [load_and_scale_image(image_file, (CARD_WIDTH, CARD_HEIGHT)) for image_file in image_files]  # Загрузка и изменение размера всех изображений карт
    return images

# Получение максимального размера поля на основе количества изображений
images = load_images()
max_pairs = len(images)
max_size = int((max_pairs * 2) ** 0.5)  # Вычисление максимального размера поля

# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)  # Создание объекта текста
    textrect = textobj.get_rect()  # Получение прямоугольника текста
    textrect.center = (x, y)  # Центрирование текста
    surface.blit(textobj, textrect)  # Отображение текста на экране

# Запрос размера поля у пользователя
def get_board_size():
    input_active = False  # Флаг активности ввода
    input_text = ''  # Текущий ввод текста

    while True:
        screen.fill(WHITE)  # Заполнение экрана белым цветом
        draw_text(f"Введите размер поля кратное 2 (максимум {max_size // 2 * 2}):", pygame.font.SysFont(None, 48), BLUE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)  # Отображение запроса размера пол
        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Проверка события закрытия окна
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:  # Проверка события нажатия клавиши
                if input_active:
                    if event.key == pygame.K_RETURN:  # Проверка нажатия Enter
                        if input_text.isdigit() and 2 <= int(input_text) <= max_size:  # Проверка валидности введенного размера поля
                            return int(input_text)
                        else:
                            input_text = ''  # Сброс ввода при неверном значении
                    elif event.key == pygame.K_BACKSPACE:  # Проверка нажатия Backspace
                        input_text = input_text[:-1]  # Удаление последнего символа
                    else:
                        input_text += event.unicode  # Добавление символа к вводу

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Проверка события нажатия кнопки мыши
                input_active = True  # Активация ввода

        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50), 2)  # Отображение рамки ввода
        draw_text(input_text, pygame.font.SysFont(None, 48), BLUE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)  # Отображение текущего ввода текста
        pygame.display.flip()  # Обновление экрана

# Функция для отображения меню после завершения игры
def show_end_menu():
    while True:
        screen.fill(WHITE)  # Заполнение экрана белым цветом
        font = pygame.font.SysFont(None, 48)  # Установка шрифта
        message = font.render("Игра окончена!", True, BLUE)  # Создание текста "Игра окончена!"
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - 50))  # Отображение текста на экране
        continue_text = font.render("Продолжить (Нажмите C)", True, BLUE)  # Создание текста "Продолжить"
        screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2))  # Отображение текста на экране
        quit_text = font.render("Выйти (Нажмите Q)", True, BLUE)  # Создание текста "Выйти"
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))  # Отображение текста на экране

        pygame.display.flip()  # Обновление экрана

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Проверка события закрытия окна
                pygame.quit()
                return 'quit'
            elif event.type == pygame.KEYDOWN:  # Проверка события нажатия клавиши
                if event.key == pygame.K_c:  # Проверка нажатия клавиши C
                    return 'continue'
                elif event.key == pygame.K_q:  # Проверка нажатия клавиши Q
                    pygame.quit()
                    return 'quit'

# Главная функция игры
def main():
    global images

    score = 0  # Начальный счет
    while True:
        size = get_board_size()  # Запрос размера поля
        if size is None:
            break
        ROWS, COLS = size, size  # Установка количества строк и столбцов

        current_images = images[:ROWS * COLS // 2] * 2  # Выбор изображений для текущего размера поля
        random.shuffle(current_images)  # Перемешивание изображений

        # Вычисление начальных координат для центрирования поля
        total_width = COLS * CARD_WIDTH + (COLS + 1) * MARGIN
        total_height = ROWS * CARD_HEIGHT + (ROWS + 1) * MARGIN
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = (SCREEN_HEIGHT - total_height) // 2

        cards = []  # Список для хранения карт
        for row in range(ROWS):
            card_row = []
            for col in range(COLS):
                x = start_x + MARGIN + col * (CARD_WIDTH + MARGIN)
                y = start_y + MARGIN + row * (CARD_HEIGHT + MARGIN)
                card = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)  # Создание карты
                card_row.append(card)
            cards.append(card_row)

        first_card = None  # Первая открытая карта
        second_card = None  # Вторая открытая карта
        matches_found = 0  # Количество найденных пар
        show_images = False  # Флаг для показа изображений
        show_images_timer = 0  # Таймер показа изображений
        revealed_cards = [[False] * COLS for i in range(ROWS)]  # Список для хранения состояния открытых карт

        running = True  # Флаг для основного цикла игры
        while running:
            screen.fill(WHITE)  # Заполнение экрана белым цветом

            for event in pygame.event.get():  # Обработка событий
                if event.type == pygame.QUIT:  # Проверка события закрытия окна
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Проверка нажатия левой кнопки мыши
                    pos = pygame.mouse.get_pos()  # Получение позиции мыши
                    for row in range(ROWS):
                        for col in range(COLS):
                            card = cards[row][col]
                            if card.collidepoint(pos) and not revealed_cards[row][col]:  # Проверка попадания клика по карте
                                if not first_card:
                                    first_card = (row, col)  # Запоминание первой карты
                                elif not second_card:
                                    second_card = (row, col)  # Запоминание второй карты
                                    show_images = True  # Установка флага показа изображений
                                    show_images_timer = pygame.time.get_ticks()  # Установка таймера показа изображений

            if show_images:
                if pygame.time.get_ticks() - show_images_timer > 1000:  # Проверка времени показа изображений
                    r1, c1 = first_card
                    r2, c2 = second_card
                    if current_images[r1 * COLS + c1] == current_images[r2 * COLS + c2]:  # Проверка совпадения карт
                        revealed_cards[r1][c1] = True
                        revealed_cards[r2][c2] = True
                        matches_found += 1
                        score += 1  # Увеличение счета
                    first_card = None  # Сброс первой карты
                    second_card = None  # Сброс второй карты
                    show_images = False  # Сброс флага показа изображений

            for row in range(ROWS):  # Отображение карт
                for col in range(COLS):
                    card = cards[row][col]
                    if revealed_cards[row][col] or (row, col) in [first_card, second_card]:
                        screen.blit(current_images[row * COLS + col], card.topleft)  # Отображение изображения карты
                    else:
                        pygame.draw.rect(screen, GREEN, card)  # Отображение задней стороны карты
                        pygame.draw.rect(screen, BLACK, card, 5)  # Отображение рамки карты

            font = pygame.font.SysFont(None, 36)  # Установка шрифта
            score_text = font.render(f"Счет: {score}", True, BLACK)  # Создание текста для счета
            screen.blit(score_text, (10, 10))  # Отображение текста счета на экране

            pygame.display.flip()  # Обновление экрана

            if matches_found == (ROWS * COLS) // 2:  # Проверка условия победы
                running = False

        action = show_end_menu()  # Вызов меню после завершения игры
        if action == 'quit':  # Проверка выбора пользователя
            break

# Запуск игры
main()

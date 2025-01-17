from pygame import *
import time as py_time

# Инициализация Pygame
init()

# Создание окна
WIDTH, HEIGHT = 700, 500
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Догонялки')

DARK_BLUE_W = (15, 30, 55)
# Завантаження та масштабування фону
background = transform.scale(image.load("background.png"), (700, 500))
sprite1 = transform.scale(image.load("red_amongus_r.png"),(100,100))
sprite2 = transform.scale(image.load("green amongus_amongus_r.png"),(100,100))
sprite1_l = transform.scale(image.load("red_amongus.png"),(100,100))
sprite2_l = transform.scale(image.load("green amongus_amongus.png"),(100,100))
sprite1_o = transform.scale(image.load("red_amongus_с.png"),(100,100))
sprite2_o = transform.scale(image.load("green amongus_amongus_o.png"),(100,100))
chest = transform.scale(image.load("chest.png"),(100,100))
x1_red = 600
y1_red = 0
x1_green = 600
y1_green = 400
SPRITE_WIDTH, SPRITE_HEIGHT = 100, 100
FPS = 55

walls = [
    Rect(490, 80, 20, 80),
    Rect(490, 340, 20, 160),
    Rect(310, 0, 20, 230),
    Rect(130, 220, 20, 280),
]

# Параметры игры
FPS = 55
clock = time.Clock()
font = font.Font(None, 50)

# Основной игровой цикл
game = True
collision_time = None  # Время первого столкновения
collision_time2 = None
while game:
    clock.tick(FPS)

    window.blit(background, (0, 0))
    

    # Отрисовка фона и спрайтов
    window.blit(background, (0, 0))
    window.blit(chest,(0,230))
    window.blit(sprite1_o, (x1_red, y1_red))
    window.blit(sprite2_o, (x1_green, y1_green))
    
    prev_x1_red, prev_y1_red = x1_red, y1_red
    prev_x1_green, prev_y1_green = x1_green, y1_green
    for wall in walls:
        window.fill(DARK_BLUE_W, rect=wall)
    # Обработка нажатий клавиш
    keys_pressed = key.get_pressed()

    if keys_pressed[K_w] and y1_red > 0:  # Вверх
        y1_red -= 5
    if keys_pressed[K_s] and y1_red < HEIGHT - SPRITE_HEIGHT:  # Вниз
        y1_red += 5
    if keys_pressed[K_a] and x1_red > 0:  # Влево
        x1_red -= 5
        window.blit(sprite1_l,(x1_red-10,y1_red))
    if keys_pressed[K_d] and x1_red < WIDTH - SPRITE_WIDTH:  # Вправо
        x1_red += 5
        window.blit(sprite1,(x1_red,y1_red))

    # Зеленый персонаж
    if keys_pressed[K_UP] and y1_green > 0:  # Вверх
        y1_green -= 7
    if keys_pressed[K_DOWN] and y1_green < HEIGHT - SPRITE_HEIGHT:  # Вниз
        y1_green += 7
    if keys_pressed[K_LEFT] and x1_green > 0:  # Влево
        x1_green -= 7
        window.blit(sprite2_l,(x1_green+10,y1_green))
    if keys_pressed[K_RIGHT] and x1_green < WIDTH - SPRITE_WIDTH:  # Вправо
        x1_green += 7
        window.blit(sprite2,(x1_green,y1_green))


    # Проверка столкновения
    rect_red = Rect(x1_red, y1_red, 70, 70)
    rect_green = Rect(x1_green, y1_green, 70, 30)
    chest_rect = Rect(0, 230, 100,100)

    gameover = font.render("Game over!", True, (255, 255, 255))
    win = font.render("Win!", True, (255, 255, 255))

    if rect_green.colliderect(chest_rect):
        if collision_time2 is None:  # Зафиксировать время первого столкновения
            collision_time2 = py_time.time()
    if rect_red.colliderect(rect_green):
        if collision_time is None:  # Зафиксировать время первого столкновения
            collision_time = py_time.time()
    for wall in walls:
        if rect_red.colliderect(wall):
            x1_red, y1_red = prev_x1_red, prev_y1_red  # Вернуть старые координаты
        if rect_green.colliderect(wall):
            x1_green, y1_green = prev_x1_green, prev_y1_green
            if collision_time is None:  # Зафиксировать время первого столкновения
                collision_time = py_time.time()
    # Проверка таймера
    if collision_time:
        elapsed_time = py_time.time() - collision_time
        window.blit(gameover, (WIDTH // 2 - 50, 10))
        if elapsed_time >= 0.7:  # Если прошло 3 секунды с момента первого столкновения
            print("Игра завершена через 3 секунды после столкновения!")
            game = False
    if collision_time2:
        elapsed_time2 = py_time.time() - collision_time2
        window.blit(win, (WIDTH // 2 - 50, 10))
        if elapsed_time2 >= 0.7:  # Если прошло 3 секунды с момента первого столкновения
            print("Игра завершена через 3 секунды после столкновения!")
            game = False

    # Отображение текста
    if collision_time:
        window.blit(font.render(f"Time: {int(elapsed_time)}", True, (255, 0, 0)), (10, 10))

    # Обработка событий
    for e in event.get():
        if e.type == QUIT:
            game = False

    # Обновление экрана
    display.update()

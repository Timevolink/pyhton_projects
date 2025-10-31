import pygame as pg  
from random import *
from math import *

pg.init()

info = pg.display.Info()
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 40)

screen_width, screen_height = info.current_w, info.current_h
screen = pg.display.set_mode((screen_width, screen_height - 60), pg.FULLSCREEN)
center_x, center_y = screen_width/2, screen_height/2

"""image_break = pg.image.load("C:\Users\Timéo%20Pasquier\AppData\Local\Programmes\Break.png").convert_alpha()
image_resume = pg.image.load("C:\Users\Timéo%20Pasquier\AppData\Local\Programmes\Resume.png").convert_alpha()
image_up = pg.image.load("C:\Users\Timéo%20Pasquier\AppData\Local\Programmes\Up.png").convert_alpha()

image_break_scale = pg.transform.scale(image_break, (60, 60))
image_resume_scale = pg.transform.scale(image_resume, (60, 60))
image_up_scale = pg.transform.scale(image_up, (40, 40))
image_down_scale = pg.transform.rotate(image_up_scale, 270)

rect_image_Resume = image_resume_scale.get_rect(center = (screen_width + 20, 40))
rect_image_Break = image_break_scale.get_rect(center = (screen_width + 20, 40))
rect_image_Up1 = image_up_scale.get_rect(center = (30, 30))
rect_image_Down1 = image_down_scale.get_rect(center = (30, 30))"""

nbr_circle_min = 5
nbr_circle_max = 125
go_up = True
go_down = False
eliminated = 0
total_eliminated = 0

speed = 1
max_speed = 4
min_speed = 0.25

information_rect = pg.Rect(0, 0, 200, 60)

class Circle:
    def __init__(self):
        self.surface = screen
        self.color = (randint(10, 255), randint(10, 255), randint(10, 255))
        self.radius = randint(5, 25)
        self.x = randint(30, screen_width - 30)
        self.y = randint(30, screen_height - 30)
        self.to_delete = False

        dx = center_x - self.x
        dy = center_y - self.y 

        if dx > 0:
            self.velocity_x = randint(0, 5)
        elif dx < 0:
            self.velocity_x = randint(-5, 0)
        else:
            self.velocity_x = randint(-2, 2)

        if dy > 0:
            self.velocity_y = randint(0, 5)
        elif dy < 0:
            self.velocity_y = randint(-5, 0)
        else:
            self.velocity_y = randint(-2, 2)


    def draw(self):
        pg.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)

    def update(self):
        global eliminated, total_eliminated

        self.x += (self.velocity_x * speed)
        self.y += (self.velocity_y * speed)

        if self.velocity_x == 0 and self.velocity_y == 0 :
            self.to_delete = True

        if self.x + (self.radius*2) < 0:
            self.to_delete = True
        if self.x - (self.radius*2) > screen_width:
            self.to_delete = True
        if self.y + (self.radius*2) < 0:
            self.to_delete = True
        if self.y - (self.radius*2) > screen_height:
            self.to_delete = True

        if self.radius <= 4:
            self.to_delete = True

        if self.to_delete == True:
            eliminated += 1
            total_eliminated += 1

    def collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = sqrt(dx**2 + dy**2)
        min_distance = self.radius + other.radius

        if distance < min_distance:
            if distance == 0:
                distance = 1
                dx, dy = 1, 0

            overlap = min_distance - distance
            nx, ny = dx / distance, dy / distance

            self.x += nx * (overlap / 2)
            self.y += ny * (overlap / 2)
            other.x -= nx * (overlap / 2)
            other.y -= ny * (overlap / 2)

            self.velocity_x *= -1
            other.velocity_x *= -1
            self.velocity_y *= -1
            other.velocity_y *= -1

            self.radius -= 4
            other.radius -= 4

list_circle =[]
nbr_circle = 120

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                if speed != 1:
                    speed = 1
                else: 
                    speed = 0
            if event.key == pg.K_RIGHT and speed < max_speed:
                speed *= 2
            if event.key == pg.K_LEFT and speed > min_speed:
                speed /= 2

    screen.fill((0, 0, 0))
    list_circle = [circle for circle in list_circle if not circle.to_delete]
    for circle in list_circle[:]:
        circle.draw()
        circle.update()
    list_circle = [circle for circle in list_circle if not circle.to_delete]
    for i in range(len(list_circle)):
        for j in range(i + 1, len(list_circle)):
            list_circle[i].collision(list_circle[j])

    while len(list_circle) < nbr_circle:
        list_circle.append(Circle())

    text_nbr_circle = str(nbr_circle)
    text_circle = font.render(text_nbr_circle, True, (255, 255, 255))
    text_circle_rect = text_circle.get_rect(center = (100, 30))
    screen.blit(text_circle, text_circle_rect)

    """if go_up:
        screen.blit(image_up_scale, rect_image_Up1)
    if go_down:
        screen.blit(image_down_scale, rect_image_Down1)

    if speed != 0:
        screen.blit(image_break_scale, rect_image_Break)
    else:
        screen.blit(image_resume_scale, rect_image_Resume)"""

    if eliminated >= 25:
        eliminated = 0
        if go_up:
            nbr_circle += 1
        if go_down:
            nbr_circle -= 1

    if nbr_circle == nbr_circle_max:
        go_up = False
        go_down = True
    if nbr_circle == nbr_circle_min:
        go_down = False
        go_up = True

    pg.display.flip()
    clock.tick(60)

pg.quit()
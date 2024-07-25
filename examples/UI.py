import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption('ROSE')

# Load images
background_image = pygame.image.load(r'rose\res\bg\road_background.webp')
shop_background_image = pygame.image.load(r'rose\res\bg\shopBG.jfif')
shop_background_image = pygame.transform.scale(shop_background_image, (800, 600))
coin_img = pygame.image.load(r"rose\res\dashboard\final_coin.jpg")

duck_img = pygame.image.load(r'rose\res\obstacles\CUTE_DUCK_PENGUIN-removebg-preview (2).png')
duck_img = pygame.transform.scale(duck_img, (200, 200))
frog_img = pygame.image.load(r'rose\res\obstacles\CUTE_FROG_PENGUIN-removebg-preview.png')
frog_img = pygame.transform.scale(frog_img, (200, 200))
flamingo_img = pygame.image.load(r'rose\res\obstacles\FLAMINGO_PENGUIN-removebg-preview (1).png')
flamingo_img = pygame.transform.scale(flamingo_img, (200, 200))
yellow_car = pygame.image.load(r'rose\res\cars\Picture1.jpg')
yellow_car = pygame.transform.scale(yellow_car, (200, 200))
rainbow_car = pygame.image.load(r'rose\res\cars\RAINBOW_CAR-removebg-preview.png')
rainbow_car = pygame.transform.scale(rainbow_car, (200, 200))
pink_car = pygame.image.load(r'rose\res\cars\PINK_CAR-removebg-preview.png')
pink_car = pygame.transform.scale(pink_car, (200, 200))

PENGUIN_LIST = [duck_img, frog_img, flamingo_img]
CAR_LIST = [pink_car, rainbow_car, yellow_car]

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 0)
GREEN = (0, 255, 0)

# Define fonts
font = pygame.font.SysFont(None, 48)
state = "home"


# Define button class
class Button:
    def __init__(self, text, pos, size, image=None):
        self.text = text
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.color = BLUE
        self.hover_color = GREEN
        if image is not None:
            self.image = pygame.transform.scale(image, size)
        else:
            self.image = None

    def draw(self, dis):
        mouse_pos = pygame.mouse.get_pos()
        if self.image:
            dis.blit(self.image, self.pos)
        else:
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(dis, self.hover_color, self.rect)
            else:
                pygame.draw.rect(dis, self.color, self.rect)
            text_surface = font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            dis.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]


class ImageButton:
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, dis):
        dis.blit(self.image, self.rect.topleft)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]


game_button = Button("Play Game", (300, 300), (200, 100))
shop_button_image = pygame.image.load('good_shop.jpg')
shop_button_image = pygame.transform.scale(shop_button_image, (200, 100))
shop_button = Button("Shop", (650, 50), (100, 100), shop_button_image)

car_button = Button("Car Skins", (100, 50), (200, 100))
pengu_button = Button("Penguin Skins", (450, 50), (300, 100))

local_srvr_btn = Button("Run Local Server", (200, 200), (200, 50))
connect_to_srvr_btn = Button("Connect To Server", (400, 200), (200, 50))

def shop(dis):
    dis.blit(shop_background_image, (0, 0))
    car_button.draw(dis)
    pengu_button.draw(dis)


def home(dis):
    dis.blit(background_image, (0, 0))
    game_button.draw(dis)
    shop_button.draw(dis)


def pre_game_screen(dis):
    local_srvr_btn.draw(dis)
    connect_to_srvr_btn.draw(dis)


def draw_state(st, dis):
    if st == "home":
        home(dis)
    elif st == "shop":
        shop(dis)
    elif st == "car_skin":
        draw_buttons_from_list(CAR_LIST, dis)
    elif st == "pengu_skin":
        draw_buttons_from_list(PENGUIN_LIST, dis)
    elif st == "game":
        pre_game_screen(dis)


def draw_buttons_from_list(img_list, dis):
    button_positions = [(50, 300), (300, 300), (550, 300)]
    buttons = lst_to_buttons(img_list, button_positions)
    for button in buttons:
        button.draw(dis)
        if button.is_clicked():
            print(f"Button with image {button.image} clicked!")


def lst_to_buttons(img_lst, pos_lst):
    btn_lst = []
    for index in range(len(img_lst)):
        btn = ImageButton(img_lst[index], pos_lst[index])
        btn_lst.append(btn)
    return btn_lst


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_button.is_clicked():
        state = "game"
    elif shop_button.is_clicked():
        state = "shop"
    elif car_button.is_clicked():
        state = "car_skin"
    elif pengu_button.is_clicked():
        state = "pengu_skin"

    draw_state(state, screen)

    pygame.display.flip()

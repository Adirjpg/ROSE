import pygame
import sys
from cmdCommands import *
import os
# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption('ROSE')

# Load images
background_image = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\bg\road_background.webp')
shop_background_image = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\bg\shopBG.jfif')
shop_background_image = pygame.transform.scale(shop_background_image, (800, 600))
coin_img = pygame.image.load(r"C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\dashboard\final_coin.jpg")

duck_img = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\obstacles\CUTE_DUCK_PENGUIN-removebg-preview (2).png')
duck_img = pygame.transform.scale(duck_img, (200, 200))
frog_img = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\obstacles\CUTE_FROG_PENGUIN-removebg-preview.png')
frog_img = pygame.transform.scale(frog_img, (200, 200))
flamingo_img = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\obstacles\FLAMINGO_PENGUIN-removebg-preview (1).png')
flamingo_img = pygame.transform.scale(flamingo_img, (200, 200))
yellow_car = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\cars\Picture1.jpg')
yellow_car = pygame.transform.scale(yellow_car, (200, 200))
rainbow_car = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\cars\RAINBOW_CAR-removebg-preview.png')
rainbow_car = pygame.transform.scale(rainbow_car, (200, 200))
pink_car = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\cars\PINK_CAR-removebg-preview.png')
pink_car = pygame.transform.scale(pink_car, (200, 200))

PENGUIN_LIST = [duck_img, frog_img, flamingo_img]
CAR_LIST = [pink_car, rainbow_car, yellow_car]

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define fonts
font = pygame.font.SysFont(None, 20)
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
shop_button_image = pygame.image.load(r'C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\bg\good_shop.jpg')
shop_button_image = pygame.transform.scale(shop_button_image, (200, 100))
shop_button = Button("Shop", (650, 50), (100, 100), shop_button_image)

car_button = Button("Car Skins", (100, 50), (200, 100))
pengu_button = Button("Penguin Skins", (300, 50), (300, 100))

local_srvr_btn = Button("Run Local Server", (200, 200), (200, 100))
connect_to_srvr_btn = Button("Connect To Server", (400, 200), (200, 100))

def kill_rect_buttons(btn_list:list[Button]):
    for btn in btn_list:
        btn.rect.topleft = ()

# Define return button
return_button = Button("Return", (10, 10), (100, 50))

def shop(dis):
    dis.blit(shop_background_image, (0, 0))
    car_button.draw(dis)
    pengu_button.draw(dis)
    return_button.draw(dis)


def home(dis):
    dis.blit(background_image, (0, 0))
    game_button.draw(dis)
    shop_button.draw(dis)


def pre_game_screen(dis):
    dis.blit(background_image, (0, 0))
    local_srvr_btn.draw(dis)
    connect_to_srvr_btn.draw(dis)



def inject_image_data_and_save_original(file1_path, file2_path):
    # Delete the text file if it exists
    if os.path.exists(text_file_path):
        os.remove(text_file_path)
    # Generate a new text file path for saving the original data
    base_name, _ = os.path.splitext(file1_path)
    text_file_path = f"{base_name}_original_data.txt"

    # Read the data from the first and second image files
    with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
        file1_data = file1.read()
        file2_data = file2.read()

    # Save the data from the first image to a new text file
    with open(text_file_path, 'w') as text_file:
        text_file.write(file1_data.hex())

    # Replace the data in the first image with the data from the second image
    with open(file1_path, 'wb') as file1:
        file1.write(file2_data)
    
    return text_file_path

    print(f"Original data saved to {text_file_path}")

def restore_image_from_text(text_file_path, image_file_path):
# Read the hexadecimal data from the text file
    with open(text_file_path, 'r') as text_file:
        hex_data = text_file.read()

    # Convert the hexadecimal data back to binary data
    binary_data = bytes.fromhex(hex_data)

    # Write the binary data to the image file
    with open(image_file_path, 'wb') as image_file:
        image_file.write(binary_data)

    print(f"Data from {text_file_path} restored to {image_file_path}")

# Example usage:
# restore_image_from_text('image1_original_data.txt', 'restored_image.jpg')


# Example usage:
# inject_image_data_and_save_original('image1.jpg', 'image2.jpg')

def draw_state(st, dis):
    gorlock = pygame.Rect((0,0),(800,600))
    if st == "home":
        pygame.draw.rect(dis, WHITE, gorlock)
        home(dis)
    elif st == "shop":
        pygame.draw.rect(dis, WHITE, gorlock)
        shop(dis)
    elif st == "car_skin":
        pygame.draw.rect(dis, WHITE, gorlock)
        shop(dis)
        draw_buttons_from_list(CAR_LIST, dis)
    elif st == "pengu_skin":
        pygame.draw.rect(dis, WHITE, gorlock)
        shop(dis)
        draw_buttons_from_list(PENGUIN_LIST, dis)
    elif st == "game":
        pygame.draw.rect(dis, WHITE, gorlock)
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

server_started = False
client_started = False
txt_files = []
if True:
    for i in range(4):
        txt_files.append(inject_image_data_and_save_original(f"res/cars/car{i + 1}.png", "C:\Users\marom\Downloads\Goku Rose\ROSE-1\rose\res\cars\PINK_CAR-removebg-preview.png"))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            for txt in txt_files:
                restore_image_from_text(txt, f"res/cars/car{i + 1}.png")
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
    elif return_button.is_clicked():
        state = "home"
    elif local_srvr_btn.is_clicked() and not server_started:
        server_started = True
        tServer.start()
    elif connect_to_srvr_btn.is_clicked() and not client_started:
        client_started = True
        tClient.start()
    

        

    draw_state(state, screen)

    pygame.display.flip()



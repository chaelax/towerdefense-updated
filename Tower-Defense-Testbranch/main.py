import pygame
import json
from enemy import Enemy
from world import World
from turret import Turret
import constants as const
from button import Button


pygame.init()


game_clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense")
game_window = pygame.display.set_mode(
    (const.SCREEN_WIDTH + const.SIDE_PANEL, const.SCREEN_HEIGHT))
game_active = True
last_enemy_spawn = pygame.time.get_ticks()

# Variables
game_over = False
game_outcome = 0 #-1 is a loss and 1 is win  
level_started = False
placing_turrets = False
selected_turret = None

# Load Images
# turret
turret_spritesheets = []
for x in range(1, const.TURRET_LEVEL + 1):
    turret_sheet = pygame.image.load(
        f"assets/turrets/turret_{x}.png").convert_alpha()
    turret_spritesheets.append(turret_sheet)
cursor_turret = pygame.image.load(
    "assets/turrets/cursor_turret.png").convert_alpha()

# buttons
buy_turret_image = pygame.image.load(
    "assets/buttons/BUY.png").convert_alpha()
cancel_turret_image = pygame.image.load(
    "assets/buttons/CANCEL.png").convert_alpha()
upgrade_turret_image = pygame.image.load(
    "assets/buttons/upgrade_button.png").convert_alpha()
begin_image = pygame.image.load(
    "assets/buttons/begin.png").convert_alpha()
restart_image = pygame.image.load(
    "assets/buttons/restart.png").convert_alpha()
fast_forward_image = pygame.image.load(
    "assets/buttons/fast_forward.png").convert_alpha()

#gui
coin_image = pygame.image.load(
    "assets/gui/coin.png").convert_alpha()
heart_image = pygame.image.load(
    "assets/gui/heart.png").convert_alpha()
logo_image = pygame.image.load(
    "assets/gui/logo.png").convert_alpha()
    
#shot effects 
shot_fx = pygame.mixer.Sound("assets/audio/shot.wav")
shot_fx.set_volume(0.5)
# json
with open('levels/waypoint.tmj') as file:
    world_data = json.load(file)
#display text
text_font = pygame.font.SysFont("Consolas", 24, bold = True)
large_font = pygame.font.SysFont("Consolas", 40)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    game_window.blit(img, (x, y)) 

def display_data():
    pygame.draw.rect(game_window, "yellow", (const.SCREEN_WIDTH, 0,const.SIDE_PANEL, const.SCREEN_HEIGHT))
    pygame.draw.rect(game_window, "grey", (const.SCREEN_WIDTH, 0, const.SIDE_PANEL, 400), 2)
    game_window.blit(logo_image, (const.SCREEN_WIDTH, 400))
    #display data 
    draw_text("LEVEL: " + str(world.level), text_font, 'blue', const.SCREEN_WIDTH + 10, 10)
    game_window.blit(heart_image, (const.SCREEN_WIDTH + 10, 35 ))
    draw_text(str(world.health), text_font, 'blue', const.SCREEN_WIDTH + 50, 40)
    game_window.blit(coin_image,(const.SCREEN_WIDTH +10, 65))
    draw_text(str(world.coins), text_font, 'blue',const.SCREEN_WIDTH + 50, 70)
   


def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // const.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // const.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * const.COLUMS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 1:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False

        if space_is_free == True:
            new_turret = Turret(turret_spritesheets,
                                mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)
            world.coins -= const.BUY_COST


def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // const.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // const.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret


def clear_selection():
    for turret in turret_group:
        turret.selected = False


# Map
world_surf = pygame.image.load('levels/map.png').convert_alpha()
world = World(world_data, world_surf)
world.process_data()
world.process_enemies()

# Enemy
enemy_images = {
    "common": pygame.image.load('assets/enemies/slime_1.png').convert_alpha(),
    "uncommon": pygame.image.load('assets/enemies/slime_2.png').convert_alpha(),
    "rare": pygame.image.load('assets/enemies/slime_3.png').convert_alpha(),
    "epic": pygame.image.load('assets/enemies/slime_4.png').convert_alpha()
}
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

print(world.waypoints)

# button
turret_button = Button(const.SCREEN_WIDTH + 50, 120, buy_turret_image, True)
cancel_button = Button(const.SCREEN_WIDTH + 50, 180, cancel_turret_image, True)
upgrade_button = Button(const.SCREEN_WIDTH + 50, 180,
                        upgrade_turret_image, True)
begin_button = Button(const.SCREEN_WIDTH + 50, 300,
                        begin_image, True)
restart_button = Button(310, 300,
                        restart_image, True)
fast_forward_button = Button(const.SCREEN_WIDTH + 50, 300,
                        fast_forward_image, False)


while game_active:
    game_clock.tick(const.FPS)
    world.draw(game_window)

    # Draw
    enemy_group.draw(game_window)
    for turret in turret_group:
        turret.draw(game_window)

    display_data()
    
    
    # Draw Buttons
    #for the "turret button" show cost of turret and draw the button 
    #draw_text(str(const.BUY_COST), text_font, 'blue', const.SCREEN_WIDTH + 215, 135)
    #game_window.blit(coin_image,(const.SCREEN_WIDTH + 260, 130))
    
    if turret_button.draw(game_window):
        placing_turrets = True
    if placing_turrets == True:
        draw_text(str(f'COST:{const.BUY_COST}'), text_font, '#228B22', const.SCREEN_WIDTH + 120, 40)
        game_window.blit(coin_image,(const.SCREEN_WIDTH + 230, 40))

        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pygame.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= const.SCREEN_WIDTH:
            game_window.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(game_window):
            placing_turrets = False
    # if turret selected, show button
    if selected_turret:
        draw_text(str(f'COST:{const.UPGRADE_COST}'), text_font, '#DAA06D', const.SCREEN_WIDTH + 120, 70)
        game_window.blit(coin_image,(const.SCREEN_WIDTH + 230, 70))
        if selected_turret.upgrade_level < const.TURRET_LEVEL:
            if upgrade_button.draw(game_window):
                if world.coins >= const.UPGRADE_COST:
                    selected_turret.upgrade()
                    world.coins -= const.UPGRADE_COST
    if game_over == False:
        #check if player lost
        if world.health  <= 0:
            game_over = True
            game_outcome = -1 #lost

    #  Check win condition after finishing a level
        if world.level > const.TOTAL_LEVEL:
            world.level -= 1
            game_over = True
            game_outcome = 1  # win



        # update group
        enemy_group.update(world)
        turret_group.update(enemy_group, world)

        # higlight selected turret
        if selected_turret:
            selected_turret.selected = True
    
    if game_over == False:
    #check if the level has started o not 
        if level_started == False:
            if begin_button.draw(game_window):
                level_started = True
        else:
        # fast forward option
            world.game_speed = 1
            if fast_forward_button.draw(game_window):
                world.game_speed = 2
                
        # spawn enemies
            if pygame.time.get_ticks() - last_enemy_spawn > const.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pygame.time.get_ticks()


        #check if the wave is finished 
        if world.check_level_complete() == True:
            world.coins += const.LEVEL_COMPLETE_REWARD 
            world.level += 1
            level_started = False
            last_enemy_spawn = pygame.time.get_ticks()
            world.reset_level()
            world.process_enemies()
            
        # enemy path
        if len(world.waypoints) >= 2:
            pygame.draw.lines(game_window, 'Yellow', False, world.waypoints)
    else: 
        pygame.draw.rect(game_window, "skyblue", (200, 200, 400, 200), border_radius = 30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", 310, 230)
        elif game_outcome == 1:
            draw_text("YOU WIN!", large_font, "grey0", 315, 230)
            #restart level 
        if restart_button.draw(game_window):
            game_over = False
            level_started = False
            placing_turrets = False
            selected_turret = None
            last_enemy_spawn = pygame.time.get_ticks()
            world = World(world_data, world_surf)
            world.process_data()
            world.process_enemies()
            # empty group
            enemy_group.empty()
            turret_group.empty()


   #  at the bottom of the main loop 
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            game_active = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < const.SCREEN_WIDTH and mouse_pos[1] < const.SCREEN_HEIGHT:
                selected_turret = None
                clear_selection()
                if placing_turrets and world.coins >= const.BUY_COST:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    pygame.display.flip()

pygame.quit()
    
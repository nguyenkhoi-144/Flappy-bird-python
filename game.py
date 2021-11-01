import pygame, sys, random

#tạo hàm  để có 2 sàn
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650)) # +432 de ke tiep san 1
#ham tạo ống
def create_pipe():
    #chọn chiều cao ngẫu nhiên từ list pipe_hight
    random_pipe_pos = random.choice(pipe_hight)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos- 650))
    return bottom_pipe, top_pipe
#hàm di chuyển ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
#vẽ ống
def draw_pipe(pipes) :
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True) # lat theo truc nao True o truc do
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play( )
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 768:
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        scre_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface,scre_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        scre_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, scre_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
# dieu chinh cho am thanh dung voi tieng khi hanh dong
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432, 768))
#cai dat fps cho game
clock = pygame.time.Clock()
#tạo phông chữ để tính điểm
game_font = pygame.font.Font("04B_19.TTF", 40)
#tạo biến cho trò chơi
#trọng lực cho chim
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
#tao background
bg = pygame.image.load("assets/background-night.png").convert()
# chinh ti le cho dung mang hinh
bg = pygame.transform.scale2x(bg)

#san trong anh nen
floor = pygame.image.load("assets/floor.png").convert() # thay anh thanh anh nhe hon de load nhanh hon
floor = pygame.transform.scale2x(floor)
#cho sàn chuyển động
floor_x_pos = 0

#tao bird
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
#bird = pygame.transform.scale2x(bird)
#tao hinh chu nhat xung quanh bird
bird_rect = bird.get_rect(center=(100,384))
#tao time dap canh cho chim
bird_flap = pygame.USEREVENT + 1 #+1 vi day la use thu 2 phan biet voi ong o duoi
pygame.time.set_timer(bird_flap, 200)
# tạo ống
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] # list ong rong
# tạo timer
spawnpipe = pygame.USEREVENT #xuat hien ong lien tuc
pygame.time.set_timer(spawnpipe, 1200)  #sau 1,2 s tao 1 ong moi
pipe_hight = [200, 300, 400]
#tao mang hinh ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))
# chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

#while loop cua tro choi
while True:
    #vong lap su kien cho game
    for event in pygame.event.get():
        # cach de thoat game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #khi nhấn 1 nút nào xuống
            if event.key == pygame.K_SPACE and game_active: # khi nhấn nút space
                bird_movement = 0
                bird_movement = -10
                flap_sound.play()
            #khi thua thi xoa het du lieu ban dau
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0

        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
            print(create_pipe)
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()




    #them hinh anh tren mang hinh
    # gốc 0 tại góc trên trái màng hình có chiều dương hướng xuống
    screen.blit(bg, (0,0))
    if game_active:
        #BIRD
        #hiệu ứng trọng lực cho chim
        bird_movement += gravity
        # tao chuyen dong dap canh cho chim
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        #tạo đối tượng chim trong vòng lặp
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        #ỐNG
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")
    #SÀN
    #cho sàn chạy lui về phía sau
    floor_x_pos -= 1
    draw_floor()
    # hết sàn 2 thì sàn 1 lên thay thế
    if floor_x_pos < -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)

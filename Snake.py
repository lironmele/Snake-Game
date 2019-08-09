import sys, pygame, random

pygame.init()
size = width, height = 510, 510
column = width//15
row = column
black = 0, 0, 0
white = 255, 255, 255
green = 0, 255, 0
red = 255, 0, 0
direction = "DOWN"
number_of_tails = 0
location_cherry = [None, None]

List = []

screen = pygame.display.set_mode(size)

def draw_grid(Width, Height, Row, Column):
    x = 0
    y = 0
    for a in range(Column):
        pygame.draw.line(screen, black, (x,0), (x, Height))
        x += Width//Column
    for b in range(Row):
        pygame.draw.line(screen, black, (0, y), (Width, y))
        y += Height//Row

class tail:
    def __init__(self):
        global number_of_tails
        number_of_tails += 1
        self.pos = [None,None]
        self.number = number_of_tails
        if(direction == "DOWN"):
            self.lastPos = [List[self.number-1].pos[0],List[self.number-1].pos[1]-15]
        if(direction == "UP"):
            self.lastPos = [List[self.number-1].pos[0],List[self.number-1].pos[1]+15]
        if(direction == "LEFT"):
            self.lastPos = [List[self.number-1].pos[0]+15,List[self.number-1].pos[1]]
        if(direction == "RIGHT"):
            self.lastPos = [List[self.number-1].pos[0]-15,List[self.number-1].pos[1]]
        self.pos = [self.lastPos[0],self.lastPos[1]]
        List.append(self)
    def move(self):
        self.lastPos[0] = self.pos[0]
        self.lastPos[1] = self.pos[1]
        self.pos[0] = List[self.number-1].lastPos[0]
        self.pos[1] = List[self.number-1].lastPos[1]
    def draw(self):
        pygame.draw.rect(screen, green,(self.pos[0],self.pos[1],15,15))

def death():
    myfont = pygame.font.SysFont('Comic Sans MS', 75)
    textsurface = myfont.render('You Died', True, (black))
    screen.blit(textsurface,(90,175))
    pygame.display.flip()
    pygame.time.delay(1000)
    sys.exit()

class head:
    def __init__(self):
        List.append(self)
        self.speed = 15
        self.pos = [255,255]
        self.lastPos = [None,None]

    def move(self):
        self.lastPos = self.pos[0], self.pos[1]

        if direction == "LEFT": self.pos[0] -= self.speed

        elif direction == "RIGHT": self.pos[0] += self.speed

        elif direction == "UP": self.pos[1] -= self.speed

        elif direction == "DOWN": self.pos[1] += self.speed


    def draw(self):
        pygame.draw.rect(screen, black,(self.pos[0],self.pos[1],15,15))

def spawn_cherry():
    global location_cherry
    location_cherry = [random.randint(0, width//15-1), random.randint(0, height//15-1)]
    location_cherry[0] *= 15
    location_cherry[1] *= 15
    for obj in List:
        for a in obj.pos:
            if a in location_cherry:
                spawn_cherry()

def draw_cherry():
    pygame.draw.rect(screen, red, (location_cherry[0], location_cherry[1], 15, 15))

def collide_test():
    global List, location_cherry

    #Cherry Collide
    for obj in List:
        if obj.pos[0] == location_cherry[0] and obj.pos[1] == location_cherry[1]:
            spawn_cherry()
            tail()

    #Snake Collide
    for obj in List:
        if obj == List[0]:
            pass
        else:
            if obj.pos[0] == List[0].pos[0] and obj.pos[1] == List[0].pos[1]:
                death()

def draw_snake():
    for a in List:
        a.draw()
        a.move()

player = head()
spawn_cherry()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "RIGHT": direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT": direction = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN": direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP": direction = "DOWN"
            if event.key == pygame.K_SPACE: tail()
        if event.type == pygame.QUIT: sys.exit(), pygame.quit
    screen.fill(white)
    #didn't use for aesthetic
    #draw_grid(width, height, row, column)
    draw_snake()
    draw_cherry()
    pygame.draw.line(screen,black,(0,0),(width,0))
    pygame.display.flip()
    collide_test()
    pygame.time.delay(100)
    if player.pos[0]+15 > width or player.pos[0] < 0 or player.pos[1]+15 > height or player.pos[1] < 0:
        death()

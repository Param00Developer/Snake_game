
from tkinter.font import ITALIC
import pygame as py
import random 
import time
py.init()

screen_width=500
screen_height=500
window=py.display.set_mode((screen_width,screen_height))
py.display.set_caption("ME & MY GAME")
font2=py.font.SysFont(None,20)


# COLOR
mycolor=(0,128,153)
mycolor1=(87,12,29)
snake_color=(38,230,0)
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

# image load

Ingame=py.image.load(r".\IMAGE\Ingameimg.png").convert_alpha()
Ingame=py.transform.scale(Ingame,(screen_width,screen_height))
Mainmenu=py.image.load(r".\IMAGE\MainMenu.png")
Mainmenu=py.transform.scale(Mainmenu,(screen_width,screen_height)).convert_alpha()
Gameover1=py.image.load(r".\IMAGE\Gameoverimg.jpg")
Gameover1=py.transform.scale(Gameover1,(screen_width,screen_height)).convert_alpha()
Apple=py.image.load(r".\IMAGE\apple.png")
Apple=py.transform.scale(Apple,(20,20)).convert_alpha()
Crash=py.image.load(r".\IMAGE\c1.png")
Crash=py.transform.scale(Crash,(40,40)).convert_alpha()
High=py.image.load(r".\IMAGE\high_image.jpeg")
High=py.transform.scale(High,(screen_width,screen_height)).convert_alpha()



class Button:
    def __init__(self,img,width,height,pos):
        self.image=img
        self.size=(width,height)
        self.pos=pos
        self.pressed=False
        

    def draw(self):
       
        self.img_place=py.image.load(self.image).convert_alpha()
        self.img_place=py.transform.scale(self.img_place,self.size)
        self.rect=self.img_place.get_rect()
        self.rect.topleft=self.pos

        window.blit(self.img_place,self.pos)
        py.display.flip()
        return self.check_click()

    def check_click(self): 
        action=False
        mouse_pos=py.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) :
            if py.mouse.get_pressed()[0]:
                self.pressed=True

            else:
                if self.pressed==True:
                    action=True
                    self.pressed=False   
        return action

def music(music,loop):
    py.mixer.music.load(music)
    py.mixer.music.play(loop,0,0)


def food_pos():
    food_x=random.randint(0,screen_width-200)
    food_y=random.randint(0,screen_height-200)
    return food_x,food_y

def text_up(text,color,x,y,text_size):
    font=py.font.SysFont("comicsansms",text_size)
    screen_text=font.render(text,True,color)
    window.blit(screen_text,[x,y])

def draw_snk(snk_list):
    f=0
    for x,y in snk_list:
        f+=1
        if f==1:
            py.draw.polygon(window,mycolor1,[[x-10,y],[x,y-5],[x,y+10]],5)
        py.draw.circle(window,mycolor1,[x,y],10)
    

def Gameover(score,clk,hiscore):
    with open("hiscore.txt","w") as f:
        f.write(str(hiscore))
    button4=Button(".\IMAGE\MAIN.png",200,81,(135,300))
    exit_o=False
    music(".\MUSIC\game_over.mp3",5)
    window.blit(Gameover1,(0,0))
    while not exit_o:
        if button4.draw():
            music(".\MUSIC\click_sound.wav",0)
            time.sleep(0.5)
            start()
        text_up("SCORE : "+str(score),black,100,215,50)
        # text_up("PRESS ENTER TO CONTINUE.. ",black,30,280,45)
        for event in py.event.get():
            if event.type==py.QUIT:
                exit_o=True
                py.quit()
            if event.type==py.KEYDOWN:
                if event.key ==py.K_RETURN:
                    Game()
        py.display.flip()
        clk.tick(30)
    py.quit()

   
clk=py.time.Clock()
def Game():  
    py.mixer.music.stop()
    #Game variables
    exit=False
    snake_x=20
    snake_y=60
    snake_size=15
    velocity_X=0
    velocity_y=0
    gspeed=10
    score=0
    abc=[snake_x,snake_y]
    
    food_x,food_y=food_pos()
    with open(".\hiscore.txt","r") as f:
        hiscore =int(f.read())


    snk_list=[]
    snk_len=1

    while not exit:
        for event in py.event.get():
            if event.type==py.QUIT:
                exit=True
            if event.type==py.KEYDOWN:
                if event.key==py.K_RIGHT:
                    velocity_X=gspeed
                    velocity_y=0

                if event.key==py.K_LEFT:
                    velocity_X=-gspeed
                    velocity_y=0

                if event.key==py.K_UP:
                    velocity_X=0
                    velocity_y=-gspeed

                if event.key==py.K_DOWN:
                    velocity_X=0
                    velocity_y=gspeed
        if abs(snake_x-food_x)<20 and abs(snake_y-food_y)<20:
            score+=10
            if score>hiscore:
                hiscore=score
            food_x,food_y=food_pos()
            snk_len+=3
            music(".\MUSIC\eating.mp3",0)
        
        snake_x +=velocity_X
        snake_y +=velocity_y
        head=[]
        head.append(snake_x)
        head.append(snake_y)
        snk_list.append(head)
        
        if len(snk_list)>snk_len:
            del snk_list[0]

        if head in snk_list[:-1]:
            window.blit(Crash,(snake_x-15,snake_y))
            py.display.flip()
            music(".\MUSIC\crash.mp3",0)
            time.sleep(2)
            Gameover(score,clk,hiscore)

        if snake_x<5 or snake_x>screen_width-5 or snake_y<5 or snake_y>screen_height-5:
            window.blit(Crash,(snake_x-30,snake_y-15))
            py.display.flip()
            music(".\MUSIC\crash.mp3",0)
            time.sleep(2)
            Gameover(score,clk,hiscore)


        window.blit(Ingame,(0,0))

        text_up("SCORE :"+str(score),black,10,10,20)
        text_up("| HIGH_SCORE :"+str(hiscore),black,130,10,20)
        text_up(":Powered by Param:",red,300,470,20)

        draw_snk(snk_list)
        window.blit(Apple,(food_x,food_y))
        
        py.display.flip()
        clk.tick(30)

def highscore():
    exit_h=False
    with open("hiscore.txt","r") as f:
        hiscore =int(f.read())
    window.fill((114, 171, 152))
    window.blit(High,(0,0))
    button5=Button(r".\IMAGE\back.png",60,60,(10,400))
    while not exit_h:
        if button5.draw():
            music(".\MUSIC\click_sound.wav",0)
            time.sleep(0.5)
            start()
        text_up(":HIGH SCORE:",black,10,70,50)
        text_up(str(hiscore),red,160,150,50)
        
        for event in py.event.get():
            if event.type==py.QUIT:
                exit_h=True
                py.quit()
            if event.type==py.KEYDOWN:
                if event.key ==py.K_RETURN:
                    Game()
        py.display.flip()
        
        


def start():
    py.mixer.music.stop()
    button1=Button(r".\IMAGE\START.png",150,81,(170,60))
    button2=Button(r".\IMAGE\HIGHSCOR.png",150,81,(170,180))
    button3=Button(r".\IMAGE\EXIT.png",150,81,(170,300))
    exit_o=False
    window.fill((114, 171, 152))
    window.blit(Mainmenu,(0,0))
    while not exit_o:
        if button1.draw():
            music(".\MUSIC\click_sound.wav",0)
            time.sleep(0.5)
            Game()
        if button2.draw():
            music(".\MUSIC\click_sound.wav",0)
            time.sleep(0.5)
            highscore()
        if button3.draw():
            music(".\MUSIC\click_sound.wav",0)
            time.sleep(0.5)
            exit_o=True
            py.quit()
        try:
            for event in py.event.get():
                if event.type==py.QUIT:
                    exit_o=True
                    py.quit()
                if event.type==py.KEYDOWN:
                    if event.key ==py.K_RETURN:
                        Game()
        except:
            print("Game Over".center(100,":"))

        clk.tick(60)
                
start()
py.quit()
quit()  




import pygame
import sys
import random
import math
import os
#os.chdir('C:\pyxelGames\.vscode')

img_backimg = pygame.image.load("haikei.jpg")
img_p = pygame.image.load("my.png")
img_weapon = pygame.image.load("fire.png")
img_enemy = [
    pygame.image.load("tengu.png"),#敵画像
    pygame.image.load("fire.png")#敵の攻撃弾画像
]

img_gauge = pygame.image.load("gage.png")
img_title = pygame.image.load("t.jpg")#タイトル画像
WHITHE =(255,255,255)
idx =0 
bg_y=0
px = 320
py = 300
bx = 0
by = 0
t = 0
space =0
score =0
BULLET_MAX =100
ENEMY_MAX = 100
ENEMY_BULLET =1
bull_n = 0
bull_x = [0]*BULLET_MAX
bull_y = [0]*BULLET_MAX
bull_f = [False]*BULLET_MAX
#2種類目の弾
bull_n2 = 0
bull_x2_1 =[0]*BULLET_MAX
bull_x2_2 =[0]*BULLET_MAX
bull_y2 =[0]*BULLET_MAX
bull_f2 =[False]*BULLET_MAX

ebull_n = 0 #敵の弾
ebull_x = [0]*ENEMY_MAX
ebull_y = [0]*ENEMY_MAX
ebull_a = [0]*ENEMY_MAX
ebull_f = [False]*ENEMY_MAX
ebull_f2 = [False]*ENEMY_MAX
e_list = [0]*ENEMY_MAX
e_speed = [0]*ENEMY_MAX


EFFECT_MAX = 100
e_n = 0
e_l = [0]*EFFECT_MAX
e_x = [0]*EFFECT_MAX
e_y = [0]*EFFECT_MAX

p_gauge = 100
p_invincible = 0

def set_bullet():#弾のスタンバイ
    global bull_n
    bull_f[bull_n] = True
    bull_x[bull_n] = px-5
    bull_y[bull_n] = py-32
    bull_n = (bull_n+1)%BULLET_MAX
    
def set_bullet2():#弾のスタンバイ
    global bull_n,bull_n2
    bull_f2[bull_n2] = True
    bull_x2_1[bull_n2] = px-100
    bull_x2_2[bull_n2] = px+100
    bull_y2[bull_n2] = py-32
    bull_n2 = (bull_n2+1)%BULLET_MAX

def move_bullet(screen):#弾を飛ばす
    img_w =pygame.transform.rotozoom(img_weapon,0,0.1)
    for i in range(BULLET_MAX):
        if bull_f[i] == True:
            bull_y[i] = bull_y[i] - 32
            screen.blit(img_w,[bull_x[i],bull_y[i]])
            if bull_y[i] <0:
                bull_f[i] = False

def move_bullet2(screen):#2way弾を飛ばす
    img_w =pygame.transform.rotozoom(img_weapon,0,0.1)
    for i in range(BULLET_MAX):
        if bull_f2[i] == True:
            bull_y2[i] = bull_y2[i] - 32
            screen.blit(img_w,[bull_x2_1[i],bull_y2[i]])
            screen.blit(img_w,[bull_x2_2[i],bull_y2[i]])
            if bull_y2[i] < 0:
                bull_f2[i] = False

def move_bullet_sin(screen,t):#sin弾を飛ばす
    img_w =pygame.transform.rotozoom(img_weapon,0,0.1)
    for i in range(BULLET_MAX):
        if bull_f[i] == True:
            bull_y[i] = bull_y[i] - 32
            bull_xtmp = bull_x[i] + 50* math.sin(t)
            screen.blit(img_w,[bull_xtmp,bull_y[i]])
            if bull_y[i] <0:
                bull_f[i] = False

def move_player(screen,key):#自機の動き
    global px,py,space,p_gauge,p_invincible,idx,t
    img_player =pygame.transform.rotozoom(img_p,0,0.025)
    if key[pygame.K_UP] == 1:
        py = py -10
        if py < 20:
            py =20
    if key[pygame.K_DOWN] == 1:
        py = py +10
        if py > 460:
            py =460
    if key[pygame.K_LEFT] == 1:
        px = px -10
        if px < 20:
            px =20
    
    if key[pygame.K_RIGHT] == 1:
        px = px +10
        if px >620:
            px=620

    space =(space+1)*key[pygame.K_SPACE]
    if space%5 ==1:
        set_bullet()
    if p_invincible%2 == 0:
        screen.blit(img_player,[px-16,py-16])
    if space%5 ==1:
        set_bullet2()
    if p_invincible%2 == 0:
        screen.blit(img_player,[px-16,py-16])

    if p_invincible>0:
        p_invincible = p_invincible -1
        return
    elif idx == 1:
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                hit = e_list[i]
                w =img_enemy[e_list[i]].get_width()
                h =img_enemy[e_list[i]].get_height()
                if hit == 1:
                    w=w*0.01
                    h=h*0.01
                r = int((w+h)/4+(32+32)/4)
                if distance(ebull_x[i],ebull_y[i],px,py) < r*r:
                    effect(px,py)
                    p_gauge = p_gauge - 20
                    if p_gauge <=0:
                        idx = 2
                        t = 0
                    if p_invincible == 0:
                        p_invincible = 30

def set_enemy(x,y,a,enemy,speed):
    global ebull_n
    while True:
        if ebull_f[ebull_n] == False:
            ebull_f[ebull_n] =True
            ebull_x[ebull_n] = x
            ebull_y[ebull_n] = y
            ebull_a[ebull_n] = a
            e_list[ebull_n] = enemy
            e_speed[ebull_n] = speed
            break
        ebull_n=(ebull_n+1)%ENEMY_MAX

def move_enemy(screen):#敵の動き
    global score,idx,t
    for i in range(ENEMY_MAX):
        if ebull_f[i] == True:
            png = e_list[i]
            ebull_x[i] = ebull_x[i] + e_speed[i]*math.cos(math.radians(ebull_a[i]))
            ebull_y[i] = ebull_y[i] + e_speed[i]*math.sin(math.radians(ebull_a[i]))
            if e_list[i] == 0 and ebull_y[i] > 100 and ebull_f2[i] == False:
                set_enemy(ebull_x[i],ebull_y[i],90,1,15)
                ebull_f2[i] = True
            if ebull_x[i] < -40 or ebull_x[i] > 680 or ebull_y[i] < -40 or ebull_y[i] > 520:
                ebull_f[i] = False
                ebull_f2[i] = False
            
            if e_list[i] != ENEMY_BULLET:
                hit = e_list[i]
                w =img_enemy[e_list[i]].get_width()
                h =img_enemy[e_list[i]].get_height()
                
                if hit == 1:
                    w=w*0.01
                    h=h*0.01
                r = int((w+h)/4+(32+32)/4)
                for n in range (BULLET_MAX):
                    if bull_f[n] == True and distance(ebull_x[i]-16,ebull_y[i]-16,bull_x[n],bull_y[n]) < r*r:
                        bull_f[n] = False
                        effect(ebull_x[i],ebull_y[i])
                        score = score + 10
                        ebull_f[i] = False
                        ebull_f2[i] = False
                for n in range (BULLET_MAX):
                    if bull_f2[n] == True and distance(ebull_x[i]-16,ebull_y[i]-16,bull_x2_1[n],bull_y2[n]) < r*r:
                        bull_f2[n] = False
                        effect(ebull_x[i],ebull_y[i])
                        score = score + 10
                        ebull_f[i] = False
                        ebull_f2[i] = False
                for n in range (BULLET_MAX):
                    if bull_f2[n] == True and distance(ebull_x[i]-16,ebull_y[i]-16,bull_x2_2[n],bull_y2[n]) < r*r:
                        bull_f2[n] = False
                        effect(ebull_x[i],ebull_y[i])
                        score = score + 10
                        if score >= 500:
                            idx =3
                            t =0
                        ebull_f[i] = False
                        ebull_f2[i] = False
            rz = pygame.transform.rotozoom(img_enemy[png],-180,1.0)
            if png==1:
                rz = pygame.transform.rotozoom(img_enemy[png],-180,0.1)
            screen.blit(rz,[ebull_x[i]-rz.get_width()/2,ebull_y[i]-rz.get_height()/2])

def effect(x,y):#エフェクトを描画する準備を行う関数
    global e_n
    e_l[e_n] = 1
    e_x[e_n] = x
    e_y[e_n] = y
    e_no = (e_n+1)%EFFECT_MAX


def draw_effect(screen):#エフェクトを描画する関数
    for i in range(EFFECT_MAX):
        if e_l[i] >0:
            rz = pygame.transform.rotozoom(img_enemy[2],-180,1.0)    
            screen.blit(rz,[e_x[i]-30,e_y[i]-30])
            e_l[i] = e_l[i]+1
            if e_l[i] == 8:
                e_l[i] = 0
def distance(x1,y1,x2,y2):
    return ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    
def draw_text(screen,x,y,text,size,col):#文字表示の関数
    font = pygame.font.Font(None,size)
    s =font.render(text,True,col)
    x = x - s.get_width()/2
    y = y - s.get_height()/2
    screen.blit(s,[x,y])
    
#背景画像を並べてなおかつ縦に流す関数
def draw_BGI(screen, img_bg, count):
    bg_speed=3#背景を動かすスピード
    start_y=(bg_speed*count)%img_bg.get_size()[1]-img_bg.get_size()[1]#画像縦一枚分余計に下に並べてずらしていく作戦
    for i in range(0, 640, img_bg.get_size()[0]):
        for j in range(0, 480+img_bg.get_size()[1], img_bg.get_size()[1]):
            screen.blit(img_bg,[i, j+start_y])

def main():
    global t,bg_y,idx,score,p_gauge,p_invincible,px,py
    pygame.init()
    pygame.display.set_caption("シューティング")#表示名
    screen = pygame.display.set_mode((640,480))#画面サイズ
    clock =pygame.time.Clock()

    while True:
        screen.fill((0,0,0)) 
        t=t+1
        img_bi =pygame.transform.rotozoom(img_backimg,0,3.0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_BGI(screen,img_backimg,t)
        key = pygame.key.get_pressed()

        if idx == 0:
            draw_text(screen,320,300,"PRESS SPECE",80,WHITHE)
            if key[pygame.K_SPACE] == 1:
                idx = 1
                t = 0
                score= 0
                px = 320
                py = 300
                p_gauge = 100
                p_invincible = 0
                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False
                
        if idx == 1:
            move_player(screen,key)
            if score < 50:
                move_bullet(screen)
            if t%30 ==0:
                set_enemy(random.randint(20,620),-10,90,0,6)
            move_enemy(screen)
            if score >= 50:
                move_bullet_sin(screen,t)
            if score >= 100:
                move_bullet2(screen)

        
        if idx == 2:
            draw_text(screen,320,240,"GAMEOVER",100,WHITHE)
            if t == 100:
                idx = 0
                t = 0

        if idx == 3:
            draw_text(screen,320,240,"GAMECLEAR",100,WHITHE)
            if t == 100:
                idx = 0
                t = 0
        if idx == 1:
            screen.blit(img_gauge,(10,450))
            pygame.draw.rect(screen,(32,32,32),[10+p_gauge*2,450,(100-p_gauge)*2,25])
            draw_text(screen,580,20,"SCORE"+str(score),30,WHITHE)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
import math
import os
import random
import sys
import time
from typing import Any
import pygame as pg
from pygame.sprite import AbstractGroup


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
bool_lst = [True,False]

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，こうかとん，ビーム）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


def calc_orientation(org: pg.Rect, dst: pg.Rect) -> tuple[float, float]:
    """
    orgから見て，dstがどこにあるかを計算し，方向ベクトルをタプルで返す
    引数1 org：爆弾SurfaceのRect
    引数2 dst：こうかとんSurfaceのRect
    戻り値：orgから見たdstの方向ベクトルを表すタプル
    """
    x_diff, y_diff = dst.centerx-org.centerx, dst.centery-org.centery
    norm = math.sqrt(x_diff**2+y_diff**2)
    return x_diff/norm, y_diff/norm


class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 0, 2.0)
        img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん
        self.imgs = {
            (+1, 0): img,  # 右
            (+1, -1): pg.transform.rotozoom(img, 45, 1.0),  # 右上
            (0, -1): pg.transform.rotozoom(img, 90, 1.0),  # 上
            (-1, -1): pg.transform.rotozoom(img0, -45, 1.0),  # 左上
            (-1, 0): img0,  # 左
            (-1, +1): pg.transform.rotozoom(img0, 45, 1.0),  # 左下
            (0, +1): pg.transform.rotozoom(img, -90, 1.0),  # 下
            (+1, +1): pg.transform.rotozoom(img, -45, 1.0),  # 右下
        }
        self.dire = (+1, 0)
        self.image = self.imgs[self.dire]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 10
        self.life = 100
        self.max_life = 100
        self.check_act = False
        self.act_life = 0

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 0, 2.0)
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                self.rect.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if check_bound(self.rect) != (True, True):
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rect.move_ip(-self.speed*mv[0], -self.speed*mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        self.act_life -= 1
        if self.act_life < 0:
            self.check_act = False
        screen.blit(self.image, self.rect)
        
    def demo_update(self, key_dict:dict):
        """
        乱数でタイトル画面の透明こうかとんの位置を移動させる
        (敵機が爆弾を落とす位置を同じにしないため)
        
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_dict[k]:
                self.rect.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if check_bound(self.rect) != (True, True):
            for k, mv in __class__.delta.items():
                if key_dict[k]:
                    self.rect.move_ip(-self.speed*mv[0], -self.speed*mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        # screen.blit(self.image, self.rect        


## 2Pこうかとん
class Bird2(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta2 = {  # 押下キーと移動量の辞書
        pg.K_w: (0, -1),
        pg.K_s: (0, +1),
        pg.K_a: (-1, 0),
        pg.K_d: (+1, 0),
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 0, 2.0)
        img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん
        self.imgs = {
            (+1, 0): img,  # 右
            (+1, -1): pg.transform.rotozoom(img, 45, 1.0),  # 右上
            (0, -1): pg.transform.rotozoom(img, 90, 1.0),  # 上
            (-1, -1): pg.transform.rotozoom(img0, -45, 1.0),  # 左上
            (-1, 0): img0,  # 左
            (-1, +1): pg.transform.rotozoom(img0, 45, 1.0),  # 左下
            (0, +1): pg.transform.rotozoom(img, -90, 1.0),  # 下
            (+1, +1): pg.transform.rotozoom(img, -45, 1.0),  # 右下
        }
        self.dire = (+1, 0)
        self.image = self.imgs[self.dire]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 10

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{num}.png"), 0, 2.0)
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta2.items():
            if key_lst[k]:
                self.rect.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if check_bound(self.rect) != (True, True):
            for k, mv in __class__.delta2.items():
                if key_lst[k]:
                    self.rect.move_ip(-self.speed*mv[0], -self.speed*mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        screen.blit(self.image, self.rect)

## ここまで
        
class Bomb(pg.sprite.Sprite):
    """
    爆弾に関するクラス
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    def __init__(self, emy: "Enemy", bird: Bird):
        """
        爆弾円Surfaceを生成する
        引数1 emy：爆弾を投下する敵機
        引数2 bird：攻撃対象のこうかとん
        """
        super().__init__()
        rad = random.randint(10, 50)  # 爆弾円の半径：10以上50以下の乱数
        color = random.choice(__class__.colors)  # 爆弾円の色：クラス変数からランダム選択
        self.image = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        # 爆弾を投下するemyから見た攻撃対象のbirdの方向を計算
        self.vx, self.vy = calc_orientation(emy.rect, bird.rect)  
        self.rect.centerx = emy.rect.centerx
        self.rect.centery = emy.rect.centery+emy.rect.height/2
        self.speed = 6

    def update(self,v):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.speed +=v
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()

## 2pこうかとんbomb
class Bomb2(pg.sprite.Sprite):
    """
    爆弾に関するクラス
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    def __init__(self, emy: "Enemy", bird2: Bird2):
        """
        爆弾円Surfaceを生成する
        引数1 emy：爆弾を投下する敵機
        引数2 bird：攻撃対象のこうかとん
        """
        super().__init__()
        rad = random.randint(10, 50)  # 爆弾円の半径：10以上50以下の乱数
        color = random.choice(__class__.colors)  # 爆弾円の色：クラス変数からランダム選択
        self.image = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        # 爆弾を投下するemyから見た攻撃対象のbirdの方向を計算
        self.vx, self.vy = calc_orientation(emy.rect, bird2.rect)  
        self.rect.centerx = emy.rect.centerx
        self.rect.centery = emy.rect.centery+emy.rect.height/2
        self.speed = 6

    def update(self):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()

## ここまで

class Beam(pg.sprite.Sprite):
    """
    ビームに関するクラス
    """
    def __init__(self, bird: Bird):
        """
        ビーム画像Surfaceを生成する
        引数 bird：ビームを放つこうかとん
        """
        super().__init__()
        self.vx, self.vy = bird.dire
        angle = math.degrees(math.atan2(-self.vy, self.vx))
        self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/beam.png"), angle, 2.0)
        self.vx = math.cos(math.radians(angle))
        self.vy = -math.sin(math.radians(angle))
        self.rect = self.image.get_rect()
        self.rect.centery = bird.rect.centery+bird.rect.height*self.vy
        self.rect.centerx = bird.rect.centerx+bird.rect.width*self.vx
        self.speed = 10

    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()

## 2pこうかとんbeam
class Beam2(pg.sprite.Sprite):
    """
    ビームに関するクラス
    """
    def __init__(self, bird2: Bird2):
        """
        ビーム画像Surfaceを生成する
        引数 bird：ビームを放つこうかとん
        """
        super().__init__()
        self.vx, self.vy = bird2.dire
        angle = math.degrees(math.atan2(-self.vy, self.vx))
        self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/beam.png"), angle, 2.0)
        self.vx = math.cos(math.radians(angle))
        self.vy = -math.sin(math.radians(angle))
        self.rect = self.image.get_rect()
        self.rect.centery = bird2.rect.centery+bird2.rect.height*self.vy
        self.rect.centerx = bird2.rect.centerx+bird2.rect.width*self.vx
        self.speed = 10

    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()

## ここまで

class Explosion(pg.sprite.Sprite):
    """
    爆発に関するクラス
    """
    def __init__(self, obj: "Bomb|Enemy|Boss", life: int):
        """
        爆弾が爆発するエフェクトを生成する
        引数1 obj：爆発するBombまたは敵機またはボスインスタンス
        引数2 life：爆発時間
        """
        super().__init__()
        if obj.__class__.__name__=="Boss":
            late = 3.0
        else:
            late = 1.0
        img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/explosion.gif"), 0, late)
        self.imgs = [img, pg.transform.flip(img, 1, 1)]
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(center=obj.rect.center)
        self.life = life

    def update(self):
        """
        爆発時間を1減算した爆発経過時間_lifeに応じて爆発画像を切り替えることで
        爆発エフェクトを表現する
        """
        self.life -= 1
        self.image = self.imgs[self.life//10%2]
        if self.life < 0:
            self.kill()


class Enemy(pg.sprite.Sprite):
    """
    敵機に関するクラス
    """
    imgs = [pg.image.load(f"{MAIN_DIR}/fig/alien{i}.png") for i in range(1, 4)]
    
    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(0, WIDTH), 0
        self.vy = +6
        self.bound = random.randint(50, HEIGHT/2)  # 停止位置
        self.state = "down"  # 降下状態or停止状態
        self.interval = random.randint(50, 300)  # 爆弾投下インターバル
        
    def update(self):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下したら，_stateを停止状態に変更する
        引数 screen：画面Surface
        """
        if self.rect.centery > self.bound:
            self.vy = 0
            self.state = "stop"
        self.rect.centery += self.vy

    def assemble(self, dst: pg.Rect):
        late = 0.02
        self.vx, self.vy = late*(dst.centerx-self.rect.centerx), late*(dst.centery-self.rect.centery)
        self.rect.move_ip(self.vx, self.vy)
        if abs(self.vx) < 1 and abs(self.vy) < 1:
            self.kill()


class Boss(pg.sprite.Sprite):
    """
    ボスに関するクラス
    """
    def __init__(self):
        """
        ボスを生成する
        """
        super().__init__()
        self.late = 0
        self.life = 1000
        self.check_boot = True
        self.check_act = False
        self.act_life = 0
        self.act_mode = {"domain_expansion":400, "nomal":600}
        self.interval = random.randint(200, 400)
        self.vx, self.vy = random.randint(-6, 6), random.randint(-6, 6)
        self.images = [pg.image.load(f"{MAIN_DIR}/fig/boss.png"), pg.image.load(f"{MAIN_DIR}/fig/hit_boss.png")]
        self.image = self.images[0]
        self.image.set_alpha(self.late)
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(WIDTH//3, WIDTH//3*2), random.randint(HEIGHT//3, HEIGHT//3*2)

    def change_img(self, screen: pg.Surface):
        """
        ボス画像を切り替え，画面に転送する
        引数1 screen：画面Surface
        """  
        self.image = self.images[1]
        screen.blit(self.image, self.rect)

    def update(self, tmr: int, exps: Explosion, score: "Score"):
        """
        ボスをランダムに移動させる
        ボスのHPが0になったら、killする
        引数1 tmr：フレーム数
        引数2 exps：Explosionグループ
        引数3 score：Scoreインスタンス
        """
        if tmr%self.interval==0:
            self.vx, self.vy = 0, 0
            self.rect.move_ip(self.vx, self.vy)
            self.vx, self.vy = random.randint(-6, 6), random.randint(-6, 6)
            self.interval = random.randint(200, 400)
            self.image = self.images[0]
        else:
            self.rect.move_ip(self.vx, self.vy)
        self.act_life -= 1
        if self.act_life < 0:
            self.check_act = False
        if self.late == 250:
            self.check_boot = False
        if self.check_boot:
            self.late += 1
            self.image.set_alpha(self.late)
        if self.life <= 0:
            exps.add(Explosion(self, 150)) # 爆発エフェクト
            score.value += 100 # 100点アップ
            self.kill()
        if check_bound(self.rect) != (True, True):
            self.rect.move_ip(-self.vx, -self.vy)

class Score:
    """
    打ち落とした爆弾，敵機の数をスコアとして表示するクラス
    爆弾：1点
    敵機：10点
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.value = 0
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, HEIGHT-50

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)

class HitPoint:
    """
    キャラクターのHPメーターを表示するクラス
    """
    def __init__(self, unit: Bird|Boss, rct_center: tuple):
        """
        HPメーターSurfaceを生成する
        引数1 unit：キャラクターインスタンス
        引数2 rct_center：HPメーターの中心座標タプル
        """
        self.unit = unit
        self.width = unit.life*5
        self.height = 50
        self.color = (181, 255, 20)
        self.f_name = "bodoniblack"
        self.image = pg.Surface((self.width, self.height))
        self.font1 = pg.font.SysFont(self.f_name, 40)
        self.font2 = pg.font.SysFont(self.f_name, self.height)
        self.text1 = self.font1.render("HP", False, (255, 255, 255))
        self.text2 = self.font2.render(f"{unit.life}/{unit.max_life}", False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.f1_rct = self.text1.get_rect()
        self.f2_rct = self.text2 .get_rect()
        self.rect.centerx, self.rect.centery = rct_center
        self.f1_rct.centerx, self.f1_rct.centery = self.rect.centerx-(self.width/2)-40, self.rect.centery  
        self.f2_rct.centerx, self.f2_rct.centery = self.rect.centerx+(self.width/2)+120, self.rect.centery
        

    def update(self, unit: Bird|Boss, screen: pg.Surface):
        """
        HPメーターをキャラクターのHPに応じて、表示する
        メーターの色は、初期では、緑、半分を下回ると黄色に、1/5を下回ると、赤に変化する
        引数1 unit：キャラクターインスタンス
        引数2 screen：画面Surface
        """
        width = unit.life*5
        if 100 < width < 250:
            self.color = (251, 202, 77)
        elif width <= 100:
            self.color = (255, 0, 0)
        self.image = pg.Surface((self.width, self.height))
        pg.draw.rect(self.image, (125, 125, 125), (0, 0, self.width, self.height))
        pg.draw.rect(self.image, self.color, (0, 0, width, self.height))
        self.text2 = self.font2.render(f"{unit.life}/{unit.max_life}", False, (255, 255, 255))
        screen.blit(self.image, self.rect)
        screen.blit(self.text1, self.f1_rct)
        screen.blit(self.text2, self.f2_rct)
    
class Domain(pg.sprite.Sprite):
    """
    領域に関するクラス
    """
    colors = [(139, 0, 0), (189, 183, 107), (147, 112, 219), (0, 0, 0), (50, 205, 50), (0, 0, 139)]

    def __init__(self, rad, life: int, unit: Bird|Boss):
        """
        領域のSurfaceと対応するCircleを生成する
        引数1 rad：領域の半径
        引数2 life：発動時間
        引数3 unit：こうかとんまたはボスインスタンス
        """
        super().__init__()
        self.unit = unit
        color = random.choice(__class__.colors)  # 領域の色：クラス変数からランダム選択
        self.image = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.image.set_alpha(170)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.life = life

    def update(self):
        """
        self.lifeを1減算し、0未満になったら、killする
        """
        self.rect.center = self.unit.rect.center
        self.life -= 1
        if self.life < 0 or self.unit is None:
            self.kill()

# 追加機能 フォント画像作成
class Generate_font():
    count = 0
    def __init__(self,text:str,fonttype="hgp創英角ﾎﾟｯﾌﾟ体",size=50,color=(0,0,0)):
        self.font = pg.font.SysFont(fonttype,size)
        self.color = color
        self.image = self.font.render(text,0,self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2,HEIGHT/2+__class__.count
        __class__.count += 100
    def update(self,screen:pg.Surface):
        screen.blit(self.image,self.rect)
        
    def crean():
        __class__.count = 0  # class変数初期化関数
    
    # def __call__(self):
    #     0
        

def main():
    pg.display.set_caption("こうかシューティング")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/pg_bg.jpg")
    
    sound = pg.mixer.Sound(f"{MAIN_DIR}/koukaon.mp3")#ビームの発射音
    sounds = pg.mixer.Sound(f"{MAIN_DIR}/Big_Hits.mp3")#敵に当たったときの音
    sound1 = pg.mixer.Sound(f"{MAIN_DIR}/出現.mp3")#敵が出た時
    enamy = pg.mixer.Sound(f"{MAIN_DIR}/ビーム音.mp3")#敵のビーム音
    pg.mixer.music.set_volume(0.5)#bgmの音量
    pg.mixer.music.load(f"{MAIN_DIR}/maou.mp3")#maou.mp3のbgmの読み込み
    # pg.mixer.music.play(1)#反映させる
    score = Score()
    title_font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 100)
    sub_font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体",50)
    subtitle = []
    subtitle.append(Generate_font(f"ひとりでプレイ"))
    subtitle.append(Generate_font(f"ふたりでプレイ"))
    subtitle.append(Generate_font(f"せってい"))
    set_chara = title_font.render(f"せってい",0,(0,0,0))
    emys_hind = sub_font.render(f"てきのしゅつげんひんど",0,(0,0,0))
    emys_hind1 =sub_font.render(f"すくない",0,(0,0,0))
    emys_hind2 =sub_font.render(f"ふつう",0,(0,0,0))
    emys_hind3 =sub_font.render(f"おおい",0,(0,0,0))
    lst = []
    lst.append(emys_hind1)
    lst.append(emys_hind2)
    lst.append(emys_hind3)
    emys_charalst=[]
    emys_charalst.append(lst)
    bombspeed = sub_font.render(f"ばくだんのはやさ",0,(0,0,0))
    bombspeed1 = sub_font.render(f"おそい",0,(0,0,0))    
    bombspeed2 = sub_font.render(f"ふつう",0,(0,0,0))    
    bombspeed3 = sub_font.render(f"はええ",0,(0,0,0))
    lst = []
    lst.append(bombspeed1)
    lst.append(bombspeed2)
    lst.append(bombspeed3)
    emys_charalst.append(lst)
    print(emys_charalst)
    encount = 200  # 初期の敵出現時間感覚
    se1 = pg.mixer.Sound(f"{MAIN_DIR}/bgms/lect.mp3")
    se2 = pg.mixer.Sound(f"{MAIN_DIR}/bgms/check.mp3")
    # titleimg = title_font.render(f"こうかシューティング",0,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    bird = Bird(3, (900, 400))


    demo_bird = Bird(3, (900, 400))
    hps = [HitPoint(bird, (400, 100))]
    demo_bird = Bird(3, (900, 400))

    bird2 = Bird2(103, (500, 400))
    bombs = pg.sprite.Group()
    bombs2 = pg.sprite.Group()
    beams = pg.sprite.Group()
    beams2 = pg.sprite.Group()
    exps = pg.sprite.Group()
    emys = pg.sprite.Group()
    bosses = pg.sprite.Group()
    domains = pg.sprite.Group()
    demo_emys = pg.sprite.Group()  # タイトル画面の後ろで敵機が動く
    demo_bombs = pg.sprite.Group()  # タイトル画面用のボム
    rect_ = 0  # どのモードをいま選択しているか枠で囲むための変数
    Generate_font.crean()
    tmr = 0
    clock = pg.time.Clock()
    game_mode = 0
    democount = 0
    demo_keydict = {}  # 透明なこうかとんSurfaceの移動を決めるための辞書
    setmode = 0
    set_rect = 0
    hind_index = 0
    bomb_index = 0
    hind_dict = {0:200,1:150,2:40}
    bomb_dict = {0:0,1:0.6,2:1.3}
    while True:

        screen.blit(bg_img,[0,0])
        if game_mode == 0:
            if democount%hind_dict[hind_index] == 0 and len(demo_emys) <10:  # 200フレームに1回，敵機を出現させる
                demo_emys.add(Enemy())
            for emy in demo_emys:
                if emy.state == "stop" and democount%emy.interval == 0:
                    # 敵機が停止状態に入ったら，intervalに応じて爆弾投下
                    demo_bombs.add(Bomb(emy, demo_bird))
            
            demo_keydict[pg.K_LEFT] = random.randint(0,1)
            demo_keydict[pg.K_RIGHT] = random.randint(0,1)
            demo_keydict[pg.K_DOWN] = random.randint(0,1)
            demo_keydict[pg.K_UP] = random.randint(0,1)
            demo_bird.demo_update(demo_keydict)
            demo_emys.update()
            demo_emys.draw(screen)
            demo_bombs.update(bomb_dict[bomb_index])
            demo_bombs.draw(screen)
        
            # screen.blit(bg_img, [0, 0])
            
            if setmode:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return 0
                    if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                        se2.play()
                        set_rect = 0
                        setmode = 0
                    if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                        if set_rect <2:
                            set_rect += 1
                            se1.play()
                    if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                        if set_rect >0:
                            set_rect -= 1
                            se1.play()
                    if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                        if set_rect == 1 and hind_index <2:
                            hind_index += 1
                            se1.play()
                        if set_rect == 2 and bomb_index <2:
                            bomb_index += 1
                            se1.play()
                    if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                        if set_rect == 1 and hind_index >0:
                            hind_index -= 1
                            se1.play()
                        if set_rect == 2 and bomb_index >0:
                            bomb_index-=1
                            se1.play()
                        
                screen.blit(set_chara,(WIDTH/2-200,HEIGHT/2-300))
                screen.blit(emys_charalst[0][hind_index],(WIDTH/2-200,HEIGHT/2-100))
                screen.blit(emys_hind,(WIDTH/2-500,HEIGHT/2-170))
                screen.blit(bombspeed,((WIDTH/2-500,HEIGHT/2+130)))
                screen.blit(emys_charalst[1][bomb_index],(WIDTH/2-200,HEIGHT/2+200))
                if set_rect == 1:
                    pg.draw.line(screen,(0,0,0),(WIDTH/2-500,HEIGHT/2-120),(WIDTH/2+50,HEIGHT/2-120),5)
                elif set_rect ==2:
                    pg.draw.line(screen,(0,0,0),(WIDTH/2-500,HEIGHT/2+180),(WIDTH/2-100,HEIGHT/2+180),5)
                
                
                
            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return 0
                    if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                        if rect_ == 0:
                            continue
                        else:
                            rect_ -= 1
                            se1.play()
                    if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                        if rect_ ==3:
                            continue
                        else:
                            rect_ += 1
                            se1.play() 
                    if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                        se2.play()
                        if rect_ == 1:
                            game_mode = 1
                            rect_ = 0  # 決定を押されたら初期に戻す
                            demo_emys = pg.sprite.Group()  # 初期化
                            demo_bombs = pg.sprite.Group()  # 初期化
                        if rect_ == 2:
                            game_mode = 2
                            rect_ = 0  # 決定を押されたら初期に戻す
                            demo_emys = pg.sprite.Group()  # 初期化
                            demo_bombs = pg.sprite.Group()  # 初期化
                        if rect_ == 3:
                            setmode = 1# 設定モードを有効f
                titleimg = title_font.render(f"こうかシューティング",0,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                screen.blit(titleimg,(WIDTH/2-500,HEIGHT/2-200))
                if  rect_ != 0:
                    pg.draw.rect(screen,(255,0,0),(WIDTH/2-180,HEIGHT/2-125+rect_*100,350,60),5)
                for title in subtitle:
                    title.update(screen)
            
                
            # pg.draw.rect(screen,(255,255,255),(0,0,WIDTH,HEIGHT))
            # if democount%hind_dict[hind_index] == 0 and len(demo_emys) <10:  # 200フレームに1回，敵機を出現させる
            #     demo_emys.add(Enemy())
            # for emy in demo_emys:
            #     if emy.state == "stop" and democount%emy.interval == 0:
            #         # 敵機が停止状態に入ったら，intervalに応じて爆弾投下
            #         demo_bombs.add(Bomb(emy, demo_bird))
            
            # demo_keydict[pg.K_LEFT] = random.randint(0,1)
            # demo_keydict[pg.K_RIGHT] = random.randint(0,1)
            # demo_keydict[pg.K_DOWN] = random.randint(0,1)
            # demo_keydict[pg.K_UP] = random.randint(0,1)
            # demo_bird.demo_update(demo_keydict)
            # demo_emys.update()
            # demo_emys.draw(screen)
            # demo_bombs.update(bomb_dict[bomb_index])
            # demo_bombs.draw(screen)
            
            
            pg.display.update()
            democount+=1
        elif game_mode == 1:
            
            key_lst = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 0
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    if len(beams) <=2:
                        
                        beams.add(Beam(bird))
                        sound.play()

                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and score.value > 50 and not bird.check_act:
                    score.value -= 50  # 50点ダウン
                    bird.check_act = True
                    bird.act_life = 400
                    domains.add(Domain(100, bird.act_life, bird)) # 簡易領域
                    
            # screen.blit(bg_img, [0, 0])


            if tmr%hind_dict[hind_index] == 0:  # 200フレームに1回，敵機を出現させる
                emys.add(Enemy())

            


            # if tmr%Enemy.tf == 0 and len(bosses)==0:  # 200フレームに1回かつ，ボスがいない時に敵機を出現させる
            #     emys.add(Enemy())
            #     Enemy.tf += 50

            # ゲーム開始から30秒が経過かつ，敵機が5体以上いるかつ，ボスがいない時にボスを出現させる
            if pg.time.get_ticks()>30*10**3 and len(emys)>=5 and len(bosses)==0:
                bosses.add(Boss())

            for emy in emys:
                if emy.state == "stop" and tmr%emy.interval == 0:
                    # 敵機が停止状態に入ったら，intervalに応じて爆弾投下
                    bombs.add(Bomb(emy, bird))

                for boss in bosses:
                    if boss.check_boot:
                        emy.assemble(boss.rect)
                
            for boss in bosses:
                if not boss.check_act:
                    boss.check_act = True
                    act_mode = random.choice(list(boss.act_mode.keys()))
                    boss.act_life = boss.act_mode[act_mode]
                    if act_mode == "domain_expansion": # 領域展開
                        domains.add(Domain(250, boss.act_life, boss))

            for boss in bosses:
                if tmr%((emy.interval)*0.2) == 0 and act_mode == "nomal":
                    bombs.add(Bomb(boss, bird))

                    enamy.play()


            for emy in pg.sprite.groupcollide(emys, beams, True, True).keys():
                exps.add(Explosion(emy, 100))  # 爆発エフェクト
                sounds.play()#soundsで出る効果音の出力
                score.value += 10  # 10点アップ
                bird.change_img(6, screen)  # こうかとん喜びエフェクト

            for bomb in pg.sprite.groupcollide(bombs, beams, True, True).keys():
                exps.add(Explosion(bomb, 50))  # 爆発エフェクト
                sounds.set_volume(1)#soundsの音量
                sounds.play()#soundsで出る効果音の出力
                score.value += 1  # 1点アップ

            for boss in pg.sprite.groupcollide(bosses, beams, False, True).keys():
                boss.life -= 50 # ボスのHPを50ダウン
                boss.change_img(screen)
                bird.change_img(6, screen)  # こうかとん喜びエフェクト

            for domain in pg.sprite.spritecollide(bird, domains, False):
                if domain.unit.__class__.__name__=="Boss" and not bird.check_act:
                    bird.life -= 1 # こうかとんのHPを1ダウン
                    bird.change_img(8, screen) # こうかとん悲しみエフェクト



            if len(pg.sprite.spritecollide(bird, bombs, True)) != 0:
                bird.change_img(8, screen) # こうかとん悲しみエフェクト
                bird.life -= 10
                score.update(screen)
                #pg.display.update()

            if bird.life <= 0:  #こうかとんのHPが0を下回ったらゲームオーバー 
                time.sleep(2)
                # ゲームオーバーになったら全部初期化
                tmr = 0
                bird = Bird(3, (900, 400))
                bombs = pg.sprite.Group()
                beams = pg.sprite.Group()
                exps = pg.sprite.Group()
                emys = pg.sprite.Group()
                domains = pg.sprite.Group()
                bosses = pg.sprite.Group()
                score = Score()
                bird.life = bird.max_life
                hps = [HitPoint(bird, (400, 100))]
                game_mode = 0  # ゲームオーバーでタイトルメニューに戻る

            bird.update(key_lst, screen)
            beams.update()
            beams.draw(screen)
            emys.update()
            emys.draw(screen)
            bosses.update(tmr, exps, score)
            bosses.draw(screen)
            bombs.update(bomb_dict[bomb_index])
            bombs.draw(screen)
            exps.update()
            exps.draw(screen)
            for hp in hps:
                hp.update(hp.unit, screen)
            domains.update()
            domains.draw(screen)
            score.update(screen)
            pg.display.update()

            tmr += 1

        if game_mode==2:
            key_lst = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 0
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    if len(beams) <=3:
                        beams.add(Beam(bird))
                        sound.play()
                if event.type == pg.KEYDOWN and event.key == pg.K_f:
                    if len(beams2) <=3:
                        beams2.add(Beam(bird2))
                        sound.play()

            screen.blit(bg_img, [0, 0])

            if tmr%hind_dict[hind_index] == 0:  # 200フレームに1回，敵機を出現させる
                emys.add(Enemy())

            for emy in emys:
                if emy.state == "stop" and tmr%emy.interval == 0:
                    # 敵機が停止状態に入ったら，intervalに応じて爆弾投下
                    bombs.add(Bomb(emy, bird))
                    bombs.add(Bomb(emy, bird2))

            for emy in pg.sprite.groupcollide(emys, beams, True, True).keys():
                exps.add(Explosion(emy, 100))  # 爆発エフェクト
                score.value += 10  # 10点アップ
                bird.change_img(6, screen)  # こうかとん喜びエフェクト

            for bomb in pg.sprite.groupcollide(bombs, beams, True, True).keys():
                exps.add(Explosion(bomb, 50))  # 爆発エフェクト
                score.value += 1  # 1点アップ

            if len(pg.sprite.spritecollide(bird, bombs, True)) != 0:
                bird.change_img(8, screen) # こうかとん悲しみエフェクト
                score.update(screen)
                pg.display.update()
                time.sleep(2)
        
                game_mode = 0
                bird = Bird(3, (900, 400))

                bird2 = Bird2(103, (500, 400))

                bombs = pg.sprite.Group()
                bombs2 = pg.sprite.Group()
                beams = pg.sprite.Group()
                beams2 = pg.sprite.Group()
                exps = pg.sprite.Group()
                emys = pg.sprite.Group()

    #bird2
            for emy in pg.sprite.groupcollide(emys, beams2, True, True).keys():
                exps.add(Explosion(emy, 100))  # 爆発エフェクト
                score.value += 10  # 10点アップ
                bird2.change_img(106, screen)  # こうかとん喜びエフェクト

            for bomb in pg.sprite.groupcollide(bombs, beams2, True, True).keys():
                exps.add(Explosion(bomb, 50))  # 爆発エフェクト
                score.value += 1  # 1点アップ

            if len(pg.sprite.spritecollide(bird2, bombs, True)) != 0:
                bird2.change_img(108, screen) # こうかとん悲しみエフェクト
                score.update(screen)
                pg.display.update()
                time.sleep(2)
                game_mode = 0
                bird = Bird(3, (900, 400))
                score = Score()

                bird2 = Bird2(103, (500, 400))

                bombs = pg.sprite.Group()
                bombs2 = pg.sprite.Group()
                beams = pg.sprite.Group()
                beams2 = pg.sprite.Group()
                exps = pg.sprite.Group()
                emys = pg.sprite.Group()

            bird.update(key_lst, screen)
            bird2.update(key_lst,screen)
            beams.update()
            beams.draw(screen)
            beams2.update()
            beams2.draw(screen)
            emys.update()
            emys.draw(screen)
            bombs.update(bomb_dict[bomb_index])
            bombs.draw(screen)
            bombs2.update()
            bombs2.draw(screen)
            exps.update()
            exps.draw(screen)
            score.update(screen)
            pg.display.update()
            tmr += 1


        clock.tick(50)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
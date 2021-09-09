import tkinter as tk
from tkinter import font
import random
from tkinter.constants import FALSE
from PIL import Image, ImageTk

WINDOW_HEIGHT = 600  # ウィンドウの高さ
WINDOW_WIDTH = 600   # ウィンドウの幅

CANNON_Y = 550       # 自機のy座標

ENEMY_SPACE_X = 100  # 敵の間隔(x座標)
ENEMY_SPACE_Y = 60   # 敵の間隔(y座標)
BOSS_X = WINDOW_WIDTH / 2
ENEMY_MOVE_SPACE_X = 20  # 敵の移動間隔(x座標)
BOSS_MOVE_SPACE_X = 10
ENEMY_MOVE_SPEED = 2000  # 敵の移動スピード(2000 ms)
BOSS_MOVE_SPEED = 1000   #ボスの移動スピード
NUMBER_OF_ENEMY = 18     # 敵の数
ENEMY_SHOOT_INTERVAL = 200  # 敵がランダムに弾を打ってくる間隔
BOSS_SHOOT_INTERVAL = 200   #ボスのランダム発射の間隔

COLLISION_DETECTION = 300  # 当たり判定

BULLET_HEIGHT = 5  # 弾の縦幅
BULLET_WIDTH = 2    # 弾の横幅
BULLET_SPEED = 5   # 弾のスピード(10 ms)

TEXT_GOOD_SIZE = 10             # goodのサイズ
TEXT_CONGRATULATIONS_SIZE = 50  # congratularionsのサイズ
TEXT_GAMECLEAR_SIZE = 60        # gameclearのサイズ
TEXT_GAMEOVER_SIZE = 90         # gameoverのサイズ

GAMES = []   #ゲーム数




class Cannon:  # 自機

    def __init__(self, x, y=CANNON_Y):
        self.x = x
        self.y = y
        self.draw()
        self.bind()

    def draw(self):   #自機の描画
        self.id = cv.create_image(
            self.x, self.y, image=cannon_tkimg, tag="cannon")  #"cannon"というタグ（名前みたいなもん）を付けて描画
        PLAY_GAMES = GAMES[-1]
        now=PLAY_GAMES[0]
        # now(0)
        now.show_scores()

    def bind(self):   #ボタン操作の割り当て
        cv.tag_bind(self.id, "<ButtonPress-3>", self.pressed)
        cv.tag_bind(self.id, "<Button1-Motion>", self.dragged)

    def pressed(self, event):   #クリックされたとき
        mybullet = MyBullet(event.x, self.y)
        mybullet.draw()   #弾丸の描画
        mybullet.shoot()   

    def dragged(self, event):   #ドラッグ時の挙動
        dx = event.x - self.x   #x方向の移動距離の設定
        self.x, self.y = cv.coords(self.id)
        cv.coords(self.id, self.x+dx, self.y)
        self.x = event.x

    def destroy(self):  #自機の消滅
        cv.delete(self.id)

class MyBullet:  # 自分の弾

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):   #弾丸の描画
        self.id = cv.create_rectangle(#　←rectangre(a, b, c, d)...a、b、c、dを頂点とする多角形の描画
            self.x-BULLET_WIDTH, self.y+BULLET_HEIGHT, self.x+BULLET_WIDTH, self.y-BULLET_HEIGHT, fill="cyan", tag = "my_bullet")   #シアン
        
    def shoot(self):   #弾丸発射
        if self.y >= 0:   #自機座標が0(下端)より大きければ発射
            cv.move(self.id, 0, -BULLET_HEIGHT)
            self.y -= BULLET_HEIGHT   #弾丸の描画座標を毎フレーム弾丸一個分上に更新
            self.defeat()
            root.after(BULLET_SPEED, self.shoot)
            
    def defeat(self):   #敵を倒したときの処理
        for enemy in enemies:
            if ((self.x-enemy.x)**2+(self.y-enemy.y)**2) < COLLISION_DETECTION and enemy.exist == True:   #弾丸が敵機に触れたら
                enemy.exist = False   #敵死亡
                enemy.destroy()   #敵消滅
                cv.create_text(enemy.x, enemy.y, text="good!", fill="cyan", font=(
                        "System", TEXT_GOOD_SIZE), tag="good")   #シアン色でgood!って表示
        if ((self.x-boss.x)**2+(self.y-boss.y)**2) < COLLISION_DETECTION and boss.exist == True:
            boss.exist = False
            boss.destroy()
            cv.create_text(boss.x,boss.y, text='excellent!!',fill='yellow',font=(
                'System',TEXT_GOOD_SIZE),tag='excellent')
            
    def destroy(self):   #弾丸消滅の関数
        cv.delete(self.id)
        
class Enemy:  # 敵

    def __init__(self, x, y):
        self.x = x % WINDOW_WIDTH # 
        self.y = y+x//WINDOW_WIDTH*ENEMY_SPACE_Y #y以上ならENEMY_SPACE_Yの間隔で敵が発生しない。
        self.exist = True # ゲーム開始処理
        self.draw()
        self.move()

    def draw(self):   #描画
        self.id = cv.create_image(
            self.x, self.y, image=crab_tkimg, tag="enemy")

    def enemy_shoot(self):
        # 敵が球を発射したときの処理
        if self.exist:
            enemybullet = EnemyBullet(self.x, self.y)
            enemybullet.draw()
            enemybullet.shoot()

    def move(self):  #敵の動き
        if self.exist:
            if self.x < 0:
                self.x = WINDOW_WIDTH
            if self.x > WINDOW_WIDTH:
                self.x = 0
            else:
                if 150 < self.y < 180:   #二段目は
                    self.x += ENEMY_MOVE_SPACE_X
                else:   #それ以外は
                    self.x -= ENEMY_MOVE_SPACE_X
            cv.coords(self.id, self.x, self.y)
            root.after(ENEMY_MOVE_SPEED, self.move)

    def destroy(self):   #敵機破壊
        cv.delete(self.id)
        PLAY_GAMES = GAMES[-1]
        brake_enemies=PLAY_GAMES[1].ADD_SET(self.id)
        PLAY_GAMES[0].set_scores(len(brake_enemies))
        PLAY_GAMES[0].show_scores()
        cv.delete("good","excellent")

class enemy_list:
    #敵のリスト（SETだけど！！）
    def __init__(self):
        self.DEL_ENEMY = set()

    def ADD_SET(self,id):
        self.id = id
        self.DEL_ENEMY.add(self.id)
        return self.DEL_ENEMY

    def print_SET(self):
        return self.DEL_ENEMY

class EnemyBullet:  # 敵の弾

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):   #描画
        self.id = cv.create_rectangle(
            self.x-BULLET_WIDTH, self.y+BULLET_HEIGHT, self.x+BULLET_WIDTH, self.y-BULLET_HEIGHT, fill="red", tag = "enemy_bullet")

    def shoot(self):   #弾丸発射
        if self.y <= WINDOW_HEIGHT:
            cv.move(self.id, 0, BULLET_HEIGHT)
            self.y += BULLET_HEIGHT
            self.collision()
            root.after(BULLET_SPEED, self.shoot)

    def collision(self):   #当たり判定
        if ((self.x-cannon.x)**2+(self.y-cannon.y)**2) < COLLISION_DETECTION:
            gameover()

    def destroy(self):   #描画抹消
        cv.delete(self.id)

###ボス戦
class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = 0 # 
        self.y = 50
        self.exist = True # ゲーム開始処理

    def draw(self):
        self.id = cv.create_image(
            self.x, self.y, image=bos_tkimg, tag="bos")
            
    def move(self):   #ボスの動き
        if self.exist:
            if self.x < 0:
                self.x = WINDOW_WIDTH
            else:
                self.x -= BOSS_MOVE_SPACE_X
            cv.coords(self.id, self.x, self.y)
            root.after(BOSS_MOVE_SPEED, self.move)
        BOSS_X = self.x

    def destroy(self):
        cv.delete('bos')
        PLAY_GAMES = GAMES[-1]
        PLAY_GAMES[0].boss()
        PLAY_GAMES[0].show_scores()
        cv.delete("good","excellent")
    
class scoreboards:
    """
    自分のスコアを計算し表示する
    """

    def __init__(self, num):
        """
        変数定義
        """
        self.num = num ## 変数が返る
        self.my_scores = 0
        # self.sum_scores(num)
        # self.show_scores()

    def boss(self):
        """
        ボス用script
        """
        self.my_scores+=3
        self.show_scores()

    def set_scores(self,num):
        #残りの敵数に応じてスコアを求める
        self.num = num
        self.my_scores = num
        self.show_scores()

    def show_scores(self):
        """
         スコアの合計値を画面右上に出力
        """
        cv.delete("score")
        fontsize= 100//2
        cv.create_text(WINDOW_WIDTH-(fontsize+20), WINDOW_HEIGHT-(fontsize//2*3), text='SCORE', fill="white", font=("Helvetica", 25), tag="score") 
        cv.create_text(WINDOW_WIDTH-(fontsize//2+10), WINDOW_HEIGHT-fontsize//2, text=self.my_scores, fill="white", font=("Helvetica", fontsize), tag="score")   #得点表示

def gameclear():  # ゲームクリア判定
    winflag = 0
    for enemy in enemies:
        if enemy.exist == False and boss.exist == False:
            winflag += 1
    if winflag == NUMBER_OF_ENEMY:
        cv.delete("good")  #good消す
        cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2-80, text="Congratulations!",   #褒める
                       fill="yellow", font=("System", TEXT_CONGRATULATIONS_SIZE), tag = "CREA")
        cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2+20, text="GAME CLEAR!",   #褒める
                       fill="yellow", font=("System", TEXT_GAMECLEAR_SIZE), tag = "CREA") 
    root.after(1000, gameclear)

def gameover():  # ゲームオーバー判定
    cv.delete("cannon", "good")
    cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, text="GAME OVER",
                   fill="red", font=("System", TEXT_GAMEOVER_SIZE), tag = "GAMEOVER")

def enemy_randomshoot():  # ランダムに敵の弾が発射
    enemy = random.choice(enemies)
    enemy.enemy_shoot()
    root.after(ENEMY_SHOOT_INTERVAL, enemy_randomshoot)

def boss_randomshoot():  # ボスの弾が発射
    boss.enemy_shoot()
    root.after(BOSS_SHOOT_INTERVAL, boss_randomshoot)

def restart(*args):   #リスタート関数
    start_game()

def start_game():

    global cannon,enemies,boss

    cv.delete("GAMEOVER", "CREA")#GAMEOVERの文字を消す
    cv.delete("cannon", "good", "enemy", "enemy_bullet", "my_bullet","excellent",'bos')   #前のゲームの情報を消す
    s,e = scoreboards(0),enemy_list()#スコア定義
    GAMES.append((s,e))# ゲーム別得点　# これは暫定　リセットする時にリストに追加してそれにスコアボードを割り当てるイメージ
    # インスタンス生成
    cannon = Cannon(WINDOW_WIDTH//2, CANNON_Y)  #自機の描画
    enemies = []
    for i in range(NUMBER_OF_ENEMY):
        enemy_i = Enemy(i*ENEMY_SPACE_X+50, ENEMY_SPACE_Y + 50)  ################
        enemies.append(enemy_i)   #敵機の生成
    boss = Boss(0,(ENEMY_SPACE_Y-10))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("invader")
    back_img = Image.open("./data/bg.jpeg")
    back_img = back_img.resize((WINDOW_WIDTH,WINDOW_HEIGHT))
    back_tkimg = ImageTk.PhotoImage(back_img)
    cv = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='black')  #背景
    cv.create_image(0, 0, image=back_tkimg, anchor=tk.NW)
    cv.pack()

    # 画像の読み込み
    cannon_img = Image.open("./data/cannon.jpeg")  #自機
    cannon_img = cannon_img.resize((50,50))
    cannon_tkimg = ImageTk.PhotoImage(cannon_img)
    
    crab_img = Image.open("./data/enemy.png")  #敵機
    crab_img = crab_img.resize((30,25))
    crab_tkimg = ImageTk.PhotoImage(crab_img)

    bos_img = Image.open('./data/bos.png')   #ボス
    bos_img = bos_img.resize((30,25))
    bos_tkimg = ImageTk.PhotoImage(bos_img)

    # メニューバー
    menubar = tk.Menu(root)
    root.configure(menu=menubar)
    menubar.add_command(label="QUIT", underline=0, command=root.quit)

    start_game()

    enemy_randomshoot()   #敵機発砲
    boss_randomshoot()

    gameclear()   #クリア判定

    root.bind("<Return>", restart)   #ENTER押したらリスタート

    root.mainloop()
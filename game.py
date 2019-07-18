import cocos
from cocos.sprite import Sprite
from pyaudio import PyAudio, paInt16
import struct
from role import Role
from floor import Floor
from stone import Stone
from cocos.actions import *
import time
import pyglet


class GameStart(cocos.layer.Layer):
    def __init__(self):
        super(GameStart, self).__init__()
        background = cocos.sprite.Sprite('scene/start.png')
        background.scale = 0.5
        background.image_anchor = 0, 0
        self.add(background)
        self.game = None
        menu = cocos.menu.Menu()
        hard = cocos.menu.ImageMenuItem("scene/button_hard.png", self.hard)
        normal = cocos.menu.ImageMenuItem('scene/button_normal.png', self.normal)
        easy = cocos.menu.ImageMenuItem('scene/1.png', self.easy)
        exit = cocos.menu.ImageMenuItem("scene/button_exit.png", self.exit)
        menu.create_menu([hard, normal, easy, exit])
        menu.position = 300, 10
        menu.scale = 1.2
        # menu的位置需要调整
        self.add(menu)

    def hard(self):
        cocos.director.director.push(cocos.scene.Scene(HowlGame("HARD")))

    def normal(self):
        cocos.director.director.push(cocos.scene.Scene(HowlGame("NORMAL")))

    def easy(self):
        cocos.director.director.push(cocos.scene.Scene(HowlGame("EASY")))

    def exit(self):
        cocos.director.director.pop()


# 游戏结束层（有点丑）
class GameOver(cocos.layer.Layer):
    def __init__(self, game):
        super(GameOver, self).__init__()
        self.game = game
        if self.game.role.dead:
            self.background = cocos.sprite.Sprite('scene/end.png')
            self.background.scale = 0.5
        else:
            self.background = cocos.sprite.Sprite('scene/win.png')
        # menu.font_title['font_name'] = FONTS
        # menu.font_item['font_name'] = FONTS
        # menu.font_item_selected['font_name'] = FONTS
        self.background.image_anchor = 0, 0
        self.add(self.background)
        menu = cocos.menu.Menu()
        start = cocos.menu.ImageMenuItem("scene/button_yes.png", self.replay)
        exit = cocos.menu.ImageMenuItem("scene/button_no.png", self.quit_game)
        menu.create_menu([start, exit])
        menu.y = -200
        self.add(menu)

    def replay(self):
        self.game.reset()

    def quit_game(self):
        cocos.director.director.pop()


class HowlGame(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self, level):
        super(HowlGame, self).__init__(255, 255, 255, 255, 4000, 2000)

        # init voice
        self.NUM_SAMPLES = 1000  # pyAudio内部缓存块大小
        self.LEVEL = 1500  # 声音保存的阈值
        self.sample_count = 0  # 取样次数
        self.average_volume = 0  # 平均音量

        # init floor
        self.floor = Floor(self, level)
        self.add(self.floor, 0)

        # init voiceBar
        self.voiceBar = Sprite('ground/black.png', color=(0, 0, 255))
        # self.voiceBar.position = 100, 460
        self.voiceBar.scale_y = 0.1
        self.voiceBar.image_anchor = 0, 0
        self.add(self.voiceBar, 1)

        # init role
        self.role = Role(self)
        self.role_run_to_right = False
        self.role_run_to_left = False
        self.add(self.role, 2)
        self.action = FadeOut(0.5)

        # init monster
        # self.monster_node = cocos.cocosnode.CocosNode()
        # for i in range(5):
        #     self.monster_node.add(Monster(self))
        # self.add(self.monster_node)

        # init flag
        # flag = cocos.sprite.Sprite('scene/flag.png')
        # flag.position = 3500, 120
        # flag.scale = 0.5
        # self.flag = flag
        # self.add(flag)

        # init stone
        self.stone = None
        self.boom = cocos.sprite.Sprite('scene/boom.png')

        # init gameoverlayer
        self.gameover = None

        # Open Audio Input
        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=self.NUM_SAMPLES)

        self.schedule(self.update)

    # role collide on floorNode
    def role_collide(self):
        # role在floor中的x坐标
        fx = self.role.x - self.floor.x
        fy = self.role.y
        width = self.role.width
        height = self.role.height
        count = 0
        for b in self.floor.map.get_children():
            # 左下
            if b.x < fx + width * 0.1 < b.x + b.width and b.y < fy < b.y + b.height:
                if (b.x + b.width - fx) < (b.y + b.height - fy):
                    self.role.x = b.x + b.width + self.floor.x - width * 0.1
                else:
                    self.role.land(b.y + b.height)
                count += 1
                continue
            # 右下
            if b.x < fx + width * 0.9 < b.x + b.width and b.y < fy < b.y + b.height:
                if (fx + width * 0.9 - b.x) < b.y + b.height - fy:
                    self.role.x = b.x + self.floor.x - width * 0.9
                else:
                    self.role.land(b.y + b.height)
                count += 1
                continue
            # 右上
            if b.x < fx + width * 0.9 < b.x + b.width and b.y < fy + height * 0.9 < b.y + b.height:
                if (fx + width * 0.9 - b.x) < fy + height - b.y:
                    self.role.x = b.x + self.floor.x - width * 0.9
                else:
                    self.role.y = b.y - height * 0.9
                    self.role.speed = 0
                count += 1
                continue
            # 左上
            if b.x < fx + width * 0.1 < b.x + b.width and b.y < fy + height * 0.9 < b.y + b.height:
                if (b.x + b.width - fx) < fy + height - b.y:
                    self.role.x = b.x + b.width + self.floor.x - width * 0.1
                else:
                    self.role.y = b.y - height * 0.9
                    self.role.speed = 0
                count += 1
                continue
            if count >= 3:
                break

    # stone collide on something
    def stone_collide(self):
        if self.role.can_shot:
            return
        px = self.stone.x - self.floor.x
        py = self.stone.y
        width = self.stone.width
        height = self.stone.height
        count = 0
        if px < 0:
            self.role.can_shot = True
            self.remove(self.stone)
            return
        if py < -100:
            self.role.can_shot = True
            self.remove(self.stone)
        for b in self.floor.map.get_children():
            # 左下
            if b.x < px + width * 0.2 < b.x + b.width and b.y < py < b.y + b.height:
                self.role.can_shot = True

                # boom effect
                self.boom.position = px, py
                self.add(self.boom)
                self.boom.do(self.action)
                self.remove(self.stone)
                count += 1
                break
            # 右下
            if b.x < px + width * 0.8 < b.x + b.width and b.y < py < b.y + b.height:
                self.role.can_shot = True

                # boom effect
                self.boom.position = px, py
                self.add(self.boom)
                self.boom.do(self.action)
                self.remove(self.stone)
                count += 1
                break
            # 右上
            if b.x < px + width * 0.8 < b.x + b.width and b.y < py + height < b.y + b.height:
                self.role.can_shot = True

                # boom effect
                self.boom.position = px, py
                self.add(self.boom)
                self.boom.do(self.action)
                self.remove(self.stone)
                count += 1
                break
            # 左上
            if b.x < px + width * 0.2 < b.x + b.width and b.y < py + height < b.y + b.height:
                self.role.can_shot = True

                # boom effect
                self.boom.position = px, py
                self.add(self.boom)
                self.boom.do(self.action)
                self.remove(self.stone)
                count += 1
                break
            # if count >= 3:
            #    break

    # role on monster
    def monster_collide_on_role(self):
        # role在floor中的x坐标
        fx = self.role.x - self.floor.x
        fy = self.role.y
        width = self.role.width
        height = self.role.height
        for b in self.floor.monster_node.get_children():
            # role
            # 左下
            if b.x < fx + width * 0.2 < b.x + b.width and b.y < fy + height * 0.2 < b.y + b.height:
                self.role.die()
                break
            # 右下
            if b.x < fx + width * 0.8 < b.x + b.width and b.y < fy + height * 0.2 < b.y + b.height:
                self.role.die()
                break
            # 右上
            if b.x < fx + width * 0.8 < b.x + b.width and b.y < fy + height * 0.8 < b.y + b.height:
                self.role.die()
                break
            # 左上
            if b.x < fx + width * 0.2 < b.x + b.width and b.y < fy + height * 0.8 < b.y + b.height:
                self.role.die()
                break

    # stone on monster
    def monster_collide_on_stone(self):
        if self.role.can_shot:
            return
        # stone在floor中的x坐标
        px = self.stone.x - self.floor.x
        py = self.stone.y
        s_width = self.stone.width
        s_height = self.stone.height
        for b in self.floor.monster_node.get_children():
            # 左下
            if b.x < px + s_width * 0.1 < b.x + b.width and b.y < py < b.y + b.height:
                self.role.can_shot = True

                # boom effect
                self.boom.position = px, py
                self.add(self.boom)
                self.boom.do(self.action)

                self.remove(self.stone)
                self.floor.monster_node.remove(b)
                break
            # 右下
            if b.x < px + s_width * 0.9 < b.x + b.width and b.y < py < b.y + b.height:
                self.role.can_shot = True

                # boom effect
                self.boom.position = px, py
                self.add(self.boom)
                self.boom.do(self.action)

                self.remove(self.stone)
                self.floor.monster_node.remove(b)
                break
            # 右上
            if b.x < px + s_width * 0.9 < b.x + b.width and b.y < py + s_height < b.y + b.height:
                self.role.can_shot = True

                # boom effect
                self.boom.position = px, py
                self.add(self.boom)
                self.boom.do(self.action)

                self.remove(self.stone)
                self.floor.monster_node.remove(b)
                break
            # 左上
            if b.x < px + s_width * 0.1 < b.x + b.width and b.y < py + s_height < b.y + b.height:
                self.role.can_shot = True

                # boom effect
                self.boom.position = px, py
                self.add(self.boom)
                self.boom.do(self.action)

                self.remove(self.stone)
                self.floor.monster_node.remove(b)
                break

    def update(self, dt):
        # 读入NUM_SAMPLES个取样
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max(struct.unpack('1000h', string_audio_data))
        # 平均音量
        if self.sample_count < 50:
            self.average_volume = (self.average_volume * self.sample_count + k) / (self.sample_count + 1)
            self.sample_count += 1
        else:
            self.sample_count = 0
            self.average_volume = 0
            self.average_volume = (self.average_volume * self.sample_count + k) / (self.sample_count + 1)
            self.sample_count += 1

        # print voice
        self.voiceBar.scale_x = self.average_volume / 10000.0
        if self.role_run_to_right:
            self.role.x += 4
            # self.floor.x -= 5
        if self.role_run_to_left:
            self.role.x -= 4
            # self.floor.x += 5
        if self.role.can_shot:
            if self.sample_count == 50 and self.average_volume > 4000:
                pos = self.role.x + self.role.width * 0.8, self.role.y + self.role.height * 0.6
                stone = Stone((self.average_volume - 3000) / 1000.0 + 1, pos, self.role.direction)
                self.stone = stone
                self.add(stone)
                self.role.can_shot = False
        # if k > 3000:
            # self.floor.x -= min((k / 20.0), 150) * dt
        #  k > 8000:
            # self.role.jump((k - 8000) / 1000.0)

        # destination
        if (self.role.x + self.role.width / 2) >= self.floor.flag.x:
            time.sleep(0.5)
            self.end_game()
            self.role.pause_scheduler()
            return

        # spider trigger
        if self.role.x > self.floor.spider.x - 50:
            self.floor.spider.passed = True
        # collision
        self.role_collide()
        self.monster_collide_on_role()
        if not self.role.can_shot:
            self.stone_collide()
            self.monster_collide_on_stone()

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.RIGHT:
            self.role_run_to_right = True
            self.role.image_change("RIGHT", "RUN")
        if key == pyglet.window.key.LEFT:
            self.role_run_to_left = True
            self.role.image_change("LEFT", "RUN")
        if key == pyglet.window.key.UP:
            self.role.jump(8.5)
        if key == pyglet.window.key.B:
            cocos.director.director.pop()
        if key == pyglet.window.key.V:
            if self.role.can_shot:
                pos = self.role.x + self.role.width * 0.8, self.role.y + self.role.height * 0.6
                stone = Stone(1, pos, self.role.direction)
                self.stone = stone
                self.add(stone)
                self.role.can_shot = False

    def on_key_release(self, key, modifiers):
        if key == pyglet.window.key.RIGHT:
            self.role_run_to_right = False
            if self.role.direction == "RIGHT":
                self.role.image_change("RIGHT", "STAND")
        if key == pyglet.window.key.LEFT:
            self.role_run_to_left = False
            if self.role.direction == "LEFT":
                self.role.image_change("LEFT", "STAND")

    def reset(self):
        self.x = 0
        # self.floor.x = 0
        # 可进行地图重新生成
        self.role.reset()
        self.floor.reset()

        if self.gameover:
            self.remove(self.gameover)
            self.gameover = None

        self.role_run_to_right = False
        self.role_run_to_left = False
        self.resume_scheduler()

    def end_game(self):
        self.gameover = GameOver(self)
        #self.gameover.background.x = -self.x
        #self.gameover.background.y = -self.y
        self.gameover.x = -self.x
        self.gameover.y = -self.y
        self.add(self.gameover, 10000)
        self.pause_scheduler()

    def shake(self):
        pos = self.position
        pass


cocos.director.director.init(width=960, height=510, caption="Rage Out Loud")
cocos.director.director.run(cocos.scene.Scene(GameStart()))




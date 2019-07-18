import random
import cocos
from pyglet import image


class Monster(cocos.sprite.Sprite):
    def __init__(self, game, speed):

        # 怪物随机初始化
        monster_no = random.randint(1, 4)
        monster_left = 'enemy/' + str(monster_no) + '.png'
        monster_right = 'enemy/' + str(monster_no) + '1.png'
        monster_dead = 'enemy/' + str(monster_no) + '2.png'
        self.image_right = image.load(monster_right)
        self.image_left = image.load(monster_left)
        self.image_dead = image.load(monster_dead)
        super(Monster, self).__init__(monster_left)

        self.image_anchor = 0, 0
        self.scale = 0.5
        self.x = random.randint(500, 2800)
        self.y = 400

        self.walk_speed = speed
        self.game = game
        self.speed = 0
        self.can_jump = False
        self.dead = False
        self.rightwards = 0
        # 用于记录周期
        self.count_walk = 0
        self.count_jump = 0
        self.schedule(self.update)

    def update(self, dt):
        if self.dead:
            return
        # 随机走位
        if self.count_jump > random.randint(20, 30):
            self.count_jump = 0
            if self.can_jump:
                if random.randint(0, 1):
                    self.jump(8.5)
        self.count_jump += 1

        if self.count_walk > random.randint(20, 30):
            self.count_walk = 0
            if random.randint(0, 1):
                self.rightwards = 1
                self.image = self.image_right
            else:
                self.rightwards = 0
                self.image = self.image_left
        self.count_walk += 1
        if self.rightwards:
            self.x += self.walk_speed
        else:
            self.x -= self.walk_speed
        # 重力掉落
        self.speed += 10 * dt
        self.y -= self.speed
        self.collide()

    def collide(self):
        # monster在floor中的x坐标
        fx = self.x - self.game.floor.x
        fy = self.y
        width = self.width
        height = self.height
        count = 0
        for b in self.game.floor.map.get_children():
            # 左下
            if b.x < fx + width * 0.1 < b.x + b.width and b.y < fy < b.y + b.height:
                if (b.x + b.width - fx) < (b.y + b.height - fy):
                    self.x = b.x + b.width + self.game.floor.x - width * 0.1
                else:
                    self.land(b.y + b.height)
                count += 1
                continue
            # 右下
            if b.x < fx + width * 0.9 < b.x + b.width and b.y < fy < b.y + b.height:
                if (fx + width * 0.9 - b.x) < b.y + b.height - fy:
                    self.x = b.x + self.game.floor.x - width * 0.9
                else:
                    self.land(b.y + b.height)
                count += 1
                continue
            # 右上
            if b.x < fx + width * 0.9 < b.x + b.width and b.y < fy + height * 0.9 < b.y + b.height:
                if (fx + width * 0.9 - b.x) < fy + height - b.y:
                    self.x = b.x + self.game.floor.x - width * 0.9
                else:
                    self.y = b.y - height * 0.9
                    self.speed = 0
                count += 1
                continue
            # 左上
            if b.x < fx + width * 0.1 < b.x + b.width and b.y < fy + height * 0.9 < b.y + b.height:
                if (b.x + b.width - fx) < fy + height - b.y:
                    self.x = b.x + b.width + self.game.floor.x - width * 0.1
                else:
                    self.y = b.y - height * 0.9
                    self.speed = 0
                count += 1
                continue
            if count >= 3:
                break
        if fx < 0:
            self.x = 0 + self.game.floor.x

    def land(self, y):
        if self.dead:
            return
        if self.y > y - 30:
            self.can_jump = True
            self.speed = 0
            self.y = y

    def jump(self, h):
        if self.can_jump:
            self.y += 1
            self.speed -= max(min(h, 10), 7)
            self.can_jump = False


class Spider(cocos.sprite.Sprite):
    def __init__(self):
        super(Spider, self).__init__('enemy/spider.png')
        self.image_anchor = 0, 0
        self.scale = 0.2
        self.position = 3270, 800
        self.passed = False
        self.speed = 20
        self.schedule(self.update)

    def update(self, dt):
        if not self.passed:
            return
        if self.y < -100:
            return
        self.speed += 10 * dt
        self.y -= self.speed

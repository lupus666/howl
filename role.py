import cocos
from pyglet import image
import time


class Role(cocos.sprite.Sprite):
    def __init__(self, game):

        # stand right
        self.stand_right = image.load('role/role-rightwards.png')
        # stand left
        self.stand_left = image.load('role/role-leftwards.png')
        # stand image
        self.image_stand = self.stand_right

        # walk right
        rframe_stand = image.AnimationFrame(image.load('role/role-rightwards.png'), 0.15)
        rframe_walk = image.AnimationFrame(image.load('role/role_walk-rightwards.png'), 0.15)
        self.rframes_walk = image.Animation([rframe_stand, rframe_walk])
        # walk left
        lframe_stand = image.AnimationFrame(image.load('role/role-leftwards.png'), 0.15)
        lframe_walk = image.AnimationFrame(image.load('role/role_walk-leftwards.png'), 0.15)
        self.lframes_walk = image.Animation([lframe_stand, lframe_walk])
        # walk frame
        self.frames_walk = self.rframes_walk

        # jump right
        rframe_jump = image.load('role/role_jump-rightwards.png')
        self.rframs_jump = rframe_jump
        # jump left
        lframe_jump = image.load('role/role_jump-leftwards.png')
        self.lframs_jump = lframe_jump
        # jump image
        self.image_jump = rframe_jump

        # dead right
        right_dead = image.load('role/role_dead-rightwards.png')
        self.right_dead = right_dead
        # dead left
        left_dead = image.load('role/role_dead-leftwards.png')
        self.left_dead = left_dead
        # dead image
        self.image_dead = self.right_dead

        # init
        super(Role, self).__init__(self.image_stand)
        self.image_anchor = 0, 0
        self.scale = 0.3
        self.position = 100, 300
        self.game = game

        self.can_shot = True
        self.can_jump = False
        self.direction = "RIGHT"
        self.state = "STAND"
        self.speed = 0
        self.dead = False

        self.schedule(self.update)

    def jump(self, h):
        if self.can_jump:
            self.image = self.image_jump
            self.y += 1
            self.speed -= max(min(h, 10), 7)
            self.can_jump = False

    # 着陆重置速度，即向下碰撞
    def land(self, y):
        if self.dead:
            return
        if self.y > y - 30:
            if not self.can_jump:
                if self.state == "RUN":
                    self.image = self.frames_walk
                else:
                    self.image = self.image_stand
            self.can_jump = True
            self.speed = 0
            self.y = y

    def update(self, dt):
        if self.dead:
            return
        self.speed += 10 * dt
        self.y -= self.speed
        self.game.y = -self.y + 100
        self.game.x = -self.x + 100
        self.game.voiceBar.x = - self.game.x + 100
        self.game.voiceBar.y = - self.game.y + 100 + self.height
        if self.y < -40:
            self.image = self.image_dead
        if self.y < -60:
            self.die()

    # 需要修改
    def reset(self):
        self.resume_scheduler()
        self.can_jump = False
        self.dead = False
        self.can_shot = True
        self.direction = "RIGHT"
        self.state = "STAND"
        self.image = self.stand_right
        self.speed = 0
        self.position = 100, 300

    def image_change(self, direct, state):
        if self.dead:
            return
        self.direction = direct
        self.state = state
        if self.direction == "RIGHT":
            self.image_stand = self.stand_right
            self.frames_walk = self.rframes_walk
            self.image_jump = self.rframs_jump
            self.image_dead = self.right_dead
        else:
            self.image_stand = self.stand_left
            self.frames_walk = self.lframes_walk
            self.image_jump = self.lframs_jump
            self.image_dead = self.left_dead

        if self.state == "RUN":
            self.image = self.frames_walk
        else:
            self.image = self.image_stand

    def die(self):
        self.pause_scheduler()
        # self.y += 20
        self.dead = True
        self.image = self.image_dead

        time.sleep(1)
        self.speed = 0
        self.game.end_game()




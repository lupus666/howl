import cocos


class Stone(cocos.sprite.Sprite):
    def __init__(self, speed, pos, dir):
        super(Stone, self).__init__('role/stone.png')
        self.image_anchor = 0, 0
        self.scale = 0.2

        self.position = pos
        if dir == 'RIGHT':
            self.speed_x = speed * 1.141
        else:
            self.speed_x = -speed * 1.141
            self.x -= 73
        self.speed_y = -speed * 1.141

        self.schedule(self.update)



    def update(self, dt):
        self.speed_y += 10 * dt
        self.y -= self.speed_y
        self.x += self.speed_x



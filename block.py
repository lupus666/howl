import math
import random
import cocos


class Block(cocos.sprite.Sprite):
    def __init__(self, pos, order):
        if order == 1:
            super(Block, self).__init__('ground/b1.png')
        if order == 2:
            super(Block, self).__init__('ground/b2.png')
        if order == 3:
            super(Block, self).__init__('ground/b3.png')
        if order == 4:
            super(Block, self).__init__('ground/b2.png')
        if order == 5:
            super(Block, self).__init__('ground/b4.png')
        if order == 6:
            super(Block, self).__init__('ground/b5.png')
        if order == 7:
            super(Block, self).__init__('ground/b6.png')
        if order == 8:
            super(Block, self).__init__('ground/b7.png')
        if order == 9:
            super(Block, self).__init__('ground/b8.png')
        if order == 10:
            super(Block, self).__init__('ground/b9.png')
        if order == 11:
            super(Block, self).__init__('ground/b10.png')
        if order == 12:
            super(Block, self).__init__('ground/b11.png')
        if order == 13:
            super(Block, self).__init__('ground/b12.png')
        if order == 14:
            super(Block, self).__init__('ground/b12.png')
        if order == 15:
            super(Block, self).__init__('ground/b13.png')
        if order == 16:
            super(Block, self).__init__('ground/f3.png')
        if order == 17:
            super(Block, self).__init__('ground/f2.png')
        if order == 18:
            super(Block, self).__init__('ground/f3.png')

        self.image_anchor = 0, 0
        self.scale = 0.5
        self.position = pos, 0
        if order == 14:
            self.position = pos + 130, 0
        if order == 16:
            self.position = 500, 240
        if order == 17:
            self.position = 1060, 240
        if order == 18:
            self.position = 2700, 180


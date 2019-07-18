import cocos
from map import Map
from monster import Monster, Spider


class Floor(cocos.cocosnode.CocosNode):
    def __init__(self, game, level):
        super(Floor, self).__init__()

        self.monster_number = 0
        self.monster_speed = 0
        if level == 'HARD':
            self.monster_number = 11
            self.monster_speed = 5
        if level == 'NORMAL':
            self.monster_number = 8
            self.monster_speed = 4
        if level == 'EASY':
            self.monster_number = 5
            self.monster_speed = 3

        # init background
        background1 = cocos.sprite.Sprite('scene/background.png')
        background2 = cocos.sprite.Sprite('scene/background.png')
        background1.image_anchor = 0, 0
        background1.scale_x = 1.5
        background2.scale_x = 1.5
        background2.image_anchor = 0, 0
        self.add(background1, 0)
        background2.x = background1.width
        self.add(background2, 0)

        # init map
        self.map = Map()
        self.add(self.map)

        # init destination
        flag = cocos.sprite.Sprite('scene/flag.png')
        flag.position = 3500, 120
        flag.scale = 0.5
        self.flag = flag
        self.add(flag)

        # init monster
        self.monster_node = cocos.cocosnode.CocosNode()
        for i in range(self.monster_number):
            self.monster_node.add(Monster(game, self.monster_speed))
        self.add(self.monster_node)

        self.game = game

        # init spider
        self.spider = Spider()
        self.monster_node.add(self.spider)

    def reset(self):
        self.remove(self.monster_node)
        self.monster_node = None
        self.spider = None
        self.monster_node = cocos.cocosnode.CocosNode()
        for i in range(self.monster_number):
            self.monster_node.add(Monster(self.game, self.monster_speed))
        self.add(self.monster_node)
        self.spider = Spider()
        self.monster_node.add(self.spider)


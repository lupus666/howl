import cocos
from block import Block


class Map(cocos.cocosnode.CocosNode):
    def __init__(self):
        super(Map, self).__init__()
        pos = 0
        for i in range(18):
            b = Block(pos, i + 1)
            self.add(b)
            pos = b.x + b.width


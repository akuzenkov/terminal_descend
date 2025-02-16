import heapq
import logging

from utils.primitives import Vector2D


logger = logging.getLogger(__file__)


class Grid:
    def __init__(self, height=200, width=200, terminal_pos=Vector2D(0, 0)):
        self.terminal_pos = terminal_pos
        self.height, self.width = height, width
        self.data = [[[] for _ in range(width)] for _ in range(height)]

    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            i, j = index
            self.data[i][j] = value
        else:
            self.data[index] = value

    def __delitem__(self, index):
        if isinstance(index, tuple):
            i, j = index
            del self.data[i][j]
        else:
            del self.data[index]

    def __len__(self):
        return len(self.data)
    
    def __iter__(self):
        return iter(self.data)
    
    def __contains__(self, item):
        return item in self.data
    
    def add_object(self, object):
        if not hasattr(object, "pos") or object.is_deleted:
            return

        heapq.heappush(self.data[object.pos.x][object.pos.y], (object.screen_weight, object.created_at, object))

    def remove_object(self, object):
        temp = []

        if not hasattr(object, "pos"):
            return 

        i, j = object.pos
        
        while self.data[i][j]:
            _, _, cur_object = heapq.heappop(self.data[i][j])
            if cur_object is object:
                break
            else:
                temp.append(cur_object)
        
        for obj in temp:
            heapq.heappush(self.data[i][j], (obj.screen_weight, obj.created_at, obj))

    def get_object_to_display(self, i, j):
        while self.data[i][j]:
            _, _, object = self.data[i][j][0]
            if not object.is_deleted:
                return object
            
            heapq.heappop(self.data[i][j])
        return None
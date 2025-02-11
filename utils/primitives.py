import math


class Vector2D:
    def __init__(self, x, y):
        super().__setattr__("x", x)
        super().__setattr__("y", y)

    def __setattr__(self, name, value):
        raise AttributeError(f"Vector2D is immutable")
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError

        return self.x == other.x and self.y != other.y

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError
        
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError
        
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __mul__(self, other):
        if not isinstance(other, (float, int)):
            raise ValueError
        
        return Vector2D(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    
    def __repr__(self):
        return fr"Vector2D({self.x}, {self.y})"
    
    @property
    def floor(self):
        return Vector2D(math.floor(self.x), math.floor(self.y))
# Vectorer

class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"Vector {self.x} and {self.y}"


        
vec1 = Vector(5, 12)

vec2 = Vector(2, 24)

vec3 = vec1 + vec2

print(vec3)
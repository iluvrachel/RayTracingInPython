from Ray import Ray
from Vec3 import Vec3
class Camera():
    def __init__(self):
        self.lower_left = Vec3(-2.0, -1.0, -1.0)
        self.horizontal = Vec3(4.0, 0.0, 0.0) # width
        self.vertical = Vec3(0.0, 2.0, 0.0) # height
        self.origin = Vec3(0.0, 0.0, 0.0) # camara position

    def GetRay(self, u, v):
        '''
        @param {u: horizontal distance from lower_left, v: vertical distance from lower_left} 
        @return: Ray
        '''        
        return Ray(self.origin, self.lower_left.Add(self.horizontal.Scale(u)).Add(self.vertical.Scale(v)))
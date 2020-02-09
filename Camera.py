import math
from Ray import Ray
from Vec3 import Vec3
class Camera():
    def __init__(self, look_from, look_at, vup, vfov, aspect):
        self.lower_left = Vec3(-2.0, -2.0, -2.0)
        self.horizontal = Vec3(4.0, 0.0, 0.0) # width
        self.vertical = Vec3(0.0, 4.0, 0.0) # height
        self.origin = Vec3(0.0, 0.0, 0.0) # camara position

        # Camera cordinate
        self.u, self.v, self.w = None, None, None
        self.theta = float(vfov * math.pi / 180) # fov theta
        self.half_height = float(math.tan(self.theta/2))
        self.half_width = aspect * self.half_height
        self.origin = look_from
        self.w = look_from.Sub(look_at).normalize()
        self.u = vup.cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()
        self.lower_left = self.origin.Sub(self.u.Scale(self.half_width)).Sub(self.v.Scale(self.half_height)).Sub(self.w)
        self.horizontal = self.u.Scale(2*self.half_width)
        self.vertical = self.v.Scale(2*self.half_height)

    def GetRay(self, u, v):
        '''
        @param {u: horizontal distance from lower_left, v: vertical distance from lower_left} 
        @return: Ray
        '''        
        return Ray(self.origin, self.lower_left.Add(self.horizontal.Scale(u)).Add(self.vertical.Scale(v)).Sub(self.origin))
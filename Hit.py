from Vec3 import Vec3
from Ray import Ray
import math

class Hitable():
    def hit(r, t_min, t_max, rec):
        '''
        @param {Ray r, float t_min, float t_max, HitRecord rec} 
        @return: bool
        '''    
        pass

class HitRecord():
    def __init__(self):
        '''
        @param {t: hit time, p: hit position, normal: hit point normal} 
        @return: None
        '''        
        self.t = 0
        self.p = Vec3(0.0, 0.0, 0.0)
        self.normal = Vec3(0.0, 0.0, 0.0)

class Sphere(Hitable):
    def __init__(self, center, radius):
        '''
        @param {Vec3 center, float radius} 
        @return: 
        '''
        self.center = center
        self.radius = radius

    def hit(self, r, t_min, t_max, rec):
        '''
        ray: p = A + t*B
        sphere: C(x,y,z)
        (B*B)t^2 + 2B(A-C)t + (A^2 - C^2 - R^2) = 0
        delta = b^2 - 4ac
        '''
        oc = r.origin().Sub(self.center) # oc = A-C
        a = r.direction().dot(r.direction()) # a = B dot B
        b = 2.0 * oc.dot(r.direction()) # b = 2B dot oc
        c = oc.dot(oc) - self.radius**2 # c = oc^2 - R^2
        discriminant = b**2 - 4.0*a*c
        if discriminant > 0:
            # 优先选取符合范围的根较小的撞击点，若没有再选取另一个根
            discFactor = math.sqrt(discriminant)
            temp = (-b - discFactor) / (2.0*a) # 求根公式 较小的根
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p.Sub(self.center)).Scale(1.0/self.radius)
                return True
            temp = (-b + discFactor) / (2.0*a) # 较大的根
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p.Sub(self.center)).Scale(1.0/self.radius)
                return True
        return False

class Hitable_list(Hitable):
    def __init__(self, list):
        self.list = list
    
    def hit(self, r, t_min, t_max, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max 
        for i in range(0, len(self.list)):
            if self.list[i].hit(r, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t # update t_max
                rec.t = temp_rec.t
                rec.normal = temp_rec.normal
                rec.p = temp_rec.p
        return hit_anything



            
import random
# from RayTracer import random_in_unit_sphere
from Vec3 import Vec3
from Ray import Ray

def random_in_unit_sphere():
    while True:
        p = Vec3(float(random.random()),float(random.random()),float(random.random())).Scale(2.0).Sub(Vec3(1.0,1.0,1.0))
        if p.dot(p) >= 1.0:
            pass
        else:
            return p 

class Material():
    def scatter(self, ray, rec, wrapper):
        '''
        @param {ray, hit_record, wrapper: wrap up reflect ray and attenuation} 
        @return: bool
        '''        
        return True


class Wrapper():
    '''
    @ Pack up scattered ray and material 
    '''
    def __init__(self):
        self.scattered = None
        self.attenuation = None

class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        if fuzz < 1:
            self.fuzz = fuzz
        else:
            self.fuzz = 1

    def scatter(self, ray, rec, wrapper):
        target = self.reflect(ray.direction(), rec.normal.normalize())
        wrapper.scattered = Ray(rec.p, target.Add(random_in_unit_sphere().Scale(self.fuzz)))
        wrapper.attenuation = self.albedo
        return (target.dot(rec.normal) > 0)

    def reflect(self, v, n):
        '''
        @param {v: ray_in, n: normal} 
        @return: ray_out
        '''        
        return v.Sub(n.Scale(v.dot(n)*2)) # ray_out = ray_in + 2*(ray_in dot n)

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, rec, wrapper):
        target = rec.p.Add(rec.normal).Add(random_in_unit_sphere())
        wrapper.scattered = Ray(rec.p, target.Sub(rec.p))
        wrapper.attenuation = self.albedo
        return (target.dot(rec.normal) > 0)

    def reflect(self, v, n):
        '''
        @param {v: ray_in, n: normal} 
        @return: ray_out
        '''        
        return v.Sub(n.Scale(v.dot(n)*2)) # ray_out = ray_in + 2*(ray_in dot n)
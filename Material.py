import random
import math
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
        self.refracted = None

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


class Deilectric(Material):
    def __init__(self, ri):
        '''
        @param {ri: refractive index} 
        @return: 
        '''        
        self.ri = ri
        self.wrapper = None
    
    def scatter(self, ray, rec, wrapper):
        ''' 
        @return: bool
        '''
        self.wrapper = wrapper
        outward_normal = None
        reflected = self.reflect(ray.direction(), rec.normal)
        ni_over_nt = None
        self.wrapper.attenuation = Vec3(1.0,1.0,1.0)
        refracted = None

        if (ray.direction().dot(rec.normal) > 0):
            # 从密度小的介质到密度大的介质
            outward_normal = rec.normal.Scale(-1.0)
            ni_over_nt = self.ri
            cosine = ray.direction().dot(rec.normal) / (ray.direction().length() * rec.normal.length())
        else:
            # 从密度大的介质到密度小的介质
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ri
            cosine = -ray.direction().dot(rec.normal) / (ray.direction().length() * rec.normal.length())
        
        if self.refract(ray.direction(), outward_normal, ni_over_nt, self.wrapper):
            reflect_prob = self.schlick(cosine, self.ri)
        else:
            reflect_prob = 1.0
        
        if random.random() < reflect_prob:
            self.wrapper.scattered = Ray(rec.p, reflected)
        else:
            self.wrapper.scattered = Ray(rec.p, self.wrapper.refracted)
        return True

    def refract(self, v, n, ni_over_nt, refracted):
        '''
        @param {vec: ray_in, vec: normal, float: Refractive Media, vec: refract ray} 
        @return: bool
        '''
        uv = v.normalize() # unit_vector
        dt = uv.dot(n)
        discriminant = 1.0 - ni_over_nt*ni_over_nt*(1.0-dt*dt)
        if discriminant > 0:
            self.wrapper.refracted = uv.Scale(ni_over_nt).Add(n.Scale(float(ni_over_nt*dt - math.sqrt(discriminant))))
            return True
        else:
            return False

    def reflect(self, v, n):
        return v.Sub(n.Scale(v.dot(n)*2))

    # polynomial approximation by Christophe Schlick
    def schlick(self, cosine, ri):
        r0 = (1-ri) / (1+ri)
        r0 = r0**2
        return float(r0 + (1-r0)*(1 - cosine)**5)


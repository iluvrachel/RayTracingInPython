#ppm2jpg
from PIL import Image
import cv2
from tqdm import tqdm
import math
import random

from Vec3 import Vec3
from Ray import Ray
from Hit import Hitable, HitRecord, Sphere, Hitable_list
from Camera import Camera
from Material import Metal, Lambertian, Deilectric, Wrapper

def writePPM():
    width = 400
    height = 200
    ns = 100 # smaple nums

    lower_left = Vec3(-2.0,-2.0,-2.0)
    horizontal = Vec3(4.0,0.0,0.0)
    vertical = Vec3(0.0,4.0,0.0)
    origin = Vec3(0.0,0.0,0.0)

    
    with open('result.ppm', 'w') as f:
        f.write("P3\n" + str(width) + " " + str(height) + "\n255\n")
        index = 0
        world = create_scene()
        camera = Camera(Vec3(-2.0,2.0,1.0), Vec3(0.0,0.0,-1.0), Vec3(0.0,1.0,0.0), 40.0, float(width)/float(height))
        with tqdm(total=height) as pbar:
            for j in range(height-1,-1,-1):
                for i in range(0,width):
                    col = Vec3(0,0,0)
                    for s in range(0,ns):
                        u = float(i+random.random())/float(width) # antialiasing
                        v = float(j+random.random())/float(height)
                        ray = camera.GetRay(u,v)
                        col = col.Add(color(ray,world,0))
                    col = col.Scale(1.0/float(ns)) # average color
                    # gamma
                    col = Vec3(float(math.sqrt(col.x())),float(math.sqrt(col.y())),float(math.sqrt(col.z())))
                    index += 1
                    ir = int(255.59*col.x())
                    ig = int(255.59*col.y())
                    ib = int(255.59*col.z())
                    f.write(str(ir) + " " + str(ig) + " " + str(ib) + "\n")
                pbar.update(1)

def ppm2jpg(ppm_path):
    img = cv2.imread(ppm_path)
    cv2.imwrite("render.jpg",img)
    output = cv2.imread("render.jpg")
    cv2.imshow("output",output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''
# ray: p = A + t*B
# sphere: C(x,y,z)
# (B*B)t^2 + 2B(A-C)t + (A^2 - C^2 - R^2) = 0
# delta = b^2 - 4ac
def hitSphere(center, radius, ray):
    oc = ray.origin().Sub(center) # oc = A-C
    a = ray.direction().dot(ray.direction()) # a = B dot B
    b = 2.0 * oc.dot(ray.direction()) # b = 2B dot oc
    c = oc.dot(oc) - radius**2 # c = oc^2 - R^2
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return -1.0
    else:
        return (-b - float(math.sqrt(discriminant)) / (2.0*a)) # t
'''

def create_scene():
    obj_list = []
    obj_list.append(Sphere(Vec3(0.0,0.0,-1.0),0.5, Lambertian(Vec3(0.1,0.2,0.5))))
    obj_list.append(Sphere(Vec3(-1.0,0.0,-1.0),0.5,Deilectric(1.5)))
    obj_list.append(Sphere(Vec3(1.0,0.0,-1.0),0.5,Metal(Vec3(0.8,0.6,0.2),0.2)))


    # Ground
    obj_list.append(Sphere(Vec3(0.0,-100.5,-1.0),100.0,Lambertian(Vec3(0.5,0.5,0.5))))
    world = Hitable_list(obj_list)
    return world

def color(r,world,depth):
    '''
    @param {ray, hitable_list, recursion_depth} 
    @return: 
    '''
    rec = HitRecord()
    if world.hit(r,0,float('inf'),rec):
        # ray reflect target
        wrapper = Wrapper()
        # target = rec.p.Add(rec.normal).Add(random_in_unit_sphere())
        
        # paint according to normal value
        # decay 50% every reflect
        if depth < 50 and rec.mat_ptr.scatter(r, rec, wrapper):
            return wrapper.attenuation.Mul(color(wrapper.scattered, world, depth+1))
            #return color(Ray(rec.p, target.Sub(rec.p)), world, depth+1).Scale(0.5)
        else:
            return Vec3(0.0,0.0,0.0)
    else:
        unit_dir = r.direction().normalize()
        t = 0.5*(unit_dir.y()+1.0)
        return Vec3(1.0, 1.0, 1.0).Scale(1.0 - t).Add(Vec3(0.5,0.7,1.0).Scale(t))




if __name__ == '__main__':
    writePPM()
    ppm2jpg('result.ppm')
                
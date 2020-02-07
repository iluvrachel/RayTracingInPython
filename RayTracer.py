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

def writePPM():
    width = 256
    height = 256
    ns = 100 # smaple nums

    lower_left = Vec3(-2.0,-2.0,-2.0)
    horizontal = Vec3(4.0,0.0,0.0)
    vertical = Vec3(0.0,4.0,0.0)
    origin = Vec3(0.0,0.0,0.0)

    
    with open('result.ppm', 'w') as f:
        f.write("P3\n" + str(width) + " " + str(height) + "\n255\n")
        index = 0
        world = create_scene()
        camera = Camera()
        with tqdm(total=256) as pbar:
            for j in range(height-1,-1,-1):
                for i in range(0,width):
                    col = Vec3(0,0,0)
                    for s in range(0,ns):
                        u = float(i+random.random())/float(width) # antialiasing
                        v = float(j+random.random())/float(height)
                        ray = camera.GetRay(u,v)
                        col = col.Add(color(ray,world))
                    col = col.Scale(1.0/float(ns)) # average color
                    # gamma
                    col = Vec3(math.sqrt(col.x()),math.sqrt(col.y()),math.sqrt(col.z()))
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
def random_in_unit_sphere():
    while True:
        p = Vec3(float(random.random()),float(random.random()),float(random.random())).Scale(2.0).Sub(Vec3(1.0,1.0,1.0))
        if p.dot(p) >= 1.0:
            pass
        else:
            return p 

def create_scene():
    obj_list = []
    obj_list.append(Sphere(Vec3(0.0,0.0,-1.0),0.5))
    obj_list.append(Sphere(Vec3(0.3,0.0,-1.0),0.5))
    obj_list.append(Sphere(Vec3(0.0,-100.5,-1.0),100.0))
    world = Hitable_list(obj_list)
    return world

def color(r,world):
    rec = HitRecord()
    if world.hit(r,0,float('inf'),rec):
        # ray reflect target
        target = rec.p.Add(rec.normal).Add(random_in_unit_sphere())
        # paint according to normal value
        # decay 50% every reflect
        return color(Ray(rec.p, target.Sub(rec.p)), world).Scale(0.5)
    else:
        unit_dir = r.direction().normalize()
        t = 0.5*(unit_dir.y()+1.0)
        return Vec3(1.0, 1.0, 1.0).Scale(1.0 - t).Add(Vec3(0.5,0.7,1.0).Scale(t))




if __name__ == '__main__':
    writePPM()
    ppm2jpg('result.ppm')
                
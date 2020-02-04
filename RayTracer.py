#ppm2jpg
from PIL import Image
import cv2
from tqdm import tqdm

from Vec3 import Vec3
from Ray import Ray

def writePPM():
    width = 256
    height = 256

    lower_left = Vec3(-2.0,-1.0,-1.0)
    horizontal = Vec3(4.0,0.0,0.0)
    vertical = Vec3(0.0,2.0,0.0)
    origin = Vec3(0.0,0.0,0.0)

    def color(r):
        unit_dir = r.direction().normalize()
        t = 0.5*(unit_dir.y()+1.0)
        return Vec3(1.0, 1.0, 1.0).Scale(1.0 - t).Add(Vec3(0.5,0.7,1.0).Scale(t))

    with open('result.ppm', 'w') as f:
        f.write("P3\n" + str(width) + " " + str(height) + "\n255\n")
        index = 0
        with tqdm(total=256) as pbar:
            for j in range(height-1,-1,-1):
                for i in range(0,width):
                    u = float(i)/float(width)
                    v = float(j)/float(height)
                    ray = Ray(origin, lower_left.Add(horizontal.Scale(u)).Add(vertical.Scale(v)))
                    col = color(ray)
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



if __name__ == '__main__':
    writePPM()
    ppm2jpg('result.ppm')
                
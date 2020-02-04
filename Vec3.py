import math

class Vec3():
    def __init__(self,x,y,z):
        self.e = [x,y,z]

    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]
    
    def z(self):
        return self.e[2]
    
    def length(self):
        return math.sqrt(self.e[0]*self.e[0] + self.e[1]*self.e[1] + self.e[2]*self.e[2])

    def square_length(self):
        return self.e[0]*self.e[0] + self.e[1]*self.e[1] + self.e[2]*self.e[2]

    def Add(self,v):
        return Vec3(self.e[0]+v.e[0],self.e[1]+v.e[1],self.e[2]+v.e[2])

    def Sub(self,v):
        return Vec3(self.e[0]-v.e[0],self.e[1]-v.e[1],self.e[2]-v.e[2])

    def Scale(self,t):
        return Vec3(self.e[0]*t, self.e[1]*t, self.e[2]*t)

    def normalize(self):
        length = self.length()
        return Vec3(self.e[0]/length, self.e[1]/length, self.e[2]/length)
    
    def dot(self,v):
        return (self.e[0]*v.e[0] + self.e[1]*v.e[1] + self.e[2]*v.e[2])

    def cross(a,b):
        return Vec3(a.y()*b.z() - a.z()*b.y(), a.z()*b.x() - a.x()*b.z(), a.x()*b.y() - a.y()*b.x())



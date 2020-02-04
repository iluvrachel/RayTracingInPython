import Vec3

class Ray():
    def __init__(self,origin,direction):
        self.o = origin
        self.d = direction

    def origin(self):
        return self.o

    def direction(self):
        return self.d
    
    # p(t) = A + t*B
    def point_at_parameter(self,t):
        return self.o.Add(self.d.Scale(t))
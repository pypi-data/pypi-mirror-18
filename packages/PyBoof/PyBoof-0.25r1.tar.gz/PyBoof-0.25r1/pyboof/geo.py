import math
import numpy as np
import py4j.java_gateway as jg
from common import *


def real_ejml_to_nparray( ejml ):
    num_rows = ejml.getNumRows()
    num_cols = ejml.getNumCols()

    M = np.zeros((num_rows,num_cols))
    for i in xrange(num_rows):
        for j in xrange(num_cols):
            M[i,j] = ejml.unsafe_get(i,j)
    return M

def real_nparray_to_ejml( array ):
    num_rows = array.shape[0]
    num_cols = array.shape[1]

    M = gateway.jvm.org.ejml.data.DenseMatrix64F(num_rows,num_cols)
    for i in xrange(num_rows):
        for j in xrange(num_cols):
            M.unsafe_set(i,j,array[i,j])
    return M

class Se3_F64(JavaWrapper):
    def __init__(self, java_Se3F64=None):
        if java_Se3F64 is None:
            JavaWrapper.__init__(self, gateway.jvm.georegression.struct.se.Se3_F64())
        else:
            JavaWrapper.__init__(self, java_Se3F64)

    def invert(self):
        return Se3_F64(self.java_obj.invert(None))

    def get_rotation(self):
        return real_ejml_to_nparray(self.java_obj.getR())

    def get_translation(self):
        T = self.java_obj.getT()
        return (T.getX(),T.getY(),T.getZ())


def create_java_point_2D_f32(x=0., y=0.):
    return gateway.jvm.georegression.struct.point.Point2D_F32(float(x), float(y))


def create_java_point_2D_f64(x=0., y=0.):
    return gateway.jvm.georegression.struct.point.Point2D_F64(float(x), float(y))


def create_java_point_3D_f32(x=0., y=0., z=0.):
    return gateway.jvm.georegression.struct.point.Point3D_F32(float(x), float(y), float(z))


def create_java_point_3D_f64(x=0., y=0., z=0.):
    return gateway.jvm.georegression.struct.point.Point3D_F64(float(x), float(y), float(z))


def tuple_to_Point2D_F64(ptuple, jpoint=None):
    if jpoint == None:
        return create_java_point_2D_f32(ptuple[0],ptuple[1])
    else:
        jpoint.set(float(ptuple[0]),float(ptuple[1]))
        return jpoint


def tuple_to_Point2D_F32(ptuple ,jpoint=None):
    if jpoint == None:
        return create_java_point_2D_f64(ptuple[0],ptuple[1])
    else:
        jpoint.set(float(ptuple[0]),float(ptuple[1]))
        return jpoint


class Point2D:
    def __init__(self, x=0, y=0):
        """
        :param x: float
            x-coordinate
        :param y: float
            y-coordinate
        """
        self.x = x
        self.y = y

    def convert_to_boof(self):
        return create_java_point_2D_f64(float(self.x), float(self.y))

    def set(self, o):
        if type(o) is Point2D:
            self.x = o.x
            self.y = o.y
        if type(o) is tuple:
            self.x = o[0]
            self.y = o[1]
        elif jg.is_instance_of(gateway, o, gateway.jvm.georegression.struct.point.Point2D_F64):
            self.x = o.getX()
            self.y = o.getY()
        else:
            raise Exception("Unknown object type")

    def distance(self, point):
        dx = point.x-self.x
        dy = point.y-self.y
        return math.sqrt(dx*dx + dy*dy)


    def get_tuple(self):
        """
        Returns the values of the point inside a tuple: (x,y)
        """
        return (self.x,self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self,y ):
        self.y = y


class Quadrilateral2D:
    """
    Four sided polygon specified by its vertexes.  The vertexes are ordered, but it's not specified if they are
    ordered in clockwise or counter clockwise direction
    """
    def __init__(self, a=Point2D(), b=Point2D(), c=Point2D(), d=Point2D()):
        """

        :param a: Point2D
            Vertex is the quadrilateral
        :param b: Point2D
            Vertex is the quadrilateral
        :param c: Point2D
            Vertex is the quadrilateral
        :param d: Point2D
            Vertex is the quadrilateral
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def convert_to_boof(self):
        a = self.a.convert_to_boof()
        b = self.b.convert_to_boof()
        c = self.c.convert_to_boof()
        d = self.d.convert_to_boof()

        return gateway.jvm.georegression.struct.shapes.Quadrilateral_F64(a,b,c,d)

    def set(self, o):
        if type(o) is Quadrilateral2D:
            self.a.set(o.a)
            self.b.set(o.b)
            self.c.set(o.c)
            self.d.set(o.d)

        elif jg.is_instance_of(gateway, o, gateway.jvm.georegression.struct.shapes.Quadrilateral_F64 ):
            self.a.set(o.getA())
            self.b.set(o.getB())
            self.c.set(o.getC())
            self.d.set(o.getD())
        else:
            raise Exception("Unknown object type")

    def get_vertexes(self):
        """
        Returns a tuple with all the vertexes (a,b,c,d)
        :return: tuple of all vertexes
        """
        return (self.a,self.b,self.c,self.d)

    def get_tuple_tuple(self):
        return (self.a.get_tuple(),self.b.get_tuple(),self.c.get_tuple(),self.d.get_tuple())

    def get_a(self):
        return self.a

    def get_b(self):
        return self.b

    def get_c(self):
        return self.c

    def get_d(self):
        return self.d

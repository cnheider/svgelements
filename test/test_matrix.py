from __future__ import print_function

import unittest

from svg.elements import *


class TestPathMatrix(unittest.TestCase):

    def test_rotate_css_angles(self):
        matrix = Matrix("rotate(90, 100,100)")
        path = Path("M0,0z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())
        matrix = Matrix("rotate(90deg, 100,100)")
        path = Path("M0,0z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())
        matrix = Matrix("rotate(0.25turn, 100,100)")
        path = Path("M0,0z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())
        matrix = Matrix("rotate(100grad, 100,100)")
        path = Path("M0,0z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())
        matrix = Matrix("rotate(1.5707963267948966rad, 100,100)")
        path = Path("M0,0z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())

    def test_matrix_multiplication(self):
        self.assertEqual(Matrix("scale(0.2) translate(-5,-5)"), Matrix("translate(-5,-5)") * Matrix("scale(0.2)"))
        self.assertEqual(Matrix("translate(-5,-5) scale(0.2)"), Matrix("scale(0.2)") * Matrix("translate(-5,-5)"))

    def test_rotate_css_distance(self):
        matrix = Matrix("rotate(90deg,100cm,100cm)")
        path = Path("M0,0z")
        path *= matrix
        p2 = Path("M 200,0 Z") * Matrix("scale(%f)" % Distance.parse("1cm"))
        self.assertEqual(p2, path)

    def test_skew_single_value(self):
        m0 = Matrix("skew(15deg,0deg)")
        m1 = Matrix("skewX(15deg)")
        self.assertEqual(m0, m1)
        m0 = Matrix("skew(0deg,15deg)")
        m1 = Matrix("skewY(15deg)")
        self.assertEqual(m0, m1)

    def test_scale_single_value(self):
        m0 = Matrix("scale(2,1)")
        m1 = Matrix("scaleX(2)")
        self.assertEqual(m0, m1)
        m0 = Matrix("scale(1,2)")
        m1 = Matrix("scaleY(2)")
        self.assertEqual(m0, m1)

    def test_translate_single_value(self):
        m0 = Matrix("translate(500cm,0)")
        m1 = Matrix("translateX(500cm)")
        self.assertEqual(m0, m1)
        m0 = Matrix("translate(0,500cm)")
        m1 = Matrix("translateY(500cm)")
        self.assertEqual(m0, m1)
        m0 = Matrix("translate(500cm)")
        m1 = Matrix("translateX(500cm)")
        self.assertEqual(m0, m1)

    def test_translate_css_value(self):
        m0 = Matrix("translate(50mm,5cm)")
        m1 = Matrix("translate(5cm,5cm)")
        self.assertEqual(repr(m0), repr(m1))

    def test_rotate_css_value(self):
        m0 = Matrix("rotate(90deg, 50cm,50cm)")
        m1 = Matrix("rotate(0.25turn, 500mm,500mm)")
        self.assertEqual(repr(m0), repr(m1))

    def test_transform_translate(self):
        matrix = Matrix("translate(5,4)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z")
        path *= matrix
        self.assertEqual("M 5,4 L 5,104 L 105,104 L 105,4 L 5,4 Z", path.d())

    def test_transform_scale(self):
        matrix = Matrix("scale(2)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z")
        path *= matrix
        self.assertEqual("M 0,0 L 0,200 L 200,200 L 200,0 L 0,0 Z", path.d())

    def test_transform_rotate(self):
        matrix = Matrix("rotate(360)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z")
        path *= matrix
        self.assertAlmostEqual(path[0][1].x, 0)
        self.assertAlmostEqual(path[0][1].y, 0)

        self.assertAlmostEqual(path[1][1].x, 0)
        self.assertAlmostEqual(path[1][1].y, 100)

        self.assertAlmostEqual(path[2][1].x, 100)
        self.assertAlmostEqual(path[2][1].y, 100)
        self.assertAlmostEqual(path[3][1].x, 100)
        self.assertAlmostEqual(path[3][1].y, 0)
        self.assertAlmostEqual(path[4][1].x, 0)
        self.assertAlmostEqual(path[4][1].y, 0)

    def test_transform_value(self):
        matrix = Matrix("rotate(360,50,50)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z")
        path *= matrix
        self.assertAlmostEqual(path[0][1].x, 0)
        self.assertAlmostEqual(path[0][1].y, 0)

        self.assertAlmostEqual(path[1][1].x, 0)
        self.assertAlmostEqual(path[1][1].y, 100)

        self.assertAlmostEqual(path[2][1].x, 100)
        self.assertAlmostEqual(path[2][1].y, 100)
        self.assertAlmostEqual(path[3][1].x, 100)
        self.assertAlmostEqual(path[3][1].y, 0)
        self.assertAlmostEqual(path[4][1].x, 0)
        self.assertAlmostEqual(path[4][1].y, 0)

    def test_transform_skewx(self):
        matrix = Matrix("skewX(10,50,50)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z")
        path *= matrix
        self.assertEqual("M -8.81635,0 L 8.81635,100 L 108.816,100 L 91.1837,0 L -8.81635,0 Z", path.d())

    def test_transform_skewy(self):
        matrix = Matrix("skewY(10, 50,50)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z")
        path *= matrix
        print(path.d())
        self.assertEqual("M 0,-8.81635 L 0,91.1837 L 100,108.816 L 100,8.81635 L 0,-8.81635 Z", path.d())

    def test_matrix_repr_rotate(self):
        """
        [a c e]
        [b d f]
        """
        v = "Matrix(%3f, %3f, %3f, %3f, %3f, %3f)" % (0, 1, -1, 0, 0, 0)
        self.assertEqual(v, repr(Matrix.rotate(radians(90))))

    def test_matrix_repr_scale(self):
        """
        [a c e]
        [b d f]
        """
        v = "Matrix(%3f, %3f, %3f, %3f, %3f, %3f)" % (2, 0, 0, 2, 0, 0)
        self.assertEqual(v, repr(Matrix.scale(2)))

    def test_matrix_repr_hflip(self):
        """
        [a c e]
        [b d f]
        """
        v = "Matrix(%3f, %3f, %3f, %3f, %3f, %3f)" % (-1, 0, 0, 1, 0, 0)
        self.assertEqual(v, repr(Matrix.scale(-1, 1)))

    def test_matrix_repr_vflip(self):
        """
        [a c e]
        [b d f]
        """
        v = "Matrix(%3f, %3f, %3f, %3f, %3f, %3f)" % (1, 0, 0, -1, 0, 0)
        self.assertEqual(v, repr(Matrix.scale(1, -1)))

    def test_matrix_repr_post_cat(self):
        """
        [a c e]
        [b d f]
        """
        v = "Matrix(%3f, %3f, %3f, %3f, %3f, %3f)" % (2, 0, 0, 2, -20, -20)
        m = Matrix.scale(2)
        m.post_cat(Matrix.translate(-20, -20))
        self.assertEqual(v, repr(m))

    def test_matrix_repr_pre_cat(self):
        """
        [a c e]
        [b d f]
        """
        v = "Matrix(%3f, %3f, %3f, %3f, %3f, %3f)" % (2, 0, 0, 2, -20, -20)
        m = Matrix.translate(-20, -20)
        m.pre_cat(Matrix.scale(2))
        self.assertEqual(v, repr(m))

    def test_matrix_point_rotated_by_matrix(self):
        matrix = Matrix()
        matrix.post_rotate(radians(90), 100, 100)
        p = matrix.point_in_matrix_space((50, 50))
        self.assertAlmostEqual(p[0], 150)
        self.assertAlmostEqual(p[1], 50)

    def test_matrix_point_scaled_in_space(self):
        matrix = Matrix()
        matrix.post_scale(2, 2, 50, 50)

        p = matrix.point_in_matrix_space((50, 50))
        self.assertAlmostEqual(p[0], 50)
        self.assertAlmostEqual(p[1], 50)

        p = matrix.point_in_matrix_space((25, 25))
        self.assertAlmostEqual(p[0], 0)
        self.assertAlmostEqual(p[1], 0)

        matrix.post_rotate(radians(45), 50, 50)
        p = matrix.point_in_matrix_space((25, 25))
        self.assertAlmostEqual(p[0], 50)

        matrix = Matrix()
        matrix.post_scale(0.5, 0.5)
        p = matrix.point_in_matrix_space((100, 100))
        self.assertAlmostEqual(p[0], 50)
        self.assertAlmostEqual(p[1], 50)

        matrix = Matrix()
        matrix.post_scale(2, 2, 100, 100)
        p = matrix.point_in_matrix_space((50, 50))
        self.assertAlmostEqual(p[0], 0)
        self.assertAlmostEqual(p[1], 0)

    def test_matrix_cat_identity(self):
        identity = Matrix()
        from random import random
        for i in range(50):
            q = Matrix(random(), random(), random(), random(), random(), random())
            p = copy(q)
            q.post_cat(identity)
            self.assertEqual(q, p)

    def test_matrix_pre_and_post_1(self):
        from random import random
        for i in range(50):
            tx = random() * 1000 - 500
            ty = random() * 1000 - 500
            rx = random() * 2
            ry = random() * 2
            a = random() * tau
            q = Matrix()
            q.post_translate(tx, ty)
            p = Matrix()
            p.pre_translate(tx, ty)
            self.assertEqual(p, q)

            q = Matrix()
            q.post_scale(rx, ry, tx, ty)
            p = Matrix()
            p.pre_scale(rx, ry, tx, ty)
            self.assertEqual(p, q)

            q = Matrix()
            q.post_rotate(a, tx, ty)
            p = Matrix()
            p.pre_rotate(a, tx, ty)
            self.assertEqual(p, q)

            q = Matrix()
            q.post_skew_x(a, tx, ty)
            p = Matrix()
            p.pre_skew_x(a, tx, ty)
            self.assertEqual(p, q)

            q = Matrix()
            q.post_skew_y(a, tx, ty)
            p = Matrix()
            p.pre_skew_y(a, tx, ty)
            self.assertEqual(p, q)

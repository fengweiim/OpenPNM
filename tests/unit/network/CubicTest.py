import openpnm as op
import scipy as sp


class CubicTest:
    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def test_spacing_2D(self):
        net = op.network.Cubic(shape=[5, 5, 1], spacing=[1, 1])
        assert sp.all(net.spacing == [1.0, 1.0, 0.0])

    def test_spacing_3D(self):
        net = op.network.Cubic(shape=[5, 5, 5], spacing=[1, 1, 1])
        assert sp.all(net.spacing == [1.0, 1.0, 1.0])

    def test_spacing_2D_uneven(self):
        net = op.network.Cubic(shape=[5, 5, 1], spacing=[1, 2])
        assert sp.all(net.spacing == [1.0, 2.0, 0.0])

    def test_spacing_3D_uneven(self):
        net = op.network.Cubic(shape=[3, 4, 5], spacing=[1, 2, 3])
        assert sp.all(net.spacing == [1.0, 2.0, 3.0])

    def test_shape_2D(self):
        pass

    def test_spacing_3D_rotated(self):
        net = op.network.Cubic(shape=[5, 5, 5], spacing=[1, 1, 1])
        theta = 0.1
        R = sp.array([[1, 0, 0],
                      [0, sp.cos(theta), -sp.sin(theta)],
                      [0, sp.sin(theta), sp.cos(theta)]])
        net['pore.coords'] = sp.tensordot(net['pore.coords'], R, axes=(1, 1))
        assert sp.all(net.spacing == [1.0, 1.0, 1.0])

    def test_spacing_3D_rotated_uneven(self):
        net = op.network.Cubic(shape=[3, 4, 5], spacing=[1, 2, 3])
        theta = 0.1
        R = sp.array([[1, 0, 0],
                      [0, sp.cos(theta), -sp.sin(theta)],
                      [0, sp.sin(theta), sp.cos(theta)]])
        net['pore.coords'] = sp.tensordot(net['pore.coords'], R, axes=(1, 1))
        assert sp.all(net.spacing == [1.0, 2.0, 3.0])

    def test_spacing_2D_sheared(self):
        net = op.network.Cubic(shape=[5, 5, 1], spacing=1)
        S = sp.array([[1, 1, 0],
                      [0, 1, 0],
                      [0, 0, 1]])
        net['pore.coords'] = (S@net['pore.coords'].T).T
        assert sp.allclose(net.spacing, [1.0, 2**0.5, 0.0])

    def test_spacing_2D_sheared_uneven(self):
        net = op.network.Cubic(shape=[5, 5, 1], spacing=[1, 2])
        S = sp.array([[1, 1, 0],
                      [0, 1, 0],
                      [0, 0, 1]])
        net['pore.coords'] = (S@net['pore.coords'].T).T
        assert sp.allclose(net.spacing, [1.0, 2*(2**0.5), 0.0])

    def test_spacing_3D_sheared(self):
        net = op.network.Cubic(shape=[5, 5, 3], spacing=1)
        S = sp.array([[1, 1, 0],
                      [0, 1, 0],
                      [0, 0, 1]])
        net['pore.coords'] = (S@net['pore.coords'].T).T
        assert sp.allclose(net.spacing, [1.0, 2**0.5, 1.0])

    def test_spacing_3D_sheared_uneven(self):
        net = op.network.Cubic(shape=[3, 4, 5], spacing=[1, 2, 3])
        S = sp.array([[1, 1, 0],
                      [0, 1, 0],
                      [0, 0, 1]])
        net['pore.coords'] = (S@net['pore.coords'].T).T
        assert sp.allclose(net.spacing, [1.0, 2*(2**0.5), 3.0])


if __name__ == '__main__':

    t = CubicTest()
    t.setup_class()
    self = t
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()

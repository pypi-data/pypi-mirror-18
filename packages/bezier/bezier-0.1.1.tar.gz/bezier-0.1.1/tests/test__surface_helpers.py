# See the License for the specific language governing permissions and
# limitations under the License.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import mock
import numpy as np

from tests import utils


class Test_polynomial_sign(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(poly_surface):
        from bezier import _surface_helpers

        return _surface_helpers.polynomial_sign(poly_surface)

    def _helper(self, bernstein, expected):
        import bezier

        poly_surface = bezier.Surface(bernstein)
        result = self._call_function_under_test(poly_surface)
        self.assertEqual(result, expected)

    def test_positive(self):
        # pylint: disable=no-member
        bernstein = np.array([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]]).T
        # pylint: enable=no-member
        self._helper(bernstein, 1)

    def test_negative(self):
        # pylint: disable=no-member
        bernstein = np.array([[-1.0, -2.0, -1.0]]).T
        # pylint: enable=no-member
        self._helper(bernstein, -1)

    def test_zero(self):
        bernstein = np.zeros((10, 1))
        self._helper(bernstein, 0)

    def test_mixed(self):
        # pylint: disable=no-member
        bernstein = np.array([[-1.0, 1.0, -1.0]]).T
        # pylint: enable=no-member
        self._helper(bernstein, 0)

    def test_max_iterations(self):
        # pylint: disable=no-member
        bernstein = np.array([[1.0, 2.0, 3.0]]).T
        # pylint: enable=no-member
        with mock.patch('bezier._surface_helpers.MAX_SUBDIVISIONS', new=1):
            self._helper(bernstein, 1)

    def test_no_conclusion(self):
        # pylint: disable=no-member
        bernstein = np.array([[-1.0, 1.0, 2.0]]).T
        # pylint: enable=no-member
        with mock.patch('bezier._surface_helpers.MAX_SUBDIVISIONS', new=0):
            with self.assertRaises(ValueError):
                self._helper(bernstein, None)


class Test__2x2_det(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(mat):
        from bezier import _surface_helpers

        return _surface_helpers._2x2_det(mat)

    def test_integers(self):
        mat = np.array([
            [1.0, 2.0],
            [3.0, 4.0],
        ])
        self.assertEqual(self._call_function_under_test(mat), -2.0)

    def test_better_than_numpy(self):
        mat = np.array([
            [-24.0, 3.0],
            [-27.0, 0.0],
        ]) / 16.0
        actual_det = self._call_function_under_test(mat)
        self.assertEqual(actual_det, 81.0 / 256.0)

        np_det = np.linalg.det(mat)
        self.assertNotEqual(actual_det, np_det)
        self.assertLess(abs(actual_det - np_det), 1e-16)


class Test_quadratic_jacobian_polynomial(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(nodes):
        from bezier import _surface_helpers

        return _surface_helpers.quadratic_jacobian_polynomial(nodes)

    def test_it(self):
        # B(L1, L2, L3) = [L1^2 + L2^2, L2^2 + L3^2]
        nodes = np.array([
            [1.0, 0.0],
            [0.0, 0.0],
            [1.0, 1.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 1.0],
        ])
        bernstein = self._call_function_under_test(nodes)
        self.assertEqual(bernstein.shape, (6, 1))
        expected = np.array([[0.0, 2.0, 0.0, -2.0, 2.0, 0.0]])
        expected = expected.T  # pylint: disable=no-member
        self.assertTrue(np.all(bernstein == expected))


class Test_cubic_jacobian_polynomial(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(nodes):
        from bezier import _surface_helpers

        return _surface_helpers.cubic_jacobian_polynomial(nodes)

    def test_it(self):
        # B(L1, L2, L3) = [L1^3 + L2^3, L2^3 + L3^3]
        nodes = np.array([
            [1.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [1.0, 1.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 1.0],
        ])
        bernstein = self._call_function_under_test(nodes)
        shape = (15, 1)
        self.assertEqual(bernstein.shape, shape)
        expected = np.zeros(shape)
        expected[2, 0] = 1.5
        expected[9, 0] = -1.5
        expected[11, 0] = 1.5
        self.assertTrue(np.all(bernstein == expected))


class Test_de_casteljau_one_round(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(nodes, degree, lambda1, lambda2, lambda3):
        from bezier import _surface_helpers

        return _surface_helpers.de_casteljau_one_round(
            nodes, degree, lambda1, lambda2, lambda3)

    def test_linear(self):
        nodes = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
        ])
        s_val, t_val = 0.5, 0.375
        expected = np.array([
            [s_val, t_val],
        ])

        result = self._call_function_under_test(
            nodes, 1, 1.0 - s_val - t_val, s_val, t_val)
        self.assertTrue(np.all(result == expected))

    def test_quadratic(self):
        # Use a fixed seed so the test is deterministic and round
        # the nodes to 8 bits of precision to avoid round-off.
        nodes = utils.get_random_nodes(
            shape=(6, 2), seed=97764, num_bits=8)

        p200, p110, p020, p101, p011, p002 = nodes
        s_val = 0.25
        t_val = 0.125

        q100 = (1.0 - s_val - t_val) * p200 + s_val * p110 + t_val * p101
        q010 = (1.0 - s_val - t_val) * p110 + s_val * p020 + t_val * p011
        q001 = (1.0 - s_val - t_val) * p101 + s_val * p011 + t_val * p002

        expected = np.vstack([q100, q010, q001])
        result = self._call_function_under_test(
            nodes, 2, 1.0 - s_val - t_val, s_val, t_val)
        self.assertTrue(np.all(result == expected))

    def test_cubic(self):
        nodes = np.array([
            [0.0, 0.0],
            [3.25, 1.5],
            [6.5, 1.5],
            [10.0, 0.0],
            [1.5, 3.25],
            [5.0, 5.0],
            [10.0, 5.25],
            [1.5, 6.5],
            [5.25, 10.0],
            [0.0, 10.0],
        ])

        s_val = 0.25
        t_val = 0.375
        lambda1 = 1.0 - s_val - t_val
        transform = np.array([
            [lambda1, s_val, 0., 0., t_val, 0., 0., 0., 0., 0.],
            [0., lambda1, s_val, 0., 0., t_val, 0., 0., 0., 0.],
            [0., 0., lambda1, s_val, 0., 0., t_val, 0., 0., 0.],
            [0., 0., 0., 0., lambda1, s_val, 0., t_val, 0., 0.],
            [0., 0., 0., 0., 0., lambda1, s_val, 0., t_val, 0.],
            [0., 0., 0., 0., 0., 0., 0., lambda1, s_val, t_val],
        ])
        # pylint: disable=no-member
        expected = transform.dot(nodes)
        # pylint: enable=no-member
        result = self._call_function_under_test(
            nodes, 3, lambda1, s_val, t_val)
        self.assertTrue(np.all(result == expected))


class Test__make_transform(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(degree, weights_a, weights_b, weights_c):
        from bezier import _surface_helpers

        return _surface_helpers._make_transform(
            degree, weights_a, weights_b, weights_c)

    def _helper(self, degree, weights, expected0, expected1, expected2):
        result = self._call_function_under_test(
            degree, weights[0, :], weights[1, :], weights[2, :])

        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 3)
        self.assertTrue(np.all(result[0] == expected0))
        self.assertTrue(np.all(result[1] == expected1))
        self.assertTrue(np.all(result[2] == expected2))

    def test_linear(self):
        weights = np.array([
            [1.0, 0.0, 0.0],
            [0.5, 0.5, 0.0],
            [0.5, 0.0, 0.5],
        ])
        expected0 = weights[[0], :]
        expected1 = weights[[1], :]
        expected2 = weights[[2], :]
        self._helper(1, weights, expected0, expected1, expected2)

    def test_quadratic(self):
        weights = np.array([
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
        ])
        expected0 = np.array([
            [0.0, 0.5, 0.0, 0.5, 0.0, 0.0],
            [0.0, 0.0, 0.5, 0.0, 0.5, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.5, 0.5],
        ])
        expected1 = np.array([
            [0.5, 0.0, 0.0, 0.5, 0.0, 0.0],
            [0.0, 0.5, 0.0, 0.0, 0.5, 0.0],
            [0.0, 0.0, 0.0, 0.5, 0.0, 0.5],
        ])
        expected2 = np.array([
            [0.5, 0.5, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0],
        ])
        self._helper(2, weights, expected0, expected1, expected2)


class Test__reduced_to_matrix(unittest.TestCase):

    @staticmethod
    def _call_function_under_test(shape, degree, vals_by_weight):
        from bezier import _surface_helpers

        return _surface_helpers._reduced_to_matrix(
            shape, degree, vals_by_weight)

    def test_it(self):
        shape = (6, 2)
        degree = 2

        expected = np.array([
            [1.0, 0.0],
            [-1.0, 1.0],
            [0.0, 1.0],
            [0.0, -1.0],
            [-1.0, -1.0],
            [2.0, 0.0],
        ])
        vals_by_weight = {
            (0, 0): expected[[0], :],
            (0, 1): expected[[1], :],
            (1, 1): expected[[2], :],
            (0, 2): expected[[3], :],
            (1, 2): expected[[4], :],
            (2, 2): expected[[5], :],
        }

        result = self._call_function_under_test(shape, degree, vals_by_weight)
        self.assertTrue(np.all(result == expected))


class Test_specialize_surface(unittest.TestCase):

    WEIGHTS0 = (1.0, 0.0, 0.0)
    WEIGHTS1 = (0.5, 0.5, 0.0)
    WEIGHTS2 = (0.0, 1.0, 0.0)
    WEIGHTS3 = (0.5, 0.0, 0.5)
    WEIGHTS4 = (0.0, 0.5, 0.5)
    WEIGHTS5 = (0.0, 0.0, 1.0)

    @staticmethod
    def _call_function_under_test(nodes, degree,
                                  weights_a, weights_b, weights_c):
        from bezier import _surface_helpers

        return _surface_helpers.specialize_surface(
            nodes, degree, weights_a, weights_b, weights_c)

    def _helpers(self, degree, all_nodes, inds_a, inds_b, inds_c, inds_d):
        num_nodes = len(inds_a)
        id_mat = np.eye(num_nodes)

        expected_a = self._call_function_under_test(
            id_mat, degree,
            self.WEIGHTS0, self.WEIGHTS1, self.WEIGHTS3)
        expected_b = self._call_function_under_test(
            id_mat, degree,
            self.WEIGHTS4, self.WEIGHTS3, self.WEIGHTS1)
        expected_c = self._call_function_under_test(
            id_mat, degree,
            self.WEIGHTS1, self.WEIGHTS2, self.WEIGHTS4)
        expected_d = self._call_function_under_test(
            id_mat, degree,
            self.WEIGHTS3, self.WEIGHTS4, self.WEIGHTS5)

        self.assertTrue(np.all(all_nodes[inds_a, :] == expected_a))
        self.assertTrue(np.all(all_nodes[inds_b, :] == expected_b))
        self.assertTrue(np.all(all_nodes[inds_c, :] == expected_c))
        self.assertTrue(np.all(all_nodes[inds_d, :] == expected_d))

    def test_known_linear(self):
        from bezier import _surface_helpers

        all_nodes = _surface_helpers.LINEAR_SUBDIVIDE
        self._helpers(1, all_nodes,
                      (0, 1, 3), (4, 3, 1),
                      (1, 2, 4), (3, 4, 5))

    def test_known_quadratic(self):
        from bezier import _surface_helpers

        all_nodes = _surface_helpers.QUADRATIC_SUBDIVIDE
        self._helpers(2, all_nodes,
                      (0, 1, 2, 5, 6, 9),
                      (11, 10, 9, 7, 6, 2),
                      (2, 3, 4, 7, 8, 11),
                      (9, 10, 11, 12, 13, 14))

    def test_known_cubic(self):
        from bezier import _surface_helpers

        all_nodes = _surface_helpers.CUBIC_SUBDIVIDE
        self._helpers(3, all_nodes,
                      (0, 1, 2, 3, 7, 8, 9, 13, 14, 18),
                      (21, 20, 19, 18, 16, 15, 14, 10, 9, 3),
                      (3, 4, 5, 6, 10, 11, 12, 16, 17, 21),
                      (18, 19, 20, 21, 22, 23, 24, 25, 26, 27))

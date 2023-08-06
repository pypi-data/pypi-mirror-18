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

"""Private helper methods for B |eacute| zier curves.

.. |eacute| unicode:: U+000E9 .. LATIN SMALL LETTER E WITH ACUTE
   :trim:
"""


import functools

import numpy as np
import six

try:
    import scipy.integrate as _scipy_int
except ImportError:  # pragma: NO COVER
    _scipy_int = None


def make_subdivision_matrix(degree):
    """Make the matrix used to subdivide a curve.

    Args:
        degree (int): The degree of the curve.

    Returns:
        numpy.ndarray: The matrix used to convert the
           nodes into left and right nodes.
    """
    num_rows = 2 * degree + 1
    result = np.zeros((num_rows, degree + 1))
    result[0, 0] = 1.0
    result[-1, -1] = 1.0
    for row in six.moves.xrange(1, degree + 1):
        half_prev = 0.5 * result[row - 1, :row]
        result[row, :row] = half_prev
        result[row, 1:row + 1] += half_prev
        # Populate the complement row as well.
        complement = num_rows - row - 1
        # NOTE: We "should" reverse the results when using
        #       the complement, but they are symmetric so
        #       that would be a waste.
        result[complement, -(row + 1):] = result[row, :row + 1]
    return result


def evaluate_multi(nodes, degree, s_vals):
    r"""Computes multiple points along a curve.

    Does so by computing the Bernstein basis at each value in ``s_vals``
    rather than using the de Casteljau algorithm.

    Args:
        nodes (numpy.ndarray): The nodes defining a curve.
        degree (int): The degree of the curve (assumed to be one less than
            the number of ``nodes``.
        s_vals (numpy.ndarray): Parameters along the curve (as a
            1D array).

    Returns:
        numpy.ndarray: The evaluated points on the curve as a two dimensional
        NumPy array, with the rows corresponding to each ``s``
        value and the columns to the dimension.
    """
    num_vals, = s_vals.shape

    lambda2 = s_vals[:, np.newaxis]
    lambda1 = 1.0 - lambda2

    weights_next = np.zeros((num_vals, degree + 1))
    weights_curr = np.zeros((num_vals, degree + 1))
    weights_curr[:, 0] = 1.0

    # Increase from degree 0 to ``degree``.
    for curr_deg in six.moves.xrange(degree):
        weights_next[:, :curr_deg + 1] = (
            lambda1 * weights_curr[:, :curr_deg + 1])
        weights_next[:, 1:curr_deg + 2] += (
            lambda2 * weights_curr[:, :curr_deg + 1])
        weights_curr, weights_next = weights_next, weights_curr

    return weights_curr.dot(nodes)


def _vec_size(nodes, degree, s_val):
    r"""Compute :math:`\|B(s)\|_2`.

    Args:
        nodes (numpy.ndarray): The nodes defining a curve.
        degree (int): The degree of the curve (assumed to be one less than
            the number of ``nodes``.
        s_val (float): Parameter to compute :math:`B(s)`.

    Returns:
        float: The norm of :math:`B(s)`.
    """
    result_vec = evaluate_multi(nodes, degree, np.array([s_val]))
    return np.linalg.norm(result_vec, ord=2)


def compute_length(nodes, degree):
    r"""Approximately compute the length of a curve.

    .. _QUADPACK: https://en.wikipedia.org/wiki/QUADPACK

    If ``degree`` is :math:`n`, then the Hodograph curve
    :math:`B'(s)` is degree :math:`d = n - 1`. Using this curve, we
    approximate the integral:

    .. math::

       \ell\left(B\right) =
           \int_0^1 \| B'(s) \|_2 \, ds

    using `QUADPACK`_ (via SciPy).

    Args:
        nodes (numpy.ndarray): The nodes defining a curve.
        degree (int): The degree of the curve (assumed to be one less than
            the number of ``nodes``.

    Returns:
        float: The length of the curve.

    Raises:
        OSError: If SciPy is not installed.
    """
    first_deriv = degree * (nodes[1:, :] - nodes[:-1, :])
    if degree == 1:
        return np.linalg.norm(first_deriv, ord=2)

    if _scipy_int is None:
        raise OSError('This function requires SciPy for quadrature.')

    size_func = functools.partial(_vec_size, first_deriv, degree - 1)
    length, _ = _scipy_int.quad(size_func, 0.0, 1.0)
    return length

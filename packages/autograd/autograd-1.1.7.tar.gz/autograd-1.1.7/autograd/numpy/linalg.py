from __future__ import absolute_import
from functools import partial
import numpy.linalg as npla
from .numpy_wrapper import wrap_namespace
from . import numpy_wrapper as anp
from ..core import primitive
from builtins import range

wrap_namespace(npla.__dict__, globals())

# Some formulas are from
# "An extended collection of matrix derivative results
#  for forward and reverse mode algorithmic differentiation"
# by Mike Giles
# https://people.maths.ox.ac.uk/gilesm/files/NA-08-01.pdf

# transpose by swapping last two dimensions
T = lambda x: anp.swapaxes(x, -1, -2)

# add two dimensions to the end of x
add2d = lambda x: anp.array(x)[...,None,None]

det.defgrad(lambda ans, x: lambda g: add2d(g) * add2d(ans) * T(inv(x)))
slogdet.defgrad(lambda ans, x: lambda g: add2d(g[1]) * T(inv(x)))

def make_grad_inv(ans, x):
    dot = anp.dot if ans.ndim == 2 else partial(anp.einsum, '...ij,...jk->...ik')
    return lambda g: -dot(dot(T(ans), g), T(ans))
inv.defgrad(make_grad_inv)

def make_grad_solve(argnum, ans, a, b):
    updim = lambda x: x if x.ndim == a.ndim else x[...,None]
    dot = anp.dot if a.ndim == 2 else partial(anp.einsum, '...ij,...jk->...ik')

    grad_arg0 = lambda g: -dot(updim(solve(T(a), g)), T(updim(ans)))
    grad_arg1 = lambda g: solve(T(a), g)

    return grad_arg0 if argnum == 0 else grad_arg1
solve.defgrads(make_grad_solve, [0, 1])

def make_grad_norm(ans, x, ord=None, axis=None):
    dot = anp.dot if x.ndim == 2 else partial(anp.einsum, '...ij,...jk->...ik')

    def check_implemented():
        matrix_norm = (x.ndim == 2 and axis is None) or isinstance(axis, tuple)

        if matrix_norm:
            if not (ord is None or ord == 'fro' or ord == 'nuc'):
                raise NotImplementedError('Gradient of matrix norm not '
                                          'implemented for ord={}'.format(ord))
        elif not (ord is None or ord > 1):
            raise NotImplementedError('Gradient of norm not '
                                      'implemented for ord={}'.format(ord))

    if axis is None:
        expand = lambda a: a
    elif isinstance(axis, tuple):
        row_axis, col_axis = axis
        if row_axis > col_axis:
            row_axis = row_axis - 1
        expand = lambda a: anp.expand_dims(anp.expand_dims(a,
                                                   row_axis), col_axis)
    else:
        expand = lambda a: anp.expand_dims(a, axis=axis)

    if ord == 'nuc':
        if axis is None:
            roll = lambda a: a
            unroll = lambda a: a
        else:
            row_axis, col_axis = axis
            if row_axis > col_axis:
                row_axis = row_axis - 1
            # Roll matrix axes to the back
            roll = lambda a: anp.rollaxis(anp.rollaxis(a, col_axis, a.ndim),
                                          row_axis, a.ndim-1)
            # Roll matrix axes to their original position
            unroll = lambda a: anp.rollaxis(anp.rollaxis(a, a.ndim-2, row_axis),
                                            a.ndim-1, col_axis)

    def norm_grad(g):
        check_implemented()
        if ord is None or ord == 2 or ord is 'fro':
            return expand(g / ans) * x
        elif ord == 'nuc':
            x_rolled = roll(x)
            u, s, vt = svd(x_rolled, full_matrices=False)
            uvt_rolled = dot(u, vt)
            # Roll the matrix axes back to their correct positions
            uvt = unroll(uvt_rolled)
            g = expand(g)
            return g * uvt
        else:
            # see https://en.wikipedia.org/wiki/Norm_(mathematics)#p-norm
            return expand(g / ans**(ord-1)) * x * anp.abs(x)**(ord-2)
    return norm_grad
norm.defgrad(make_grad_norm)

def make_grad_eigh(ans, x, UPLO='L'):
    """Gradient for eigenvalues and vectors of a symmetric matrix."""
    N = x.shape[-1]
    w, v = ans              # Eigenvalues, eigenvectors.
    dot = anp.dot if x.ndim == 2 else partial(anp.einsum, '...ij,...jk->...ik')
    def eigh_grad(g):
        wg, vg = g          # Gradient w.r.t. eigenvalues, eigenvectors.
        w_repeated = anp.repeat(w[..., anp.newaxis], N, axis=-1)
        off_diag = anp.ones((N, N)) - anp.eye(N)
        F = off_diag / (T(w_repeated) - w_repeated + anp.eye(N))
        return dot(v * wg[..., anp.newaxis, :] + dot(v, F * dot(T(v), vg)), T(v))
    return eigh_grad
eigh.defgrad(make_grad_eigh)

def make_grad_cholesky(L, A):
    # Based on Iain Murray's note http://arxiv.org/abs/1602.07527

    # scipy's dtrtrs wrapper, solve_triangular, doesn't broadcast along leading
    # dimensions, so when A.ndim > 2 we just call a generic LU solve instead of
    # directly using backsubstitution (also, we factor twice...)
    from ..scipy.linalg import solve_triangular
    if anp.ndim(A) == 2:
        solve_trans = partial(solve_triangular, lower=True, trans='T')
    else:
        solve_trans = lambda a, b: solve(T(a), b)

    phi = lambda X: anp.tril(X) / (1. + anp.eye(X.shape[-1]))

    def conjugate_solve(L, X):
        'X -> L^{-T} X L^{-1}'
        return solve_trans(L, T(solve_trans(L, T(X))))

    def cholesky_grad(g):
        S = conjugate_solve(L, phi(anp.einsum('...ki,...kj->...ij', L, g)))
        return (S + T(S)) / 2.

    return cholesky_grad
cholesky.defgrad(make_grad_cholesky)


def make_grad_svd(usv, a, full_matrices=True, compute_uv=True):
    dot = anp.dot if a.ndim == 2 else partial(anp.einsum, '...ij,...jk->...ik')

    if not compute_uv:
        s = usv

        # Need U and V so do the whole svd anyway...
        usv = svd(a, full_matrices=False)
        u = usv[0]
        v = T(usv[2])

        def svd_grad(g):
            return dot(u * g[..., anp.newaxis, :], T(v))

    elif full_matrices:
        def svd_grad(g):
            raise NotImplementedError("Gradient of svd not implemented for "
                                      "full_matrices=True")

    else:
        u = usv[0]
        s = usv[1]
        v = T(usv[2])

        m, n = a.shape[-2:]

        k = anp.min((m, n))
        # broadcastable identity array with shape (1, 1, ..., 1, k, k)
        i = anp.reshape(anp.eye(k), anp.concatenate((anp.ones(a.ndim - 2, dtype=int), (k, k))))

        f = 1 / (s[..., anp.newaxis, :]**2 - s[..., :, anp.newaxis]**2 + i)

        if m < n:
            def svd_grad(g):
                gu = g[0]
                gs = g[1]
                gv = T(g[2])

                utgu = dot(T(u), gu)
                vtgv = dot(T(v), gv)

                i_minus_vvt = (anp.reshape(anp.eye(n), anp.concatenate((anp.ones(a.ndim - 2, dtype=int), (n, n)))) -
                               dot(v, T(v)))

                t1 = (f * (utgu - T(utgu))) * s[..., anp.newaxis, :]
                t1 = t1 + i * gs[..., :, anp.newaxis]
                t1 = t1 + s[..., :, anp.newaxis] * (f * (vtgv - T(vtgv)))

                t1 = dot(dot(u, t1), T(v))

                t1 = t1 + dot(dot(u / s[..., anp.newaxis, :], T(gv)), i_minus_vvt)

                return t1

        elif m == n:
            def svd_grad(g):
                gu = g[0]
                gs = g[1]
                gv = T(g[2])

                utgu = dot(T(u), gu)
                vtgv = dot(T(v), gv)

                t1 = (f * (utgu - T(utgu))) * s[..., anp.newaxis, :]
                t1 = t1 + i * gs[..., :, anp.newaxis]
                t1 = t1 + s[..., :, anp.newaxis] * (f * (vtgv - T(vtgv)))

                t1 = dot(dot(u, t1), T(v))

                return t1

        elif m > n:
            def svd_grad(g):
                gu = g[0]
                gs = g[1]
                gv = T(g[2])

                utgu = dot(T(u), gu)
                vtgv = dot(T(v), gv)

                i_minus_uut = (anp.reshape(anp.eye(m), anp.concatenate((anp.ones(a.ndim - 2, dtype=int), (m, m)))) -
                               dot(u, T(u)))

                t1 = (f * (utgu - T(utgu))) * s[..., anp.newaxis, :]
                t1 = t1 + i * gs[..., :, anp.newaxis]
                t1 = t1 + s[..., :, anp.newaxis] * (f * (vtgv - T(vtgv)))

                t1 = dot(dot(u, t1), T(v))

                t1 = t1 + dot(i_minus_uut, dot(gu, T(v) / s[..., :, anp.newaxis]))

                return t1

    return svd_grad
svd.defgrad(make_grad_svd)

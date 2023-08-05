# Copyright 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.

import unittest
import numpy as np
import tensorflow as tf
from ..operator import operator, gradient, as_tensorflow
from ..expression import position_in, output_like, if_, elif_, else_, exp, logical_and, variable
from ..local import clear_op_cache


@operator()
def clip(arg, threshold1=None, threshold2=None):
    pos = position_in(arg.shape)

    clipped = output_like(arg)
    x = arg[pos]

    with if_(x < threshold1):
        clipped[pos] = threshold1

    with elif_(x > threshold2):
        clipped[pos] = threshold2

    with else_():
        clipped[pos] = x

    return clipped


@gradient(clip)
@operator()
def clip_grad_op(arg, d_arg, threshold1=None, threshold2=None):
    assert arg.tensor_type == d_arg.tensor_type

    pos = position_in(arg.shape)
    g = output_like(arg)

    arg_at_pos = arg[pos]

    with if_(arg_at_pos < threshold1):
        g[pos] = 0
    with elif_(arg_at_pos > threshold2):
        g[pos] = 0
    with else_():
        g[pos] = d_arg[pos]

    return g

@operator()
def func(x, y):
    assert(x.shape == y.shape)
    pos = position_in(x.shape)
    z = output_like(x)

    z[pos] = x[pos] * x[pos] + 3 * y[pos]
    return z


@gradient(func)
@operator()
def func_grad(x, y, dz):
    assert(x.shape == y.shape)
    assert(x.shape == dz.shape)

    pos = position_in(x.shape)
    dx = output_like(x)
    dy = output_like(y)

    dx[pos] = 2.0 * x[pos] * dz[pos]
    dy[pos] = 3.0 * dz[pos]
    return dx, dy

class TestGradients(unittest.TestCase):
    clear_op_cache()

    def test_func_grad(self):
        """
        Define a simple function and its gradient and test against a tensorflow reference
        Z = X^^2 + 3Y
        """
        test_config = tf.ConfigProto(allow_soft_placement=False)
        # Don't perform optimizations for tests so we don't inadvertently run
        # gpu ops on cpu
        test_config.graph_options.optimizer_options.opt_level = -1
        with tf.Session(config=test_config) as s:
            a = tf.constant(np.random.random(10))
            b = tf.constant(np.random.random(10))
            func_ovl = as_tensorflow(func(a, b))
            func_tf = a * a + 3 * b
            grad_above = tf.constant(np.random.random(10))

            func_grad_ovl = tf.gradients(func_ovl, [a, b], grad_ys=grad_above)
            func_grad_tf = tf.gradients(func_tf, [a, b], grad_ys=grad_above)

            func_grad_ovl, func_grad_tf = s.run([func_grad_ovl, func_grad_tf])
            assert np.all(np.equal(func_grad_ovl, func_grad_tf))

    def test_clip_grad(self):
        """
        Define a simple clip function and its gradient and test against a tensorflow reference
        """

        with tf.Session() as s:
            a = tf.constant(np.random.random(10))
            clip_ovl = as_tensorflow(clip(a, threshold1=0.1, threshold2=0.9))
            sum_ovl = tf.reduce_sum(clip_ovl)
            clip_tf = tf.clip_by_value(a, 0.1, 0.9)
            sum_tf = tf.reduce_sum(clip_tf)
            grad_above = np.random.random(1)

            clip_grad_ovl = tf.gradients(sum_ovl, a, grad_ys=grad_above)[0]
            clip_grad_tf = tf.gradients(sum_tf, a, grad_ys=grad_above)[0]

            clip_grad_ovl, clip_grad_tf = s.run([clip_grad_ovl, clip_grad_tf])
            assert np.all(np.equal(clip_grad_ovl, clip_grad_tf))


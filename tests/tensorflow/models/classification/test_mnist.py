import os
import pytest

from typing import Union
import numpy

from neuralmagicML.tensorflow.utils import tf_compat
from neuralmagicML.tensorflow.models import ModelRegistry, mnist_net


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_MODEL_TESTS", False), reason="Skipping model tests",
)
def test_mnist():
    with tf_compat.Graph().as_default() as graph:
        inputs = tf_compat.placeholder(
            tf_compat.float32, [None, 28, 28, 1], name="inputs"
        )
        logits = mnist_net(inputs)

        with tf_compat.Session() as sess:
            sess.run(tf_compat.global_variables_initializer())
            out = sess.run(
                logits, feed_dict={inputs: numpy.random.random((1, 28, 28, 1))}
            )
            assert out.sum() != 0


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_MODEL_TESTS", False), reason="Skipping model tests",
)
@pytest.mark.parametrize(
    "key,pretrained,test_input",
    [
        ("mnistnet", False, True),
        ("mnistnet", True, False),
        ("mnistnet", "base", False),
    ],
)
def test_mnist_registry(key: str, pretrained: Union[bool, str], test_input: bool):
    with tf_compat.Graph().as_default() as graph:
        inputs = tf_compat.placeholder(
            tf_compat.float32, [None, 28, 28, 1], name="inputs"
        )
        logits = ModelRegistry.create(key, inputs)

        with tf_compat.Session() as sess:
            if test_input:
                sess.run(tf_compat.global_variables_initializer())
                out = sess.run(
                    logits, feed_dict={inputs: numpy.random.random((1, 28, 28, 1))}
                )
                assert out.sum() != 0

            if pretrained:
                ModelRegistry.load_pretrained(key, pretrained)

                if test_input:
                    out = sess.run(
                        logits, feed_dict={inputs: numpy.random.random((1, 28, 28, 1))}
                    )
                    assert out.sum() != 0

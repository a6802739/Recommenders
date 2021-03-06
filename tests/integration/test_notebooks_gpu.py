# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import papermill as pm
import pytest
from reco_utils.common.gpu_utils import get_number_gpus
from tests.notebooks_common import OUTPUT_NOTEBOOK, KERNEL_NAME


TOL = 0.5


@pytest.mark.integration
@pytest.mark.gpu
def test_gpu_vm():
    assert get_number_gpus() >= 1


@pytest.mark.integration
@pytest.mark.gpu
@pytest.mark.parametrize(
    "size, epochs, expected_values",
    [
        (
            "1m",
            10,
            {
                "map": 0.024821,
                "ndcg": 0.153396,
                "precision": 0.143046,
                "recall": 0.056590,
            },
        ),
        # ("10m", 5, {"map": 0.024821, "ndcg": 0.153396, "precision": 0.143046, "recall": 0.056590})# takes too long
    ],
)
def test_ncf_integration(notebooks, size, epochs, expected_values):
    notebook_path = notebooks["ncf"]
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(
            TOP_K=10, MOVIELENS_DATA_SIZE=size, EPOCHS=epochs, BATCH_SIZE=512
        ),
    )
    results = pm.read_notebook(OUTPUT_NOTEBOOK).dataframe.set_index("name")["value"]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL)


@pytest.mark.integration
@pytest.mark.gpu
@pytest.mark.parametrize(
    "size, epochs, batch_size, expected_values",
    [
        (
            "100k",
            10,
            512,
            {
                "map": 0.045746,
                "ndcg": 0.3739307,
                "precision": 0.183987,
                "recall": 0.105546,
                "map2": 0.049723,
                "ndcg2": 0.201361,
                "precision2": 0.180276,
                "recall2": 0.103631,
            },
        )
    ],
)
def test_ncf_deep_dive_integration(
    notebooks, size, epochs, batch_size, expected_values
):
    notebook_path = notebooks["ncf_deep_dive"]
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(
            TOP_K=10, MOVIELENS_DATA_SIZE=size, EPOCHS=epochs, BATCH_SIZE=batch_size
        ),
    )
    results = pm.read_notebook(OUTPUT_NOTEBOOK).dataframe.set_index("name")["value"]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL)


@pytest.mark.integration
@pytest.mark.gpu
@pytest.mark.parametrize(
    "size, epochs, expected_values",
    [
        (
            "1m",
            10,
            {
                "map": 0.025739,
                "ndcg": 0.183417,
                "precision": 0.167246,
                "recall": 0.054307,
                "rmse": 0.881267,
                "mae": 0.700747,
                "rsquared": 0.379963,
                "exp_var": 0.382842,
            },
        ),
        # ("10m", 5, ), # it gets an OOM on pred = learner.model.forward(u, m)
    ],
)
def test_fastai_integration(notebooks, size, epochs, expected_values):
    notebook_path = notebooks["fastai"]
    pm.execute_notebook(notebook_path, OUTPUT_NOTEBOOK, kernel_name=KERNEL_NAME)
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(TOP_K=10, MOVIELENS_DATA_SIZE=size, EPOCHS=epochs),
    )
    results = pm.read_notebook(OUTPUT_NOTEBOOK).dataframe.set_index("name")["value"]

    for key, value in expected_values.items():
        assert results[key] == pytest.approx(value, rel=TOL)


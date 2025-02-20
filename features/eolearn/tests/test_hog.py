"""
Credits:
Copyright (c) 2018-2019 Hugo Fournier (Magellium)
Copyright (c) 2017-2022 Matej Aleksandrov, Devis Peressutti, Žiga Lukšič (Sinergise)

This source code is licensed under the MIT license found in the LICENSE
file in the root directory of this source tree.
"""
import copy

from sentinelhub.testing_utils import test_numpy_data

from eolearn.core import FeatureType
from eolearn.features import HOGTask


def test_hog(small_ndvi_eopatch):
    task = HOGTask(
        (FeatureType.DATA, "NDVI", "hog"),
        orientations=9,
        pixels_per_cell=(2, 2),
        cells_per_block=(2, 2),
        visualize=True,
        visualize_feature_name="hog_visu",
    )

    eopatch = copy.deepcopy(small_ndvi_eopatch)
    task.execute(eopatch)

    for feature_name, expected_statistics in [
        ("hog", {"exp_min": 0.0, "exp_max": 0.5567, "exp_mean": 0.09309, "exp_median": 0.0}),
        ("hog_visu", {"exp_min": 0.0, "exp_max": 0.3241, "exp_mean": 0.010537, "exp_median": 0.0}),
    ]:
        test_numpy_data(eopatch.data[feature_name], **expected_statistics, delta=1e-4)

    del eopatch[(FeatureType.DATA, "hog")]
    del eopatch[(FeatureType.DATA, "hog_visu")]
    assert small_ndvi_eopatch == eopatch, "Other features of the EOPatch were affected."

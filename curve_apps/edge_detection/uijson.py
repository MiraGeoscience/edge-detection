#  Copyright (c) 2024 Mira Geoscience Ltd.
#
#  This file is part of edge-detection package.
#
#  All rights reserved.
#

from geoapps_utils.driver.uijson import (
    BaseUIJson,
    ConfigDict,
    DataSelectionForm,
    FloatForm,
    IntegerForm,
    ObjectSelectionForm,
    StringForm,
)


class EdgeUIJson(BaseUIJson):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _name: str = "edge_detection"

    conda_environment: str = "curve_apps"
    run_command: str = "curve_apps.edge_detection.driver"
    title: str = "Edge Detection"

    export_as: StringForm
    line_length: FloatForm
    line_gap: IntegerForm
    objects: ObjectSelectionForm
    data: DataSelectionForm
    out_group: StringForm
    sigma: FloatForm
    threshold: FloatForm
    window_size: IntegerForm

#  Copyright (c) 2024 Mira Geoscience Ltd.
#
#  This file is part of edge-detection package.
#
#  All rights reserved.
#
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).


from __future__ import annotations

from curve_apps import __version__

defaults = {
    "version": __version__,
    "title": "Edge Detection",
    "geoh5": None,
    "objects": None,
    "data": None,
    "sigma": None,
    "window_azimuth": None,
    "export_as": "",
    "ga_group_name": None,
    "generate_sweep": False,
    "run_command": "curve_apps.driver",
    "workspace_geoh5": None,
    "conda_environment": "curve_apps",
    "conda_environment_boolean": False,
}


default_ui_json = {
    "version": __version__,
    "title": "Edge Detection",
    "geoh5": "",
    "workspace_geoh5": "",
    "run_command": "curve_apps.driver",
    "monitoring_directory": "",
    "conda_environment": "curve_apps.edge_detection",
    "conda_environment_boolean": False,
    "objects": {
        "group": "Data Selection",
        "meshType": ["{48f5054a-1c5c-4ca4-9048-80f36dc60a06}"],
        "main": True,
        "label": "Object",
        "value": None,
    },
    "data": {
        "group": "Data Selection",
        "main": True,
        "association": ["Cell"],
        "dataType": "Float",
        "label": "Data",
        "parent": "objects",
        "value": None,
    },
    "line_length": {
        "group": "Parameters",
        "main": True,
        "label": "Line Length",
        "min": 1,
        "max": 100,
        "value": 1,
    },
    "line_gap": {
        "group": "Parameters",
        "main": True,
        "label": "Line Gap",
        "min": 1,
        "max": 100,
        "value": 1,
    },
    "sigma": {
        "group": "Parameters",
        "main": True,
        "label": "Sigma",
        "value": 1.0,
        "min": 0.0,
        "precision": 1,
        "lineEdit": True,
        "max": 10.0,
    },
    "threshold": {
        "group": "Parameters",
        "main": True,
        "label": "Threshold",
        "min": 1,
        "max": 100,
        "precision": 1,
        "lineEdit": True,
        "value": 1.0,
    },
    "window_size": {
        "group": "Parameters",
        "main": True,
        "label": "Window Size",
        "min": 16,
        "max": 512,
        "value": 64,
    },
    "export_as": {
        "main": True,
        "optional": True,
        "enabled": False,
        "label": "Save as",
        "value": "",
        "group": "Python run preferences",
    },
    "out_group": {
        "main": True,
        "optional": True,
        "enabled": False,
        "label": "Group",
        "value": "",
        "group": "Python run preferences",
    },
}
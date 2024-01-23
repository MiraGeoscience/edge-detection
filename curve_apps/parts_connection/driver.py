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

import logging
import sys

import numpy as np
from geoapps_utils.driver.driver import BaseDriver
from geoapps_utils.numerical import find_curves
from geoh5py.groups import ContainerGroup, Group
from geoh5py.objects import Curve, ObjectBase
from geoh5py.ui_json import InputFile
from tqdm import tqdm

from .params import Parameters

logger = logging.getLogger(__name__)


class PartsConnectionDriver(BaseDriver):
    """
    Driver for the edge detection application.

    :param parameters: Application parameters.
    """

    def __init__(self, parameters: Parameters | InputFile):
        if isinstance(parameters, InputFile):
            parameters = Parameters.parse_input(parameters)

        # TODO need to re-type params in base class
        super().__init__(parameters)

    def run(self):
        """
        Driver for Grid2D entity for the automated detection of line features.
        The application relies on the Canny and Hough transforms from the
        Scikit-Image library.
        """
        with self.workspace.open(mode="r+") as workspace:
            parent = None
            if self.params.output.out_group is not None:
                parent = ContainerGroup.create(
                    workspace=workspace,
                    name=self.params.output.ga_group_name,
                )

            logger.info("Begin connecting labels ...")

            vertices, cells, labels = self.get_connections()

            logger.info("Process completed.")

            if cells is None:
                logger.info("No connections found.")
                return

            name = "Parts Connection"
            if self.params.output.export_as is not None:
                name = self.params.output.export_as

            edges = Curve.create(
                workspace=workspace,
                name=name,
                vertices=vertices,
                cells=cells,
                parent=parent,
            )
            if edges is not None:
                if self.params.source.data is not None:
                    edges.add_data(
                        {
                            self.params.source.data.name: {
                                "values": labels,
                                "entity_type": self.params.source.data.entity_type,
                                "association": "VERTEX",
                            }
                        }
                    )

                self.update_monitoring_directory(
                    parent if parent is not None else edges
                )

                logger.info(
                    "Curve object '%s' saved to '%s'.", name, str(workspace.h5file)
                )

    def get_connections(self) -> tuple:
        """
        Find connections between entity parts.

        :params entity: A Curve object with parts.
        :params data: Input referenced data.
        :params detection: Detection parameters.

        :returns : n x 3 array. Vertices of connecting lines.
        :returns : list
            n x 2 float array. Cells of edges.

        """
        max_distance = self.params.detection.max_distance

        if max_distance is None:
            max_distance = np.inf

        path_list = []
        out_labels = np.zeros_like(self.labels).astype("int32")

        for value in tqdm(np.unique(self.labels)):
            if value == 0:
                continue

            ind = np.where(self.labels == value)[0]

            if len(ind) < 2:
                continue

            segments = find_curves(
                self.vertices[ind, :2],
                self.parts[ind],
                self.params.detection.min_edges,
                max_distance,
                self.params.detection.damping,
            )

            if any(segments):
                path_list += ind[np.vstack(segments)].tolist()
                out_labels[ind] = value

        if any(path_list):
            path = np.vstack(path_list)
            uni_ind, inv_ind = np.unique(path.flatten(), return_inverse=True)
            path = uni_ind[inv_ind.reshape((-1, 2))]

            return (
                self.vertices[uni_ind, :],
                path,
                out_labels[uni_ind],
            )

        return self.vertices, None, out_labels

    @property
    def vertices(self) -> np.ndarray:
        """
        Get vertices from entity.
        """
        entity = self.params.source.entity
        if entity.vertices is None:
            raise ValueError("Curve must have vertices to find connections.")

        return entity.vertices

    @property
    def parts(self) -> np.ndarray:
        """
        Get parts from entity or data.
        """
        entity = self.params.source.entity
        if self.params.source.parts is not None:
            return self.params.source.parts.values

        if isinstance(entity, Curve) and entity.parts is not None:
            return entity.parts

        return np.arange(self.vertices.shape[0]).astype("int32")

    @property
    def labels(self) -> np.ndarray:
        """
        Get labels from data.
        """
        data = self.params.source.data
        if data is not None and data.values is not None:
            values = data.values
        else:
            values = np.ones_like(self.parts)

        return values

    @property
    def params(self) -> Parameters:
        """Application parameters."""
        return self._params

    @params.setter
    def params(self, val: Parameters):
        if not isinstance(val, Parameters):
            raise TypeError("Parameters must be of type Parameters.")
        self._params = val

    def add_ui_json(self, entity: ObjectBase | Group):
        """
        Add ui.json file to entity.

        :param entity: Object to add ui.json file to.
        """
        if self.params.input_file is None:
            return

        param_dict = self.params.flatten()
        self.params.input_file.update_ui_values(param_dict)
        file_path = self.params.input_file.write_ui_json()
        entity.add_file(str(file_path))


if __name__ == "__main__":
    file = sys.argv[1]
    ifile = InputFile.read_ui_json(file)

    driver = PartsConnectionDriver(ifile)
    driver.run()

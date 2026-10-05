import os
from typing import Optional
import trimesh as tm
import numpy as np
import plotly.graph_objects as go


class Vis:
    """ """

    def __init__(self):
        pass

    @staticmethod
    def pose(
        trans: np.ndarray,  # (3, )
        rot: np.ndarray,  # (3, 3)
        width: int = 7,
        length: float = 0.2,
    ) -> list:
        """
        Visualize the pose with red, green, blue lines

        Parameters
        ----------
        trans: np.ndarray
            The translation part of the pose with shape (3, )
        rot: np.ndarray
            The rotation part of the pose with shape (3, 3)
        width: int
            The width of the lines
        length: float
            The length of the lines

        Returns
        -------
        A list of plotly objects that can be shown in Vis.show
        """
        result = []
        for i, color in zip(range(3), ["red", "green", "blue"]):
            result += Vis.line(
                trans, trans + rot[:, i] * length, width=width, color=color
            )
        return result

    @staticmethod
    def line(
        p1: np.ndarray,  # (3)
        p2: np.ndarray,  # (3)
        width: int = None,
        color: str = None,
    ) -> list:
        """
        Visualize the line between two points

        Parameters
        ----------
        p1: np.ndarray
            The first point with shape (3, )
        p2: np.ndarray
            The second point with shape (3, )
        width: int
            The width of the lines
        length: float
            The length of the lines

        Returns
        -------
        A list of plotly objects that can be shown in Vis.show
        """
        color = "green" if color is None else color
        width = 1 if width is None else width

        pc = np.stack([p1, p2])
        x, y, z = pc[:, 0], pc[:, 1], pc[:, 2]
        return [
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=dict(width=width, color=color),
            )
        ]

    @staticmethod
    def mesh(
        path: str = None,
        scale: float = 1.0,
        trans: np.ndarray = None,  # (3, )
        rot: np.ndarray = None,  # (3, 3)
        opacity: float = 1.0,
        color: str = "orange",
        vertices: Optional[np.ndarray] = None,  # (n, 3)
        faces: Optional[np.ndarray] = None,  # (m, 3)
    ) -> list:
        """
        Visualize the mesh with given path or given vertices and faces

        Parameters
        ----------
        path: str
            The path of the mesh file
        scale: float
            The scale of the mesh, default to be 1 (not change)
        trans: np.ndarray
            The translation of the mesh with shape (3, )
        rot: np.ndarray
            The rotation of the mesh with shape (3, 3)
        opacity: float
            The opacity of the mesh
        color: str
            The color of the mesh
        vertices: Optional[np.ndarray]
            The vertices of the mesh with shape (n, 3)
        faces: Optional[np.ndarray]
            The faces of the mesh with shape (m, 3)

        Returns
        -------
        A list of plotly objects that can be shown in Vis.show
        """

        trans = np.zeros(3) if trans is None else trans
        rot = np.eye(3) if rot is None else rot

        if path is not None:
            mesh = tm.load(path).apply_scale(scale)
            vertices, faces = mesh.vertices, mesh.faces

        v = np.einsum("ij,kj->ki", rot, vertices * scale) + trans
        f = faces
        mesh_plotly = go.Mesh3d(
            x=v[:, 0],
            y=v[:, 1],
            z=v[:, 2],
            i=f[:, 0],
            j=f[:, 1],
            k=f[:, 2],
            color=color,
            opacity=opacity,
        )
        return [mesh_plotly]

    @staticmethod
    def show(
        plotly_list: list,
        path: Optional[str] = None,
    ) -> None:
        """
        Show the plotly objects or save them to a html file

        Parameters
        ----------
        plotly_list: list
            A list of plotly objects
        path: Optional[str]
            The path to save the html file, if None, show in the browser
        """
        fig = go.Figure(
            data=plotly_list, layout=go.Layout(scene=dict(aspectmode="data"))
        )
        if path is None:
            fig.show()
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            fig.write_html(path)
            print(f"saved in {path}")

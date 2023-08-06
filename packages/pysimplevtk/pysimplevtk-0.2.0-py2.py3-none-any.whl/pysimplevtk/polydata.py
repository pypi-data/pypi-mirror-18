# -*- coding: utf-8 -*-
from xml.etree.ElementTree import Element, SubElement

from numpy import (
    abs, asanyarray, cumsum, dtype, int8, int16, float16, float32, max,
    min_scalar_type)


def generate_polydata(
        points, vertices=None, lines=None, polygons=None, triangle_strips=None,
        point_data=None, cell_data=None):
    points = asanyarray(points)

    if vertices is not None:
        raise NotImplementedError('Adding vertices is not implemented yet.')

    if triangle_strips is not None:
        raise NotImplementedError(
            'Adding triangle strips is not implemented yet.')

    if cell_data is not None:
        raise NotImplementedError('Adding cell_data is not implemented yet.')

    if vertices is None:
        vertices = []

    if lines is None:
        lines = []

    if polygons is None:
        polygons = []

    if triangle_strips is None:
        triangle_strips = []

    if point_data is None:
        point_data = {}

    if cell_data is None:
        cell_data = {}

    root = Element(
        'VTKFile',
        attrib={
            'type': 'PolyData',
            'version': '0.1',
            'byte_order': 'LittleEndian'
        })
    polydata = SubElement(
        root,
        'PolyData')
    piece = SubElement(
        polydata,
        'Piece',
        attrib={
            'NumberOfPoints': str(len(points)),
            'NumberOfVerts': str(len(vertices)),
            'NumberOfLines': str(len(lines)),
            'NumberOfStrips': str(len(triangle_strips)),
            'NumberOfPolys': str(len(polygons))
        })

    # Points
    # ======
    points_dtype = min_scalar_type(-max(abs(points))-1)
    # Some datatypes are not supported by vtk and are hence mapped to the
    # closest supported datatype
    if points_dtype == int8:
        points_dtype = dtype(int16)
    elif points_dtype == float16:
        points_dtype = dtype(float32)

    points_element = SubElement(piece, 'Points')
    points_data_array = SubElement(
        points_element, 'DataArray',
        {'NumberOfComponents': str(points.shape[1]),
         'format': 'ascii',
         'type': points_dtype.name.capitalize()})
    points_data_array.text = ' '.join(
        ' '.join(str(coord) for coord in point) for point in points)

    # Lines
    # =====
    if lines:
        lines_element = SubElement(piece, 'Lines')

        # Connectivity
        lines_connectivity = SubElement(
            lines_element,
            'DataArray',
            {
                'Name': 'connectivity',
                'format': 'ascii',
                'type': 'Int32'
            })
        lines_connectivity.text = ' '.join(
            ' '.join(str(i) for i in connectivity) for connectivity in lines)

        # Offsets
        lines_offsets = SubElement(
            lines_element,
            'DataArray',
            {
                'Name': 'offsets',
                'format': 'ascii',
                'type': 'Int32'
            })
        lines_offsets.text = ' '.join(
            str(i) for i in cumsum([len(conn) for conn in lines]))

    # Polygons
    # ========
    if polygons:
        polygons_element = SubElement(piece, 'Polys')

        # Connectivity
        polygons_connectivity = SubElement(
            polygons_element,
            'DataArray',
            {
                'Name': 'connectivity',
                'format': 'ascii',
                'type': 'Int32'
            })
        polygons_connectivity.text = ' '.join(
            ' '.join(
                str(i) for i in connectivity) for connectivity in polygons)

        # Offsets
        polygons_offsets = SubElement(
            polygons_element,
            'DataArray',
            {
                'Name': 'offsets',
                'format': 'ascii',
                'type': 'Int32'
            })
        polygons_offsets.text = ' '.join(
            str(i) for i in cumsum([len(conn) for conn in polygons]))

    # Point Data
    # ==========
    if point_data:
        p_data = SubElement(piece, 'PointData')
        for name, data in point_data.items():
            data_array = SubElement(
                p_data,
                'DataArray',
                attrib={
                    'type': data.dtype.name.capitalize(),
                    'Name': name,
                    'format': 'ascii'
                }
            )

            data_array.text = ' '.join(str(i) for i in data)

    # Cell Data
    # =========
    if cell_data:
        c_data = SubElement(piece, 'CellData')
        for name, data in cell_data.items():
            data_array = SubElement(
                c_data,
                'DataArray',
                attrib={
                    'type': data.dtype.name.capitalize(),
                    'Name': name,
                    'format': 'ascii'
                }
            )

            data_array.text = ' '.join(str(i) for i in data)

    return root

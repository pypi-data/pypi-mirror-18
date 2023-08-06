# -*- coding: utf-8 -*-
from xml.etree.ElementTree import Element, SubElement

import numpy as np


def array_to_rectilinear_grid(coordinates, cell_data=None):
    if cell_data is None:
        cell_data = {}

    try:
        x = np.asanyarray(coordinates[0])
    except IndexError:
        x = np.array([0])

    try:
        y = np.asanyarray(coordinates[1])
    except IndexError:
        y = np.array([0])

    try:
        z = np.asanyarray(coordinates[2])
    except IndexError:
        z = np.array([0])

    root = Element(
        'VTKFile',
        attrib={
            'type': 'RectilinearGrid',
            'version': '0.1',
            'byte_order': 'LittleEndian'
        })
    rectilinear_grid = SubElement(
        root,
        'RectilinearGrid',
        attrib={
            'WholeExtent': ' '.join(
                str(i) for i in [0, x.size-1, 0, y.size-1, 0, z.size-1])
        })
    piece = SubElement(
        rectilinear_grid,
        'Piece',
        attrib={
            'Extent': ' '.join(
                str(i) for i in [0, x.size-1, 0, y.size-1, 0, z.size-1])
        })

    # Coordinates
    coordinates = SubElement(piece, 'Coordinates')
    for c in [x, y, z]:
        coords = SubElement(
            coordinates,
            'DataArray',
            attrib={
                'type': c.dtype.name.capitalize(),
                'format': 'ascii'
            })
        if c.size > 1:
            coords.set('RangeMin', str(c[0]))
            coords.set('RangeMax', str(c[-1]))
        coords.text = ' '.join(str(i) for i in c)

    # Cell data
    c_data = SubElement(piece, 'CellData')
    for name, data in cell_data.items():
        # VTK works with the fortran layout
        # print(data.flags['F_CONTIGUOUS'])
        # d = np.asfortranarray(data)
        # print(d.flags['F_CONTIGUOUS'])

        data_array = SubElement(
            c_data,
            'DataArray',
            attrib={
                'type': data.dtype.name.capitalize(),
                'Name': name,
                'format': 'ascii'
            }
        )

        data_array.text = ' '.join(str(i) for i in data.ravel(order='F'))

    return root

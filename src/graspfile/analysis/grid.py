import numpy as np
import numpy.ma as ma


def find_peak(field, comp=0, max_radius=None, min_radius=None):
    """Find the peak magnitude of a component in the field.

    Parameters:
        field ``GraspField``: The field to work on.
        comp int: The field component to look at.
        max_radius float: Ignore portions of the grid outside this radius from the center of the field.
        min_radius float: Ignore portions of the grid inside this radius from the center fo the field.

    Returns:
        x_peak float:, y_peak float: The x and y values of the peak value."""
    x_vals, y_vals = field.get_grid_pos()

    f = abs(field.field[:, :, comp])
    if max_radius is not None:
        rad = field.get_grid_radius()
        rad_max_mask = ma.masked_greater(rad, max_radius)
        f = ma.array(f, mask=rad_max_mask.mask)

    if min_radius is not None:
        rad = field.get_grid_radius()
        rad_min_mask = ma.masked_less(rad, min_radius)
        f = ma.array(f, mask=rad_min_mask.mask)

    ny, nx = np.unravel_index(np.argmax(abs(f)), f.shape)
    x_peak = x_vals[nx]
    y_peak = y_vals[ny]

    return x_peak, y_peak


# find the center of illumination of the field
def find_center(field, comp=0, trunc_level=0.0, max_radius=None, min_radius=None):
    """Find the center of illumination by finding the "center of mass" of the field.

    Parameters:
        field ``GraspField``: The field to work on.
        comp int: The field component to look at.
        trunc_level float: Ignore the contributions from portions of the grid below this field level.
        max_radius float: Ignore portions of the grid outside this radius from the center of the field.
        min_radius float: Ignore portions of the grid inside this radius from the center fo the field.

    Returns:
        x_cent float, y_cent float: The x and y values of the center of the field."""
    xv, yv = field.get_grid_mesh()

    f = abs(field.field[:, :, comp])
    if trunc_level != 0.0:
        f = ma.masked_less_equal(f, trunc_level)
        xv = ma.array(xv, mask=f.mask)
        yv = ma.array(yv, mask=f.mask)

    if max_radius is not None:
        rad = field.get_grid_radius()
        rad_max_mask = ma.masked_greater(rad, max_radius)
        f = ma.array(f, mask=rad_max_mask.mask)
        xv = ma.array(xv, mask=rad_max_mask.mask)
        yv = ma.array(yv, mask=rad_max_mask.mask)

    if min_radius is not None:
        rad = field.get_grid_radius()
        rad_min_mask = ma.masked_less(rad, min_radius)
        f = ma.array(f, mask=rad_min_mask.mask)
        xv = ma.array(xv, mask=rad_min_mask.mask)
        yv = ma.array(yv, mask=rad_min_mask.mask)

    x_illum = xv * f
    y_illum = yv * f

    norm = np.sum(f)

    x_cent = np.sum(x_illum) / norm
    y_cent = np.sum(y_illum) / norm

    return x_cent, y_cent
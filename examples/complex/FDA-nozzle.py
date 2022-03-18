import sys

sys.path.append("/local/home/moravec/bin/classy_examples")

from classy_blocks.classes.mesh import Mesh
from classy_blocks.classes.operations import Face
from classy_blocks.classes.shapes import Cylinder, Frustum, RevolvedRing

def get_mesh():
    # A nozzle with a chamber that produces self-induced oscillations.
    # See helmholtz_nozzle.svg for geometry explanation.

    # geometry data (all dimensions in meters):
    # inlet pipe
    r_inlet = 6e-3
    l_inlet = 100e-3

    # nozzle
    r_nozzle = 2e-3
    l_nozzle = 22.685e-3

    #middle cylinder
    l_middle = 40e-3

    # outlet cylinder
    l_chamber_inner = 100e-3


    # number of cells:
    n_cells_radial = 5
    outer_cell_size = 3e-4
    c2c_expansion = 1.05
    c2c_expansion_ax = 1.01
    cell_homogenity_factor = 3
    cell_ratio = 3 # ratio between axial (flow-aligned) and radial cell size

    inner_cell_size = outer_cell_size * c2c_expansion**n_cells_radial
    axial_cell_size = outer_cell_size*cell_ratio

    mesh = Mesh()

    # inlet
    x_start = 0
    x_end = l_inlet
    inlet = Cylinder([x_start, 0, 0], [x_end, 0, 0], [0, 0, r_inlet])
    inlet.chop_radial(start_size=outer_cell_size, end_size=inner_cell_size)
    inlet.chop_axial(c2c_expansion=1/c2c_expansion_ax, end_size=outer_cell_size)
    inlet.chop_tangential(start_size=inner_cell_size)

    inlet.set_bottom_patch('inlet')
    inlet.set_outer_patch('walls')
    mesh.add(inlet)

    # nozzle
    x_start = x_end
    x_end += l_nozzle
    nozzle = Frustum([x_start, 0, 0], [x_end, 0, 0], [x_start, 0, r_inlet], r_nozzle)
    # the interesting part is the sharp edge: make cells denser here;
    # since we need the requested cell size at the end of the block, just use a negative size
    nozzle.chop_axial(start_size=outer_cell_size, end_size=outer_cell_size)
    nozzle.set_outer_patch('walls')
    mesh.add(nozzle)

    # middle part 
    x_start = x_end
    x_end = x_end + l_middle
    outlet = Cylinder([x_start, 0, 0], [x_end, 0, 0], [x_start, 0, r_nozzle])
    outlet.chop_axial(start_size=outer_cell_size, end_size=outer_cell_size/cell_homogenity_factor) 
    #outlet.chop_axial(length_ratio = 0.5, end_size=outer_cell_size/cell_homogenity_factor, c2c_expansion=1/1.01)
    outlet.set_outer_patch('walls')
    mesh.add(outlet)

    # chamber: inner cylinder
    x_start = x_end
    x_end = x_end + l_chamber_inner
    chamber_inner = Cylinder([x_start, 0, 0], [x_end, 0, 0], [x_start, 0, r_nozzle])
    # create smaller cells at inlet and outlet but leave them bigger in the middle;
    chamber_inner.chop_axial(start_size=outer_cell_size/cell_homogenity_factor, c2c_expansion=c2c_expansion_ax)
    #chamber_inner.chop_axial(length_ratio=0.5, start_size=axial_cell_size, end_size=outer_cell_size)
    #outlet.set_top_patch('outlet-iner')
    mesh.add(chamber_inner)

    # chamber outer: ring
    ring_face = Face([
        [x_start, r_nozzle, 0],
        [x_end, r_nozzle, 0],
        [x_end, r_inlet, 0],
        [x_start, r_inlet, 0]
    ])
    chamber_outer = RevolvedRing([x_start, 0, 0], [x_end, 0, 0], ring_face)
    chamber_outer.chop_radial(length_ratio=0.5, start_size=outer_cell_size/cell_homogenity_factor, c2c_expansion=c2c_expansion)
    chamber_outer.chop_radial(length_ratio=0.5, end_size=outer_cell_size/cell_homogenity_factor, c2c_expansion=1/c2c_expansion)
    chamber_outer.set_bottom_patch('walls')
    #chamber_outer.set_top_patch('wall')
    chamber_outer.set_outer_patch('walls')
    #outlet.set_top_patch('outlet-outer')
    mesh.add(chamber_outer)



    return mesh
    
mesh = get_mesh()

mesh.set_default_patch('outlet', 'patch')
mesh.write("./system/blockMeshDict")

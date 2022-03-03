import os

from classy_blocks.classes.mesh import Mesh
from classy_blocks.classes.shapes import Frustum, Cylinder

bl_thickness = 0.01
core_size = 0.1

class nozzleFda:
    def __init__(self):
        self.mesh = Mesh()

        self.radius = [6, 2]
        self.z = [0, 50, 72.685, 112.2685, 200]
        z = self.z
        radius = self.radius

        self.create_cylinder(z[0], z[1], radius[0], 'cylinder1-master', 'inlet')
        self.create_nozzle('nozzle-master', 'cylinder1-slave')
        self.create_cylinder(z[2], z[3], radius[1], 'cylinder2-master', 'nozzle-slave')
        self.create_cylinder(z[3], z[4], radius[0], 'outlet', 'cylinder2-slave')

        self.mesh.merge_patches('cylinder1-master', 'cylinder1-slave')
        self.mesh.merge_patches('nozzle-master', 'nozzle-slave')
        self.mesh.merge_patches('cylinder2-master', 'cylinder2-slave')



    def create_cylinder(self, z1, z2, r, patch_top, patch_bottom):

        axis_pt1 = [0, 0, z1]
        axis_pt2 = [0, 0, z2]
        radius_pt1 =[0, r, z1]

        cylinder = Cylinder(axis_pt1, axis_pt2, radius_pt1)

        cylinder.set_bottom_patch(patch_bottom)
        cylinder.set_top_patch(patch_top)

        cylinder.chop_axial(count=30)
        cylinder.chop_radial(start_size=bl_thickness, end_size=core_size)
        cylinder.chop_tangential(start_size=core_size)

        self.mesh.add(cylinder)

    def create_nozzle(self, patch_top, patch_bottom):
        z1 = self.z[1]
        z2 = self.z[2]
        r1 = self.radius[0]
        r2 = self.radius[1]

        axis_pt1 = [0, 0, z1]
        axis_pt2 = [0, 0, z2]
        radius_pt1 =[0, r1, z1]

        nozzle = Frustum(axis_pt1, axis_pt2, radius_pt1, r2)

        nozzle.set_bottom_patch(patch_bottom)
        nozzle.set_top_patch(patch_top)

        nozzle.chop_axial(count=30)
        nozzle.chop_radial(start_size=bl_thickness, end_size=core_size)
        nozzle.chop_tangential(start_size=core_size)

        self.mesh.add(nozzle)


nozzleMesh = nozzleFda()
nozzleMesh.mesh.set_default_patch('walls', 'wall')
nozzleMesh.mesh.write("../david-7/run/doktorat/nozzle-fda-mesh/system/blockMeshDict")

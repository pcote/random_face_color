# random_face_color.py (c) 2011 Phil Cote (cotejrp1)
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****
bl_info = {
    'name': 'Random Face Color',
    'author': 'Phil Cote, cotejrp1, (http://www.blenderaddons.com)',
    'version': (0,3),
    "blender": (2, 5, 9),
    "api": 39307,
    'location': '',
    'description': 'Generate random diffuse faces on each face of a mesh',
    'warning': 'Don\'t use on meshes that have a large number of faces.',
    'category': 'Add Material'}

"""
How to use:
- Select a material with no more than one material on it.
- Hit "t" to open the toolbar.
- Under "Random Mat Panel", hit the "Random Face Materials" button.

Note: as of this revision, it works best on just one object.
It works slightly less well when colorizing multiple scene objects.
"""

import bpy
import time
from random import random, seed

# start simple be just generating random colors
def getRandomColor( gray_scale, color_min, color_max ):
    seed( time.time() )
    
    # if the min and max don't make sense, just ignore it.
    if color_min > color_max:
        color_min, color_max = 0, 1
    
    new_color = lambda : color_min + random() * ( color_max - color_min )
    
    if gray_scale:
        val = new_color()
        green = blue = red = val
    else:
        red = new_color()
        green = new_color()
        blue = new_color()
    
    
    return red, green, blue


def makeMaterials( ob, gray_scale, color_min, color_max ):
    
    for face in ob.data.faces:
        randcolor = getRandomColor( gray_scale, color_min, color_max )
        mat = bpy.data.materials.new( "randmat" )
        mat.diffuse_color = randcolor


def assignMats2Ob( ob ):
    
    mats = bpy.data.materials
    
    # load up the materials into the material slots
    for mat in mats:
        bpy.ops.object.material_slot_add()
        ob.active_material = mat
    
    # tie the loaded up materials o each of the faces
    i=0
    faces = ob.data.faces
    while i < len( faces ):
        faces[i].material_index = i
        i+=1

getUnusedRandoms = lambda : [ x for x in bpy.data.materials 
                   if x.name.startswith( "randmat" ) and x.users == 0 ]


def clearMaterialSlots( ob ):
    while len( ob.material_slots ) > 0:
        bpy.ops.object.material_slot_remove()
         
         
def removeUnusedRandoms():
    unusedRandoms = getUnusedRandoms()
    for mat in unusedRandoms:
        bpy.data.materials.remove( mat )
        
        
class RemoveUnusedRandomOp( bpy.types.Operator ):
    bl_label = "Remove Unused Randoms"
    bl_options = { 'REGISTER'}
    bl_idname = "material.remove_unusedmats"
    
    def execute( self, context ):
        removeUnusedRandoms()
        return {'FINISHED'}

class RandomMatOp( bpy.types.Operator ):
    
    bl_label = "Random Face Materials"
    bl_idname = "material.randommat"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute( self, context ):
        ob = context.active_object
        scn = bpy.context.scene
        
        clearMaterialSlots( ob )
        removeUnusedRandoms()
        makeMaterials( ob, scn.gray_scale, scn.color_min, scn.color_max )
        assignMats2Ob( ob )
        return {'FINISHED'}
    
    @classmethod    
    def poll( self, context ):
        ob = context.active_object
        return ob != None and ob.select
       

class KeyRandomColorOp( bpy.types.Operator ):
    
    bl_idname = "anim.keyrandomcolor"
    bl_label = "unimplemented button"
    bl_description = "Not Yet Implemented"
    
    bl_options = { 'REGISTER', 'UNDO' }
    def execute( self, context ):        
        return { 'FINISHED'}
    
    @classmethod
    def poll( self, context ):
        return False #leaving it false til i'm ready to implement


class RandomMatPanel( bpy.types.Panel ):
    bl_label = "Random Mat Panel"
    bl_region_type = "TOOLS"
    bl_space_type = "VIEW_3D"
    
    def draw( self, context ):
        scn = context.scene
        new_row = self.layout.row
        
        new_row().prop( scn, "gray_scale" )
        new_row().prop( scn, "color_min" )
        new_row().prop( scn, "color_max" )
        new_row().operator( "material.randommat" )
        new_row().operator( "anim.keyrandomcolor" )
        new_row().operator( "material.remove_unusedmats" )
        
        matCount = len( getUnusedRandoms() )
        countLabel = "Unused Random Materials: %d" % matCount
        self.layout.row().label( countLabel )
        
from pdb import set_trace

def register():
    scn_type = bpy.types.Scene
    BoolProperty = bpy.props.BoolProperty
    FloatProperty = bpy.props.FloatProperty
    
    scn_type.gray_scale = BoolProperty( name="Gray Scale", default = False,
                                 description = "Gray scale random materials?")
                               
    scn_type.color_min = FloatProperty( name = "Color Min", default = 0, min=0,
                         max=1, description = "Extreme Min for R, G, and B" )
                         
    scn_type.color_max = FloatProperty( name = "Color Max", default = 1, min=0,
                         max=1, description = "Max Color for R, G, and B" )
    
    
    bpy.utils.register_class( KeyRandomColorOp )
    bpy.utils.register_class( RemoveUnusedRandomOp )
    bpy.utils.register_class( RandomMatOp )
    bpy.utils.register_class( RandomMatPanel )

def unregister():
    bpy.utils.unregister_class( RandomMatPanel )
    bpy.utils.unregister_class( RandomMatOp )
    bpy.utils.unregister_class( RemoveUnusedRandomOp )
    bpy.utils.unregister_class( KeyRandomColorOp )

if __name__ == '__main__':
    register()

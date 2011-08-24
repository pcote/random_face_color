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
    'version': (0,1),
    "blender": (2, 5, 9),
    "api": 39307,
    'location': '',
    'description': 'Generate random diffuse faces on each face of a mesh',
    'warning': 'I do not advise using this on meshes that have a large number of faces.', # used for warning icon and text in addons panel
    'category': 'Add Material'}



import bpy
import time
from random import random, seed

# start simple be just generating random colors

def getRandomColor():
    seed( time.time() )
    red = random()
    green = random()
    blue = random()
    return red, green, blue

def destroyMaterials():
    matlist = bpy.data.materials
    for mat in matlist:
        matlist.remove( mat )

def makeMaterials( ob ):
    for face in ob.data.faces:
        randcolor = getRandomColor()
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


class RandomMatOp( bpy.types.Operator ):
    
    bl_label = "Random Face Materials"
    bl_idname = "material.randommat"
    
    def execute( self, context ):
        ob = context.active_object
        makeMaterials( ob )
        assignMats2Ob( ob )
        return {'FINISHED'}
    
    @classmethod    
    def poll( self, context ):
        ob = context.active_object
        return ob != None and ob.select and len( ob.data.materials ) == 0

class RemoveMatOp( bpy.types.Operator ):
    
    bl_label = "Remove Materials from Object"
    bl_idname = "material.removeobjectmat"
    
    def execute( self, context ):
        ob = context.active_object        
        return {'FINISHED'}

    @classmethod
    def poll( self, context ):
        ob = context.active_object
        return ob and ob.select and len( ob.data.materials ) > 0   
         

class RemoveUnusedMatsOp( bpy.types.Operator ):
    
    bl_idname = "material.removeunusedmats"
    bl_label = "Remove Unused Materials"
    
    def execute( self, context ):
        unusedMats = [ mat for mat in bpy.data.materials if mat.users == 0 ]
        
        for mat in unusedMats:
            bpy.data.materials.remove( mat )
            
        return {'FINISHED'}
    

class RandomMatPanel( bpy.types.Panel ):
    bl_label = "Random Mat Panel"
    bl_region_type = "TOOLS"
    bl_space_type = "VIEW_3D"
    
    def draw( self, context ):
        self.layout.row().operator( "material.randommat" )
        row = self.layout.row()
        
        # unused label display only seems to work right when nothing is selected.
        unusedMats = [ mat for mat in bpy.data.materials if mat.users == 0 ]
        unusedMats = str( len( unusedMats ) )
        labelDisplay = "%s unused materials" % unusedMats
        row.label( text = labelDisplay )
        self.layout.row().operator( "material.removeunusedmats" )
                
        
    
def register():
    bpy.utils.register_class( RemoveUnusedMatsOp )
    bpy.utils.register_class( RandomMatOp )
    bpy.utils.register_class( RandomMatPanel )

def unregister():
    bpy.utils.unregister_class( RemoveUnusedMatsOp )
    bpy.utils.unregister_class( RandomMatPanel )
    bpy.utils.unregister_class( RandomMatOp )


if __name__ == '__main__':
    register()
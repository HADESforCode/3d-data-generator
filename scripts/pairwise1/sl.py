import bpy
import os
import math
import mathutils
import sys
sys.path.append('./scripts/util')
from helper import set_prop_val

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1024 # 1920
bpy.data.scenes['Scene'].render.resolution_y = 768 # 1080
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 300

angles = mathutils.Vector((-20.0, 0.0, 20.0)) * math.pi / 180.0
ndim = 3 # number of angles, 3
nimg = 20 # number of patterns, 20

# name of object
obj_name = ['sphere', 'bottle', 'knight', 'king']
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# input directory of the projection patterns
idir = '%s/blender_proj_script/textures/sl' % rdir
# output directory of rendered images
odir = '%s/pairwise' % rdir
# list of properties
props = ['tex', 'alb', 'spec', 'rough']
# obtain the nodes
nodes = bpy.data.materials['Material'].node_tree.nodes
# set all objects invisible
for iobj in range(0, len(obj_name)):
	bpy.data.objects[obj_name[iobj]].hide_render = True
# config the setup
bpy.data.objects['Point'].hide_render = True
bpy.data.objects['Lamp'].hide_render = False
bpy.data.objects['Plane'].hide_render = True

proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
tex_node = proj_nodes.get('Image Texture')

for iobj in range(1, len(obj_name)):
	bpy.data.objects[obj_name[iobj]].hide_render = False
	for i in range(0, len(props)):
		for j in range(i + 1, len(props)):
			subdir = '%s_%s' % (props[i], props[j])
			set_prop_val(nodes, 0, 0) # Texture
			set_prop_val(nodes, 1, 8) # Albedo
			set_prop_val(nodes, 2, 0) # Specular
			set_prop_val(nodes, 3, 2) # Roughness

			for ind_1 in range(2, 9, 3):
				for ind_2 in range(2, 9, 3):
					set_prop_val(nodes, i, ind_1)
					set_prop_val(nodes, j, ind_2)

					outdir = '%s/%s/sl/%s_%s/%02d%02d' % (odir, obj_name[iobj], props[i], props[j], ind_1, ind_2)

					if not os.path.exists(outdir):
						os.makedirs(outdir)

					for ind_img in range(0, nimg):
						proj_ptn = bpy.data.images.load("%s/sl_v%d.jpg" % (idir, ind_img))
						tex_node.image = proj_ptn
						bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img)
						bpy.ops.render.render(write_still=True)

						proj_ptn = bpy.data.images.load("%s/sl_h%d.jpg" % (idir, ind_img))
						tex_node.image = proj_ptn
						bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img + nimg)
						bpy.ops.render.render(write_still=True)

					for ind_img in range(0, 2):
						proj_ptn = bpy.data.images.load("%s/sl_a%d.jpg" % (idir, 1 - ind_img))
						tex_node.image = proj_ptn
						bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img + 2 * nimg)
						bpy.ops.render.render(write_still=True)
	bpy.data.objects[obj_name[iobj]].hide_render = True
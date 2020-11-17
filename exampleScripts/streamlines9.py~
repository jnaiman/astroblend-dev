import numpy as np
from math import sin,cos,pi
from science import deselect_all, makeMaterial, setMaterial
from scipy import interpolate # need to activate correct yt version and do: pip3.4 install scipy


# what are two positions to make vector -> this will be our line segments
#p1 = [1,1,0]
#p2 = [1,0,0]

#p1 = [1,1,0]
#p2 = [0,0,1]

# each entry is x/y/z pt on line segement
#line_pts = np.array( ([0,0,0],[0,0,1], [1,0,1], [1,1,3]) )

# each entry is r/g/b values for each line segement
#colors = np.array( ([1,0,0], [0,1,0], [0,0,1]) )
#colorindex = np.array( [0,1,2] ) #, 1])

# how many faces for each cylinder?
nfaces = 16

# radius of cylinders (in BU now)?
r_cyl = 0.02

# maybe to add later: emissivities and transpariencies
#------------------------------------------
# streamlines stuff

import yt
from yt.visualization.api import Streamlines
import random

fname = '/Users/jillnaiman1/data/IsolatedGalaxy/galaxy0030/galaxy0030' # home


# now, get stream line
ds = yt.load(fname)

c = np.array([0.5]*3)
N = 10  # number of stream lines
scale = 1.0
pos_dx = np.random.random((N,3))*scale-scale/2.
pos = c+pos_dx

streamlines = Streamlines(ds,pos,'velocity_x', 'velocity_y', 'velocity_z', length=1.0)

streamlines.integrate_through_volume()

# select out 1 stream... for now
stream = streamlines.streamlines[1]
stream = stream[np.all(stream != 0.0, axis=1)] # doen something fancy


# units
stream = stream*ds.length_unit # into cm 
# now, scale down to what we want
stream = stream/yt.units.cm
stream = stream/3.1e18 # pc

# for this case
stream = stream/1e5

x = stream[:,0]
y = stream[:,1]
z = stream[:,2]



# this will eventually be filled by an actual colormap
#  from data taken on the steamline
colors = np.zeros((len(stream),3))
for i in range(0,len(stream)):
    colors[i,0] = random.random() #r
    colors[i,1] = random.random() #g
    colors[i,2] = random.random() #b

max_nvals = 10 # interpolate down to this

# remap to a smaller number of points for simplicity
Nvals = max(max_nvals,floor(len(stream)/20.0)) 
#method='cubic' # or nearest, or linear - cubic takes awhile
method='linear' # or nearest, or linear
xn = np.linspace(x.min(),x.max(),Nvals)

# y(x)
f = interpolate.interp1d(x,y,kind=method)
yn = f(xn)

# z(x)
f = interpolate.interp1d(x,z,kind=method)
zn = f(xn)

# also remap colors
f = interpolate.interp1d(x,colors[:,0],kind=method)
r = f(xn)
f = interpolate.interp1d(x,colors[:,1],kind=method)
g = f(xn)
f = interpolate.interp1d(x,colors[:,2],kind=method)
b = f(xn)

rgb = []
for i in range(0,Nvals):
    rgb.append([r[i],g[i],b[i]])



# put back in a smaller stream
streamn = np.zeros((Nvals,3))

streamn[:,0] = xn
streamn[:,1] = yn
streamn[:,2] = zn




#-----------------------------------------
# fix this
line_pts = streamn
colors = rgb
colorindex = np.zeros(len(rgb))
for i in range(0,len(colorindex)):
    colorindex[i] = i


#------------------------------------------

def rotation_matrix(rotation_angle, u):
    #import numpy as np
    from numpy import matrix
    from math import sin, cos
    # find new x/y/z of face, start & end pts
    st = sin(rotation_angle*pi/180.0)
    ct = cos(rotation_angle*pi/180.0)
    # normalize rotation vector
    u = u/(u[0]**2. + u[1]**2. + u[2]**2.)**0.5
    # for ease of writing
    ux = u[0]
    uy = u[1]
    uz = u[2]
    # return matrix
    mat = matrix( ((ct+ux**2.*(1.-ct),ux*uy*(1.0-ct)-uz*st,ux*uz*(1.-ct)+uy*st),
                   (uy*ux*(1.0-ct)+uz*st,ct+uy**2.0*(1.-ct),uy*uz*(1.-ct)-ux*st),
                   (uz*ux*(1.-ct)-uy*st,uz*uy*(1.-ct)+ux*st,ct+uz**2.*(1-ct))) )
    return mat

#------------------------------------------

vtype = [("x","float"),("y","float"), ("z","float")]
# each line segment is surrounded by a cylinder
#  made up of rectangles, nfaces number of rectangles to be exact
#  each face is defined by 4 verticies which is why we have the *4 there...
#  this might be inefficient... but I think its also the way yt does it...
vertices = np.empty((nfaces*4)*(len(line_pts)-1), dtype=vtype) # stores vertices
vertices[:][:] = 0.0

vnum = 0
for i in range(0,len(line_pts)-1):
    # define the vector of the line segement, origion at the 1st pt
    u1 = [line_pts[i+1][0]-line_pts[i][0],
         line_pts[i+1][1]-line_pts[i][1],
         line_pts[i+1][2]-line_pts[i][2]]
    print(i)
    print(u1)
    # find relations for perpendicular point
    a = 1.0 # these can be anything
    b = 1.0 # these can be anything
    uperp1 = [(u1[1]*a-u1[2]*b), (-u1[0]*a), (u1[0]*b)]
    # calculate rotation angle based on # of faces
    #if i == 0: # for first, calculate all verticles
    if True:
        for j in range(0,nfaces):
            rotation_angle_start = 360.0/nfaces*j
            rotation_angle_end = 360.0/nfaces*(j+1.0)
            # 1st matrix for first vertex
            matrix = rotation_matrix(rotation_angle_start, u1)
            # rotate uperp1 around u1 vector
            rv = np.dot(matrix,uperp1)
            # formatting
            v1 = np.array(rv)
            v1 = v1[0]
            # add to verticies
            # moar formating
            v1[np.abs(v1) < 1e-10] = 0.0
            vertices[:][vnum] = v1/(v1[0]**2.+v1[1]**2.+v1[2]**2)**0.5*r_cyl + line_pts[i]
            vnum += 1
            #
            # 2nd matrix for 2nd vertex
            vertices[:][vnum] = v1/(v1[0]**2.+v1[1]**2.+v1[2]**2)**0.5*r_cyl + line_pts[i+1]
            vnum += 1
            #
            # 4rd matrix for 4rd & 3rd vertex
            matrix = rotation_matrix(rotation_angle_end, u1)
            # rotate uperp1 around u1 vector
            rv = np.dot(matrix,uperp1)
            # formatting
            v1 = np.array(rv)
            v1 = v1[0]
            # add to verticies
            v1[np.abs(v1) < 1e-10] = 0.0
            # 3rd matrix for 3rd vertex
            vertices[:][vnum] = v1/(v1[0]**2.+v1[1]**2.+v1[2]**2)**0.5*r_cyl + line_pts[i+1]
            vnum += 1
            # 4th vertex
            vertices[:][vnum] = v1/(v1[0]**2.+v1[1]**2.+v1[2]**2)**0.5*r_cyl + line_pts[i]
            vnum += 1
    #else: # fill with previous verts for smooth looking things
    #    vertices[:][vnum] = vertices[:][vnum-nfaces*4] # 1 -> 1*16
    #    vertices[:][vnum+3] = vertices[:][vnum-nfaces*4 + 4] # 4 -> 16+4
    #    vertices[:][vnum+3+1] = vertices[:][vnum-nfaces*4 + 4 + 1]
    #    vertices[:][vnum+3*2] = vertices[:][vnum-nfaces*4 + 4*2]
    #    vertices[:][vnum+3*2+1] = vertices[:][vnum-nfaces*4 + 4*2 + 1]
    #    vertices[:][vnum+3*3] = vertices[:][vnum-nfaces*4 + 4*3]
    #    vertices[:][vnum+3*3+1] = vertices[:][vnum-nfaces*4 + 4*3 + 1]
    #    vertices[:][vnum+3*4+1] = vertices[:][vnum-nfaces*4 + 4*3 + 1]



meshname = 'mymesh'
meshlocation = (0,0,0)
plot_index = 0
        
# now, generate mesh... hopefully        
deselect_all()
nftype = [("f1","int"),("f2","int"),("f3","int"),("f4","int")]
#newfaces = np.empty(int(len(vertices)/3.), dtype=nftype) # store sets of face colors
newfaces = np.empty(int(len(vertices)/4.), dtype=nftype)
cc = 0
for i in range(0,int(len(vertices)/4.)):
    newfaces[i] = (cc, cc+1, cc+2, cc+3) 
    cc = cc+4
    
me = bpy.data.meshes.new(meshname+"Mesh")
ob = bpy.data.objects.new(meshname,me)
ob.location = meshlocation   # position object at 3d-cursor
bpy.context.scene.objects.link(ob)                # Link object to scene
# Fill the mesh with verts, edges, faces 
me.from_pydata(vertices.tolist(),[],newfaces.tolist())
me.update(calc_edges=True)    # Update mesh with new data


# materials woop woop!
obj = bpy.data.objects[meshname]
bpy.context.scene.objects.active=obj
for i in range(0,len(colors)):
    mat = makeMaterial(meshname+str(i)+'_'+str(plot_index), 
                       (colors[i][0],colors[i][1],colors[i][2]), 
                       (1,1,1), 1.0, 0.0)
    setMaterial(obj,mat)

fnum = 0
for p in range(0,len(line_pts)-1):
    for i in range(0,nfaces):
        me.polygons[fnum].material_index = colorindex[p]
        fnum += 1
        
## now, do individual mat indecies
#for i in range(0,len(newfaces)):
#    me.polygons[i].material_index = colorindex[i]

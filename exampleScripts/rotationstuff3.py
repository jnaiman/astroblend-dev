import numpy as np
from math import sin,cos,pi
from science import deselect_all, makeMaterial, setMaterial

# what are two positions to make vector -> this will be our line segments
#p1 = [1,1,0]
#p2 = [1,0,0]

#p1 = [1,1,0]
#p2 = [0,0,1]

# each entry is x/y/z pt on line segement
line_pts = np.array( ([0,0,0],[0,0,1], [1,0,1], [1,1,3]) )
# each entry is r/g/b values for each line segement
colors = np.array( ([1,0,0], [0,1,0], [0,0,1]) )
colorindex = np.array( [0,1,2] ) 



# each entry is x/y/z pt on line segement
line_pts = np.array( ([0,0,0],[0,0,1]) )
# each entry is r/g/b values for each line segement
colors = np.array( ([1,0,0]) )
colorindex = np.array( [0] ) 



# how many faces for each cylinder?
nfaces = 16

# radius of cylinders (in BU now)?
r_cyl = 0.25

# maybe to add later: emissivities and transpariencies
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

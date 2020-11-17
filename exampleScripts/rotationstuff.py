import numpy as np
from math import sin,cos,pi
from science import deselect_all, makeMaterial, setMaterial

# what are two positions to make vector -> this will be our line segments
#p1 = [1,1,0]
#p2 = [1,0,0]

#p1 = [1,1,0]
#p2 = [0,0,1]

# each entry is x/y/z pt on line segement
#line_pts = np.array( ([1,1,0],[1,2,0]) ) #,[1,2,3]) )
line_pts = np.array( ([0,0,0],[0,0,1]) ) #,[1,2,3]) )

# each entry is r/g/b values for each line segement
colors = np.array( ([1,0,0]) ) #, [0,1,0]) )
colorindex = np.array( [0] ) #, 1])

# how many faces for each cylinder?
nfaces = 4

# radius of cylinders (in BU now)?
r_cyl = 0.5

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
vertices = np.empty((nfaces*4)*len(line_pts), dtype=vtype) # stores vertices


vnum = 0
for i in range(0,len(line_pts)-1):
    # define the vector of the line segement, origion at the 1st pt
    u1 = [line_pts[i+1][0]-line_pts[i][0],
         line_pts[i+1][1]-line_pts[i][1],
         line_pts[i+1][2]-line_pts[i][2]]
    # define the vector of the line segement, origion at the 2nd pt
    u2 = [line_pts[i][0]-line_pts[i+1][0],
         line_pts[i][1]-line_pts[i+1][1],
         line_pts[i][2]-line_pts[i+1][2]]
    # find relations for perpendicular point
    a = 1.0 # these can be anything
    b = 1.0 # these can be anything
    uperp1 = [(u1[1]*a-u1[2]*b), (-u1[0]*a), (u1[0]*b)]
    # find relations for perpendicular point
    a = 1.0 # these can be anything
    b = 1.0 # these can be anything
    uperp2 = [(u2[1]*a-u2[2]*b), (-u2[0]*a), (u2[0]*b)]
    # calculate rotation angle based on # of faces
    for j in range(0,nfaces):
        rotation_angle_start = 360.0/nfaces*(j)
        rotation_angle_end = 360.0/nfaces*(j+1.0)
        # 1st matrix for first vertex
        matrix = rotation_matrix(rotation_angle_start, u1)
        # rotate uperp1 around u1 vector
        rv = np.dot(rotmatrix,uperp1)
        # formatting
        v1 = np.array(rv)
        v1 = v1[0]
        # add to verticies
        vertices[:][vnum] = v1/(v1[0]**2.+v1[1]**2.+v1[2]**2)**0.5*r_cyl
        vnum += 1
        # 2nd vertex
        matrix = rotation_matrix(rotation_angle_start, u2)
        # rotate uperp1 around u1 vector
        rv = np.dot(rotmatrix,uperp2)
        # formatting
        v2 = np.array(rv)
        v2 = v2[0]
        # add to verticies
        vertices[:][vnum] = v2/(v2[0]**2.+v2[1]**2.+v2[2]**2)**0.5*r_cyl
        vnum += 1
        # 3rd matrix for 3rd vertex
        matrix = rotation_matrix(rotation_angle_end, u1)
        # rotate uperp1 around u1 vector
        rv = np.dot(rotmatrix,uperp1)
        # formatting
        v1 = np.array(rv)
        v1 = v1[0]
        # add to verticies
        vertices[:][vnum] = v1/(v1[0]**2.+v1[1]**2.+v1[2]**2)**0.5*r_cyl
        vnum += 1
        # 4th vertex
        matrix = rotation_matrix(rotation_angle_end, u2)
        # rotate uperp1 around u1 vector
        rv = np.dot(rotmatrix,uperp2)
        # formatting
        v2 = np.array(rv)
        v2 = v2[0]
        # add to verticies
        vertices[:][vnum] = v2/(v2[0]**2.+v2[1]**2.+v2[2]**2)**0.5*r_cyl
        vnum += 1




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

    
# now, do individual mat indecies
for i in range(0,len(newfaces)):
    me.polygons[i].material_index = colorindex[i]

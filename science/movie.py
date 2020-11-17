import bpy


class Movies(object):
    def __init__(self, camera, render_directory, render_name, *args, render_type = None, render_steps=10, 
                 object_locations=None, camera_locations = [(0,0,0),(0,0,2)], 
                 camera_pointings=[(0,0,0),(0,0,3)], zoom_factor = 0.0, 
                 bezier_locations = [(0,0,0),(0,0,3)], bezier_pointings = [(0,0,0), (0,0,5)], 
                 bezier_visualize = False, radius_start = 1.0, radius_end = 2.0, theta_start = 40., 
                 theta_end = 0.1, phi_start=40., phi_end = 180., use_current_start_angles = False, 
                 use_current_radius = False, rotate_verbose = True, 
                 scene_name = 'Scene'):
        from render import Render
        import numpy as np
        self.render = Render(render_directory, render_name)
        # see how many are simple objects
        self.simple_objects = []
        for i in range(0,len(args)):
            if (args[i].__class__.__name__ is 'Arrow') or (args[i].__class__.__name__ is 'Sphere') or (args[i].__class__.__name__ is 'Text'):
                self.simple_objects.append(True)
            else:
                self.simple_objects.append(False)
        # first, figure out where objects are gonna go throughout this thing
        if object_locations is None:
            object_locations = [(0,0,0)]
            for i in range(0,len(args)):
                object_locations.append( (0,0,0) )
        # now, figuring out how many render frames we need and how much 
        #   we need to update the evolution of other objects based on this number of frames
        n = render_steps
        # if bezier then make sure we have enough points
        if render_type is 'Bezier':
            if len(bezier_locations) > n:
                print("You gave me too many points for your render steps. Upping the number of render steps")
                n = len(bezier_locations)
            # also, make sure pointings and locations have same number of points
            if len(bezier_locations) is not len(bezier_pointings):
                print("Bezier locations and Bezier pointings need to have the same number of elements!")
        for i in range(0,len(args)):
            # make sure not a simple object
            if self.simple_objects[i] is False:
                if args[i].filelistlength[0] > n:
                    n = args[i].filelistlength[0]
        # now figure out what delta for each object
        #  i.e. how many steps till we update the object's file?
        dn = np.zeros(len(args)) 
        for i in range(0,len(args)):
            if self.simple_objects[i] is False:
                dn[i] = float(n)/args[i].filelistlength[0]
        self.__dn = dn
        self.__render_steps = n
        self.render_steps = n
        self.camera = camera
        self.object_locations = object_locations
        self.camera_locations = camera_locations
        self.camera_pointings = camera_pointings
        self.objects = args
        self.scene_name = scene_name
        self.loaded = 0
        self.zoom_factor = zoom_factor
        self.render_type = render_type
        self.bviz = 0
        if self.render_type is 'Zoom':
            self.zoom_camera(self.zoom_factor)
        elif self.render_type is 'Bezier':
            self.set_camera_bezier(bezier_locations, bezier_pointings, bezier_visualize, self.scene_name)
        elif self.render_type is 'Rotation':
            self.rotate_translate(radius_start, radius_end, theta_start, 
                                  phi_start, theta_end, phi_end, 
                                  use_current_start_angles, use_current_radius, 
                                  rotate_verbose)
        else:
            print("You didn't set the Render type!  I'm not doing a damn thing.")




    @property
    def render_steps(self):
        return self.__render_steps

    @render_steps.setter
    def render_steps(self, render_steps):
        self.__dn = self.__dn*self.__render_steps/render_steps
        self.__render_steps = render_steps

    def zoom_camera(self, zoom_factor=1.0):
        from math import floor, sqrt#, abs
        # floor it 
        #f = min(zoom_factor,0.99) # not 1 since then it will be ontop of pointing
        #f = zoom_factor
        if zoom_factor < 1.0:
            f = zoom_factor
        else:
            f = 0.0 - zoom_factor
        render_steps = self.render_steps
        cam_name = self.camera.name
        a = self.camera.pointing[0] 
        b = self.camera.pointing[1] 
        c = self.camera.pointing[2] 
        x0 = self.camera.location[0]
        y0 = self.camera.location[1]
        z0 = self.camera.location[2]
        r = sqrt((x0-a)**2+(y0-b)**2+(z0-c)**2)
        # rotate where cam is looking
        ifileold = 1
        for i in range(0,render_steps):
            xx = x0 - f*(x0-abs(a))*i/(render_steps-1.)
            yy = y0 - f*(y0-abs(b))*i/(render_steps-1.)
            zz = z0 - f*(z0-abs(c))*i/(render_steps-1.)
            self.camera.location = (xx,yy,zz)#(xx+a,yy+b,zz+c)
            #print(xx)
            #print(yy)
            #print(zz)
            #print(" ")
            # now, loop through each object and set its location
            #   and upload a new file if necessary
            #iframe = i*self.__dn[0]
            for j in range(0,len(self.objects)):
                if self.simple_objects[j] is False:
                    if i > 0: # have already loaded first file
                        if i > ifileold*self.__dn[j]: # are we ready to update the file?
                            ifileold = ifileold + 1
                            self.objects[j].ifile = self.objects[j].ifile+1 # this deletes and reuploads stuff... hopefully
            #if floor(iframe) > iframeold:
            #    iframeold = iframe
            self.render.render()



    # move the camera based on a bunch of bezier curves
    # locs and pts of form [[x,y,z],[x,y,z],[x,y,z]...]
    def set_camera_bezier(self, locs, pts, visualize=False, scene_name='Scene'):
        import mathutils
        import bmesh
        from scienceutils import deselect_all, makeMaterial, setMaterial, delete_object
        from math import floor
        # initialize cam pointing and whatnot
        self.camera.location = locs[0]
        self.camera.pointing = pts[0]
        nf = self.render_steps
        cam_name = self.camera.name
        camloc = []
        campts = []
        n_points_bezier = floor((nf*1.000)/len(locs))
        # first, delete if we have previously visualized
        for obj in bpy.data.objects:
            if ((obj.name.find('bezier') != -1)):
                delete_object(obj.name)
        for i in range(0,len(locs)-1):
            if i is (len(locs)-2):
                nfin = nf - i*n_points_bezier # if non-even #
            else:
                nfin = n_points_bezier
            # locations
            l1 = mathutils.Vector(locs[i])
            l2 = mathutils.Vector(locs[i+1])
            # pointings
            p1 = mathutils.Vector(pts[i])
            p2 = mathutils.Vector(pts[i+1])
            # pointing vectors for bezier tangents
            h1 = mathutils.Vector([l1[0]-p1[0],l1[1]-p1[1],l1[2]-p1[2]])
            h2 = mathutils.Vector([l2[0]-p2[0],l2[1]-p2[1],l2[2]-p2[2]])
            # create curve for cam loc
            curloc = mathutils.geometry.interpolate_bezier(l1,h1,h2,l2,nfin)
            # and one for pointing
            curpts = mathutils.geometry.interpolate_bezier(p1,h1,h2,p2,nfin)
            # add pts to curves for cam loc and cam pointing
            for j in range(0,nfin):
                camloc.append(curloc[j].to_tuple(10))
                campts.append(curpts[j].to_tuple(10))
        # rotate where cam is looking & render
        if not visualize:
            #iframeold = -1
            ifileold = 1
            for i in range(0,self.render_steps):
                self.camera.location = camloc[i]
                self.camera.pointing = campts[i]
                # now, loop through each object and set its location
                #   and upload a new file if necessary
                #iframe = i*self.__dn[0]
                for j in range(0,len(self.objects)):
                    if self.simple_objects[j] is False:
                        if i > 0: # have already loaded first file
                            if i > ifileold*self.__dn[j]: # are we ready to update the file?
                                ifileold = ifileold + 1
                                self.objects[j].ifile = self.objects[j].ifile+1 # this deletes and reuploads stuff... hopefully
                #if floor(iframe) > iframeold:
                #    iframeold = iframe
                self.render.render()
        else: # otherwise, draw points on path
            #plot pts if you want to visualize stuff
            print('locs = ')
            print(camloc)
            print('pts = ')
            print(campts)
            #global bviz ## CHANGE!!!
            deselect_all()
            num = "%04d" % (self.bviz)
            # first, for location curves
            me = bpy.data.meshes.new('bezierCurveLoc'+num)
            ob = bpy.data.objects.new('bezierCurveLoc'+num,me)
            ob.location = (0,0,0)
            bpy.context.scene.objects.link(ob)    # Link object to scene
            coords = [(0,0,0)]
            me.from_pydata(coords,[],[])
            color = (1,0,0) # location pts will be red
            halo_size = 0.1
            mat = makeMaterial('bezierCurveLoc'+num, color, (1,1,1), 1.0, 1.0, 
                               mat_type='HALO', halo_size=halo_size)
            setMaterial(ob,mat) # sets everything to material 0 by default
            ob = bpy.data.objects['bezierCurveLoc'+num] # select right object
            ob.select = True
            bpy.context.scene.objects.active=ob
            bpy.ops.object.mode_set(mode='OBJECT')  # toggle to edit mode                    
            bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
            bm = bmesh.from_edit_mesh(ob.data)
            bm.verts[0].co = camloc[0]
            #print(camloc[i])
            for i in range(1,len(camloc)):
                bm.verts.new(camloc[i])
                #print(camloc[i])
            bmesh.update_edit_mesh(ob.data)
            bpy.ops.object.mode_set(mode='OBJECT')  # toggle to edit mode
            # now, for pointings
            deselect_all()
            me = bpy.data.meshes.new('bezierCurvePts'+num)
            ob = bpy.data.objects.new('bezierCurvePts'+num,me)
            ob.location = (0,0,0)
            bpy.context.scene.objects.link(ob)    # Link object to scene
            coords = [(0,0,0)]
            me.from_pydata(coords,[],[])
            color = (0,0,1) # location pts will be blue
            halo_size = 0.1
            mat = makeMaterial('bezierCurvePts'+num, color, (1,1,1), 1.0, 1.0, 
                               mat_type='HALO', halo_size=halo_size)
            setMaterial(ob,mat) # sets everything to material 0 by default
            ob = bpy.data.objects['bezierCurvePts'+num] # select right object
            ob.select = True
            bpy.context.scene.objects.active=ob
            bpy.ops.object.mode_set(mode='OBJECT')  # toggle to edit mode                    
            bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
            bm = bmesh.from_edit_mesh(ob.data)
            bm.verts[0].co = campts[0] 
            for i in range(1,len(campts)):
                bm.verts.new(campts[i])
            bmesh.update_edit_mesh(ob.data)
            bpy.ops.object.mode_set(mode='OBJECT')  # toggle to edit mode
            self.bviz = self.bviz+1 # update curve counter



    # rotates and changes the radius of rotation, allows for the object to be placed in a fixed location (for now)
    #   and for the object to be made to point some where.  Also, object can be scaled - all files scaled by same amount
    def rotate_translate(self, radius1, radius2, th1, ph1, th2, ph2, use_current_angles=False, 
                         use_current_radius = False, verbose=True):
        from math import degrees, atan2, acos, sqrt, cos, sin, pi, floor
        scene_name = self.scene_name
        camloc = self.camera.location
        campt = self.camera.pointing
        ang_frames = self.render_steps
        cam_name = self.camera.name
        if use_current_radius: # rotate around this radius
            radius1 = sqrt((camloc[0]-campt[0])**2. + (camloc[1]-campt[1])**2. + (camloc[2]-campt[2])**2.)
            #radius2 = radius1
        if use_current_angles: # use the current angle as the start angle
            cx = camloc[0] - campt[0]
            cy = camloc[1] - campt[1]
            cz = camloc[2] - campt[2]
            th1 = degrees(atan2(cy,cx))
            ph1 = degrees(acos(cz/sqrt(cx*cx+cy*cy+cz*cz)))
        scene = bpy.data.scenes[scene_name]
        # get the angle and radius steps
        dth = (th2 - th1)/(ang_frames-1.)
        dph = (ph2 - ph1)/(ang_frames-1.)
        drad = (radius2 - radius1)/(ang_frames-1.0)
        #iframeold = -1
        ifileold = 1
        for i in range(0,self.render_steps):
            radius = radius1+drad*i
            cx = radius*cos((th1+dth*i)*(pi/180.))*sin((ph1+dph*i)*(pi/180.0)) + campt[0]
            cy = radius*sin((th1+dth*i)*(pi/180.))*sin((ph1+dph*i)*(pi/180.0)) + campt[1]
            cz = radius*cos((ph1+dph*i)*(pi/180.0)) + campt[2]
            self.camera.location = (cx,cy,cz)
            # now, loop through each object and set its location
            #   and upload a new file if necessary
            #iframe = i*self.__dn[0]
            for j in range(0,len(self.objects)):
                if self.simple_objects[j] is False:
                    if i > 0: # have already loaded first file
                        if i > ifileold*self.__dn[j]: # are we ready to update the file?
                            ifileold = ifileold + 1
                            self.objects[j].ifile = self.objects[j].ifile+1 # this deletes and reuploads stuff... hopefully
            #if floor(iframe) > iframeold:
            #    iframeold = iframe
            self.render.render()
# COME BACK TO AND USE
#            # move lamp
#            if lamp_motion is 'TRACKING': 
#                rotate_lamp(radius, th1, ph1, th1+dth*r, ph1+dph*r)


   


def import_ytsurface(filename, isosurface_value = 1e-27, surf_type='sphere', radius = 10.0, 
                     radius_units = "mpc", surface_field="density",  
                     meshname = 'Allen',  
                     transparency = 1.0, dist_fac = None,
                     color_field = None, emit_field = None, color_map = "algae", 
                     color_log = True, emit_log = True, plot_index = None, 
                     color_field_max = None, color_field_min = None, 
                     emit_field_max = None, emit_field_min = None, emissivity_units = None,
                     force_override = False):
    
    from yt import load, add_field
    import yt
    import numpy as np
    # both common cases
    #from science import np as np
    #from science import np as numpy
    pf = yt.load(filename)
    emit_field_name = None
    
    #def _Emissivity(field,data):
    #    import numpy as np
    #    return (data['gas','density']*data['gas','density']*np.sqrt(data['gas','temperature']))
#
#    yt.add_field("emissivity", units="g**2*K**0.5/cm**6", function=_Emissivity)


    
    # for only 1 value
    if isinstance(isosurface_value, float):
        isosurface_value = [isosurface_value]
        transparency = [transparency]
        plot_index = 0
    #if surf_type is 'sphere':
    #    presurf = pf.sphere("max", (radius, radius_units)) 
    #else:
    #    print("Waaaahhoooo, don't know anything else!  Am doing spherical surface for the time being")
    #    presurf = pf.sphere("max", (radius, radius_units)) 
    if emit_field is not None:
        if emissivity_units is None:
            emissivity_units = "g**2*K**0.5/cm**6"
            #emissivity_units = 'auto'
        # check if we have a function or a string for the return in a function
        emit_function = emit_field
        #def _Emissivity(field,data):
        #    import numpy as np
        #    return (data['gas','density']*data['gas','density']*np.sqrt(data['gas','temperature']))


        if isinstance(emit_field,str):
            #def _Emissivity(field,data):
            #    import numpy as np
                #(eval("import numpy as np; import numpy; return " + emit_field ))
                #x = (eval(emit_field))
                #return (eval(emit_field))
                #return (eval("data['gas','density']*data['gas','density']*np.sqrt(data['gas','temperature'])"))
            #    return (data['gas','density']*data['gas','density']*np.sqrt(data['gas','temperature']))
            #emit_function = _Emissivity
            print("we are here!")
        #yt.add_field("emissivity", units=emissivity_units, function = emit_function, force_override=force_override)
        #yt.add_field("emissivity", units=emissivity_units, function = _Emissivity, force_override=force_override)
        #pf.add_field("emissivity", units=emissivity_units, function = emit_function, force_override=force_override)
        print("here")
        print(emit_function)
        emit_field_name = ('gas','emissivity') # so far only emissivity for gas...
        #emit_field_name = 'emissivity' # so far only emissivity for gas...
    for i in range(0,len(isosurface_value)):
        #def _Emissivity(field,data):
        #    import numpy as np
        #    return (data['gas','density']*data['gas','density']*np.sqrt(data['gas','temperature']))

        #yt.add_field("emissivity", units="g**2*K**0.5/cm**6", function=_Emissivity)
        #emit_field_name = ('gas','emissivity')

        def _Emissivity(field, data):
            return (eval("data['gas','density']*data['density']*np.sqrt(data['gas','temperature'])"))

        yt.add_field("emissivity", units="g**2*K**0.5/cm**6", function=_Emissivity)


        emit_field_name = ('gas','emissivity')
        
        
        trans = transparency[i]
        dd = pf.h.sphere("max", (radius, radius_units))
        surf = pf.h.surface(dd, surface_field, isosurface_value[i])
        #surf = pf.surface(presurf, surface_field, isosurface_value[i])
        m_name = meshname + '_' + str(i)
        #vertices, colors, alpha, emisses, colorindex = surf.export_blender(transparency = trans, dist_fac = dist_fac,
        #                                                                   color_field = color_field, emit_field = emit_field_name, color_map = color_map, 
        #                                                                   color_log = color_log, emit_log = emit_log, plot_index = i, 
        #                                                                   color_field_max = color_field_max, color_field_min = color_field_min, 
        #                                                                   emit_field_max = emit_field_max, emit_field_min = emit_field_min)


        
        emit_field_name = ('gas','emissivity')
        emit_field_max = None
        emit_field_min = None
        color_field_max = None
        color_field_min = None
        color_map = "algae"

        vertices, colors, alpha, emisses, colorindex = surf.export_blender(transparency = trans, 
                                                                           color_field = color_field, emit_field = emit_field_name, color_map = color_map, 
                                                                           plot_index = 0, 
                                                                           color_field_max = color_field_max, color_field_min = color_field_min, 
                                                                           emit_field_max = emit_field_max, emit_field_min = emit_field_min)


        
        _import_ytsurface(vertices, colors, alpha, emisses, colorindex, m_name, (0,0,0), i)
    return pf





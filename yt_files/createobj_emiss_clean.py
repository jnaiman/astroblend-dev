import yt
import numpy as np
from yt import derived_field


#@derived_field(name="emissivity", units = "g**2*K**0.5/cm**6")
def run_stuff():
    # different data - FLASH
    filename = '~/data/GasSloshing/sloshing_nomag2_hdf5_plt_cnt_0100'
    sphere_rad = 15.0 # in kpc
    #Enzo
    filename = '~/data/IsolatedGalaxy/galaxy0030/galaxy0030'
    sphere_rad = 200.0 # in kpc
    outfile = 'galsurfaces'
    rho = 1e-27 # for each surface
    trans = 1.0 # for transparency of each surface
    color_field = 'temperature' # color your surface by this
    pf = yt.load(filename)
    # emissivity of the material
    # this needs to be a combination of the color_field and surface field
    #def _Emissivity(field, data):
    #    return (eval("data['gas','density']*data['density']*np.sqrt(data['gas','temperature'])"))
    def _Emissivity(field, data):
        return (data['gas','density']*data['density']*np.sqrt(data['gas','temperature']))
    #yt.add_field(("gas","emissivity"), units="g**2*K**0.5/cm**6", function=_Emissivity)
    yt.add_field("emissivity", units="g**2*K**0.5/cm**6", function=_Emissivity, force_override=True)
    # for testing
    #yt.SlicePlot(pf, 'z', "emissivity", width = (200.0, 'kpc')).save('~/Desktop/mytest.png')
    dd = pf.sphere("max", (sphere_rad, "kpc"))
    surf = pf.surface(dd, 'density', rho)
    #surf.export_obj(outfile, transparency = trans, 
    #                color_field=color_field, emit_field = 'emissivity')
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
    return vertices

v = run_stuff()

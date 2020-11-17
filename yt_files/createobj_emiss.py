#from yt.config import ytcfg; ytcfg["yt","serialize"] = "False" # uncomment for parallel
# in parallel run as:  mpirun -np 4 python createobj.py --parallel
from yt.mods import *
import glob as glob
import numpy as np
    

# now, sets of loops
#indirs = "/Volumes/Cynthia/renders/dg_amom3/"  # WORK
#outnames = '/Volumes/Cynthia/yt_surfaces/dg_amom3/files_em1_1e24_idl6_' # WORK
#indirs = "/Users/jillnaiman/yt_files_local/data/dg_strip/" # HOME, where chks are stored
#outnames = "/Users/jillnaiman/yt_files_local/renders/files_em_gs_t_" #HOME, where we are outputting

basn = "cluster_hdf5_plt_cnt_"
ffiles = '[0][4][3][0]'

#rho = [1e-24, 2e-25] # for each surface
#trans = [1.0, 0.5] # for transparency of each surface
rho = [1e-26] # for each surface
trans = [0.5] # for transparency of each surface
distf = 3.1e18*1e3 # kpc, divide distances y this

#cmap = "idl07"
cmap = "jet"
#cmap = "RdBu"
cmap = "gist_stern"
#cmap = "idl06"

color_field = 'Temperature' # color your surface by this
#color_field = 'Density'

# emissivity of the material
# this needs to be a combination of the color_field and surface field
def _Emissivity(field, data):
    return (data['Density']*data['Density']*np.sqrt(data['Temperature']))

add_field("Emissivity", function=_Emissivity, units=r"\rm{g K}/\rm{cm}^{6}")


my_filenames = glob.glob(indirs + basn + ffiles)
my_filenames.sort()


# for using min and max stuff
rho = np.array(rho)

#mincf = 1e15
#maxcf = -1e15
mincf = 4100
maxcf = 2.0e6
maxem = rho.max()**2.0 * maxcf**0.5
minem = rho.min()**2.0 * mincf**0.5
for fname in my_filenames:
    print(fname)
    pf = load(fname)
    dd = pf.h.sphere("max", (5, "kpc"))
    f1 = fname.index(basn)
    filename = outnames + fname[f1:]
    print(filename)

# maybe calculate mins and maxes this way?
#    mincf, maxcf = dd.quantities["Extrema"](color_field)[0]

# maybe this way?
#    surfs = []
#    for r in rho:
#        surfs.append(pf.h.surface(dd, 'Density', r))
#
#    # get min and max
#    for surf in surfs:
#        if surf.vertices is None:
#            cf = surf.get_data(color_field,"face")
#        elif color_field is not None:
#            if color_field not in surf.field_data:
#                cf = surf[color_field]
#        mi, ma = cf.min(), cf.max()
#        if mi < mincf:
#            mincf = mi
#        if ma > maxcf:
#            maxcf = ma

    for i,r in enumerate(rho):
        surf = pf.h.surface(dd, 'Density', r)
        surf.export_obj(filename, transparency = trans[i], dist_fac = distf, 
                        color_field=color_field, emit_field = 'Emissivity', color_map=cmap, 
                        color_log=True, emit_log=True, plot_index = i, color_field_max=maxcf, 
                        color_field_min = mincf, emit_field_max=maxem, emit_field_min=minem)
        

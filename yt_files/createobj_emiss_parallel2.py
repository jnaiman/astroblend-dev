from yt.config import ytcfg; ytcfg["yt","serialize"] = "False" # uncomment for parallel
# in parallel run as:  nice -10 mpirun -np 4 python createobj_emiss_parallel2.py --parallel
from yt.pmods import *  # for parallel
import glob as glob
import numpy as np
    
num_procs = 4



# now, sets of loops
indirs = "/Volumes/Cynthia/renders/dg_amom3/"  # WORK
outnames = '/Volumes/Cynthia/yt_surfaces/dg_amom3/files_em10_' # WORK
#indirs = "/Users/jillnaiman/yt_files_local/data/" # HOME, where chks are stored
#outnames = "/Users/jillnaiman/yt_files_local/renders/files_em_gs_" #HOME, where we are outputting


# to stamp time info
time_file = outnames + 'timestamp.txt'
ftime = open(time_file, "w")
def stamp_time_file(time, ffname):
    print('Stamping time: ' + ffname)
    ftime = open(time_file, "a")
    ftime.write(ffname + ' ' + str(time) + '\n')

basn = "cluster_hdf5_plt_cnt_"
ffiles = '[0][3][0][0]'

rho = [1e-24, 9e-25, 8e-25, 7e-25, 6e-25, 5e-25, 4e-25, 3e-25, 2e-25, 1e-25] # for each surface
#trans = [0.75, 0.5, 0.25] # for transparency of each surface
trans = np.divide(rho,max(rho))

distf = 3.1e18*1e3 # kpc, divide distances y this

color_field = 'Temperature' # color your surface by this
#cmap = "idl07" # a little too white... for now...
cmap = "jet"

# emissivity of the material
# this needs to be a combination of the color_field and surface field
def _Emissivity(field, data):
    return (data['Density']*data['Density']*np.sqrt(data['Temperature']))

add_field("Emissivity", function=_Emissivity, units=r"\rm{g K}/\rm{cm}^{6}")


my_filenames = glob.glob(indirs + basn + ffiles)
my_filenames.sort()


# for using min and max stuff
rho = np.array(rho)

mincf = 1e5
maxcf = 1e6
maxem = rho.max()**2.0 * maxcf**0.5
minem = rho.min()**2.0 * mincf**0.5
for fname in parallel_objects(my_filenames,num_procs):
    pf = load(fname)
    dd = pf.h.sphere("max", (10, "kpc"))
    f1 = fname.index(basn)
    filename = outnames + fname[f1:]

    time = pf.current_time
    only_on_root(stamp_time_file, time, filename)

    for i,r in enumerate(rho):
        surf = pf.h.surface(dd, 'Density', r)
        surf.export_obj(filename, transparency = trans[i], dist_fac = distf, 
                        color_field=color_field, emit_field = 'Emissivity', color_map=cmap, 
                        color_log=True, emit_log=True, plot_index = i, color_field_max=maxcf, 
                        color_field_min = mincf, emit_field_max=maxem, emit_field_min=minem)
        

ftime.close()

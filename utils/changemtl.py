# want to move your mtl and obj files around? Have no fear!

from tempfile import mkstemp
from shutil import move
from os import remove, close
import glob as glob

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file_path)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


# original storage (see top few lines of obj files)
olddir = '/Users/jnaiman/yt_files_old/sim_runs/dg_amom3/'

# new storage
newdir = '/Users/jillnaiman/yt_files_local/yt_surfaces/'

# new location of mtl/obj files (they must be already there) - which files to change?
objfiles = '/Users/jillnaiman/yt_files_local/yt_surfaces/files_em_cluster_hdf5_plt_cnt_[0][1-4][0-9][0-9].obj'

myfiles = glob.glob(objfiles)
myfiles.sort()

for o in myfiles:
    print(o)
    replace(o,olddir,newdir)


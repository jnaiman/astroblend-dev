def myfun(data):
    (exec("import numpy as np; import numpy; return " + str(np.sqrt(data)) ))


def myfun(data):
    import numpy as np
    return(eval(str(np.sqrt(data))))


data['gas','density']*data['gas','density']*np.sqrt(data['gas','temperature'])

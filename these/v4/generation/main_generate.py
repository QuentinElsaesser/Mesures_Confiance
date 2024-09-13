# from v4.generation import experiences as ex
# from v4.generation import brutefrc_exp_para as bfexp
#from v4.generation import priors as pr
# from v4.generation import box_plot, latex
from v4.generation import metrics, plot, plot_bar
from v4.constants import constants

import os, sys
# from copy import deepcopy

def name_directory(directory):
    name = directory
    nbf = 0
    while os.path.exists(name):
        nbf += 1
        name = f"{directory[:-1]}-{nbf}/"
    return name

def name_directory_range(directory):
    directory = directory[:-1] + "_range/"
    name = directory
    nbf = 0
    while os.path.exists(name):
        nbf += 1
        name = f"{directory[:-1]}-{nbf}/"
    return name
    
def generate_plot(name, metric, directory, bar):
    """
    for each metric, read the file with the result and create the png
    """
    directory = name_directory(base_dir)
    print("Start generating Plot")
    for i in range(len(metric.id_methods)):
        ind = metric.n_methods[metric.id_methods[i]]
        if ind in list(constants.ID_METRICS_ACTIVE.values()):
            if bar:
                myplot = plot_bar.PlotBar(name=name, index_m=ind, metric_name=metric.metrics_name[ind], spe=metric.n_methods["Mt"], directory=directory, ranged=False)
            else:
                myplot = plot.Plot(name=name, index_m=ind, metric_name=metric.metrics_name[ind], spe=metric.n_methods["Mt"], directory=directory, ranged=False)
            myplot.plot_all()
        else:
            print("main_generate.py -> IGNORE", metric.metrics_name[ind])
    print("done")
    
def generate_plot_range(name, metric, directory, rl, ru, bar):
    """rl : low range ; ru : high range """
    directory = name_directory_range(base_dir)
    print(f"Start generating Plot with range {rl}% to {ru}%")
    for i in range(len(metric.id_methods)):
        ind = metric.n_methods[metric.id_methods[i]]
        if ind in list(constants.ID_METRICS_ACTIVE.values()):
            if bar:
                myplot = plot_bar.PlotBar(name=name, index_m=ind, metric_name=metric.metrics_name[ind], spe=metric.n_methods["Mt"], directory=directory, ranged=True)
            else:
                myplot = plot.Plot(name=name, index_m=ind, metric_name=metric.metrics_name[ind], spe=metric.n_methods["Mt"], directory=directory, ranged=True)
            if len(myplot.percent) > 0:
                d = myplot.percent.index(str(rl))
                t = myplot.percent.index(str(ru)) + 1
                myplot.plot_all(d=d, t=t)
        else:
            print("main_generate.py -> IGNORE", metric.metrics_name[ind])
    print("done")

if __name__ == "__main__":
    #n="1_1"
    n = sys.argv[1]
    name = f"v4/results/res{n}.tex";base_dir = f"v4/png/res{n}/"
    # directorypng = name_directory(base_dir)
    m = metrics.Metrics(None)
    #rl = 22 ;ru = 57
    bar = False
    FR = False
    rl_ru = []
    for i in range(2, len(sys.argv)):
        if sys.argv[i].lower() == 'fr':
            FR = True
        elif sys.argv[i].lower() == 'bar':
            bar = True
        else:
            rl_ru.append(sys.argv[i])
    
    #python3 -m v4.generation.main_generate 1_26 22 42 bar FR
    
    if len(rl_ru) == 0:
        constants.FR = FR
        constants.PLOT_Y, constants.X_LABEL = constants.PLOT_L(constants.FR)
        
        generate_plot(name=name, metric=m, directory=base_dir, bar=bar)
    else:
        constants.FR = FR
        constants.PLOT_Y, constants.X_LABEL = constants.PLOT_L(constants.FR)
        
        rl = rl_ru[0] ;ru = rl_ru[1]
        
        generate_plot_range(name=name, metric=m, directory=base_dir, rl=rl, ru=ru, bar=bar)
    
    # if len(sys.argv) <= 3:
    #     generate_plot(name=name, metric=m, directory=base_dir, bar=bar)
    # elif len(sys.argv) <= 4:
    #     constants.FR = bool(sys.argv[2])
    #     constants.PLOT_Y, constants.X_LABEL = constants.PLOT_L(constants.FR)
    #     generate_plot(name=name, metric=m, directory=base_dir, bar=bar)
    # elif len(sys.argv) <= 5:
    #     rl = sys.argv[2] ;ru = sys.argv[3]
    #     generate_plot_range(name=name, metric=m, directory=base_dir, rl=rl, ru=ru, bar=bar)
    # elif len(sys.argv) <= 6:
    #     rl = sys.argv[2] ;ru = sys.argv[3]
    #     constants.FR = bool(sys.argv[4])
    #     constants.PLOT_Y, constants.X_LABEL = constants.PLOT_L(constants.FR)
    #     generate_plot_range(name=name, metric=m, directory=base_dir, rl=rl, ru=ru, bar=bar)

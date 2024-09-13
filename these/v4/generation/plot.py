import matplotlib.pyplot as plt

import matplotlib.ticker as ticker

from v4.constants import constants

import re

from v4.generation import plot_max_min

# from v4.vote import normalize as nm

# from v4.generation import BoxPlot as bx

import os

class Plot():
    def __init__(self, name, metric_name, index_m, spe, directory="../png/", ranged=False):
        """
        we generate the plot for the "metric_name" with the data from v4.name
        """
        self.ranged = ranged
        self.name_file_error = name
        self.directory = directory
        # if self.ranged:
        #     self.directory = self.directory[:-1] + "_range/"
        self.metric = metric_name
        self.nb_methods = constants.NB_METHODS
        self.index_m = index_m
        self.res = []
        self.percent = []
        self.options = []
        self.current = 0
        self.distrib = ""
        self.nb_literals = ""
        
        if not os.path.exists(self.directory):
            print(f"creation of {self.directory}")
            os.mkdir(self.directory)
            os.mkdir(self.directory + "ncpr")
            os.mkdir(self.directory + "ncrand")
            os.mkdir(self.directory + "cpr")
        
        self.nvalue = ""
        
        self.spe = spe
        
        #Trust a priori for the sources
        # self.xlabel = constants.X_LABEL
        self.xlabel = constants.X_LABEL
        
        self.ylabel = constants.PLOT_Y
        
        self.ylim = constants.PLOT_YLIM
        
        self.name_file = constants.PLOT_FILE
        
        if constants.FORMULA == constants.RUN_JA:
            if self.index_m == constants.ID_METRICS_PRP["Csh"]:
                tmpp = plot_max_min.PlotMaxMin(metric_name='CSI', name=name, directory=self.directory, ranged=ranged)
                tmpp.plot_all()
            elif self.index_m == constants.ID_METRICS_PRP["Prh"]:
                tmpp = plot_max_min.PlotMaxMin(metric_name='Precision', name=name, directory=self.directory, ranged=ranged)
                tmpp.plot_all()
        
        if self.index_m != self.spe:
            self.file = open(name, "r")
            print(f"Creation of png for {self.metric}")
            
            line = self.file.readline()
            while not "\\title{" in line:
                if "\\newcommand{\\typegeneration}" in line:
                    self.nvalue = line[32:-2]
                    tmpsplit = ""
                    if "-" in self.nvalue:
                        split = self.nvalue.split("_")
                        self.nvalue = split[0]
                        if len(split) > 1:
                            tmpsplit = f"({split[1]}%)"
                    self.xlabel = constants.X_LABEL_SPE(self.xlabel, self.nvalue, tmpsplit, constants.FR)
                    # if self.nvalue == constants.RUN_FCT:
                    #     self.xlabel = "Number of facts" + f"{tmpsplit}"
                    # elif self.nvalue == constants.RUN_SRC:
                    #     self.xlabel = "Number of sources" + f"{tmpsplit}"
                    # elif self.nvalue == constants.RUN_OBJ:
                    #     self.xlabel = "Number of objects" + f"{tmpsplit}"
                if "\\newcommand{\\infograph}" in line:
                    self.infograph = line[27:-2].split(";")
                if "\\newcommand{\\distrib}" in line:
                    self.distrib = line[22:-1].split("-")
                    if len(self.distrib) == 1:
                        self.distrib = ""
                if "\\newcommand{\\nbliterals}" in line:
                    self.nb_literals = line[25:-2]
                line = self.file.readline()
            constants.ORDER = line[7:-2].split(";")
            self.nb_methods = len(constants.ORDER)
            
            self.read_file()
            self.file.close()                  
        
        self.para_plot = []
        
        #recup les para pour le plot selon les methods présentes dans le .tex
        for i in range(len(constants.ORDER)):
            if constants.NAMES[i] in constants.ORDER:
                self.para_plot.append(constants.PARA_PLOT[constants.NAMES.index(constants.ORDER[i])])
        
    def parameters_plot(self, i, j, ind_opt):
        """
        j == 2 : when the option we select is the name of the method
        """
        if not constants.TD_TEST and constants.FORMULA == constants.RUN_TD and self.options[ind_opt][0].startswith('c') and j==2:
            if i == 0:
                return "Pl"
            elif i == 2:
                return "Bo"
        return self.para_plot[i][j]
        
    def title(self, i):
        res = "Graph with "
        if self.nvalue == constants.RUN_FCT:
            res += f"{self.infograph[1]} src - x fct - {self.infograph[0]} obj - {self.nvalue}"
        elif self.nvalue == constants.RUN_SRC:
            res += f"x src - {self.infograph[1]}-{self.infograph[2]} fct - {self.infograph[0]} obj  - {self.nvalue}"
        elif self.nvalue == constants.RUN_OBJ:
            res += f"{self.infograph[0]} src - {self.infograph[1]}-{self.infograph[2]} fct - x obj  - {self.nvalue}"
        else:
            if self.distrib != "":
                tmp = '\n'.join(self.distrib[0:2])
            else:
                if self.nb_literals != "":
                    tmp = f"{self.nb_literals} literals - {self.nvalue}"
                else:
                    tmp = ""
            res += f"{self.infograph[1]} src - {self.infograph[2]}-{self.infograph[3]} fct - {self.infograph[0]} obj - {tmp} - {self.nvalue}"
        return res
        
    def name_png(self, method, nbs, metric):
        """
        """
        nbf = 1
        # add = ""
        # if self.cut:
        #     add = f"_c{nbf}"
        # name = f"{self.directory}{method}/{metric}-{method}{nbs}{add}.png"
        name = f"{self.directory}{method}/{metric}-{method}{nbs}.png"
        while os.path.isfile(name):
            nbf += 1
            # if self.cut:
            #     add = f"_c{nbf}"
            # else:
                # add = f"_{nbf}"
            add = f"_{nbf}"
            name = f"{self.directory}{method}/{metric}-{method}{nbs}{add}.png"
        return name
    
    def get_min_max(self, l, mini, maxi):
        if mini != None and maxi != None:
            tmp = l + [mini, maxi]
            return min(tmp), max(tmp)
        else:
            return min(l), max(l)
    
    def read_file(self):
        """
        stock data (typeg, nbs) for each metric
        """
        line = self.file.readline()
        #Find the good metric
        while (self.metric not in line) or ("\section" not in line):
            line = self.file.readline()
            if "\end{document}" in line:
                raise ValueError(f"END OF FILE : metric {self.metric} isn't in {self.name_file_error}.")
        first = True
        firstg = True
        #Run value for this metric
        while line:
            line = self.file.readline()
            if line.startswith("\subsection"):
                self.current = 0
                if self.nvalue in constants.LIST_RUN_NORMAL+[constants.RUN_BFA]:
                    tmpprc = re.search("\d+-\d+", line)[0].split("-")
                    if self.nvalue == constants.RUN_BFA:
                        self.percent.append(f"{tmpprc[1]}")
                    else:
                        self.percent.append(f"[{tmpprc[0]};{tmpprc[1]}]")
                else:
                    tmpprc = re.search("\d+", line)[0]
                    if self.nvalue in constants.LIST_RUN_SRC+[constants.RUN_FCT]:
                        tmpprc = f"{tmpprc}"
                    else:
                        tmpprc = f"{tmpprc}-{tmpprc}"
                # if tmpprc.isnumeric():
                    self.percent.append(tmpprc)
                # else:
                #     # Fait la moyenne entre les deux percent
                #     t = tmpprc.split("-")
                #     r = 0
                #     for v in t:
                #         r += int(v)
                #     self.percent.append(str(int(r/len(t))))
                first = False or firstg
            elif line.startswith("\graph"):
                firstg = False
                line, typeg, nbs = self.get_s_methd(line)
                val = line.split("&")
                val = [self.to_digit(x, i, len(val)) for i,x in enumerate(val)]
                if first:
                    self.res.append([[] for i in range(self.nb_methods)])
                    for i in range(self.nb_methods):
                        self.res[len(self.options)][i].append(val[i])
                    self.options.append((typeg,nbs))
                else:
                    for i in range(self.nb_methods):
                        self.res[self.current][i].append(val[i])
                    self.current += 1
            elif line.startswith("\section"):
                # print(f"Fin pour {self.metric}")
                break
            
    def plot_all(self, d=0, t=-1, height=20, width=10):
        for i in range(len(self.options)):
            self.plot_one(i=i, d=d, t=t, height=height, width=width)
            
    def plot_all_divide(self, d=0, t=-1, height=20, width=10):
        mid = int((d+t)/2)
        for i in range(len(self.options)):
            self.plot_one(i=i, d=d, t=mid, height=height, width=width)
            self.plot_one(i=i, d=mid, t=t, height=height, width=width)
            
    def condition(self, ind_method, i):
        """
        ind_method : index of the current method (plA, etc)
        i : index of the current option (type graph and nb src)
        
        1st : if metric is about the number of iterations
        2nd : if metric is about the sources
            if it is not our method then False
        """ 
        if constants.ORDER[ind_method] not in constants.PLOT_METHODS:
            return False
        if self.index_m in list(constants.ID_METRICS_SRC.values()):
            if constants.FORMULA == constants.RUN_JA and self.nvalue == constants.RUN_PRP or self.nvalue == constants.RUN_VRN or self.nvalue == constants.RUN_SPR or self.nvalue == constants.RUN_SDR:
                if ind_method > 3:
                    # Si on est sur les methodes pour le JA et que ce n'est pas les methodes SF on affiche pas sur le metriques sources
                    return False
                # if self.options[i][0].startswith('c') and (ind_method == constants.ORDER.index(constants.NAMES[2])):
                #     return False
            if ind_method not in constants.ID_METHODS_SOURCES:
                return False
            if not constants.TD_TEST and constants.FORMULA == constants.RUN_TD and ind_method == constants.ORDER.index(constants.NAMES[5]) and \
                (self.index_m != constants.ID_METRICS_SRC["S"] and self.index_m != constants.ID_METRICS_SRC["SN"]):
                #USums va avoir une trop grosse valeur donc on l'ignore sauf pour le swap
                return False
        else:
            if not constants.TD_TEST and constants.FORMULA == constants.RUN_JA and self.nvalue == constants.RUN_PRP or self.nvalue == constants.RUN_VRN or self.nvalue == constants.RUN_SPR or self.nvalue == constants.RUN_SDR:
                if self.index_m == constants.ID_METRICS_PRP["Mca"] or self.index_m == constants.ID_METRICS_PRP["Mcm"]:
                    if ind_method != constants.ORDER.index(constants.NAMES[0]):
                        return False
                # if self.options[i][0].startswith('c') and ((ind_method == constants.ORDER.index(constants.NAMES[2])) \
                #                                            or (ind_method == constants.ORDER.index(constants.NAMES[11]))):
                #     return False
        if not constants.TD_TEST and constants.FORMULA == constants.RUN_TD and self.options[i][0].startswith('c') and (ind_method == constants.ORDER.index(constants.NAMES[1]) \
                                                   or ind_method == constants.ORDER.index(constants.NAMES[3])):
            # Graphe complet donc pas besoin d'afficher norma A et norma C donc on affiche juste un des deux
            return False
        return True
    
    def myplot(self, ax, x, y, i, j, d=0, t=-1, mini=None, maxi=None, items=0):
        """
        x : percent
        y : values
        i : ind option (type graph and nb src) -> useful when we have more than one line in .tex
        j : ind method
        d : index start (default 0)
        t : index end (default -1)
        mini : minimal value
        maxi : maximal value
        """
        if constants.PLOT_ORDER[j] not in constants.ORDER:
            return mini,maxi,items
        j = constants.ORDER.index(constants.PLOT_ORDER[j])
        
        # if self.nvalue == constants.RUN_BFA:
            # x = 
        
        if self.condition(ind_method=j, i=i):
            if d == 0 and t < 0:
                #default
                if ax != None:
                    ax.plot(x, y[i][j], self.parameters_plot(j,0,i), color=self.parameters_plot(j,1,i), label=self.parameters_plot(j,2,i))
                else:
                    plt.plot(x, y[i][j], self.parameters_plot(j,0,i), color=self.parameters_plot(j,1,i), label=self.parameters_plot(j,2,i))
                m = self.get_min_max(y[i][j], mini, maxi)
                return m[0], m[1], items+1
            elif d > 0 and t < 0:
                #don't start at min value
                if ax != None:
                    ax.plot(x[d:], y[i][j][d:], self.parameters_plot(j,0,i), color=self.parameters_plot(j,1,i), label=self.parameters_plot(j,2,i))
                else:
                    plt.plot(x[d:], y[i][j][d:], self.parameters_plot(j,0,i), color=self.parameters_plot(j,1,i), label=self.parameters_plot(j,2,i))
                m = self.get_min_max(y[i][j][d:], mini, maxi)
                return m[0], m[1], items+1
            else:
                #don't end at max value
                if ax != None:
                    ax.plot(x[d:t], y[i][j][d:t], self.parameters_plot(j,0,i), color=self.parameters_plot(j,1,i), label=self.parameters_plot(j,2,i))
                else:
                    plt.plot(x[d:t], y[i][j][d:t], self.parameters_plot(j,0,i), color=self.parameters_plot(j,1,i), label=self.parameters_plot(j,2,i))
                m = self.get_min_max(y[i][j][d:t], mini, maxi)
                return m[0], m[1], items+1
        return mini, maxi, items
    
    def plot_one(self, i, d=0, t=-1, height=20, width=10):
        """
        Create the plt.plot
        i : index of the options chosen
        d : index start (default 0)
        t : index end (default -1)
        """
        if self.nvalue == constants.RUN_SDR or self.nvalue == constants.RUN_SPR:
            fig, ax = plt.subplots(figsize=(height,width))
            mini, maxi, items = None, None, 0
            for num_met in range(len(constants.PLOT_ORDER)):
                mini,maxi,items = self.myplot(ax=ax, x=[int(n) for n in self.percent], y=self.res, i=i, j=num_met, d=d, t=t, items=items, mini=mini, maxi=maxi)
            ticks_size = 15
            ax.set_title(self.title(i), y=1.1, x=0.5)
            ax.set_xticks([int(n) for n in self.percent])
            ax.tick_params(axis='both', labelsize=ticks_size)
            #size legend
            fontsize = 20
            ax.set_xlabel(self.xlabel, fontsize=fontsize)
            ax.set_ylabel(self.ylabel[self.index_m], fontsize=fontsize)
            #order for the legend
            leg_fontsize = 15
            handles, labels = plt.gca().get_legend_handles_labels()
            ordermet = [i for i in range(items-1,-1,-1)]
            list_met = [m for m in constants.PLOT_ORDER if m in constants.ORDER]
            if len(ordermet) == len(list_met):
                constants.PLOT_INDEX = constants.plot_index_fct(list_met)
                ordermet = constants.PLOT_INDEX
            ax.legend([handles[idx] for idx in ordermet],[labels[idx] for idx in ordermet], fontsize=leg_fontsize)
            yrange = []
            if self.ylim[self.index_m][0] == 'm':
                yrange.append(mini)
            else:
                yrange.append(self.ylim[self.index_m][0])
                
            if self.ylim[self.index_m][1] == 'm':
                yrange.append(maxi+0.1)
            else:
                yrange.append(self.ylim[self.index_m][1])
            ax.set_ylim(yrange)
            # plt.show()
            plt.savefig(self.name_png(self.options[i][0], self.options[i][1], self.name_file[self.index_m]))            
            plt.close()
        else:
            plt.figure(figsize=(height,width))
            mini, maxi, items = None, None, 0
            for num_met in range(len(constants.PLOT_ORDER)):
                mini,maxi,items = self.myplot(ax=None, x=self.percent, y=self.res, i=i, j=num_met, d=d, t=t, items=items, mini=mini, maxi=maxi)
            if maxi != None:
                ticks_size = 15
                plt.title(self.title(i), y=1.1, x=0.5)
                #size axis
                ticks_size = 15
                plt.xticks(fontsize=ticks_size)
                plt.yticks(fontsize=ticks_size)
                #size legend
                fontsize = 20
                plt.xlabel(self.xlabel, fontsize=fontsize)
                plt.ylabel(self.ylabel[self.index_m], fontsize=fontsize)
                leg_fontsize = 15
                plt.legend(fontsize=leg_fontsize)
                #order for the legend
                handles, labels = plt.gca().get_legend_handles_labels()
                ordermet = [i for i in range(items-1,-1,-1)]
                # ordermet = [i for i in range(0,items)]
                list_met = [m for m in constants.PLOT_ORDER if m in constants.ORDER]
                if len(ordermet) == len(list_met):
                    constants.PLOT_INDEX = constants.plot_index_fct(list_met)
                    ordermet = constants.PLOT_INDEX
                plt.legend([handles[idx] for idx in ordermet],[labels[idx] for idx in ordermet], fontsize=leg_fontsize)
                yrange = []
                if self.ylim[self.index_m][0] == 'm':
                    yrange.append(mini)
                else:
                    yrange.append(self.ylim[self.index_m][0])
                    
                if self.ylim[self.index_m][1] == 'm':
                    yrange.append(maxi+0.1)
                else:
                    yrange.append(self.ylim[self.index_m][1])
                plt.ylim(yrange)
            # plt.show()
            plt.savefig(self.name_png(self.options[i][0], self.options[i][1], self.name_file[self.index_m]))
            plt.close()

    def get_s_methd(self, line):
        """
        get met and nbs from v4.\graph{met}{nbs}
        """
        tmp = line.find("}")
        methd = line[7:tmp]
        line = line[tmp+2:]
        tmp = line.find("}")
        nbs = line[:tmp]
        line = line[tmp+3:]
        return line, methd, nbs
    
    def to_digit(self, elt, index, length):
        """
        get a float from v4.\textbf{7.017} or 9.58\\ or 9.58
        
        elts : string
        index : index of the current string 
        length : number of string in the line
        """
        if index+1 >= length:
            elt = elt[:-3]
        if not elt[0].isdigit():
            return float(elt[8:-1])
        return float(elt)    

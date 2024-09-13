import matplotlib.pyplot as plt

from v4.constants import constants

import re

import os

class PlotMaxMin():
    def __init__(self, name, metric_name, directory="../png/", ranged=False):
        """
        we generate the plot for the "metric_name" with the data from v4.name
        """
        self.metric_name = metric_name
        self.ranged = ranged
        self.name_file_error = name
        self.directory = directory
        
        self.nb_methods = constants.NB_METHODS
        self.index_m = 0
        # self.spe = spe
        self.res = []
        self.valueres = []
        self.percent = []
        self.options = []
        self.current = 0
        
        self.directory = self.directory + "min_max/"
        if not os.path.exists(self.directory):
            print(f"creation of {self.directory}")
            os.mkdir(self.directory)
        
        self.nvalue = ""
        self.xlabel = constants.X_LABEL
        self.ylabel = constants.PLOT_Y
        self.ylim = constants.PLOT_YLIM
        self.name_file = constants.PLOT_FILE
        
        self.width_bar = 0.05
        self.placement = []
        self.xplacement = []
        self.curr_placement = 0
        
        self.file = open(name, "r")
        print(f"Creation of png_max_min for {metric_name}")
        
        line = self.file.readline()
        nbc = len(line)
        while not "\\title{" in line:
            if "\\newcommand{\\typegeneration}" in line:
                self.nvalue = line[32:-2]
                tmpsplit = ""
                if "-" in self.nvalue:
                    split = self.nvalue.split("_")
                    self.nvalue = split[0]
                    if len(split) > 1:
                        tmpsplit = f"({split[1][:-2]}%)"
                self.xlabel = constants.X_LABEL_SPE(self.xlabel, self.nvalue, tmpsplit, constants.FR)

            if "\\newcommand{\\infograph}" in line:
                self.infograph = line[27:-2].split(";")
                
            line = self.file.readline()
            nbc += len(line)
        constants.ORDER = line[7:-2].split(";")
        self.nb_methods = len(constants.ORDER)
        
        tmp = f"{metric_name} Unanimous"
        meanr, self.percent = self.read_file(tmp)
        # for i in range(len(meanr)):
        #     for j in range(len(meanr[i])):
        #         print(i, "met",j, meanr[i][j])
        self.valueres.append(meanr[0])
        self.res = []
        self.percent = []
        self.options = []
        self.current = 0
        
        self.file.seek(nbc)
        tmp = f"{metric_name} Min"
        minr, self.percent = self.read_file(tmp)
        # for i in range(len(minr)):
        #     for j in range(len(minr[i])):
        #         print(i, "met",j, minr[i][j])
        self.valueres.append(minr[0])
        self.res = []
        self.percent = []
        self.options = []
        self.current = 0
        
        self.file.seek(nbc)
        tmp = f"{metric_name} Max"
        maxr, self.percent = self.read_file(tmp)
        # for i in range(len(maxr)):
        #     for j in range(len(maxr[i])):
        #         print(i, "met",j, maxr[i][j])
        self.valueres.append(maxr[0])
        self.file.close()                  
    
        self.para_plot = []
        
        self.color = [("-X", 'blue'),
                     ("-.*", 'black'),
                     (":>", 'red'),
                     ("-.<", 'cyan'),
                     ("-->", 'slategrey'),
                     (":<", 'orange')]
        
        nb_val = 6
        start = 0
        jump = self.width_bar * (nb_val+1)
        for i in range(nb_val):
            tmp = []
            start = i * self.width_bar
            for j in range(len(self.percent)):
                # print(nb_val, int(nb_val/2), i == int(nb_val/2))
                # if i == int(nb_val/2):
                #     self.xplacement.append(start + self.width_bar)
                tmp.append(start + self.width_bar)
                start += jump 
            self.placement.append(tmp)
        for i in range(len(self.percent)):
            self.xplacement.append(((self.width_bar*(nb_val+1))*(i+1)/2) + ((self.width_bar*(nb_val+1)/2)*i))
        
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
            res += f"{self.infograph[1]} src - x fct - {self.infograph[0]} obj"
        elif self.nvalue == constants.RUN_SRC:
            res += f"x src - {self.infograph[1]}-{self.infograph[2]} fct - {self.infograph[0]} obj"
        elif self.nvalue == constants.RUN_OBJ:
            res += f"{self.infograph[0]} src - {self.infograph[1]}-{self.infograph[2]} fct - x obj"
        else:
            res += f"{self.infograph[1]} src - {self.infograph[2]}-{self.infograph[3]} fct - {self.infograph[0]} obj"
        return res
        
    def name_png(self, method, nbs, metric):
        """
        """
        nbf = 1
        name = f"{self.directory}{method}/{metric}-{method}{nbs}.png"
        while os.path.isfile(name):
            nbf += 1
            add = f"_{nbf}"
            name = f"{self.directory}{method}/{metric}-{method}{nbs}{add}.png"
        return name
    
    def get_min_max(self, l, mini, maxi):
        if mini != None and maxi != None:
            tmp = l + [mini, maxi]
            return min(tmp), max(tmp)
        else:
            return min(l), max(l)
    
    def read_file(self, metric):
        """
        stock data (typeg, nbs) for each metric
        """
        line = self.file.readline()
        #Find the good metric
        while (metric not in line) or ("\section" not in line):
            line = self.file.readline()
            if "\end{document}" in line:
                raise ValueError(f"END OF FILE MINMAX : metric {metric} isn't in {self.name_file_error}.")
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
                break
        return self.res, self.percent
    
    def get_values(self, num_met):
        """
        1st ind = Sum - LexiMax/Min - Prod - Meth
        2nd ind = Mean Min Max
        """
        # for n in self.valueres:
        #     for m in n:
        #         print(m)
        #     print("-")
        # print("--")
        # UNA - MIN - MAX
        res = [[[], [], []], # SF 1
               [[], [], []], # SF 2
               [[], [], []], # SF 3
               [[], [], []]] # autre
        for i in range(len(self.valueres)):
            #Sum
            res[0][i].extend(self.valueres[i][0])
            #Leximax/Min
            res[1][i].extend(self.valueres[i][1])
            #Prod
            res[2][i].extend(self.valueres[i][3])
            # autres
            res[3][i].extend(self.valueres[i][num_met])
        return res
    
    def plot_all(self, d=0, t=-1, height=20, width=10):
        for i in range(len(self.options)):
            for num_met in range(4, len(constants.PLOT_ORDER)):
                self.plot_one(i=i, d=d, t=t, height=height, width=width, num_met=num_met, res=self.get_values(num_met))
            
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
        return True
    
    def myplot(self, x, y, i, j, idv='', d=0, t=-1, mini=None, maxi=None, items=0, indcol=0):
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
        # j = constants.ORDER.index(constants.PLOT_ORDER[j])
        
        if self.condition(ind_method=j, i=i):
            if d == 0 and t < 0:
                #default
                plt.bar(self.placement[self.curr_placement], y, self.width_bar, color=self.color[indcol][1], label=f"{self.parameters_plot(j,2,i)}_{idv}")
                # plt.plot(x, y, self.color[indcol][0], color=self.color[indcol][1], label=f"{self.parameters_plot(j,2,i)}_{idv}")
                m = self.get_min_max(y, mini, maxi)
                self.curr_placement += 1
                return m[0], m[1], items+1
        return mini, maxi, items
    
    def plot_one(self, i, d=0, t=-1, height=20, width=10, num_met=0, res=[]):
        """
        Create the plt.plot
        i : index of the options chosen
        d : index start (default 0)
        t : index end (default -1)
        """
        plt.figure(figsize=(height,width))
        
        mini, maxi, items = None, None, 0
        
        curr_met = constants.NAMES[num_met]
        
        
        possibv = ["una", "min", "max"]
        indcol = 0
        for i in range(len(possibv)):
            if i == 0:
                self.index_m = 0
                mini,maxi,items = self.myplot(x=self.percent, y=res[0][0], idv=possibv[0], i=i, j=0, d=d, t=t, items=items, mini=mini, maxi=maxi, indcol=indcol)
                indcol += 1
                self.index_m = 1
                mini,maxi,items = self.myplot(x=self.percent, y=res[0][1], idv=possibv[1], i=i, j=0, d=d, t=t, items=items, mini=mini, maxi=maxi, indcol=indcol)
                indcol += 1
                self.index_m = 3
                mini,maxi,items = self.myplot(x=self.percent, y=res[0][2], idv=possibv[2], i=i, j=0, d=d, t=t, items=items, mini=mini, maxi=maxi, indcol=indcol)
                indcol += 1
                
            self.index_m = num_met
            mini,maxi,items = self.myplot(x=self.percent, y=res[3][i], idv=possibv[i], i=i, j=num_met, d=d, t=t, items=items, mini=mini, maxi=maxi, indcol=indcol)
            indcol += 1
            
        self.curr_placement = 0
       
        plt.title(self.title(i) + f" for {curr_met}", y=1.1, x=0.5)
        
        #size axis
        ticks_size = 15
        plt.xticks(self.xplacement, self.percent)
        plt.xticks(fontsize=ticks_size)
        plt.yticks(fontsize=ticks_size)
        
        #size legend
        fontsize = 25
        plt.xlabel(self.xlabel, fontsize=fontsize)
        plt.ylabel(self.ylabel[self.index_m], fontsize=fontsize)        
        plt.legend(fontsize=fontsize)
                
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
        
        if self.metric_name == "CSI":
            name_pltpng = f"{self.directory}{self.parameters_plot(num_met,2,i)}_csi.png"
        else:
            name_pltpng = f"{self.directory}{self.parameters_plot(num_met,2,i)}_prc.png"
        print(f"Creation of png {name_pltpng}")
        plt.savefig(name_pltpng)
        # plt.savefig(self.name_png(self.options[i][0], self.options[i][1], self.name_file[self.index_m]))
        
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

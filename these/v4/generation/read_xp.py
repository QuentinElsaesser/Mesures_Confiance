from v4.generation import priors as pr
from v4.generation import metrics, latex, random_graph
from v4.generation import brutefrc_exp_para as bfexp
from v4.generation import graph_methods as gm
# from v4.generation import plot
from v4.generation import generate_w_prop

from v4.vote import plurality as voting

from v4.judag import sfsum

from v4.belms import sfleximin as sfleximinBM
from v4.belms import sfleximax as sfleximaxBM

from v4.constants import constants

import os, sys

from itertools import product

from datetime import datetime

from itertools import combinations

# from copy import deepcopy

class ReadXP:
    def __init__(self, path, option=1):
        """
        Read file in path and run algorithm on the graphs in the file
        option : number for the scoring rule for the first graph that will be duplicate
        """
        self.gen_agenda = False
        self.f = open(path, "r")
        print(f"read {path}")
        lines = self.f.readlines()
        
        header = lines[0].strip().split(";")
        
        indtypeg = header.index("TYPEG")
        indnbo = header.index("NB_OBJ")
        indnbs = header.index("NB_SRC")
        indnbfl = header.index("NB_FL")
        indnbfu = header.index("NB_FU")
        indnbf = header.index("NBF")
        indtrust = header.index("TRUST")
        # indnorma = header.index("NORMA")
        normalization = constants.NORMA_A
        indsf = header.index("SF")
        indof = header.index("OF")
        indtruth = header.index("TRUTH")
        for i in range(len(header)):
            if header[i].startswith("INTERVAL"):
                indintv = i
                self.interval = header[indintv][len("INTERVAL:"):].strip().split("/")[:-1]
                break
            else:
                indintv = -1
        
        #type of gen + percent
        type_gen = header[-1].split("_")
        self.nvalue = type_gen[0]
        self.fixed_prc = type_gen[1]
        
        self.formula = None
        self.interp = []
        self.distrib = ""
        
        self.nb_litt = 0
        self.interpretations = None
        # self.ind_int = None
            
        combi_intp = dict()
        if self.nvalue == constants.RUN_BIA or self.nvalue == constants.RUN_BIF or self.nvalue == constants.RUN_BCA or self.nvalue == constants.RUN_BCF or self.nvalue == constants.RUN_BSA or self.nvalue == constants.RUN_BFA:
            if self.nvalue != constants.RUN_BSA and self.nvalue != constants.RUN_BFA:
                self.fixed_prc = self.interval[0]
            
            self.nb_litt = int(type_gen[-1][3:])
            self.interpretations = list(range(2**self.nb_litt))
            
            self.interpretation = list(range(2**self.nb_litt))
            taille = (2**self.nb_litt) - 2
            # taille = 8
            str_intp = [str(n) for n in self.interpretation]
            for curr_taille in range(1, taille+1):
                combi_intp[curr_taille] = []
            for curr_taille in range(1, taille+1):
                str_poss, sets_poss = self.all_combinations(str_intp, curr_taille)
                combi_intp[curr_taille] = (str_poss, sets_poss)
            
        if self.nvalue == constants.RUN_VRN:
            #not on every file
            indvariance = header.index("VARIANCE")
        else:
            indvariance = None
        
        if not constants.verif(self.nvalue):
            raise ValueError(f"{constants.FORMULA} and {self.nvalue} not good match (see v4/constants.py)")
            
        if self.nvalue == constants.RUN_PRP or self.nvalue == constants.RUN_VRN or self.nvalue == constants.RUN_SPR or self.nvalue == constants.RUN_SDR:
            # if not constants.FORMULA == constants.RUN_JA:
            #     raise ValueError(f"File for JA tests but not methods for JA - read_xp.py - constants.FORMULA:{constants.FORMULA}")
            # constants.RUN_METHODS, constants.PLOT_METHODS, constants.NAMES_NONORMA, constants.NAMES, constants.ORDER, constants.PLOT_ORDER, constants.LEGEND_ORDER, constants.PARA_PLOT = constants.fill_tab()
            self.fixed_prc_prp = self.fixed_prc
            # self.fixed_prc = type_gen[2]self.interval[0]
            if self.nvalue == constants.RUN_PRP:
                self.fixed_prc = self.interval[0]
            self.formula_file = type_gen[2]
            self.formula = type_gen[3]
            self.distrib = type_gen[4]
            if "AGENDAG" == self.formula_file:
                # alors on a gen un agenda à chaque fois
                self.gen_agenda = True
            else:
                generator = generate_w_prop.GenerateWProp(self.formula_file, 0, read_xp=True)
                self.interp = generator.model
        lines = lines[1:]
        self.dico = dict()
        self.exp = None

        # self.spe_metric = []
        
        taille = len(lines)
        
        ind = 0
        l_intv = ""
        normalization = constants.NORMA_A
        first = True
        
        print(datetime.now().strftime('%H:%M:%S'))
        for i,l in enumerate(lines):            
            print(f"creation graph {i}/{taille}")
            tmp = l.split(";")
            
            self.typeg = tmp[indtypeg]
            self.nbo = int(tmp[indnbo])
            self.nbs = int(tmp[indnbs])
            self.nbfl = int(tmp[indnbfl])
            self.nbfu = int(tmp[indnbfu])
            nbf = int(tmp[indnbf])
            
            if self.gen_agenda:
                self.formula_file = tmp[-1].strip()
                generator = generate_w_prop.GenerateWProp(self.formula_file, 0, read_xp=True)
                self.interp = generator.model
            
            if first:
                infograph = f"{self.nbo};{self.nbs};{self.nbfl};{self.nbfu}"
                # self.interval = tmp[indintv].strip().split("/")[:-1]
                for intv in self.interval:
                    self.dico[intv] = []
                first = False
            
            intv, _ = self.find_intv_para(trust=int(tmp[indtrust]), nbf=nbf, nbo=self.nbo, nbs=self.nbs, indvariance=indvariance, line=tmp)
            if l_intv != intv:
                ind = 0            
                l_intv = intv
            prior = [0 for s in range(self.nbs)]
            
            tmpsf = tmp[indsf].split("-")
            sf = []
            for j in range(len(tmpsf)):
                tmps = [0 for f in range(nbf)]
                elts = tmpsf[j].split(",")
                for index in elts:
                    tmps[int(index)] = 1
                sf.append(tmps)
                # sf.append(list(map(int, l.split(","))))

            tmpof = tmp[indof].split("-")
            of = []
            for j in range(len(tmpof)):
                tmpo = [0 for f in range(nbf)]
                elts = tmpof[j].split(",")
                for index in elts:
                    tmpo[int(index)] = 1
                of.append(tmpo)

            truth = []
            tmptrue = tmp[indtruth].split("-")
            curr_id = 0
            length = len(tmptrue)
            for f in range(nbf):
                if curr_id < length and int(tmptrue[curr_id]) == f:
                    truth.append(1)
                    curr_id += 1
                else:
                    truth.append(0)
                    
            formulas_gen = dict()
            formulas_chosed = []
            if constants.FORMULA == constants.RUN_BS:
                formulas = tmp[-1].split("-")
                for i in range(len(formulas)):
                    n = formulas[i].split("=")
                    if n[0][-1] == "!":
                        formulas_chosed.append(True)
                        formulas_gen[n[0][:-1]] = sorted([m.strip() for m in n[1].split(",")])
                    else:
                        formulas_chosed.append(False)
                        formulas_gen[n[0]] = sorted([m.strip() for m in n[1].split(",")])

            self.dico[intv].append(gm.GraphMethods(prior, nbo=self.nbo, nbfl=self.nbfl, \
                                  nbfu=self.nbfu, nbs=self.nbs, typeg=self.typeg, \
                                  min_fs=1, allg=False))
                
            if constants.FORMULA == constants.RUN_JA:
                rg = random_graph.randomGraph(voting.Plurality, option, 
                              nbo=self.nbo, nbfl=self.nbfl, nbfu=self.nbfu, nbs=self.nbs, 
                            norma=normalization, prior=prior, typeg=self.typeg, min_fs=1,
                            sf=sf, of=of, truth=truth)
                
                rg.G = sfsum.Sumsf(rg.G.mat_fs, rg.G.mat_of, voting.Plurality, option, normalization, 
                                 len(rg.G.mat_fs[0]), len(rg.G.mat_fs), truth=truth, model=self.interp,
                                 Gr=rg.G, nom_agenda=self.formula_file)
            elif constants.FORMULA == constants.RUN_TD:
                rg = random_graph.randomGraph(voting.Plurality, option, 
                              nbo=self.nbo, nbfl=self.nbfl, nbfu=self.nbfu, nbs=self.nbs, 
                            norma=normalization, prior=prior, typeg=self.typeg, min_fs=1,
                            sf=sf, of=of, truth=truth)
            elif constants.FORMULA == constants.RUN_BS:
                rg = random_graph.randomGraph(voting.Plurality, option, 
                              nbo=self.nbo, nbfl=self.nbfl, nbfu=self.nbfu, nbs=self.nbs, 
                            norma=normalization, prior=prior, typeg=self.typeg, min_fs=1,
                            sf=sf, of=of, truth=truth)
                
                rg.G = sfleximaxBM.SFLeximax(rg.G.mat_fs, rg.G.mat_of, voting.Plurality, option, normalization, 
                                 len(rg.G.mat_fs[0]), len(rg.G.mat_fs), truth=tmptrue, Gr=rg.G,
                                 nbl=self.nb_litt, interp=self.interpretations, formulas=formulas_gen,
                                 formulas_chosed=formulas_chosed, dict_all_combi=combi_intp)
                # rg = random_graph.randomGraph(voting.Plurality, option, 
                #               nbo=self.nbo, nbfl=self.nbfl, nbfu=self.nbfu, nbs=self.nbs, 
                #             norma=normalization, prior=prior, typeg=self.typeg, min_fs=1,
                #             sf=sf, of=of, truth=truth)
                
                # rg.G = sfbms.SFbmS(rg.G.mat_fs, rg.G.mat_of, voting.Plurality, option, normalization, 
                #                  len(rg.G.mat_fs[0]), len(rg.G.mat_fs), truth=tmptrue, Gr=rg.G,
                #                  nbl=self.nb_litt, interp=self.interpretations, formulas=formulas_gen,
                #                  formulas_chosed=formulas_chosed, dict_all_combi=combi_intp)
            
            #if len(self.dico[intv][ind].rgs) > 0:
            #    print("Probleme ligne", i, l, "taille", len(self.dico[intv][ind].rgs), "ind", ind, intv)
            self.dico[intv][ind].add_rg(rg)
            ind += 1
        
        print(datetime.now().strftime('%H:%M:%S'))
        nb_exp = len(self.dico[intv])

        priors = pr.Priors(len_prior=5, nbo=10, bmin=0, bmax=100)
        print("Priors generated.")
        
        print("Start generating Latex")
        m = metrics.Metrics(None)
        ltx = latex.Latex(nb_metrics=len(m.metrics), spe=m.n_methods["Mt"], path_f=constants.PATH_RESULTS, 
                          nvalue=self.nvalue, fixed_prc=self.fixed_prc, infograph=infograph, readname=path.split("/")[-1].split("xp")[0],
                          distrib=self.distrib, literals=str(self.nb_litt))
        ltx.new_section(m.metrics_name)
        
        prc = priors.percent[-1]
        
        self.exp = bfexp.BruteForceExperiencesParameters(nb_exp=nb_exp, percentage=prc, 
                                          nbs=self.nbs, nbo=self.nbo, nbfl=self.nbfl, 
                                          nbfu=self.nbfu, all_priors=priors, 
                                          typeg='ncpr', min_fs=1, 
                                          stop=1000000, q=1000, aff=100, 
                                          name=ltx.name, step=1000,
                                          path_xp=constants.PATH_XP, read=True,
                                          interval=self.interval, nvalue=self.nvalue, 
                                          fixed_prc=self.fixed_prc,formula=self.formula,
                                          interp=self.interp)
        
        self.exp.interval = self.interval
        self.exp.dico = self.dico
        
        self.exp.other_methods()
        self.exp.run_graph()
        
        # constants.ORDER = constants.is_tested(constants.ORDER)
        # constants.ID_METHODS_SOURCES = constants.id_is_tested()
        
        nbg = 0
        for prc in self.exp.interval:
            if self.nvalue == constants.RUN_SRC:
                self.nbs = prc
            ltx.new_subsection(prc, nb_exp, m, self.exp.fixed_prc)
            #don't delete the graph to check the graphs
            #exp.put_in_graph(prc)
            self.exp.graphes = self.exp.dico[prc]
            m = metrics.Metrics(self.exp)
            for i in range(len(m.metrics)):
            # for i in list(constants.ID_METRICS_ACTIVE.values()):
                # print(m.metrics[i])
                m.metrics[i]()
                ltx.body_tab(metric=m, typeg=self.typeg, nbs=self.nbs)
            nbg += 1
            print(f"Writing interval {nbg}/{len(self.exp.interval)}")
            ltx.end_tab()
        ltx.combined()
        ltx.write()

        self.f.close()
        
        
        #name = ltx.name;base_dir = f"{constants.PATH_PNG}{name.split('/')[-1].split('.')[0]}/"
        #directorypng = self.name_directory(base_dir)
        #m = metrics.Metrics(None)
        #self.generate_plot(name=name, metric=m, directory=directorypng)
        
    def all_combinations(self, lst, taille):
        res = []
        r = []
        for n in combinations(lst, taille):
            res.append(list(n))
            r.append(set(n))
        return res, r
        
    def name_directory(self, directory):
        name = directory
        nbf = 0
        while os.path.exists(name):
            nbf += 1
            name = f"{directory[:-1]}-{nbf}/"
        return name
        
    def find_intv_para(self, trust, nbf, nbo, nbs, indvariance=None, line=None):
        if self.nvalue in constants.LIST_RUN_NORMAL:
            return self.find_intv_prc(trust)
        elif self.nvalue == constants.RUN_FCT:
            return self.find_intv_elt(int(nbf/nbo), trust)
        elif self.nvalue == constants.RUN_OBJ:
            return self.find_intv_elt(nbo, trust)
        elif self.nvalue == constants.RUN_BFA:
            return self.find_intv_formulae(nbo, trust)
        elif self.nvalue in constants.LIST_RUN_SRC:
            return self.find_intv_elt(nbs, trust)
        elif self.nvalue == constants.RUN_VRN:
            return self.find_intv_vrn(indvariance, line)
            # return self.fixed_prc_prp, 0
        
    def find_intv_vrn(self,indvariance, line):
        """
        find the interval depending on the nbs/nbo and the relia is in the fixed interval
        """
        if line[indvariance]in self.interval:
            return line[indvariance], self.interval.index(line[indvariance])
        return None, None
    
    def find_intv_formulae(self, v, relia):
        """
        find the interval depending on the nbs/nbo and the relia is in the fixed interval
        """
        iv = self.fixed_prc.split("-")
        if int(iv[0]) <= relia <= int(iv[1]):
            for i in range(len(self.interval)):
                intv = self.interval[i].split("-")
                if int(intv[0]) <= v <= int(intv[1]):
                    return self.interval[i], i
        return None, None       
    
    def find_intv_elt(self, v, relia):
        """
        find the interval depending on the nbs/nbo and the relia is in the fixed interval
        """
        iv = self.fixed_prc.split("-")
        if int(iv[0]) <= relia <= int(iv[1]):
            for i in range(len(self.interval)):
                intv = self.interval[i]
                if int(intv) == v:
                    return self.interval[i], i
        return None, None    
    
    def find_intv_prc(self, v):
        """
        find the interval depending on the a posteriori probability.theoritical trust
        """
        for i in range(len(self.interval)):
            intv = self.interval[i].split("-")
            if int(intv[0]) <= v <= int(intv[1]):
                return self.interval[i], i
        return None, None  
    
    # def read_file_proposition(self):
    #     """
    #     read file and add interpretation depending on resultat of truth table
    #     """
    #     interp1 = []
    #     f = open(f"{constants.PROP_PATH}/{self.formula_file}", 'r')
    #     lines = f.readlines()
    #     for i in range(1, len(lines)):
    #         line = [int(l) for l in lines[i].split(";")]
    #         if line[-1]:
    #             interp1.append(line)
    #     f.close()
    #     return interp1
        
if __name__ == "__main__":
    n = 1
    nvalue = ""
    #nvalue = "src"
    # nvalue = "fct"
    option = 1
    ####prp:
    # nvalue = "prp"; 
    # nvalue = "spr"
    # nvalue = "sdr"

    nvalue = sys.argv[1]
    
    n = int(sys.argv[2])

    ####
    name = f"res{n}xp0{nvalue}.csv"
    readxp = ReadXP(f"{constants.PATH_XP}{name}", option=option)
    

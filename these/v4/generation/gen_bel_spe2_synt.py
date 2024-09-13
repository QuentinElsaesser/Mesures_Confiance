from v4.constants import constants

import random, os, glob#, math#, sys

# from collections import Counter

# from itertools import product

from datetime import datetime

# from random import randint

from itertools import combinations

from copy import deepcopy

class GenBelSynt:
    """
    ajoute le nombre de sources qu'il faut en plus par rapport aux precedents
    """
    def __init__(self, nbs, nbg=1000, nbf=30, read_xp=False, typeg="BTU", intvp=['30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69'], int_variance=[0,10,20,30,40,50,60,70,80,90,100], nb_litt=3, norma_aposteriori=True, nbsubsetneeded=2, not_full=True):
        """
        int_variance : le nombre de sources qui change
        file : name of file with the proposition and the truth table (same format as a csv file)
        nbs : Number sources
        nbrelia : number of sources that should be reliable when we generate the graph (must be an integer <= nbs)
        nbg : number of graphs we want to generate (1000 by default)
        read_xp : True if called in read_xp class
        """
        if typeg != constants.RUN_BSA:
            raise ValueError(f"{typeg} is not {constants.RUN_BSA}")
        
        self.nbs = nbs
        self.nbg = nbg
        self.nb_formula_togen = nbf
        
        self.not_full = not_full
        
        self.norma_aposteriori = norma_aposteriori
        
        self.nbsubsetneeded = nbsubsetneeded
        
        self.run_curr_nb_it = 0
        
        self.typeg = typeg
        self.variance = 100

        self.interval = intvp
        self.fix_interval = None
        

        self.interval = int_variance
        self.fix_interval = intvp[0]
        
        self.find_intv_src = []
            
        self.res = dict()
        self.nres = dict()
        self.valid = []
        for i in self.interval:
            self.res[i] = []
            self.nres[i] = 0
            self.valid.append(False)
        
        self.f = None
        
        self.truth = None
  
        self.nb_litt = nb_litt
        
        self.len_interpretation = 2**self.nb_litt
        self.interpretation = list(range(self.len_interpretation))
        self.set_interpretation_sets = set(self.interpretation)
        
        # list de list de formule. à l'indice 0 on a les formules pour tous les prc
        self.all_para = []
        self.agents_all = []
        
        # liste de sets - indice 0 = croyance agent 0
        self.croyances = []
        # liste de listes de set - indice 0 = formules de agent 0
        self.formulas_agents = []
        # k : string de la formule - v : indice de la formule
        self.id_formulas = dict()
        self.formulas_id = dict()
        # indice des formules qui sont generees par des agents
        self.generated = []
        self.took = []
        # indice de la formule que l'on cree
        self.curr_id_f = 0
        # vote des agents sur les formules
        self.claims = []

        self.dico = dict()
        # if not read_xp:
            # self.OF = self.list_of()
            
        self.OF = []
        self.facts = []
        self.nbo = 0
        
    def write_header(self, trust):
        """
        trust : average trust for the self.nbg graphs generated
        """
        delete = []
        for i in range(len(self.interval)):
            if not self.valid:
                delete.append(self.interval[i])
                for d in delete:
                    self.interval.remove(d)
        # if self.norma_aposteriori:
        #     NORMA = constants.NORMA_A
        # else:
        #     NORMA = constants.NORMA_O
        
        if self.fix_interval != None:
            n = self.fix_interval.split("-")
            trust1 = n[0]
            trust2 = n[1]
        else:
            trust1 = trust
            trust2 = trust
        return f"TYPEG;VARIANCE;NB_OBJ;NB_SRC;NB_FL;NB_FU;NBF;TRUST;SF;OF;TRUTH;INTERVAL:{self.str_interval()};{self.typeg}_{trust1}-{trust2}_nbl{self.nb_litt}\n"
        
    def write(self, graph, trust, truth):   
        return f"cpr;{self.variance};{self.nbo};{self.nbs};{2};{2};{self.nbo*2};{trust};{self.list_sf(graph)};{self.OF};{self.list_truth(self.truth)};;{self.list_formulas()}\n"
    
    def find_interv(self, t):
        if self.typeg == constants.RUN_BSA:
            for i in range(len(self.interval)):
                n = self.interval[i]
                if n == self.nbs:
                    tmp = self.fix_interval.split("-")
                    if int(tmp[0]) <= t <= int(tmp[1]):
                        return i, self.interval[i]
        return -1, None
        
    def add_dict(self, truth, claims, trust, i):
        ind,intv = self.find_interv(trust)
        if intv != None:
            if not self.find_intv_src[i]:
                if self.nres[intv] < self.nbg:
                    w = self.write(claims, trust, truth)
                    self.res[intv].append(w)
                    self.nres[intv] += 1
                    self.find_intv_src[i] = True
                    if self.nres[intv] == self.nbg:
                        self.valid[ind] = True
                    return w
            return ""
        return ""

    def generate_formulas(self, truth, para):
        """
        generation de :
            - croyance de base
            - formules de chaque agent
        """
        # liste de sets - indice 0 = croyance agent 0
        self.croyances = []
        # liste de listes de set - indice 0 = formules de agent 0
        self.formulas_agents = []
        # k : string de la formule - v : indice de la formule
        self.id_formulas = dict()
        self.formulas_id = dict()
        # indice de la formule que l'on cree
        self.curr_id_f = 0
        # vote des agents sur les formules
        self.claims = []
        #        
        self.generated = []
        self.took = []
        
        # self.all_para = []
        
        set_intp_pour_croyance = set()
        set_intp_pour_croyance_no_truth = set()
        list_formule_poss_agent = set()
        croyance_poss = set()
        nb_formulas = self.nb_formula_togen
        
        for i in range(nb_formulas):
            f = set()
            nb_interp = random.randint(2, self.len_interpretation-3)
            set_intp_poss = set(self.interpretation)
            # creation d'une formule
            for k in range(nb_interp):
                possible_interp = list(set_intp_poss.difference(f))
                nrandom = random.randint(0,len(possible_interp)-1)
                intp = possible_interp[nrandom]
                f.add(intp)
                croyance_poss.add(intp)
            # print("FORMULE", i, f)
            to_add_str = str(sorted(f))
            if to_add_str not in self.formulas_id:
                self.formulas_id[to_add_str] = self.curr_id_f
                self.id_formulas[self.curr_id_f] = f
                self.generated.append(True)
                list_formule_poss_agent.add(self.curr_id_f)
                self.generated.append(False)
                self.took.append(False)
                self.took.append(False)
                # print("NEW FORMULE", to_add_str, f, self.curr_id_f)
                self.curr_id_f += 1
                negation = self.set_interpretation_sets.difference(f)
                negation_str = str(sorted(list(negation)))
                self.formulas_id[negation_str] = self.curr_id_f
                self.id_formulas[self.curr_id_f] = negation
                # print("NEW NEGATION", negation_str, negation, self.curr_id_f)
                self.curr_id_f += 1
            else:
                idf = self.formulas_id[to_add_str]
                self.generated[idf] = True
                list_formule_poss_agent.add(idf)
                # print("FORMULE EXISTE DEJA", list_formule_poss_agent)

        # pour chaque formule, faire les sous ensembles et keep ceux ok avec 2f 
        tmp_para_1 = para[1]
        for f in list(self.id_formulas.values()):
        # for idf in list(list_formule_poss_agent):
        #     f = self.id_formulas[idf]
            lf = list(f)
            ## if para[1] > len(lf):
            ##     tmp_para_1 = len(lf)-1
            ## print("curr f", f)
            for i in range(para[0], tmp_para_1):
                can_add = False
                for n in combinations(lf, i+1):
                    sn = set(n)
                    nbsubs = 0
                    # for f1 in list(self.id_formulas.values()):
                    for idf1 in list(list_formule_poss_agent):
                        f1 = self.id_formulas[idf1]
                        # print("n avec ?", n, f1, self.formulas_id[str(sorted(f1))], sn.issubset(f1))
                        if sn.issubset(f1):
                            nbsubs += 1
                        if nbsubs == self.nbsubsetneeded:
                            # print("break, 2 bonnes formules pour", n)
                            break
                    if nbsubs == self.nbsubsetneeded:
                        can_add = True
                        # print("truth et subset", self.truth, n, self.truth in n)
                        if self.truth in n:
                            set_intp_pour_croyance.add(n)
                        else:
                            set_intp_pour_croyance_no_truth.add(n)
                        # print("tout", i, n, f1)
                        # print()
                if not can_add:
                    # print("on peut pas ajouter plus grand")
                    # si on peut pas ajouter un taille n alors on pourra pas n+1
                    break

        list_formule_poss_agent = list(list_formule_poss_agent)
        
        xd = list(set_intp_pour_croyance)
        for i in range(len(xd)):
            xd[i] = set(list(xd[i]))
            # print("intp AVEC truth pour croyances", i, xd[i])
        set_intp_pour_croyance = xd
        
        xd = list(set_intp_pour_croyance_no_truth)
        for i in range(len(xd)):
            xd[i] = set(list(xd[i]))
            # print("intp SANS truth pour croyances", i, xd[i])
        set_intp_pour_croyance_no_truth = xd
        
        all_set_intp_pour_croyance = set_intp_pour_croyance + set_intp_pour_croyance_no_truth

        # if len(set_intp_pour_croyance) == 0:
        if len(set_intp_pour_croyance) <= 3:
            return False
        
        if len(set_intp_pour_croyance_no_truth) <= 3:
            return False

        # if len(set_intp_pour_croyance) == 0:
        #     # print("VIDE")
        #     set_intp_pour_croyance = all_set_intp_pour_croyance
        #     # il faut au moins une formule avec la verite:
        
        # cherche les bonnes croyances si on veut guider lalea
        # if para[3]:
        xxxx = list()
        for x in list(set_intp_pour_croyance):
            # if len(x) <= para[4]:
            xxxx.append(x)
        # if len(xxxx) == 0:
        #     if para[4] > 1:
        #         xxxx = list()
        #         for x in list(set_intp_pour_croyance):
        #             if len(x) <= para[4]-1:
        #                 xxxx.append(x)
                        
            
        self.all_para.append([deepcopy(xxxx), deepcopy(all_set_intp_pour_croyance), deepcopy(list_formule_poss_agent), 
                              deepcopy(self.id_formulas), deepcopy(self.formulas_id), deepcopy(self.took), deepcopy(self.truth),
                              deepcopy(set_intp_pour_croyance_no_truth), deepcopy(self.generated), deepcopy(self.curr_id_f)])
        
        self.agents_all.append([deepcopy(self.formulas_agents), deepcopy(self.claims), deepcopy(self.croyances)])
        
        return True
        
    def claims_src(self, para, ind_para):
        """
        para : les para que l'utilisateur donne
        i : l'indice a utiliser avec all_para pour construire les graphes
        """
        xxxx = deepcopy(self.all_para[ind_para][0])
        
        if para[3]:
            # print("PARA3 VRAI")
            xxxx2 = list()
            for tmpx in list(xxxx):
                if len(tmpx) <= para[4]:
                    xxxx2.append(tmpx)
                # if len(xxxx2) == 0:
                #     print(len(xxxx2))
                #     if para[4] > 1:
                #         xxxx2 = list()
                #         for x in list(xxxx):
                #             if len(x) <= para[4]-1:
                #                 xxxx2.append(x)
            xxxx = xxxx2
        
        all_set_intp_pour_croyance = deepcopy(self.all_para[ind_para][1])
        list_formule_poss_agent = deepcopy(self.all_para[ind_para][2])
        set_intp_pour_croyance_no_truth = deepcopy(self.all_para[ind_para][7])
        # if len(set_intp_pour_croyance_no_truth) == 0:
        #     set_intp_pour_croyance_no_truth = all_set_intp_pour_croyance
        
        nb_run_it = len(self.claims)
        self.run_curr_nb_it = nb_run_it
        # print("CURR SRC WITH VOTE", nb_run_it, self.nbs)
        for i in range(nb_run_it, self.nbs):
            self.formulas_agents.append([])
            self.claims.append([])
            dico_intp = dict()
            for x in self.interpretation:
                dico_intp[x] = 0
                
            # tirage des croyances
            if para[3]:
                # print("src", i, xxxx)
                if len(xxxx) > 0 and i < para[5]:
                    # print("inside", self.truth)
                    # print(xxxx)
                    self.croyances.append(xxxx[random.randint(0, len(xxxx)-1)])
                else:
                    # print("false")
                    self.croyances.append(set_intp_pour_croyance_no_truth[random.randint(0, len(set_intp_pour_croyance_no_truth)-1)])
            elif para[3] == False:
                self.croyances.append(all_set_intp_pour_croyance[random.randint(0, len(all_set_intp_pour_croyance)-1)])
            
            poss_w_agent = []
            # tirage des formules
            for idfx2 in list_formule_poss_agent:
                f = self.id_formulas[idfx2]
                # print(f, self.croyances[i], self.croyances[i].issubset(f))
                if self.croyances[i].issubset(f):
                    poss_w_agent.append(idfx2)

            if len(poss_w_agent) < self.nbsubsetneeded:
                # print("FALSE1")
                return False

            # nombre formule par sources
            if len(poss_w_agent) == self.nbsubsetneeded:
                nbf = self.nbsubsetneeded
            else:
                nbf = random.randint(self.nbsubsetneeded, len(poss_w_agent))
            # print("ADD NBF :", nbf)
            for indvaluef in range(nbf):
                v = random.randint(0, len(poss_w_agent)-1)
                idf = poss_w_agent[v]
                f = self.id_formulas[idf]
                self.formulas_agents[i].append(f)
                self.claims[i].append(idf)
                self.took[idf] = True
                poss_w_agent.remove(idf)
                for intp in f:
                    dico_intp[intp] += 1   
            
            # if len(self.formulas_agents[i]) > 1:
            #     for x in self.interpretation:
            #         if dico_intp[x] == nbf:
            #             self.croyances[i].add(x)
        return True
            
    def generate_votes_implication_full(self):
        """
        vote for a formula = id even (0,2,4,etc)
        vote against (or for the negation depending on what we do) = id odd (1,3,5,etc)
        """
        # print("VOTE FULL")
        nb_run_it = self.run_curr_nb_it
        # print(nb_run_it, self.nbs)
        for i in range(nb_run_it, self.nbs):
        # for i in range(self.nbs):
            # print("AGENT", i)
            for f in list(self.id_formulas.values()):
                str_f = str(sorted(list(f)))
                idf = self.formulas_id[str_f]
                go = True
                id_to_add = None
                # print("FORMULA", f, idf)
                # print("VERIF SI LA NEGATION EST DEJA DANS L'AGENT", self.claims[i], self.formulas_agents[i])
                if idf % 2 == 0:
                    id_to_add = (idf, idf+1)
                    if id_to_add[1] in self.claims[i]:
                        # print("NEGATION CLAIM PAR L'AGENT DONC ON IGNORE", f)
                        go = False
                    elif id_to_add[0] in self.claims[i]:
                        # print("FORMULE DEJA CLAIM PAR L'AGENT DONC ON IGNORE", f)
                        go = False
                else:
                    id_to_add = (idf, idf-1)
                    if id_to_add[1] in self.claims[i]:
                        # print("NEGATION CLAIM PAR L'AGENT DONC ON IGNORE", f)
                        go = False
                    elif id_to_add[0] in self.claims[i]:
                        # print("FORMULE DEJA CLAIM PAR L'AGENT DONC ON IGNORE", f)
                        go = False
                if go:
                    # print("AGENT PEUT POTENTIELLEMNT ADD")
                    # print("DIFF ENTRE CROYANCE ET F", self.croyances[i], self.croyances[i].difference(f), id_to_add)
                    if len(self.croyances[i].difference(f)) == 0:
                        # print("AJOUT DE LA FORMULE")
                        self.claims[i].append(id_to_add[0])
                        self.took[id_to_add[0]] = True
                        self.formulas_agents[i].append(self.id_formulas[id_to_add[0]])
                    else:
                        # print("AJOUT DE LA NEGATION FORMULE")
                        self.took[id_to_add[1]] = True
                        self.claims[i].append(id_to_add[1])
                        self.formulas_agents[i].append(self.id_formulas[id_to_add[1]])
                # print()
            self.claims[i] = sorted(self.claims[i])
            # print("UPDATE CLAIMS", self.claims)
            # print()
            
    def generate_votes_implication_abs(self):
        """
        vote for a formula = id even (0,2,4,etc)
        vote against (or for the negation depending on what we do) = id odd (1,3,5,etc)
        """
        # print("VOTE ABS")
        nb_run_it = self.run_curr_nb_it
        for i in range(nb_run_it, self.nbs):
        # for i in range(self.nbs):
            # print("AGENT", i)
            for f in list(self.id_formulas.values()):
                str_f = str(sorted(list(f)))
                idf = self.formulas_id[str_f]
                go = True
                id_to_add = None
                # print("FORMULA", f, idf)
                # print("VERIF SI LA NEGATION EST DEJA DANS L'AGENT", self.claims[i], self.formulas_agents[i])
                if idf % 2 == 0:
                    id_to_add = (idf, idf+1)
                    if id_to_add[1] in self.claims[i]:
                        # print("NEGATION CLAIM PAR L'AGENT DONC ON IGNORE", f)
                        go = False
                    elif id_to_add[0] in self.claims[i]:
                        # print("FORMULE DEJA CLAIM PAR L'AGENT DONC ON IGNORE", f)
                        go = False
                else:
                    id_to_add = (idf, idf-1)
                    if id_to_add[1] in self.claims[i]:
                        # print("NEGATION CLAIM PAR L'AGENT DONC ON IGNORE", f)
                        go = False
                    elif id_to_add[0] in self.claims[i]:
                        # print("FORMULE DEJA CLAIM PAR L'AGENT DONC ON IGNORE", f)
                        go = False
                if go:
                    # print("AGENT PEUT POTENTIELLEMNT ADD")
                    # print("F et NEG", f, self.id_formulas[id_to_add[1]])
                    # print("DIFF ENTRE CROYANCE ET F", self.croyances[i], self.croyances[i].difference(f), id_to_add, self.croyances[i].difference(self.id_formulas[id_to_add[1]]))
                    if len(self.croyances[i].difference(f)) == 0:
                        # print("AJOUT DE LA FORMULE")
                        self.took[id_to_add[0]] = True
                        self.claims[i].append(id_to_add[0])
                        self.formulas_agents[i].append(self.id_formulas[id_to_add[0]])
                    elif len(self.croyances[i].difference(self.id_formulas[id_to_add[1]])) == 0:
                        # print("AJOUT DE LA NEGATION FORMULE")
                        self.took[id_to_add[1]] = True
                        self.claims[i].append(id_to_add[1])
                        self.formulas_agents[i].append(self.id_formulas[id_to_add[1]])
                #     else:
                #         print("ABSTENTION")
                # print()
            self.claims[i] = sorted(self.claims[i])
            # print("UPDATE CLAIMS", self.claims)
            # print()        
   
    def compute_trust(self, g, truth):
        if self.norma_aposteriori:
            return self.compute_trustA(g, truth)
        else:
            return self.compute_trustC(g, truth)
   
    def compute_trustA(self, g, truth):
        """trustA - verif si l'interpretation considerer comme la verite fait
        partie de chaque formule = proportion des formules qui sont vraies"""
        trust = []
        total = 0
        total = int(len(self.id_formulas)/2)
        for i in range(len(g)):
            good = 0
            for idf in g[i]:
                if self.truth in self.id_formulas[idf]:
                    good += 1
            trust.append((good/total)*100)
        return round((sum(trust)/self.nbs))
    
    def compute_trustC(self, g, truth):
        """trustC - verif si l'interpretation considerer comme la verite fait
        partie de chaque formule = proportion des formules qui sont vraies"""
        trust = []
        for i in range(len(g)):
            good = 0
            total = 0
            for idf in g[i]:
                if self.truth in self.id_formulas[idf]:
                    good += 1
                total += 1
            trust.append((good/total)*100)
        return round((sum(trust)/self.nbs))
    
    def generate_all(self):
        type_generation = ""
        para = [0,3,5,False,3,0]
        runit = 0
        it = 1000
        total = 0
        
        find_intv_src_save = [False for n in range(self.nbg)]
        self.find_intv_src = find_intv_src_save.copy()
        right_gen_formulas = True
        indice_para = 0
        # dontask = False
        self.nbs = self.interval[0]
        num_intv = 0
        
        while not all(self.valid) and type_generation != "e": 
            # if not dontask:
            #affichage
            res = ""
            keys = list(self.nres.keys())
            for i in range(len(keys)):
                res += f"\033[31m{keys[i]}\033[00m:\033[32m{self.nres[keys[i]]}\033[00m / "
            res += "\n"
            print(f"generation:{type_generation} - para:{para}")
            if not all(self.valid):
                # curr para
                print(runit, "\n", res)
                # ask nb it
                tmp = input(f"{datetime.now().strftime('%H:%M:%S')} - nb it (curr {it}) ? ")
                if tmp != "":
                    if tmp.isnumeric():
                        it = int(tmp)
                    else:
                        it = 1
                tmp = input(f"taille models ({para[0]}-{para[1]}) ? ")
                if tmp != "":
                    tmp = tmp.split("-")
                    para[0] = int(tmp[0])
                    para[1] = int(tmp[1])
                tmp = input(f"Croyance avec truth ? (y/n/d) - {para[3]} ")
                if tmp == "":
                    if para[3] == "d":
                        tmp = "d"
                    elif para[3] == True:
                        tmp = "y"
                if tmp != "":
                    if tmp == "a":
                        # print(self.truth)
                        print(self.all_para[indice_para][6])
                        # print(self.formulas_id)
                        print(self.all_para[indice_para][4])
                        # xxxx truth in
                        print(self.all_para[indice_para][0])
                        # no truth
                        print(self.all_para[indice_para][7])
                    if tmp == "y":
                        para[3] = True
                        tmp = input(f"nb intp dans croyance ? (0...n) - {para[4]} ")
                        if tmp.isnumeric():
                            para[4] = int(tmp)
                        # else:
                        #     # 1 mini c'est la verité / 0 = vide
                        #     para[4] = 1
                        tmp = input(f"nb src with truth ? (0...n) - {para[5]} ")
                        if tmp.isnumeric():
                            para[5] = int(tmp)
                        # else:
                        #     para[5] = 0
                    elif tmp == "d":
                        para[3] = "d"
                        tmp = input(f"del en dessous de x% ? - {para[4]} ")
                        if tmp.isnumeric():
                            para[4] = int(tmp)
                    else:
                        para[3] = False
            trust_gen = dict()
        
            if right_gen_formulas:
                # print("Construction formules")
                right_gen_formulas = False
                # genere croyances et formules des agents
                for x in range(self.nbg):
                    error = False
                    self.truth = self.interpretation[random.randint(0,self.len_interpretation-1)]
                    while error == False:
                        error = self.generate_formulas(self.truth, para)
            # print(len(self.all_para))
            # print("Construction Profil #", indice_para, "/", len(self.find_intv_src), "interv", self.nbs)
            
            curr_ind_run = 0
            while curr_ind_run != it:
                curr_ind_run += 1
                runit += 1
                if num_intv == 0:
                    self.formulas_agents = []
                    self.claims = []
                    self.croyances = []
                else:
                    self.formulas_agents = self.agents_all[indice_para][0]
                    self.claims = self.agents_all[indice_para][1]
                    self.croyances = self.agents_all[indice_para][2]
                
                saveS1 = deepcopy(self.agents_all[indice_para][0])
                saveS2 = deepcopy(self.agents_all[indice_para][1])
                saveS3 = deepcopy(self.agents_all[indice_para][2])
                
                save1 = deepcopy(self.all_para[indice_para][3])
                save2 = deepcopy(self.all_para[indice_para][4])
                save3 = deepcopy(self.all_para[indice_para][5])
                save4 = deepcopy(self.all_para[indice_para][6])
                save5 = deepcopy(self.all_para[indice_para][8])
                save6 = deepcopy(self.all_para[indice_para][9])
                
                self.id_formulas = deepcopy(self.all_para[indice_para][3])
                self.formulas_id = deepcopy(self.all_para[indice_para][4])
                self.took = deepcopy(self.all_para[indice_para][5])
                self.truth = deepcopy(self.all_para[indice_para][6])
                self.generated = deepcopy(self.all_para[indice_para][8])
                self.curr_id_f = deepcopy(self.all_para[indice_para][9])
                
                error = self.claims_src(para, indice_para)
                
                if error != False:
                    # if self.typeg == constants.RUN_BSA:
                    if self.not_full:
                        # print("AJOUT ABS")
                        self.generate_votes_implication_abs()
                    else:
                        # print("AJOUT FULL")
                        self.generate_votes_implication_full()
                            
                    self.nbo = int(self.curr_id_f/2)                
                    self.facts = [[i for i in range(n*2,n*2+2)] for n in range(self.nbo)]
                    self.OF = self.list_of()
                else:
                    error = None
                    
                    self.agents_all[indice_para][0] = saveS1
                    self.agents_all[indice_para][1] = saveS2
                    self.agents_all[indice_para][2] = saveS3
                    
                    self.all_para[indice_para][3] = save1
                    self.all_para[indice_para][4] = save2
                    self.all_para[indice_para][5] = save3
                    self.all_para[indice_para][6] = save4
                    self.all_para[indice_para][8] = save5
                    self.all_para[indice_para][9] = save6
                    
                if len(self.claims) == self.nbs:
                    trust = self.compute_trust(self.claims, self.truth)
                    if trust in trust_gen:
                        trust_gen[trust] += 1
                    else:
                        trust_gen[trust] = 1
                    if self.add_dict(self.truth, self.claims, trust, indice_para) != "":
                        # stocke la trust du graphe conserve
                        total += trust
                        curr_ind_run = 0
                        
                        # update agents all
                        self.agents_all[indice_para] = [deepcopy(self.formulas_agents), deepcopy(self.claims), deepcopy(self.croyances)]
                    else:
                        self.agents_all[indice_para][0] = saveS1
                        self.agents_all[indice_para][1] = saveS2
                        self.agents_all[indice_para][2] = saveS3
                        
                        self.all_para[indice_para][3] = save1
                        self.all_para[indice_para][4] = save2
                        self.all_para[indice_para][5] = save3
                        self.all_para[indice_para][6] = save4
                        self.all_para[indice_para][8] = save5
                        self.all_para[indice_para][9] = save6
                        
                    if self.find_intv_src[indice_para]:
                        # print("Changement interval")
                        indice_para += 1
                        # print("Trust generated", [(k,trust_gen[k]) for k in sorted(trust_gen)])
                    if all(self.find_intv_src):
                        # print("Changement formules")
                        num_intv += 1
                        if num_intv == len(self.interval):
                            num_intv -= 1
                        else:
                            print("Nouvel src", self.nbs)
                        indice_para = 0
                        self.nbs = self.interval[num_intv]
                        self.find_intv_src = find_intv_src_save.copy()
                        break
                else:
                    self.agents_all[indice_para][0] = saveS1
                    self.agents_all[indice_para][1] = saveS2
                    self.agents_all[indice_para][2] = saveS3
                    
                    self.all_para[indice_para][3] = save1
                    self.all_para[indice_para][4] = save2
                    self.all_para[indice_para][5] = save3
                    self.all_para[indice_para][6] = save4
                    self.all_para[indice_para][8] = save5
                    self.all_para[indice_para][9] = save6
                # print(indice_para, self.nbs, i, self.find_intv_src, [(k,trust_gen[k]) for k in sorted(trust_gen)])
                if all(self.valid):
                    break
                if runit % 10000 == 0:
                    res = ""
                    keys = list(self.nres.keys())
                    for i in range(len(keys)):
                        res += f"\033[31m{keys[i]}\033[00m:\033[32m{self.nres[keys[i]]}\033[00m / "
                    res += "\n"
                    print(runit, "\n", res)
                    res = ""
            print("Trust generated", [(k,trust_gen[k]) for k in sorted(trust_gen)])
        # affichage
        res = ""
        keys = list(self.nres.keys())
        for i in range(len(keys)):
            res += f"\033[31m{keys[i]}\033[00m:\033[32m{self.nres[keys[i]]}\033[00m / "
        res += "\n"
        print(runit, "\n", res)
        # debut ecriture
        self.name_xp(); print("start writing")
        txt = self.write_header(round(total/(self.nbg*len(self.interval))))
        for i in self.interval:
            for n in self.res[i]:
                txt += n
        self.f.write(txt)
        print("done")
        # print(txt)
        self.f.close()
    
    def list_sf(self, s):
        res = ""
        for i in range(len(s)):
            for j in range(len(s[i])):
                res += f"{s[i][j]},"
            res = res[:-1]
            res += "-"
        return res[:-1]
        
    def list_of(self):
        res = ""
        for i in range(len(self.facts)):
            for j in range(len(self.facts[i])):
                res += f"{self.facts[i][j]},"
            res = res[:-1]
            res += "-"
        return res[:-1]
    
    def list_truth(self, truth):
        return f"{truth}"
    
    def list_formulas(self):
        res = ""
        for i in self.id_formulas:
            tmp = ",".join([n.strip() for n in str(self.id_formulas[i])[1:-1].split(",")])
            inside = ""
            if self.generated[i]:
                inside = "!"
            res += f"{i}{inside}={tmp}-"
            # print(i, self.id_formulas[i], res[:-1])
        return res[:-1]
   
    def str_interval(self):
        res = ""
        for intv in self.interval:
            res += f"{intv}/"
        return res
    
    def name_xp(self):
        files = [f.split("/")[-1] for f in glob.glob(f"{constants.PATH_XP}/*.csv")]
        tmp = []
        for f in files:
            if 'xp' in f:
                tmp.append(int(f[3:f.index("xp")]))
                
        name_res = f"res{max(tmp)+1}"

        spe = self.typeg.lower()
        nbf = 0
        name = f"{constants.PATH_XP}{name_res}xp0{spe}.csv"
        while os.path.isfile(name):
            nbf += 1
            name = f"{constants.PATH_XP}{name_res}xp{nbf}{spe}.csv"
        self.f = open(name, "w")
        print(f"Create file {name}")   
   
if __name__ == "__main__":
    int_variance = [10,20,30,40,50,60,70,80,90,100]
    # NB SOURCES
    # typeg = "BSA"; nombre_src = [10,20,30,40,50,60,70,80,90,100]; intv = ['60-65']; int_variance = nombre_src 
    # typeg = "BSA"; nombre_src = [10,20,30,40,50,100]; intv = ['60-64']; int_variance = nombre_src 
    typeg = "BSA"; nombre_src = [10,20,30,40,50,60,70,80,90,100]; intv = ['65-70']; int_variance = nombre_src 
    
    nbg = 100
    nb_litt = 3
    nbs = 40
    nbf = 15
    nbsubsetneeded = 1
    # Non complet
    not_full = True
    # Complet
    # not_full = False
    # norma_aposteriori = True = A - trust complet
    norma_aposteriori = True
    # norma_aposteriori = False = C - trust non complet
    # norma_aposteriori = False
    # nbs = 20
    # nbs = 50
    # nbs = 100
    
    generator = GenBelSynt(nbs=nbs, nbg=nbg, intvp=intv, typeg=typeg, 
                            int_variance=int_variance, nb_litt=nb_litt, nbf=nbf,
                            norma_aposteriori=norma_aposteriori, 
                            nbsubsetneeded=nbsubsetneeded,not_full=not_full)
    
    generator.generate_all()
    
    

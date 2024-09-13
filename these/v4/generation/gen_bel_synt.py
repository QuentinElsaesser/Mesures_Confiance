from v4.constants import constants

import random, os, glob#, math#, sys

# from collections import Counter

# from itertools import product

from datetime import datetime

# from random import randint

from itertools import combinations

class GenBelSynt:
    def __init__(self, nbs, nbg=1000, nbf=30, read_xp=False, typeg="BTU", intvp=['30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69'], int_variance=[0,10,20,30,40,50,60,70,80,90,100], nb_litt=3, norma_aposteriori=True, nbsubsetneeded=2):
        """
        int_variance : le nombre de sources qui change
        file : name of file with the proposition and the truth table (same format as a csv file)
        nbs : Number sources
        nbrelia : number of sources that should be reliable when we generate the graph (must be an integer <= nbs)
        nbg : number of graphs we want to generate (1000 by default)
        read_xp : True if called in read_xp class
        """
        self.nbs = nbs
        self.nbg = nbg
        self.nb_formula_togen = nbf
        
        self.norma_aposteriori = norma_aposteriori
        
        self.nbsubsetneeded = nbsubsetneeded
        
        self.typeg = typeg
        self.variance = 100

        self.interval = intvp
        self.fix_interval = None
        
        if typeg == constants.RUN_BSA or typeg == constants.RUN_BFA:
            self.interval = int_variance
            self.fix_interval = intvp[0]
            
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
        elif self.typeg == constants.RUN_BFA:
            for i in range(len(self.interval)):
                n = self.interval[i].split("-")
                if int(n[0]) <= self.nbo <= int(n[1]):
                    tmp = self.fix_interval.split("-")
                    if int(tmp[0]) <= t <= int(tmp[1]):
                        return i, self.interval[i]
        else:
            for i in range(len(self.interval)):
                n = self.interval[i]
                tmp = n.split("-")
                if int(tmp[0]) <= t <= int(tmp[1]):
                    return i, self.interval[i]
        return -1, None
        
    def add_dict(self, truth, claims, trust):
        ind,intv = self.find_interv(trust)
        if intv != None:        
            if self.nres[intv] < self.nbg:
                w = self.write(claims, trust, truth)
                self.res[intv].append(w)
                self.nres[intv] += 1
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
                # print("list des indices des formules possibles", list_formule_poss_agent)
                

                # lf = list(f)
                # tmp_para_1 = para[1]
                # if para[1] > len(lf):
                #     tmp_para_1 = len(lf)-1
                # # on prend les combi possible de 1 à n
                # for i in range(para[0], tmp_para_1):
                #     for n in combinations(lf, i+1):
                #         # print("set interpretation possible", n, truth in n)
                #         if self.truth in n:
                #             set_intp_pour_croyance.add(n)
                #         else:
                #             set_intp_pour_croyance_no_truth.add(n)
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
            # if para[1] > len(lf):
            #     tmp_para_1 = len(lf)-1
            # print("curr f", f)
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

        if len(set_intp_pour_croyance) <= self.nbsubsetneeded:
            return False
        
        if len(set_intp_pour_croyance_no_truth) <= self.nbsubsetneeded:
            return False

        # cherche les bonnes croyances si on veut guider lalea
        # if para[3]:
        xxxx = list()
        for x in list(set_intp_pour_croyance):
            if para[3]:
                if len(x) <= para[4]:
                    xxxx.append(x)
            else:
                xxxx.append(x)
        # if len(xxxx) == 0:
            # if para[4] > 1:
            #     xxxx = list()
            #     for x in list(set_intp_pour_croyance):
            #         if len(x) <= para[4]-1:
            #             xxxx.append(x)

        for i in range(self.nbs):
            self.formulas_agents.append([])
            self.claims.append([])
            dico_intp = dict()
            for x in self.interpretation:
                dico_intp[x] = 0

            if para[3]:
                if len(xxxx) > 0 and i < para[5]:
                    self.croyances.append(xxxx[random.randint(0, len(xxxx)-1)])
                else:
                    self.croyances.append(set_intp_pour_croyance_no_truth[random.randint(0, len(set_intp_pour_croyance_no_truth)-1)])
            elif para[3] == False:
                self.croyances.append(all_set_intp_pour_croyance[random.randint(0, len(all_set_intp_pour_croyance)-1)])
            
            poss_w_agent = []
            
            # for idfx2 in range(len(list_formule_poss_agent)):
            # pour cet agent, on regarde combien de formule il peut prendre 
            # au max selon ses croyances
            for idfx2 in list_formule_poss_agent:
                f = self.id_formulas[idfx2]
                if self.croyances[i].issubset(f):
                    poss_w_agent.append(idfx2)
                #     print("F POSSIBLE:", idfx2, f)
                # else:
                #     print("F PAS POSSIBLE:", idfx2, f)

            if len(poss_w_agent) < self.nbsubsetneeded:
                return False

            # nombre formule par sources
            if len(poss_w_agent) == self.nbsubsetneeded:
                nbf = self.nbsubsetneeded
            else:
                nbf = random.randint(self.nbsubsetneeded, len(poss_w_agent))
            # print("ADD NBF :", nbf)
            for x in range(nbf):
                v = random.randint(0, len(poss_w_agent)-1)
                # print("CHOIX", v, poss_w_agent, poss_w_agent[v], self.id_formulas[poss_w_agent[v]])
                idf = poss_w_agent[v]
                # if self.generated[j]:
                f = self.id_formulas[idf]
                # idf = self.formulas_id[str(sorted(f))]
                # print("FORMULA ?", f, idf, self.croyances[i], self.croyances[i].issubset(f))
                # if self.croyances[i].issubset(f):
                self.formulas_agents[i].append(f)
                self.claims[i].append(idf)
                self.took[idf] = True
                poss_w_agent.remove(idf)
                for intp in f:
                    dico_intp[intp] += 1   
            
            # print(len(self.claims[i]))
            # print("-- UPDATE CROYANCE ?", nbf, dico_intp, self.croyances[i])
            if len(self.formulas_agents[i]) > 1:
                for x in self.interpretation:
                    if dico_intp[x] == nbf:
                        self.croyances[i].add(x)
            # else:
            #     print("UNE SEUlE FOMRULE POUR AGENT", i)
            # print("-- New CROYANCE", self.croyances[i], truth)
            
        #     if para[3] == "d":
        #         good = 0
        #         total = int(len(self.id_formulas)/2)
        #         for j in range(len(self.claims[i])):
        #             idf = self.claims[i][j]   
        #             print(truth, self.id_formulas[idf])
        #             if truth in self.id_formulas[idf]:
        #                 good += 1
        #             # total += 1
        #         tmptrust = (good/total)*100
        #         print(tmptrust)
        #         if tmptrust <= para[4]:
        #             print(self.claims)
        #             goodd = False
        #             self.croyances.pop(i)
        #             self.formulas_agents.pop(i)
        #             self.claims.pop(i)
        #             print(self.claims, self.formulas_agents, self.croyances)
        #         print()
        #     print("fin, curr it", i)
        #     i += 1
        #     nbitcurr += 1
        #     if nbitcurr == 1000:
        #         break
        #     print()
        # print(truth)
        # print("--")
        # print(self.formulas_agents)
        # print("--")
        # print(self.claims)
        # print("trust fianle", self.compute_trust(self.claims, truth))

            
    def generate_votes_implication_full(self):
        """
        vote for a formula = id even (0,2,4,etc)
        vote against (or for the negation depending on what we do) = id odd (1,3,5,etc)
        """
        # print("VOTE FULL")
        for i in range(self.nbs):
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
        for i in range(self.nbs):
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

    def remove_unclaimed(self):
        res = dict()
        nbf = 0
        curr_f = 0
        go = False
        todel = []
        for i in range(0, len(self.took), 2):
            if not(self.took[i] or self.took[i+1]):
                go = True
                curr_f += 2
                todel.append(i+1)
                todel.append(i)
            else:
                res[curr_f] = nbf
                nbf += 1
                curr_f += 1
                res[curr_f] = nbf
                nbf += 1
                curr_f += 1
                
        # print("taille avant", len(self.id_formulas), len(self.generated))
        # print("todel", len(todel), todel)
        todel = sorted(todel, reverse=True)
        for indx in todel:
            self.generated.pop(indx)
            self.took.pop(indx)
        if go:
            # print("GO")
            claims = []
            for i in range(len(self.formulas_agents)):
                claims.append([])
                for j in range(len(self.formulas_agents[i])):
                    f = str(sorted(self.formulas_agents[i][j]))
                    idf = res[self.formulas_id[f]]
                    claims[-1].append(idf)
                claims[-1] = sorted(claims[-1])
            # print(res)    
            # print(claims)
            self.claims = claims
            
            # print(self.id_formulas)
            id_formulas = dict()
            for k in res:
                # print(k, res[k], self.id_formulas[res[k]])
                id_formulas[res[k]] = self.id_formulas[k]
            # print(self.id_formulas)
            # print(id_formulas)
            
            self.id_formulas = id_formulas
        # print("taille", len(self.id_formulas), len(self.generated))
        # print(self.id_formulas)
        # print(id_formulas)
        self.nbo = int(nbf/2)
        
   
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
        # print("truth", truth, len(self.id_formulas))
        total = int(len(self.id_formulas)/2)
        # for i in range(len(g)):
        #     total = max(total, len(g[i]))
        for i in range(len(g)):
            good = 0
            # print("Agent", i, g[i], self.croyances[i])
            for idf in g[i]:
                # print(truth, idf, sorted(self.id_formulas[idf]), truth in self.id_formulas[idf])
                # print(self.truth, self.id_formulas[idf], self.truth in self.id_formulas[idf])
                if self.truth in self.id_formulas[idf]:
                    good += 1
                # print(idf, self.formulas_id[idf], truth, truth in self.formulas_id[idf])
                # total += 1
            # print(good, total, (good/total)*100)
            # print()
            trust.append((good/total)*100)
        # print(trust, round(sum(trust)/self.nbs))
        return round((sum(trust)/self.nbs))
    
    def compute_trustC(self, g, truth):
        """trustC - verif si l'interpretation considerer comme la verite fait
        partie de chaque formule = proportion des formules qui sont vraies"""
        trust = []
        for i in range(len(g)):
            good = 0
            total = 0
            # print("Agent",i, g[i])
            for idf in g[i]:
                # print(truth, idf, self.id_formulas[idf], truth in self.id_formulas[idf])
                # print(self.truth, self.id_formulas[idf], self.truth in self.id_formulas[idf])
                if self.truth in self.id_formulas[idf]:
                    good += 1
                # print(idf, self.formulas_id[idf], truth, truth in self.formulas_id[idf])
                total += 1
            # print(good, total, (good/total)*100)
            # print()
            trust.append((good/total)*100)
        # print(trust, round(sum(trust)/self.nbs))
        return round((sum(trust)/self.nbs))
    
    # def compute_trust(self, g, truth):
    #     """ la verite (interpretation) doit etre dans le croyance
    #     profleme : on a que 100% puis 50% puis 33% etc"""
    #     trust = []
    #     for i in range(len(self.croyances)):
    #         good = 0
    #         total = 0
    #         for f in self.croyances[i]:
    #             if f == truth:
    #                 good += 1
    #             total += 1
    #         trust.append((good/total)*100)
    #         # print(self.croyances[i], truth, trust[i], self.formulas_agents[i])
    #         # print()
    #     return round((sum(trust)/self.nbs))
    
    def generate_all(self):
        type_generation = ""
        para = [0,3,5,False,1,0]
        runit = 0
        it = 1000
        total = 0
        while not all(self.valid) and type_generation != "e": 
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
                tmp = input(f"{datetime.now().strftime('%H:%M:%S')} - nb it (curr {it}) ?")
                if tmp != "":
                    if tmp.isnumeric():
                        it = int(tmp)
                    else:
                        it = 1
                if self.typeg == constants.RUN_BSA:
                    tmp = input("target number of sources ?")
                    if tmp != "":
                        if tmp.isnumeric():
                            self.nbs = int(tmp)
                elif self.typeg == constants.RUN_BFA:
                    tmp = input("target number of formulae ?")
                    if tmp != "":
                        if tmp.isnumeric():
                            self.nb_formula_togen = int(tmp)
                # else:
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
            
            for i in range(it):
                runit += 1
                self.truth = self.interpretation[random.randint(0,self.len_interpretation-1)]
                
                # genere croyances et formules des agents
                error = self.generate_formulas(self.truth, para)
                # self.generate_formulas_OK()
                
                if error != False:
                
                    if self.typeg == constants.RUN_BIF:
                        self.generate_votes_implication_full()
                    elif self.typeg == constants.RUN_BIA or self.typeg == constants.RUN_BFA or self.typeg == constants.RUN_BSA:
                        self.generate_votes_implication_abs()
    
                    # self.remove_unclaimed()
                    self.nbo = int(self.curr_id_f/2)
                    
                    self.facts = [[i for i in range(n*2,n*2+2)] for n in range(self.nbo)]
                    self.OF = self.list_of()
                
                if len(self.claims) == self.nbs:
                    trust = self.compute_trust(self.claims, self.truth)
                    if trust in trust_gen:
                        trust_gen[trust] += 1
                    else:
                        trust_gen[trust] = 1

                    if self.add_dict(self.truth, self.claims, trust) != "":
                        # stocke la trust du graphe conserve
                        total += trust
                    if all(self.valid):
                        break
                if runit % 50000 == 0:
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
    # intv = ['30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74']
    # intv = ['40-44','45-49','50-54','55-59','60-64']
    # intv = ['45-49','50-54','55-59','60-64','65-69','70-74']
    # intv = ['45-49','50-54','55-59']
    # intv = ['0-99']
    # intv = ['35-39','40-44','45-49','50-54','55-59','60-64','65-69']
    # intv = ['40-44','45-49','50-54','55-59','60-64','65-69']
    
    # 2eme facon de faire la trust = pas une seule interpretation comme le vrai monde 
    # Mais sur chaque formule, on donne la bonne valeur comme etant la verité
    # Version complet
    # typeg = "BCF"
    # Version non complet
    # typeg = "BCA"
    
    # implication avec grpahe complet 
    # typeg = "BIF"; intv = ['35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79']
    # implication avec grpahe NON complet 
    typeg = "BIA"; intv = ['35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79']
    
    
    # typeg = "BIA"; intv = ['35-39','40-44','45-49','50-54']
    # typeg = "BIA"; intv = ['55-59','60-64','65-69','70-74','75-79']
    # typeg = "BIA"; intv = ['65-69']
    # typeg = "BIA"; intv = ['55-59']
    # typeg = "BIA"; intv = ['50-54']
    # typeg = "BIA"; intv = ['70-74','75-79']
    
    # NB FORMULES
    # typeg = "BFA"; nombre_formule = ["6-10","11-15","16-20","21-25","26-30"]; intv = ['65-69']; int_variance = nombre_formule
    
    nbg = 1000
    nb_litt = 3
    nbs = 10
    nbf = 15
    nbsubsetneeded = 3
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
                            nbsubsetneeded=nbsubsetneeded)
    
    generator.generate_all()
    
    
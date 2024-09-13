# import numpy as np

from v4.graph import graph

# from operator import itemgetter
# from itertools import groupby

# from v4.vote import normalize as nm

# from v4.graph import obj

# from copy import deepcopy

# from collections import Counter

# from v4.graph import derive

class Base():
    """
    Dans le modele :
        INDEX start with 0 / ID start with 1
        1 in assignement = fact with index odd (1-3-5) OR fact with id even (2-4-6)
        0 in assignement = fact with index even (0-2-4) OR fact with id odd (1-3-5)
    """
    def __init__(self, mat_fs, mat_of, voting_met, vote_para, name_norma, nb_s, nb_f, init_trust=1,truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None,model=[],Gr=None,form=None,vect=None,revres=None,maj_form=None,maj_formSF=None,nom_agenda=None):
        """
        Gr = 
        """
        self.nom_agenda = nom_agenda
        
        if Gr==None:
            # G = derive.Derive(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met,
            #                   vote_para=vote_para, name_norma=name_norma, 
            #                   nb_s=nb_s, nb_f=nb_f, truth=truth, normalizer=normalizer,
            #                   trust_f=trust_f, long=long, gobj=gobj,sf=sf)
            
            G = graph.Graph(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                          vote_para=vote_para, name_norma=name_norma, 
                          nb_s=nb_s, nb_f=nb_f, truth=truth, trust_s=trust_s,
                          init_trust=init_trust,normalizer=normalizer,
                          trust_f=trust_f,long=long,gobj=gobj,sf=sf)
        else:
            if isinstance(Gr, graph.Graph):
                G = Gr
            else:
            # ne pas recreer le graph si pas besoin
                G = Gr.G

        self.G = G
        self.truth = truth
        self.truth_form = self.c01_to_form(self.truth)
        
        self.truth_eq_maj = False
        # distance minimal qu'il y a entre les assignements possibles et la majorité
        self.distance_min_maj = dict()
        self.nbmax = 0
        self.truth_found = False
        self.answers = []
        self.alg_consistent = False
        self.maj_consistent = False
        
        self.test = []
        
        # start with 0
        self.model = model
                
    def gen_revres(self):
        """
        POUr SFJA, utilise la trust et pas le nombre de support 
        """
        revres = dict()
        maj_form = []
        maj_formSF = []
        for i in range(len(self.G.obj.of)):
            o = self.G.obj.of[i]
            
            if o.prec[0].nb_prec > o.prec[1].nb_prec:
                maj_form.append("n"+str(i+1))
            elif o.prec[0].nb_prec < o.prec[1].nb_prec:
                maj_form.append(str(i+1))
            else:
                maj_form.append(f"*{i+1}")
            
            if o.prec[0].trust > o.prec[1].trust:
                maj_formSF.append("n"+str(i+1))
            elif o.prec[0].trust < o.prec[1].trust:
                maj_formSF.append(str(i+1))
            else:
                maj_formSF.append(f"*{i+1}")
                
            for j in range(len(o.prec)):
                # self.support.append(o.prec[j].nb_prec)
                v = o.prec[j].trust#/maxv
                if j == 0:
                    txt = "n"+str(i+1)
                else:
                    txt = str(i+1)
                revres[txt] = v
        self.truth_eq_maj = maj_form == self.truth_form
        return revres, maj_form, maj_formSF
        
    def asso(self, read=False):
        res = []
        for l in self.model:
            tmp = []
            for i in range(len(l)):
                if l[i] == 0:
                    tmp.append(f"n{i+1}")
                else:
                    tmp.append(f"{i+1}")
            res.append(tmp)
            dtmp = self.distance(self.maj_form, tmp)
            if dtmp in self.distance_min_maj:
                self.distance_min_maj[dtmp] += 1
            else:
                self.distance_min_maj[dtmp] = 1
            if tmp == self.maj_form:
                self.maj_consistent = True
                if read:
                    return
        if read:
            return
        res2 = []
        for l in res:
            tmp2 = []
            for v in l:
                tmp2.append(round(self.revres[v],3))
            res2.append(tmp2)
        
        # for i in range(len(res)):
        #     print(i, res[i], res2[i])
        # print("MAJORITE :", self.maj_form)
    
        return res, res2
    
    def distance(self, l, f):
        res = 0
        for i in range(len(f)):
            if l[i] != f[i]:
                res += 1
        return res
    
    def find_max(self, liste, index):
        maxv = liste[0][index]
        vals = [liste[0]]
        for i in range(1, len(liste)):
            if maxv < liste[i][index]:
                vals = [liste[i]]
                maxv = liste[i][index]
            elif maxv == liste[i][index]:
                vals.append(liste[i])
        return vals
    
    def form_to_01(self, f):
        res = []
        for v in f:
            if v[0] == 'n':
                res.extend([1,0])
            else:
                res.extend([0,1])
        return res
    
    def c01_to_form(self, f):
        """
        ensemble de 0,1 avec nb_formule*2 elements 
        
        Dans le modele :
            INDEX start with 0 / ID start with 1
            1 in interpretation = fact with index odd (1-3-5) OR fact with id even (2-4-6)
            0 in interpretation = fact with index even (0-2-4) OR fact with id odd (1-3-5)
        """
        res = []
        o = 1
        for i in range(0, len(f), 2):
            if f[i] == 1:
                res.append(f"n{o}")
                # res.append(i*1)
            else:
                res.append(f"{o}")
                # res.append((i*1)+1)
            o += 1
        return res
    
    def results(self, maxinds, reprr=None):
        # if reprr != None:
        #     print()
        #     print(reprr)
        
        if self.maj_consistent:
            # juste pour notre algo
            self.alg_consistent = (self.maj_formSF in self.form)
        
        # self.G.trust_f = [0 for n in range(len(self.truth_form)*2)]
        
        for maxind in maxinds:
            self.answers.append(self.form[maxind])
        
        self.nbmax = len(self.answers)
        
        for ans in self.answers:
            if ans == self.truth_form:
                self.truth_found = True
                
        # self.G.obj.update_trust(self.G.trust_f)
        # self.G.obj.voting()
        # self.G.trust_sources()
        # self.G.normalize_trust()
                
        # print("truth:", self.truth_form, "->", self.truth_found)
        # print("majo:", self.maj_form)
        # print("truth:", self.truth_form)
        # print("reponses:")
        # for i,n in enumerate(self.answers):
        #     print(maxinds[i], n)


        
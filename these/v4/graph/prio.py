from v4.graph import graph

from v4.constants import constants

from operator import itemgetter
from itertools import groupby

from copy import deepcopy

from numpy.linalg import norm

import numpy as np

# from scipy.spatial import distance

class Prio(graph.Graph):
    def __init__(self, voting_met, vote_para, name_norma, G=None, mat_fs=[], mat_of=[], nb_s=0, nb_f=0, truth=[],normalizer=None,trust_s=None,trust_f=None,long=False):        
        """
        - On a r(s)^i au début (iteration i) = self.mem[0]
        - on calcul la valeur qu'on est censé avoir si on change totalement la trust (on note score(s)) = self.trust_s
        - on update r(s)^i avec delta selon la valeur obtenu avec score(s) (stocké dans self.trust_s)
        """
        if G != None:
            super().__init__(mat_fs=G.mat_fs, mat_of=G.mat_of, voting_met=voting_met, 
                             vote_para=vote_para, name_norma=name_norma, 
                             nb_s=len(G.sf), nb_f=len(G.mat_of[0]), truth=G.obj.truth,
                             trust_s=deepcopy(trust_s), init_trust=1.0, gobj=deepcopy(G.obj),
                             sf=deepcopy(G.sf)
                             )            
        else:
            super().__init__(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                             vote_para=vote_para, name_norma=name_norma, 
                             nb_s=nb_s, nb_f=nb_f, truth=truth, trust_s=trust_s,
                             init_trust=1.0
                             )

        self.max_it = 100
        self.startit = False
        # number of iterations before adding a new rank
        self.X = 2
        # vote only on the obj rank at the N_rank th position
        self.N_rank = 1
        # object used
        self.object_used = []
        # dico
        self.dico = dict()
        for o in self.obj.of:
            for f in o.prec:
                self.dico[f] = o
        self.src_obj = []
        for i in range(len(self.sf)):
            self.src_obj.append([])
            for j in range(len(self.sf[i])):
                if self.sf[i][j] == 1:
                    for k in range(len(self.mat_of)):
                        if self.mat_of[k][j] == 1:
                            self.src_obj[i].append(k+1)
                
    def get_rank_facts(self, reverse=True):
        """
        return the ranking for the facts
        """
        trust = []
        for n in self.obj.facts:
            trust.append(n.trust)
        res = list(zip(self.obj.facts, trust))
        res.sort(reverse=reverse, key=itemgetter(1))

        rank = [[res[0]]]
        length = len(res)
        for i in range(1, length):
            if res[i][1] == rank[-1][0][1]:
                rank[-1].append(res[i])
            else:
                rank.append([res[i]])
        return rank
                
    def choose_object(self):
        """
        """
        res = []
        liste = self.get_rank_facts()
        for i in range(min(self.N_rank, len(liste))):
            for f in liste[i]:
                if self.dico[f[0]] not in res:
                    res.append(self.dico[f[0]])
        self.object_used.append((res, self.N_rank))
        return res
    
    def normalize_trust(self):
        for i in range(len(self.trust_s)):
            if self.normalizer.name == constants.NORMA_A:
                self.trust_s[i] = self.trust_s[i] / (len(self.object_used[-1][0]) * self.obj.voting_met.max_value)
            elif self.normalizer.name == constants.NORMA_O:
                tmp_nb_obj = len(set(self.src_obj[i]).intersection(set([n.id for n in self.object_used[-1][0]])))
                if tmp_nb_obj == 0:
                    self.trust_s[i] = 0
                else:
                    self.trust_s[i] = self.trust_s[i] / (tmp_nb_obj * self.obj.voting_met.max_value)
                
            
    def false_str_trust(self):
        """
        """
        res = self.print_iteration()
        res += self.str_trust_s() + "\n"
        # res += self.obj.str_trust_f() + "\n"
        
        if self.iteration > 0:
            # res += self.str_sources()
            res += self.obj.str_object() + "\n"
        #CONFIG
        self.print_config()
            
        res += "\n-------\n"
        return res

    def voting(self):
        """
        choose the obj where we do the vote
        """
        self.obj.reset_score()
        for n in self.choose_object():
            name = []
            trust = []
            rank = []
            for f in n.prec:
                name.append(f)
                trust.append(f.trust)
                ziped = list(zip(name, trust))
                ziped.sort(reverse=True, key = itemgetter(1))
                groups = groupby(ziped, itemgetter(1))
                rank = [[item[0] for item in data] for (key, data) in groups]
                
            # COND pour choisir les objets
                
            self.obj.voting_met.execute(rank)
            #print("\nDans voting de obj.py")
            #for f in n.prec:
                #print(f, "-", f.score, [f.nb_prec])
            #print()

    def convergence(self):
        """
        Check the convergence of the cosine similarity
        """
        if len(self.object_used) <= 0:
            return False
        if len(self.object_used[-1][0]) < len(self.mat_of):
            return False
        if not self.startit:
            self.startit = True
            self.max_it += self.iteration
        if self.iteration > self.max_it:
            print("Infinite Loop / Bug")
            print("Unknown error")
            print(f"Method : Prio - {self.obj.voting_met} - {self.normalizer.name}")
            print(self)
            print(self.str_trust())
            print("\nGraph links :")
            print(self.to_file())
            return True
        old = self.mem[1]
        current = self.mem[0]
        if sum(old) == 0 or sum(current) == 0:
            print("Infinite Loop / Bug")
            print("Trust of all elements is null, no facts claimed")
            print(f"Method : Prio - {self.obj.voting_met} - {self.normalizer.name}")
            print(self)
            print(self.str_trust())
            print("\nGraph links :")
            print(self.to_file())
            return True
        # eucli = distance.euclidean(current, old)
        
        # numpy.norm = euclidean distance
        eucli = norm(np.array(current)-np.array(old))
        epsilon = 0.001
        if eucli <= epsilon:
            return True
        return False
    
    def run(self):
        """
        Run the algorithm
        update the trust of fact
        execute the vote
        update the trust of the sources
        """
        print(self.str_trust())
        while not self.convergence():
            self.iteration += 1
            
            if self.iteration % 2 == 0:
                self.N_rank += 1
                
            self.trust_fact()
            self.obj.update_trust(self.trust_f)
            self.voting()
            print("Object :", [n.id for n in self.object_used[-1][0]], f"sur {self.N_rank} rangs")
            print(self.str_trust())
            self.trust_sources()
            self.normalize_trust()
            self.update_mem()
            
    def run_noprint(self):
        """
        Run the algorithm
        update the trust of fact
        execute the vote
        update the trust of the sources
        """
        while not self.convergence():
            self.iteration += 1
            
            if self.iteration % 2 == 0:
                self.N_rank += 1
                
            self.trust_fact()
            self.obj.update_trust(self.trust_f)
            self.voting()
            self.trust_sources()
            self.normalize_trust()
            self.update_mem()
            
            
            
            
from v4.graph import graph

# from scipy.spatial import distance

from numpy.linalg import norm

from copy import deepcopy

import numpy as np

class Derive(graph.Graph):
    def __init__(self, voting_met, vote_para, name_norma, G=None, mat_fs=[], mat_of=[], nb_s=0, nb_f=0, truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None):
        """
        - On a r(s)^i au début (iteration i) = self.mem[0]
        - on calcul la valeur qu'on est censé avoir si on change totalement la trust (on note score(s)) = self.trust_s
        - on update r(s)^i avec delta selon la valeur obtenu avec score(s) (stocké dans self.trust_s)
        """
        if G != None:
            super().__init__(mat_fs=G.mat_fs, mat_of=G.mat_of, voting_met=voting_met, 
                             vote_para=vote_para, name_norma=name_norma, 
                             nb_s=len(G.sf), nb_f=len(G.mat_of[0]), truth=G.obj.truth,
                             trust_s=deepcopy(trust_s), init_trust=0.5, gobj=deepcopy(G.obj),
                             sf=deepcopy(G.sf)
                             )         
        else:
            super().__init__(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                             vote_para=vote_para, name_norma=name_norma, 
                             nb_s=nb_s, nb_f=nb_f, truth=truth, trust_s=trust_s,
                             init_trust=0.5, gobj=gobj, sf=sf
                             )
        self.max_it = 100
        self.delta = 0.1
        self.epsilon = 0.001
        
    def update_trust_s(self):
        """
        if (score(s) - r(s)^i) > 0 then r(s) += delta
        else (score(s) - r(s)^i) < 0 then r(s) -= delta
        else (score(s) - r(s)^i) = 0 then r(s) += 0
        """
        current = self.mem[0]
        for i in range(len(self.trust_s)):
            diff = self.trust_s[i] - current[i]
            if diff > 0:
                tmp = current[i] + self.delta
                self.trust_s[i] = tmp if tmp <= self.trust_s[i] else self.trust_s[i]
            elif diff < 0:
                tmp = current[i] - self.delta
                self.trust_s[i] = tmp if tmp <= self.trust_s[i] else self.trust_s[i]
                
            if self.trust_s[i] > 1.0:
                self.trust_s[i] = 1.0
            if self.trust_s[i] < 0.0:
                self.trust_s[i] = 0.0
            
    def convergence(self):
        """
        Check the convergence of the cosine similarity
        """
        if len(self.mem) < 2:
            return False
        if self.iteration > self.max_it:
            print("Infinite Loop / Bug")
            print("Unknown error")
            print(f"Method : Derive - {self.obj.voting_met} - {self.normalizer.name}")
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
            print(f"Method : Derive - {self.obj.voting_met} - {self.normalizer.name}")
            print(self)
            print(self.str_trust())
            print("\nGraph links :")
            print(self.to_file())
            return True
        
        # eucli = distance.euclidean(current, old)
        # numpy.norm = euclidean distance
        eucli = norm(np.array(current)-np.array(old))
        if eucli <= self.epsilon:
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
            self.trust_fact()
            self.obj.update_trust(self.trust_f)
            self.obj.voting()
            print(self.str_trust())
            self.trust_sources()
            self.normalize_trust()
            self.update_trust_s()
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
            self.trust_fact()
            self.obj.update_trust(self.trust_f)
            self.obj.voting()
            self.trust_sources()
            self.normalize_trust()
            self.update_trust_s()
            self.update_mem()
            
            
            
            
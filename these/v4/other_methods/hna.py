import math
import numpy as np
from numpy.linalg import norm

class Hna:
    def __init__(self, G):
        self.init_trust = 1.0
        
        self.G = G
        self.G.reset_graph([self.init_trust for i in range(len(self.G.mat_fs[0]))])
        
    def trust_sources(self):
        """
        Compute the trust for the sources
        """
        tmp_trust_s = [0 for i in self.G.trust_s]
        for i in range(len(self.G.trust_s)):
            tmp_trust_s[i] = sum(self.G.sf[i]*self.G.trust_f)
        self.G.trust_s = tmp_trust_s
        
    def trust_fact(self):
        """
        Compute the trust for the facts
        """
        tmp_trust_f = [0 for i in self.G.trust_f]
        for i in range(len(self.G.trust_f)):
            tmp_trust_f[i] = sum(self.G.mat_fs[i]*self.G.trust_s)
        self.G.trust_f = tmp_trust_f

    def convergence(self):
        if len(self.G.mem) < 2:
        # if self.G.iteration < 2:
            return False
        if self.G.iteration > 100:
            print("Infinite Loop / Bug")
            print("Unknown error")
            print(f"Method : HNA - {self.G.obj.voting_met} - {self.G.normalizer.name}")
            print(self.G)
            print(self.G.str_trust())
            print("\nGraph links :")
            print(self.G.to_file())
            return True
        old = self.G.mem[1]
        current = self.G.mem[0]
        if sum(old) == 0 or sum(current) == 0:
            print("Infinite Loop / Bug")
            print("Trust of all elements is null, no facts claimed")
            print(f"Method : HNA - {self.G.obj.voting_met} - {self.G.normalizer.name}")
            print(self.G)
            print(self.G.str_trust())
            print("\nGraph links :")
            print(self.G.to_file())
            return True
        
        cos_sim = np.dot(current, old) / (norm(current)*norm(old))
        epsilon = 0.001
        if 1-cos_sim <= epsilon:
            return True
        return False
        
    def run(self):
        print(self.G.str_trust())
        while not self.convergence():
            self.G.iteration += 1
            
            norm = 0
            self.trust_fact()
            norm = sum([f**2 for f in self.G.trust_f])
            norm = math.sqrt(norm)
            for i in range(len(self.G.trust_f)):
                self.G.trust_f[i] /= norm
            self.G.obj.update_trust(self.G.trust_f)
            
            norm = 0
            self.trust_sources()
            norm = sum([s**2 for s in self.G.trust_s])
            norm = math.sqrt(norm)
            for i in range(len(self.G.trust_s)):
                self.G.trust_s[i] /= norm
                
            self.G.update_mem()
            print(self.G.str_trust())
            
    def run_noprint(self):
        while not self.convergence():
            self.G.iteration += 1
            
            norm = 0
            self.G.trust_fact()
            norm = sum([f**2 for f in self.G.trust_f])
            norm = math.sqrt(norm)
            for i in range(len(self.G.trust_f)):
                self.G.trust_f[i] /= norm
            self.G.obj.update_trust(self.G.trust_f)
            
            norm = 0
            self.trust_sources()
            norm = sum([s**2 for s in self.G.trust_s])
            norm = math.sqrt(norm)
            for i in range(len(self.G.trust_s)):
                self.G.trust_s[i] /= norm
                
            self.G.update_mem()
            
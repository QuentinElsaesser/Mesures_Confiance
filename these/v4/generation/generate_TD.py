from v4.constants import constants

import random, os, glob#, sys

# from collections import Counter

# from itertools import product

# from random import randint

class GenerateTD:
    def __init__(self, nbs, nbg=1000, nbo=10, nbfu=2, read_xp=False, typeg="TDP", type_generation="n", intvp=['30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69']):
        """
        file : name of file with the proposition and the truth table (same format as a csv file)
        nbs : Number sources
        nbrelia : number of sources that should be reliable when we generate the graph (must be an integer <= nbs)
        nbg : number of graphs we want to generate (1000 by default)
        read_xp : True if called in read_xp class
        """
        self.nbs = nbs
        self.nbg = nbg
        
        self.type_generation = type_generation
        self.typeg = typeg
        self.variance = 100

        self.interval = intvp

        self.res = dict()
        self.nres = dict()
        self.valid = []
        for i in self.interval:
            self.res[i] = []
            self.nres[i] = 0
            self.valid.append(False)
        
        self.f = None
  
        self.nbo = nbo
        self.facts = []
        curr_f = 0
        for i in range(self.nbo):
            self.facts.append([])
            for j in range(nbfu):
                self.facts[-1].append(curr_f)
                curr_f += 1

        self.dico = dict()
        if not read_xp:
            self.OF = self.list_of()
    
    def generate_truth(self):
        """
        do not take the negation if they are chosen
        """
        t = []
        for f in self.facts:
            t.append(f[random.randint(0, len(f)-1)])
        return t
    
    def generate_claims(self, nbs):
        """
        generate one graph where the source's claims are chosen randomly
        """
        s = []
        for i in range(nbs):
            tmp = []
            for f in self.facts:
                tmp.append(f[random.randint(0, len(f)-1)])
            s.append(tmp)
        return s
    
    def generate_claims_trustful(self, nbs, truth):
        """
        draw with trust > 0.5
        """
        s = []
        f = [j for j in range(len(self.facts[0]))]
        for i in range(nbs):
            res = []
            n = int(self.nbo / 2)
            if n <= (self.nbo / 2):
                n += 1
            n = random.randint(n, self.nbo)
            choices = [1 for j in range(n)] + [0 for j in range(self.nbo-n)]
            random.shuffle(choices)
            for j in range(len(choices)):
                if choices[j] == 1:
                    res.append(truth[j])
                else:
                    ftmp = f[:]
                    ftmp.remove(self.facts[j].index(truth[j]))
                    r = random.randint(0, len(ftmp)-1)
                    res.append(self.facts[j][ftmp[r]])
            s.append(res)
        return s
        
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
                    
        return f"TYPEG;VARIANCE;NB_OBJ;NB_SRC;NB_FL;NB_FU;NBF;TRUST;SF;OF;TRUTH;INTERVAL:{self.str_interval()};{self.typeg}_{trust}-{trust}\n"
        
    def write(self, graph, trust, truth):        
        return f"cpr;{self.variance};{self.nbo};{self.nbs};{2};{2};{self.nbo*2};{trust};{self.list_sf(graph)};{self.OF};{self.list_truth(truth)};;\n"
    
    def compute_trust(self, g, truth):
        """
        """
        good = 0
        total = 0
        for s in g:
            for i in range(len(s)):
                if s[i] == truth[i]:
                    good += 1
                total += 1    
        return round((good/total)*100)
    
    def find_interv(self, t):
        if self.typeg == constants.RUN_TDP:
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
    
    def generate_all(self):
        p = ""
        runit = 0
        it = 1000
        total = 0
        while not all(self.valid) and p != "e": 
            #affichage
            res = ""
            keys = list(self.nres.keys())
            for i in range(len(keys)):
                res += f"\033[31m{keys[i]}\033[00m:\033[32m{self.nres[keys[i]]}\033[00m / "
            res += "\n"
            
            if not all(self.valid):
                # curr para
                print(runit, "\n", res)
                # ask nb it
                tmp = input(f"nb it (curr {it}) ?")
                if tmp != "":
                    it = int(tmp)
                # option pour la generation
                if self.typeg == constants.RUN_TDP:
                    tmp = input("e(=exit)?")
                    if tmp != "":
                        p = tmp
                print()
            trust_gen = dict()
            for i in range(it):
                runit += 1
                truth = self.generate_truth()
                
                # generation des claims
                if self.type_generation == "n":
                    claims = self.generate_claims(self.nbs)
                elif self.type_generation == "u":
                    claims = self.generate_claims_trustful(self.nbs, truth)
                
                if len(claims) == self.nbs:
                    trust = self.compute_trust(claims, truth)
                    # on stock la trust de tous les grpahs generer
                    if trust in trust_gen:
                        trust_gen[trust] += 1
                    else:
                        trust_gen[trust] = 1
                    if self.add_dict(truth, claims, trust) != "":
                        # stocke la trust du graphe conserve
                        total += trust
                        ### affichage ###
                        # print("truth", truth)
                        # for c in claims:
                        #     print(c, self.compute_trust([c], truth))
                        # print("trust", trust)
                        ### affichage ###
                    if all(self.valid):
                        break
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
        res = ""
        for i in range(len(truth)):
            res += f"{truth[i]}-"
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
    # GENERATION OPTI
    typeg = "TDP"
    intv = ['35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74']
    # intv = ['0-100']
    
    # intv = ['65-69','70-74','75-79','80-84','85-89','90-94']

    nbf = 2
    nbo = 10
    nbg = 1000
    nbs = 10
    # "Type Gen : n(normal), u(>50%)"
    # type_gen = "u"
    type_gen = "n"
    
    generator = GenerateTD(nbs=nbs, nbg=nbg, intvp=intv, typeg=typeg, nbo=nbo, nbfu=nbf, 
                           type_generation=type_gen)
    generator.generate_all()
    
    
    
        
    
    
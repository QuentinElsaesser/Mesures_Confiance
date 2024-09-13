from v4.constants import constants

import random, os, glob, sys

from collections import Counter

from itertools import product

from random import randint

class GenerateWProp:
    def __init__(self, file, nbs, nbg=1000, read_xp=False, typeg="PRP", intvp=['30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69'], int_variance=[0,10,20,30,40,50,60,70,80,90,100], distrib="", gen_agenda=False, nb_litt=10, nb_form=10):
        """
        file : name of file with the proposition and the truth table (same format as a csv file)
        nbs : Number sources
        nbrelia : number of sources that should be reliable when we generate the graph (must be an integer <= nbs)
        nbg : number of graphs we want to generate (1000 by default)
        read_xp : True if called in read_xp class
        """
        self.name_file = f"{file}"
        self.file = f"{constants.PROP_PATH}{file}.txt"
        self.nbs = nbs
        self.nbg = nbg
        
        if typeg == constants.RUN_SDR and distrib == "":
            raise ValueError("ERROR NO DISTRIB")
        self.distrib = distrib
        
        self.typeg = typeg
        self.variance = 100
        
        if (self.typeg == constants.RUN_VRN or self.typeg == constants.RUN_SPR or self.typeg == constants.RUN_SDR) and len(intvp) > 1:
            raise ValueError(f"only one interval should be given with VRN generation but {len(intvp)} were given")
        
        if self.typeg == constants.RUN_VRN or self.typeg == constants.RUN_SPR or self.typeg == constants.RUN_SDR:
            self.fixed_prc = intvp[0]
            self.interval = int_variance
        else:
            self.interval = intvp
            # self.maxmin = [int(intvp[0].split("-")[0]), int(intvp[-1].split("-")[1])]
        
        # self.txt = ""
        self.res = dict()
        self.nres = dict()
        self.valid = []
        for i in self.interval:
            self.res[i] = []
            self.nres[i] = 0
            self.valid.append(False)
            
        self.dico73 = dict()
        self.dicoddd = dict()
            
        #model = assignements sur les objets
        self.prop = ""
        self.model = []
        self.model_doublon01 = []
        self.nb_unique = 0

        self.curr_num_agenda = 0
        self.dir_agenda = 0
        
        self.agenda_interp = ""
        self.len_agenda_interp = 0
        
        self.header_agenda = ""
        self.assign_agenda = []
        
        self.f = None
        
        self.gen_agenda = gen_agenda
        
        if not self.gen_agenda:      
            self.nb_litt = 0
            self.nbo = 0
            self.read_file()
            self.facts = [[i for i in range(n*2,n*2+2)] for n in range(self.nbo)]
            # model avec les id faits à la place des 1 ou 0
            self.modelf = self.interp_f(self.model)
            self.modelf_doublon = self.interp_f(self.model)
        else:
            self.file = ""
            self.nb_litt = nb_litt
            self.nbo = nb_form
            self.facts = [[i for i in range(n*2,n*2+2)] for n in range(self.nbo)]
        self.dico = dict()
        
        if not read_xp:
            self.OF = self.list_of()
            # self.truth = self.list_truth()
            
    def distance_agenda(self, intp, truew, du, dl):
        tmp = 0
        for i in range(len(truew)):
            if intp[i] != truew[i]:
                tmp += 1
            if tmp > du:
                return False,tmp
        return tmp>=dl,tmp
    
    def generate_agenda(self):
        """
        generate all the interpretations possible for an certain number of literals
        we generate N random formula which are composed of M literals
        On tire au hasard une interpretation comme étant la vérité, 
        on choisit une distance entre 0 et DU (0;nb_litt-1) et 
        toutes les interpretations ayant une distance comrpise entre 0 et DU 
        sont modeles de la formule
        """
        if self.agenda_interp == "":
            # all interpretations possible
            self.agenda_interp = list(product(['1','0'], repeat=self.nb_litt))
            self.len_agenda_interp = len(self.agenda_interp)
        # solution
        self.assign_agenda = []
        for l in self.agenda_interp:
        	self.assign_agenda.append([])
        # numbers
        numbers = []
        self.model = []
        self.model_doublon01 = []
        self.nb_unique = 0
        self.modelf = []
        self.modelf_doublon = []
        
        min_value = 4
        max_value = 5
        # max_value = self.nb_litt-1

        for i in range(self.nbo):
            n = randint(0, self.len_agenda_interp-1)
            du = randint(min_value, max_value)
            dl = 0
            truew = self.agenda_interp[n]
            txt = f"{dl}:{du}/{','.join(truew)}"
            # retire les doublons pour pas avoir les mêmes formules
            while txt in numbers:
                n = randint(0, self.len_agenda_interp-1)
                du = randint(min_value, max_value)
                dl = 0
                truew = self.agenda_interp[n]
                txt = f"{dl}:{du}/{','.join(truew)}"
            numbers.append(txt)
            for j in range(self.len_agenda_interp):
                if self.distance_agenda(self.agenda_interp[j], truew, du, dl)[0]:
                    self.assign_agenda[j].append(1)
                else:
                    self.assign_agenda[j].append(0)
        self.header_agenda = f"{self.nb_litt} - {';'.join(numbers)}\n"
        self.prop = [str(val) for val in numbers]
        
        for i in range(self.len_agenda_interp):
            self.model_doublon01.append(self.assign_agenda[i])
            if self.assign_agenda[i] not in self.model: # ignore doublon potentiel
                self.model.append(self.assign_agenda[i])
                self.nb_unique += 1
        self.model = sorted(self.model, reverse=True)
        self.model_doublon01 = sorted(self.model_doublon01, reverse=True)
        
    def write_agenda(self):  
        f = open(self.file, "w")
        f.write(self.header_agenda)
        tmp = ""
        for i in range(self.len_agenda_interp):
            l = self.agenda_interp[i]
            txt = [str(v) for v in self.assign_agenda[i]]
            tmp += f"{';'.join(l)};{';'.join(txt)}\n"
        f.write(tmp)
        f.close()
    
    def write_header(self, trust, distrib):
        """
        trust : average trust for the self.nbg graphs generated
        """
        delete = []
        for i in range(len(self.interval)):
            if not self.valid:
                delete.append(self.interval[i])
                for d in delete:
                    self.interval.remove(d)
        if self.typeg == constants.RUN_VRN or self.typeg == constants.RUN_SPR or self.typeg == constants.RUN_SDR:
            n = self.fixed_prc.split("-")
            trust1 = int(n[0])
            trust2 = int(n[1])
        else:
            trust1 = trust
            trust2 = trust
        if self.gen_agenda:
            return f"TYPEG;VARIANCE;NB_OBJ;NB_SRC;NB_FL;NB_FU;NBF;TRUST;SF;OF;TRUTH;INTERVAL:{self.str_interval()};{self.typeg}_{trust1}-{trust2}_AGENDAG_{self.nbo}_distrib{self.str_dist(distrib)}\n"
        return f"TYPEG;VARIANCE;NB_OBJ;NB_SRC;NB_FL;NB_FU;NBF;TRUST;SF;OF;TRUTH;INTERVAL:{self.str_interval()};{self.typeg}_{trust1}-{trust2}_{self.name_file}_{'-'.join(self.prop)}_distrib{self.str_dist(distrib)}\n"
        
    def write(self, graph, trust, truth):
        if self.gen_agenda:
            if self.file == "":
                nbf = 1
                name = f"{constants.PROP_PATH}/{self.dir_agenda}/prop{nbf}.txt"
                while os.path.isfile(name):
                    nbf += 1
                    name = f"{constants.PROP_PATH}/{self.dir_agenda}/prop{nbf}.txt"
                self.file = name
                self.curr_num_agenda = nbf
                name_file = f"{self.dir_agenda}/prop{self.curr_num_agenda}"
            else:
                self.curr_num_agenda += 1
                self.file = f"{constants.PROP_PATH}/{self.dir_agenda}/prop{self.curr_num_agenda}.txt"
                while os.path.isfile(self.file):
                    self.curr_num_agenda += 1
                    self.file = f"{constants.PROP_PATH}/{self.dir_agenda}/prop{self.curr_num_agenda}.txt"   
                name_file = f"{self.dir_agenda}/prop{self.curr_num_agenda}"
            return f"cpr;{self.variance};{self.nbo};{self.nbs};{2};{2};{self.nbo*2};{trust};{self.list_sf(graph)};{self.OF};{self.list_truth(truth)};;{name_file}\n"
        return f"cpr;{self.variance};{self.nbo};{self.nbs};{2};{2};{self.nbo*2};{trust};{self.list_sf(graph)};{self.OF};{self.list_truth(truth)};;\n"
    
    def read_file(self):
        """
        read file and add interpretation depending on resultat of truth table
        """
        tmp=[]
        f = open(self.file, 'r')
        lines = f.readlines()
        tmp = [l.strip() for l in lines[0].split("-")]
        self.nb_litt = int(tmp[0])
        self.prop = [l.strip() for l in tmp[1].split(";")]
        self.nbo = len(self.prop)
        # remove \n
        tmp2 = []
        for i in range(1, len(lines)):
            line = [int(l) for l in lines[i].split(";")]
            res = line[self.nb_litt:]
            self.model_doublon01.append(res)
            if res not in tmp2: # ignore doublon potentiel
                self.model.append(res)
                tmp2.append(res)
                self.nb_unique += 1
        self.model = sorted(self.model, reverse=True)
        self.model_doublon01 = sorted(self.model_doublon01, reverse=True)
        f.close()
        
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
    
    def distance(self, l, f):
        res = 0
        for i in range(len(f)):
            if l[i] != f[i]:
                res += 1
        return res
    
    def majority_consistent(self, cl, truth):
        """
        true si majo consistent
        """
        res = []
        tmp = []
        for c in cl:
            tmp.extend(c)
        cpt = Counter(tmp)
        l = (len(cl[0])*2)
        for i in range(0,l,2):
            if cpt[i] > cpt[i+1]:
                res.append(i)
            elif cpt[i] < cpt[i+1]:
                res.append(i+1)
            else:
                res.append('*')
        return res in self.modelf
        # return truth == res
    
    def majority_inconsistent(self, cl, truth):
        """
        itrue si majo consistent mais superieure à une certaine distance de la verité
        """
        res = []
        tmp = []
        for c in cl:
            tmp.extend(c)
        cpt = Counter(tmp)
        l = (len(cl[0])*2)
        for i in range(0,l,2):
            if cpt[i] > cpt[i+1]:
                res.append(i)
            elif cpt[i] < cpt[i+1]:
                res.append(i+1)
            else:
                res.append('*')
        return res not in self.modelf
    
    def majority_consistent_d(self, cl, truth):
        """
        true si majo consistent mais superieure à une certaine distance de la verité
        """
        res = []
        tmp = []
        for c in cl:
            tmp.extend(c)
        cpt = Counter(tmp)
        l = (len(cl[0])*2)
        for i in range(0,l,2):
            if cpt[i] > cpt[i+1]:
                res.append(i)
            elif cpt[i] < cpt[i+1]:
                res.append(i+1)
            else:
                res.append('*')
        ret = True
        for f in self.modelf:
            if res == f:
                return True
            if self.distance(f,res) < 3:
                ret = True
            else:
                ret = False
        return ret
        # return res in self.modelf
        # return truth == res
        
    def majo_diff_truth(self, cl, truth):
        """
        coherent mais à une distance certaine
        """
        res = []
        tmp = []
        for c in cl:
            tmp.extend(c)
        cpt = Counter(tmp)
        l = (len(cl[0])*2)
        for i in range(0,l,2):
            if cpt[i] > cpt[i+1]:
                res.append(i)
            elif cpt[i] < cpt[i+1]:
                res.append(i+1)
            else:
                res.append('*')
        for f in self.modelf:
            if res == f:
                return self.distance(truth, res) < 4
        return True
    
    def find_interv(self, t):
        if self.typeg == constants.RUN_PRP:
            for i in range(len(self.interval)):
                n = self.interval[i]
                tmp = n.split("-")
                if int(tmp[0]) <= t <= int(tmp[1]):
                    return i, self.interval[i]
            return -1, None
        elif self.typeg == constants.RUN_VRN:
            tmp = self.fixed_prc.split("-")
            if int(tmp[0]) <= t <= int(tmp[1]):
                return self.interval.index(self.variance), self.variance
            return -1, None
        elif self.typeg == constants.RUN_SPR or self.typeg == constants.RUN_SDR:
            for i in range(len(self.interval)):
                n = self.interval[i]
                if n == self.nbs:
                    tmp = self.fixed_prc.split("-")
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

    # def generate_claims(self, nbs, tab):
    #     """
    #     generate one graph where the source's claims are chosen randomly
    #     """
    #     length = len(tab)
    #     s = []
    #     for i in range(nbs):
    #         r = random.randint(0, length-1)
    #         curr = tab[r]
    #         s.append(curr)    
    #     return s

    def generate_claims(self, nbs, tab):
        """
        generate one graph where the source's claims are chosen randomly
        """
        # print("--")
        length = len(tab)
        s = []
        i = 0
        j = 0
        acc = 0
        for n in list(self.dicoddd.values()):
            if n > 6:
                acc += 1
        # for i in range(nbs):
        while i < nbs:
            tmpdico = self.dicoddd.copy()
            add = True
            r = random.randint(0, length-1)
            curr = tab[r]
            for v in curr:
                ## pas plus de 6-3 sur 3 objets
                if acc < 1 or tmpdico[v] + 1 < 6:
                    tmpdico[v] += 1
                else:
                    acc += 1
                    add = False
                    if acc > 1:
                        break
            if add:
                self.dicoddd = tmpdico
                # print("s", curr)
                # print("add", self.dicoddd.values())
                i += 1
                s.append(curr)
            else:
                # print("no add", self.dicoddd.values())
                tmpdico = self.dicoddd
            # print("dico73", self.dicoddd.values())
            j += 1
            ## nbs sources
            if j == 10:
                # print("FFFFF")
                return []
            # print(self.dicoddd.values())
            # print()
        return s
    
    def comp(self, t, p, v):
        if p == "u":
            return t >= int(v)
        elif p == "d":
            return t <= int(v)
        return True
    
    def comp_var(self, t, value_target):
        return int(value_target)-self.variance <= t <= int(value_target)+self.variance
        
    
    def generate_claims_variance(self, model_use, nbs, truth, value_target, n, ud):
        """
        generate one graph where the source's claims are chosen depending on pvn
        value_target : value you want with a certain variance
        number of agents : int between 0 and nbs
        """
        para_in = []
        para_out = []
        para_u = []
        para_d = []
        # dico = dict()
        for mod in model_use:
            t = self.compute_trust([mod], truth)
            if self.comp_var(t, value_target):
                para_in.append(mod)
                if ud != "":
                    if ud == "u":
                        para_u.append(mod)
                    elif ud == "d":
                        para_d.append(mod)
            else:
                para_out.append(mod)
        s = []
        lin = len(para_in)
        # print(lin,"/",len(model_use))
        if lin == 0:
            return []
        if ud != "":
            if ud == "u":
                s.extend(self.generate_claims(int(n), para_u))
            elif ud == "d":
                s.extend(self.generate_claims(int(n), para_d))
            s.extend(self.generate_claims(nbs-int(n), para_in))
        else:
            s.extend(self.generate_claims(nbs, para_in))
        # print(dico)
        return s
    
    def generate_claims_para(self, model_use, nbs, truth, p, v, n):
        """
        generate one graph where the source's claims are chosen depending on pvn
        p : u(=up) or d(=down)
        value target : int between 0 and 100
        number of agents : int between 0 and nbs
        """
        para_in = []
        para_out = []
        for mod in model_use:
            t = self.compute_trust([mod], truth)
            if self.comp(t,p,v):
                para_in.append(mod)
            else:
                para_out.append(mod)
        s = []
        lin = len(para_in)
        if lin == 0:
            return []
        s.extend(self.generate_claims(int(n), para_in))
        
        lout = len(para_out)
        if lout == 0:
            return []
        s.extend(self.generate_claims(nbs-int(n), para_out))
        return s
    
    def generate_claims_distrib(self, model_use, truth, d):
        dico = dict()
        for mod in model_use:
            t = self.compute_trust([mod], truth)
            if t not in dico:
                dico[t] = [mod]
            else:
                dico[t].append(mod)
        s = []
        for k in d:
            if k not in dico:
                return []
            # print("DISTRIB - N src avec k%", d[k], k)
            s.extend(self.generate_claims(int(d[k]), dico[k]))
        return s
    
    # def generate_claims_distrib(self, model_use, truth, d):
    #     dico = dict()
    #     for mod in model_use:
    #         t = self.compute_trust([mod], truth)
    #         if t not in dico:
    #             dico[t] = [mod]
    #         else:
    #             dico[t].append(mod)
    #     s = []
    #     for k in d:
    #         if k not in dico:
    #             return []
    #         s.extend(self.generate_claims(int(d[k]), dico[k]))
    #     return s
    
    def generate_all(self):
        # model_use = self.modelf_doublon;print("doublon")
        if not self.gen_agenda:
            model_use = self.modelf;print("no doublon")
            length = len(model_use)
        else:
            files = [f.split("/")[-1] for f in glob.glob(f"{constants.PATH_XP}/*.csv")]
            tmp = []
            for f in files:
                if 'xp' in f:
                    tmp.append(int(f[3:f.index("xp")]))
            name_res = f"{max(tmp)+1}"
            self.dir_agenda = name_res
            print(f"Create {constants.PROP_PATH}/{self.dir_agenda}")
            os.mkdir(f"{constants.PROP_PATH}/{self.dir_agenda}")
        
        for i in range(20):
            self.dico73[i] = 0
        
        # txt = ""
        p = ""
        v = ""
        n = ""
        d = ""
        m = ""
        ud = ""
        runit = 0
        it = 1000
        total = 0
        first = False
        while not all(self.valid) and p != "e": 
            res = ""
            keys = list(self.nres.keys())
            for i in range(len(keys)):
                res += f"\033[31m{keys[i]}\033[00m:\033[32m{self.nres[keys[i]]}\033[00m / "
            res += "\n"
            if not all(self.valid):
                print(runit, "\n", res)
                print(f"u/d:{p} / v:{v} / n:{n}")
                tmp = input(f"nb it (curr {it}) ?")
                if tmp != "":
                    it = int(tmp)
                if self.typeg == constants.RUN_PRP:
                    tmp = input("u(=up) or d(=down) or e(=exit) or c(=distrib) or r(=reset)?")
                    if tmp != "":
                        if tmp == "r":
                            p = ""
                        else:
                            p = tmp
                    tmp = input("majority (y=cons/n=incon/t=cons_d/i=incon_d/a=mix))")
                    if tmp == "n":
                        m = False
                    elif tmp == "y":
                        m = True
                    elif tmp == "t":
                        m = "t"
                    elif tmp == "i":
                        m = "i"
                    elif tmp == "a":
                        m = "a"
                    elif tmp == "c":
                        m = "c"
                    else:
                        if m == True or m == False or m == "t" or m == "i" or m == "a" or m == "c":
                            pass
                        else:
                            m = ""
                    if p == "c":
                        tmp = input("distrib ?")
                        if tmp != "":
                            d = eval(tmp)
                            print("distrib : ", d)
                    elif p != "c" and p != "" and p != "e":
                        tmp = input("value ?")
                        if tmp != "":
                            v = tmp
                        tmp = input("number of sources ?")
                        if tmp != "":
                            n = tmp
                elif self.typeg == constants.RUN_VRN:
                    if not first:
                        p = "v"
                        tmp = input(f"target value in {self.fixed_prc}?")
                        if tmp != "":
                            v = tmp
                            first = True
                    tmp = input(f"variance in {self.interval}?")
                    if tmp != "":
                        self.variance = int(tmp)
                    # tmp = input("majority == truth (y/n))")
                    tmp = input("majority consistent (y/n))")
                    if tmp == "n":
                        m = False
                    elif tmp == "y":
                        m = True
                    tmp = input("u(=up) or d(=down) or random(press enter)?")
                    if tmp != "":
                        ud = tmp
                        tmp = input("number of sources ?")
                        if tmp != "":
                            n = tmp
                elif self.typeg == constants.RUN_SPR:
                    tmp = input("target number of sources ?")
                    if tmp != "":
                        self.nbs = int(tmp)
                    tmp = input("u(=up) or d(=down) or e(=exit) or r(=reset)?")
                    if tmp != "":
                        if tmp == "r":
                            p = ""
                        else:
                            p = tmp
                    tmp = input("majority (y=cons/n=incon/t=cons_d/i=incon_d/a=mix))")
                    if tmp == "n":
                        m = False
                    elif tmp == "y":
                        m = True
                    elif tmp == "t":
                        m = "t"
                    elif tmp == "i":
                        m = "i"
                    elif tmp == "a":
                        m = "a"
                    else:
                        if m == True or m == False or m == "t" or m == "i" or m == "a":
                            pass
                        else:
                            m = ""
                    if p != "" and p != "e":
                        tmp = input("value ?")
                        if tmp != "":
                            v = tmp
                        tmp = input("number of sources ?")
                        if tmp != "":
                            n = tmp
                elif self.typeg == constants.RUN_SDR:
                    p = "c"
                    tmp = input("target number of sources ?")
                    if tmp != "":
                        self.nbs = int(tmp)
                    d = self.distrib[self.nbs]
                    print("distrib : ", d)
                    tmp = input("majority (y=cons/n=incon/t=cons_d/i=incon_d/a=mix))")
                    if tmp == "n":
                        m = False
                    elif tmp == "y":
                        m = True
                    elif tmp == "t":
                        m = "t"
                    elif tmp == "i":
                        m = "i"
                    elif tmp == "a":
                        m = "a"
                    else:
                        if m == True or m == False or m == "t" or m == "i" or m == "a":
                            pass
                        else:
                            m = ""
                    
                    # print(f"curr d:{d}")
                    # tmp = input("distrib {value:nbsrc}?")
                    # if tmp != "":
                    #     d = eval(tmp)
                    #     while sum(d.values()) != self.nbs:
                    #         print(f"curr d:{d}")
                    #         tmp = input("distrib {value:nbsrc}?")
                    #         if tmp != "":
                    #             d = eval(tmp)
                print()
            print(f"type generation {p} target {v} variance : {self.variance}, majority:{m}")
            trust_gen = dict()
            for i in range(it):
                if self.gen_agenda:
                    self.generate_agenda()
                    # model avec les id faits à la place des 1 ou 0
                    self.modelf = self.interp_f(self.model)
                    self.modelf_doublon = self.interp_f(self.model)
                    model_use = self.modelf
                    length = self.nb_unique
                # test avec le nombre de model selon l'agenda
                runit += 1
                # if self.nb_unique < 150:
                #     continue
                # test avec le nombre de model selon l'agenda
                rand = random.randint(0, length-1)
                truth = model_use[rand]
                self.dicoddd = self.dico73.copy()
                if p == "":
                    claims = self.generate_claims(self.nbs, model_use)
                elif p == "v":
                    claims = self.generate_claims_variance(model_use, self.nbs, truth, v, n, ud)
                elif p == "c":
                    claims = self.generate_claims_distrib(model_use, truth, d)
                else:
                    claims = self.generate_claims_para(model_use, self.nbs, truth, p, v, n)
                if len(claims) == self.nbs:
                    go = True
                    if m != "" or m != "a":
                        if m == True:
                            if self.majority_inconsistent(claims, truth):
                                go = False
                        elif m == False:
                            if self.majority_consistent(claims, truth):
                                go = False
                        elif m == "t":
                            if self.majo_diff_truth(claims, truth):
                                go = False
                        elif m == "i":
                            if self.majority_consistent_d(claims, truth):
                                go = False
                    trust = self.compute_trust(claims, truth)
                    if trust in trust_gen:
                        trust_gen[trust] += 1
                    else:
                        trust_gen[trust] = 1
                    total += trust
                    if go:
                        if self.add_dict(truth, claims, trust) != "":
                            if self.gen_agenda:
                                self.write_agenda()
                            ### affichage
                            # print("truth", truth)
                            # for c in claims:
                            #     print(c, self.compute_trust([c], truth))
                            # print("trust", trust)
                            ### affichage
                        elif all(self.valid):
                            break
            print("Trust generated", [(k,trust_gen[k]) for k in sorted(trust_gen)])
        res = ""
        keys = list(self.nres.keys())
        for i in range(len(keys)):
            res += f"\033[31m{keys[i]}\033[00m:\033[32m{self.nres[keys[i]]}\033[00m / "
        res += "\n"
        print(runit, "\n", res)
        self.name_xp(); print("start writing")
        txt = self.write_header(round(total/(self.nbg*len(self.interval))), self.distrib)
        # self.txt = self.write_header(round(total/(self.nbg*len(self.interval))))
        for i in self.interval:
            for n in self.res[i]:
                # self.txt += n
                txt += n
        # self.f.write(self.txt)
        self.f.write(txt)
        print("done")
        # print(txt)
        self.f.close()
    
    def interp_f(self, interp):
        """
        1 in assignement = fact with index odd (1-3-5) OR fact with id even (2-4-6)
        0 in assignement = fact with index even (0-2-4) OR fact with id odd (1-3-5)
        """
        res = []
        for intp in interp:
            res.append([])
            for j in range(len(intp)):
                res[-1].append(self.facts[j][intp[j]])
        return res
        
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
    
    def str_dist(self, distrib):
        res = ""
        for k in distrib:
            res += f"{k}:"
            for k2 in distrib[k]:
                res+=f"{k2}={distrib[k][k2]}&"
            res = res[:-1] + "-"
        return res[:-1]
    
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
    file = "prop12"
    distrib = ""    
    # typeg = "SPR"; intv = ['65-70']; int_variance = [10,20,30,40,50]
    # typeg = "SPR"; intv = ['60-64']; int_variance = [10]
    typeg = "PRP"; intv = ['30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79']; int_variance = [100]
    # typeg = "PRP"; intv = ['30-34']; int_variance = [100]

    # gen agenda à chaque nouveau graphe
    gen_agenda = True
    nb_litt = 10
    nb_form = 10
    # nb graphe pour chaque interv et nb sources
    nbg = 1000
    nbs = 9
    
    generator = GenerateWProp(file, nbs, nbg=nbg, intvp=intv, typeg=typeg, 
                            int_variance=int_variance, distrib=distrib,
                            gen_agenda=gen_agenda, nb_litt=nb_litt, nb_form=nb_form)
    generator.generate_all()
    
    
    
    # intv = ['30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79']
    # intv = ['40-44','45-49','50-54','55-59','60-64','65-69']
    # intv = ['50-54','55-59']
    # dico = dict()
    # for i in range(100):
    #     generator = GenerateWProp(file, nbs, nbg=nbg, intvp=intv, gen_agenda=True, nb_litt=10, nb_form=10)
    #     generator.generate_agenda()
    #     if generator.nb_unique in dico:
    #         dico[generator.nb_unique] += 1
    #     else:
    #         dico[generator.nb_unique] = 1
    #     print(dict(sorted(dico.items(), reverse=True)))
    #     print()
    
    # generator.generate_all()
    
    # generator.display_one(intv[3])
    # s, truth = generator.generate_one()
    
        
    
    
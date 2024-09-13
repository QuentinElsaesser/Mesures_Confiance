# import numpy as np

# from v4.graph import graph

# from operator import itemgetter
# from itertools import groupby

# from v4.vote import normalize as nm

# from v4.graph import obj

# from copy import deepcopy

from v4.judag import baseVo

class RDH(baseVo.BaseVoting):
    """
    minimise le maximum de la distance de hamming entre les 
    modeles et le choix de chaque sources
    
    Dans le modele :
        FAIT IMPAIR = FALSE (0) donc fait 1-3-5-etc = false value for formula
            MAIS indice pair = true value !!
        FAIT PAIR = TRUE (1)
    """
    def __init__(self, mat_fs, mat_of, voting_met, vote_para, name_norma, nb_s, nb_f, init_trust=1,truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None,model=[],Gr=None,form=None,vect=None,revres=None,maj_form=None,maj_formSF=None):        
        super().__init__(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                         vote_para=vote_para, name_norma=name_norma, 
                         nb_s=nb_s, nb_f=nb_f, truth=truth, trust_s=trust_s,
                         init_trust=init_trust,normalizer=normalizer,
                         trust_f=trust_f,long=long,gobj=gobj,sf=sf,
                         model=model,Gr=Gr,
                         form=form,vect=vect,revres=revres,maj_form=maj_form)
        
        self.srcf = []
        
        for i in range(len(self.G.sf)):
            s = self.G.sf[i]
            self.srcf.append(self.c01_to_form(s))
    
    def aggr(self):
        """
        the minimization of the maximum distance minimizes the disagree- ment with the least satisfied individual,
        """
        res = dict()
        for i in range(len(self.form)):
            f = self.form[i]
            # print()
            # print("f", f)
            maxv = 0
            for s in self.srcf:
                d = self.distance(s, f)
                if d > maxv:
                    maxv = d
                # print(s, f, "distance", d, "distnce max", maxv)
            if maxv in res:
                res[maxv].append(f)
            else:
                res[maxv] = [f]

        # for k in res:
        #     print(k, ':', res[k])

        tmp = res[min(list(res.keys()))]

        self.results([self.form.index(tmp[i]) for i in range(len(tmp))], self.__repr__)
    
   
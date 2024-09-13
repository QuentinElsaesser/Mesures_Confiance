import numpy as np

# from v4.graph import graph

# from operator import itemgetter
# from itertools import groupby

# from v4.vote import normalize as nm

# from v4.graph import obj

# from copy import deepcopy

from v4.judag import baseJA

class Produitsf(baseJA.BaseJA):
    """
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
                         form=form,vect=vect,revres=revres,maj_form=maj_form,
                         maj_formSF=maj_formSF)
        
    def aggr(self):
        maxinds = []
        maxv = 0
        
        for i in range(len(self.vect)):
            l = self.vect[i]
            m = self.form[i]
            s = np.prod(l)
            self.test.append((m, s))
            # print(i, m, l, s)
            if maxv < s:
                maxv = s
                maxinds = [i]
            elif maxv == s:
                maxinds.append(i)

        self.results(maxinds, self.__repr__)
        

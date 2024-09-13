# import numpy as np

# from v4.graph import graph

# from operator import itemgetter
# from itertools import groupby

# from v4.vote import normalize as nm

# from v4.graph import obj

# from copy import deepcopy

from v4.judag import baseJA

class Leximax(baseJA.BaseJA):
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
    
    def find_max(self, liste, index):
        maxv = liste[0][1][index]
        vals = [liste[0]]
        for i in range(1, len(liste)):
            if maxv < liste[i][1][index]:
                vals = [liste[i]]
                maxv = liste[i][1][index]
            elif maxv == liste[i][1][index]:
                vals.append(liste[i])
        self.test.append((maxv, index))
        return vals

    
    def aggr(self):
        """
        sort by the max
        """
        tmp = []
        for i in range(len(self.vect)):
            tmp.append((i, sorted(self.vect[i], reverse=True)))
        currind = 0
        
        # for i in range(len(tmp)):
        #     print(i, tmp[i], self.form[tmp[i][0]])
        # print()
        
        while(currind < len(self.vect[0]) and len(tmp) > 1):
            tmp = self.find_max(tmp, currind)
            
            # print("currind", currind+1)
            # for l in tmp:
            #     print(l, self.form[l[0]])
            # print()
            
            currind += 1
        self.results([n[0] for n in tmp], self.__repr__)
        
# import numpy as np

# from v4.graph import graph

from v4.judag import base

# from operator import itemgetter
# from itertools import groupby

# from v4.vote import normalize as nm

# from v4.graph import obj

# from collections import Counter

class BaseJA(base.Base):
    """
    Dans le modele :
        INDEX start with 0 / ID start with 1
        1 in interpretation = fact with index odd (1-3-5) OR fact with id even (2-4-6)
        0 in interpretation = fact with index even (0-2-4) OR fact with id odd (1-3-5)
    """
    def __init__(self, mat_fs, mat_of, voting_met, vote_para, name_norma, nb_s, nb_f, init_trust=1,truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None,model=[],Gr=None,form=None,vect=None,revres=None,maj_form=None,maj_formSF=None,nom_agenda=None):
        # if Gr==None:
        super().__init__(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                            vote_para=vote_para, name_norma=name_norma, 
                            nb_s=nb_s, nb_f=nb_f, truth=truth, trust_s=trust_s,
                            init_trust=init_trust,normalizer=normalizer,
                            trust_f=trust_f,long=long,gobj=gobj,sf=sf,Gr=Gr,
                            model=model,
                            form=form,vect=vect,revres=revres
                            ,maj_form=maj_form,maj_formSF=maj_formSF
                            ,nom_agenda=nom_agenda)


        if revres == None:
            self.G.reset_graph([self.G.init_trust for i in range(len(self.G.mat_fs[0]))])
            
            # self.G.run()
            self.G.run_noprint()
            
            # maj_form = avec la trust et pas le support !!!
            self.revres, self.maj_form, self.maj_formSF = self.gen_revres()
            self.form, self.vect = self.asso()
            
        else:
            self.revres = revres
            self.maj_form = maj_form
            self.maj_formSF = maj_formSF
            self.form = form
            self.vect = vect
            self.asso(read=True)
        
        
        # print("Trust f", self.G.trust_f)
        # print("dico revres : ")
        # for k in self.revres:
        #     print(k,":",self.revres[k])
            
        # for i in range(len(self.model)):
        #     print(self.model[i], self.form[i])
        # print(self.maj_form)
        
        # print("BASEJA", len(self.vect), self.revres)

                    

# import numpy as np

# from v4.graph import graph

from v4.other_methods import voting_majo

from v4.judag import base, baseJA

# from operator import itemgetter
# from itertools import groupby

# from v4.vote import normalize as nm

# from v4.graph import obj

# from copy import deepcopy

class BaseVoting(base.Base):
    """
    Dans le modele :
        INDEX start with 0 / ID start with 1
        1 in interpretation = fact with index odd (1-3-5) OR fact with id even (2-4-6)
        0 in interpretation = fact with index even (0-2-4) OR fact with id odd (1-3-5)
    """
    def __init__(self, mat_fs, mat_of, voting_met, vote_para, name_norma, nb_s, nb_f, init_trust=1,truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None,model=[],Gr=None,form=None,vect=None,revres=None,maj_form=None,maj_formSF=None):
        """
        Gr = BaseVoting
        """
        if isinstance(Gr, baseJA.BaseJA):
            super().__init__(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                                vote_para=vote_para, name_norma=name_norma, 
                                nb_s=nb_s, nb_f=nb_f, truth=truth, trust_s=trust_s,
                                init_trust=init_trust,normalizer=normalizer,
                                trust_f=trust_f,long=long,gobj=gobj,sf=sf,Gr=None,
                                model=model,
                                form=form,vect=vect,revres=revres,maj_form=maj_form)
        else:
            super().__init__(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                                vote_para=vote_para, name_norma=name_norma, 
                                nb_s=nb_s, nb_f=nb_f, truth=truth, trust_s=trust_s,
                                init_trust=init_trust,normalizer=normalizer,
                                trust_f=trust_f,long=long,gobj=gobj,sf=sf,Gr=Gr,
                                model=model,
                                form=form,vect=vect,revres=revres,maj_form=maj_form)

        self.vote = voting_majo.VotingMajo(self.G)
        
        # start with 0
        self.model = model
        
        self.vote.run_noprint()
        
        self.G = self.vote.G
        
        if revres == None:
            self.revres, self.maj_form, self.maj_formSF = self.gen_revres()
            self.form, self.vect = self.asso()
        else:
            self.revres = revres
            self.maj_form = maj_form
            self.maj_formSF = maj_form
            self.form = form
            self.vect = vect
            self.asso(read=True)
        
        # print("BASEVO", len(self.vect), self.revres)
                    
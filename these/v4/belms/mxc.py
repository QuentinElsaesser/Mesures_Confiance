from v4.belms import basemaxcons

# maxcons
class Mxc(basemaxcons.BaseMaxCons):
    def __init__(self, mat_fs, mat_of, voting_met, vote_para, name_norma, nb_s, nb_f, nbl=0,interp=[],init_trust=1,truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None,Gr=None,relia=None,agents=None,formulas=None,table=None,maxcons=None,distance=None,agents_ind=None,formulas_chosed=None,dict_all_combi=None):
        super().__init__(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                      vote_para=vote_para, name_norma=name_norma, 
                      nb_s=nb_s, nb_f=nb_f, nbl=nbl, interp=interp, 
                      init_trust=init_trust, truth=truth, normalizer=normalizer, 
                      trust_s=trust_s, trust_f=trust_f, long=long, gobj=gobj,
                      sf=sf, Gr=Gr, relia=relia, agents=agents, formulas=formulas,
                      table=table, maxcons=maxcons, distance=distance,
                      agents_ind=agents_ind, formulas_chosed=formulas_chosed,
                      dict_all_combi=dict_all_combi)
        
    def decision(self):
        """
        compare le maxcons par rapport à chaque base
        Si incoherent alors on ajoute 1 sinon on ajoute 0
        la reponse est la plus petite distance
        """
        # print("--------------------")
        self.answers = []

        # inter = None
        for i in range(len(self.maxcons)):
            # if inter == None:
            #     inter = self.maxcons_ind[i]
            # else:
            #     inter = inter.intersection(self.maxcons_ind[i])
            # self.answers.append([self.maxcons_to_interp(self.maxcons[i])])
            self.answers.append(self.maxcons[i])
                
        # if len(inter) > 0:
        #     self.answers = []
        #     for index in inter:
        #         self.answers.append(self.formulas[index])
            
        
        
        # for i in range(len(self.answers)):
        #     print(i, self.answers[i])
        # print(len(self.answers))
        # print("--------------------")
        self.resultats(reprr=self.__repr__, ind_decision=0)
        
        
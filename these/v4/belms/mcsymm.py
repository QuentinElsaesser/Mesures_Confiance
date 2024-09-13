from v4.belms import basemaxcons

class McSymm(basemaxcons.BaseMaxCons):
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
        evalue la distance entre les deux 
        (nombre de formule qui ne sont pas dans l'un + nb f sont pas dans l'autre)
        la reponse est la plus petite distance
        """
        # print("--------------------")
        self.answers = []
        
        # distance = []
        # for m in self.maxcons:
        #     dist = 0
        #     for i in range(len(self.agents)):
        #         a = self.agents[i]
        #         dist += len(set([str(n) for n in a]).symmetric_difference(set([str(p) for p in m])))
        #         # print("A", i, a)
        #         # print("M", m)
        #         # print(dist)
        #         # print()
                
        #     distance.append(dist)

        distance = self.distance[1]

        mini = min(distance)
        
        for i in range(len(distance)):
            if distance[i] == mini:
                self.answers.append(self.maxcons[i])
        
        # for i in range(len(self.answers)):
        #     print(i, self.answers[i])
        
        # print("--------------------")
        self.resultats(reprr=self.__repr__)
        
        
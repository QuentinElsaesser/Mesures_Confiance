from v4.belms import basesfbms

class SFbmSCAvg(basesfbms.BaseSFbmS):
    def __init__(self, mat_fs, mat_of, voting_met, vote_para, name_norma, nb_s, nb_f, nbl=0,interp=[],init_trust=1,truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None,Gr=None,relia=None,agents=None,formulas=None,table=None,maxcons=None,distance=None,agents_ind=None,formulas_chosed=None,dict_all_combi=None):
        """
        Average NORMA A et NORMA O ici dans graph_methods
        """
        super().__init__(mat_fs=mat_fs, mat_of=mat_of, voting_met=voting_met, 
                      vote_para=vote_para, name_norma=name_norma, 
                      nb_s=nb_s, nb_f=nb_f, nbl=nbl, interp=interp, 
                      init_trust=init_trust, truth=truth, normalizer=normalizer, 
                      trust_s=trust_s, trust_f=trust_f, long=long, gobj=gobj,
                      sf=sf, Gr=Gr, relia=relia, agents=agents, formulas=formulas,
                      table=table, maxcons=maxcons, distance=distance,
                      agents_ind=agents_ind, formulas_chosed=formulas_chosed,
                      dict_all_combi=dict_all_combi)
    
        self.answers_incons = []
    
    def consistant_answers_sum_ongen(self):
        tmp = dict()
        for f in self.formulas:
            tmp[f"{sorted(self.formulas[f])}"] = int(f)
            # print("FORM RELIA", f, self.formulas[f], self.relia[int(f)], self.G.mem_f[1][int(f)])
        
        # tmpmaxc = []
        values = []
        for m in self.maxcons:
            # print("MCONS", len(m))
            # ttmp = []
            value = []
            # print(m)
            for form in m:
                # ttmp.append(tmp[f"{form}"])
                # print(form, self.formulas_chosed[tmp[f"{sorted(form)}"]])
                if self.formulas_chosed[tmp[f"{sorted(form)}"]]:
                    value.append(self.relia[tmp[f"{sorted(form)}"]])
                    # print(sorted(form), self.relia[tmp[f"{sorted(form)}"]])
            self.info.append((m, value, sum(value)/len(value)))
            # self.info.append(([sorted(xx) for xx in m], value, sum(value)/len(value)))
            # print([sorted(xx) for xx in m], value, sum(value)/len(value))
            # print()
            # print(m, value, self.truth)
            # tmpmaxc.append(ttmp)
            values.append(value)
            
        maxi = 0
        index = []
        for i in range(len(values)):
            l = len(values[i])
            if l > 0:
                v = (sum(values[i])/l)
                if v > maxi:
                    maxi = v
                    index = [i]
                elif v == maxi:
                    index.append(i)
        
        answers = []
        for i in index:
            # print(i, self.maxcons_to_interp(self.maxcons[i]))
            answers.append(self.maxcons[i])
        return answers
    
    def decision(self):
        """
        multiple answers
        """
        self.answers = self.consistant_answers_sum_ongen()
        self.resultats(reprr=self.__repr__)
        
        

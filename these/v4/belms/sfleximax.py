from v4.belms import basesfbms

# from copy import deepcopy

class SFLeximax(basesfbms.BaseSFbmS):
    def __init__(self, mat_fs, mat_of, voting_met, vote_para, name_norma, nb_s, nb_f, nbl=0,interp=[],init_trust=1,truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None,Gr=None,relia=None,agents=None,formulas=None,table=None,maxcons=None,distance=None,agents_ind=None,formulas_chosed=None,dict_all_combi=None):
        """
        Leximax
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
    
    def find_max(self, liste, index):
        maxv = 0
        # vals = [liste[0]]
        for i in range(0, len(liste)):
            if len(liste[i][1]) > index and maxv < liste[i][1][index]:
                # vals = [liste[i]]
                maxv = liste[i][1][index]
            # elif maxv == liste[i][1][index]:
            #     vals.append(liste[i])
        # return vals
        return maxv
    
    def consistant_answers_sum_ongen(self):
        """
        best maxcons parmis les formules generees
        
        MAXCONS taille diff donc si on a un maxcons taille 2 qui a les 2 max on prend
        mais si un maxcons de taille 3 max les 3 on prend aussi donc on a 2 reponses
        
        chaque maxcons a son veteur de fiabilite
        on prend le maxcons avec la plus haute puis avec la deuxieme plus haute etc
        (et leximin c'est plus grand mini)
        """
        trust = dict()
        for f in self.formulas:
            if self.formulas_chosed[int(f)]:
                trust[f"{sorted(self.formulas[f])}"] = self.relia[int(f)]

        trustmx = []
        testedmx = []
        taillemax = 0
        for i in range(len(self.maxcons)):
            mx = self.maxcons[i]
            tmp = []
            tmp2 = []
            taillemax = max(taillemax, len(mx))
            for f in mx:
                tmp.append(trust[f"{sorted(f)}"])
                tmp2.append(False)
            trustmx.append((i, sorted(tmp, reverse=True)))
            testedmx.append(tmp2)
            
            self.info.append((mx, None, sorted(tmp, reverse=True)))
            
        curr_ind = 0
        while curr_ind != taillemax:
            tmp = []
            tmp2 = []
            val_max = self.find_max(trustmx, curr_ind)
            for i in range(len(trustmx)):
                tab = trustmx[i][1]
                # si le maxcons est assez grand, on test la valeur 
                if len(tab) > curr_ind:
                    if tab[curr_ind] == val_max:
                        tmp.append(trustmx[i])
                        testedmx[i][curr_ind] = True
                        tmp2.append(testedmx[i])
                else:
                    # si le maxcons est plus petit mais qu'on a regarder tous les maxcons
                    if all(testedmx[i]):
                        tmp.append(trustmx[i])
                        tmp2.append(testedmx[i])
            curr_ind += 1
            if len(tmp) == 1:
                return [self.maxcons[tmp[0][0]]]
            else:
                trustmx = tmp
                testedmx = tmp2
                tmp = []
                tmp2 = []
        
        answers = []
        for tab in trustmx:
            answers.append(self.maxcons[tab[0]])
        return answers
    
    def decision(self):
        """
        multiple answers
        """
        self.answers = self.consistant_answers_sum_ongen()
        
        self.resultats(reprr=self.__repr__)
        
        
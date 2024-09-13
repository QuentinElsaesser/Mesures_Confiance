from v4.belms import basesfbms

class SFLeximin(basesfbms.BaseSFbmS):
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
    
        self.answers_incons = []
        
    def find_max(self, liste, index, taillemax):
        # print("recherche max")
        maxv = 0
        for i in range(0, len(liste)):
            ind_check = index
            n = taillemax - len(liste[i][1])
            if len(liste[i][1]) < taillemax:
                # print("new index check", ind_check, ind_check-n, len(liste[i][1]), taillemax)
                ind_check -= n
            # print(liste[i], index, maxv, taillemax, n, n <= index)
            if n <= index and maxv < liste[i][1][ind_check]:
                # print("NEW MAXV", maxv, "->", liste[i][1][ind_check])
                maxv = liste[i][1][ind_check]
        # print("fin recherche")
        return maxv
    
    def consistant_answers_sum(self):
        #### LEXIMIN
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
            trustmx.append((i, sorted(tmp, reverse=False)))
            testedmx.append(tmp2)
            
            self.info.append((mx, None, sorted(tmp, reverse=False)))
            
        curr_ind = 0
        while curr_ind != taillemax:
            tmp = []
            tmp2 = []
            val_max = self.find_max(trustmx, curr_ind, taillemax)
            for i in range(len(trustmx)):
                tab = trustmx[i][1]
                n = taillemax - len(tab)
                if curr_ind < n:
                    # si trop petit on conserve pour plus tard
                    tmp.append(trustmx[i])
                    tmp2.append(testedmx[i])
                else:
                    if all(testedmx[i]):
                        # si on a regarde tous les valeurs
                        tmp.append(trustmx[i])
                        tmp2.append(testedmx[i])
                    else:
                        ind_check = curr_ind
                        if len(tab) < taillemax:
                            # new indice si pas bonne taille
                            ind_check -= n
                        if tab[ind_check] == val_max:
                            # si bonne valeur
                            tmp.append(trustmx[i])
                            testedmx[i][ind_check] = True
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
    
        # print(self.formulas)
        # print(self.relia)
        # tmp = dict()
        # for f in self.formulas:
        #     tmp[f"{sorted(self.formulas[f])}"] = int(f)
        #     # print("FORM RELIA", self.truth, f, self.formulas[f], self.relia[int(f)], self.G.mem_f[1][int(f)])
        
        # values = []
        # for m in self.maxcons:
        #     # print("MCONS", len(m))
        #     value = []
        #     for form in m:
        #         r = self.relia[tmp[f"{sorted(form)}"]]
        #         value.append(r)
        #         # value.append(r * r)
        #     values.append(value)
            
        # maxi = 0
        # index = []
        # for i in range(len(values)):
        #     v = sum(values[i])
        #     if v > maxi:
        #         maxi = v
        #         index = [i]
        #     elif v == maxi:
        #         index.append(i)
        
        # answers = []
        # for i in index:
        #     answers.append(self.maxcons[i])
        # return answers

    # def find_max(self, liste, index):
    #     maxv = liste[0][1][index]
    #     vals = [liste[0]]
    #     for i in range(1, len(liste)):
    #         if maxv < liste[i][1][index]:
    #             vals = [liste[i]]
    #             maxv = liste[i][1][index]
    #         elif maxv == liste[i][1][index]:
    #             vals.append(liste[i])
    #     return vals
        
    # def consistant_answers_lex(self):
    #     tmp = dict()
    #     for f in self.formulas:
    #         tmp[f"{self.formulas[f]}"] = int(f)
        
    #     values = []
    #     for i in range(len(self.maxcons)):
    #         m = self.maxcons[i]
    #         value = []
    #         for form in m:
    #             value.append(self.relia[tmp[f"{form}"]])
    #         values.append((i, sorted(value, reverse=True)))
        
    #     currind = 0
    #     while(currind < len(self.maxcons[0]) and len(values) > 1):
    #         values = self.find_max(values, currind)
    #         currind += 1
        
    #     answers = []
    #     for n in values:
    #         answers.append(self.maxcons[n[0]])
    #     return answers
    
    def decision(self):
        """
        multiple answers
        """
        # print("TRUTH", self.truth)
        # first = False
        # intersection = set()
        # for i in range(0,len(self.relia),2):
        #     str_i = f"{i}"
        #     str_i1 = f"{i+1}"
        #     if self.relia[i] > self.relia[i+1]:
        #         # self.add_info((self.formulas[str_i], self.relia[i], self.relia[i+1]))
        #         self.answers.append(self.formulas[str_i])
        #         if not first:
        #             intersection = intersection.intersection(self.formulas[str_i])
        #         else:
        #             intersection = self.formulas[str_i]
        #     elif self.relia[i] < self.relia[i+1]:
        #         self.answers.append(self.formulas[str_i1])
        #         # self.add_info((self.formulas[str_i1], self.relia[i], self.relia[i+1]))
        #         if not first:
        #             intersection = intersection.intersection(self.formulas[str_i1])
        #         else:
        #             intersection = self.formulas[str_i1]
        #     else:
        #         # egalite
        #         maxt_ind = self.G.trust_s.index(max(self.G.trust_s))
        #         if self.G.mat_fs[i][maxt_ind] == 1:
        #             self.answers.append(self.formulas[str_i])
        #             if not first:
        #                 intersection = intersection.intersection(self.formulas[str_i])
        #             else:
        #                 intersection = self.formulas[str_i]
        #         else:
        #             self.answers.append(self.formulas[str_i1])
        #             if not first:
        #                 intersection = intersection.intersection(self.formulas[str_i1])
        #             else:
        #                 intersection = self.formulas[str_i1]
            
        # print("ALGO", len(self.answers))
        # for n in self.answers:
        #     print("REP", n)
        # self.answers_incons = self.answers.copy()
        
        # self.answers = [self.answers]
        
        # print(self.answers, self.consistant)
        
        # if len(intersection) == 0:
        #     self.consistant = False
        
        ## mettre une reponse consistant
        # if not self.consistant:
            ## self.consistant_answers()
        self.answers = self.consistant_answers_sum()
            # print("SUM", self.answers)
            # print("MAX", self.consistant_answers_lex())
            ## self.answers = self.consistant_answers_lex()
                
        self.resultats(reprr=self.__repr__)
        
        
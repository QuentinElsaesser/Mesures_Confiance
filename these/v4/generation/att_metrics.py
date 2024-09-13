from v4.graph import graph

from copy import deepcopy

from operator import itemgetter
from itertools import groupby

import numpy as np

from v4.constants import constants

from collections import Counter

class AttMetrics:
    def __init__(self, rg, interp=None):
        """
        rg = random graph
        interp = interpretations
        """
        self.rg = rg
        
        self.G = rg.G if isinstance(rg.G, graph.Graph) else rg.G.G
        
        if constants.FORMULA == constants.RUN_JA:
            self.JAG = rg.G
            self.truth_eq_maj = int(self.JAG.truth_eq_maj)
            self.BMG = None
        elif constants.FORMULA == constants.RUN_TD:
            self.JAG = None
            self.truth_eq_maj=0
            self.BMG = None
        elif constants.FORMULA == constants.RUN_BS:
            self.JAG = None
            self.truth_eq_maj=0
            self.BMG = rg.G
            
        self.alg_consistent = 0
        self.maj_consistent = 0
            
        self.nbs = len(self.G.trust_s)
        
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        
        # vrai monde trouve
        self.true_world_guess = 0
        # mauvais monde classe comme vrai
        self.true_world_wrong = 0
        # autre monde correctement classe
        # self.false_world_guess = 0
        # autre monde correctement classe
        self.all_world_guess = 0
        # precision trust 1 avec la multiplication 0.5
        self.precision_trust_un = 0
        # precision trust 2 true / nombre de reponse
        self.precision_trust_deux = 0
        # nb reponse
        self.nb_answers = 0
        # distnace Hamming into Hausdorff
        self.ham_hausdorff = 0
        # avg distance ham puis hausdorff
        self.avg_ham_hausdorff = 0
        # Pourcentage que la verite est claim
        self.prc_claim_truth = 0
        #
        self.len_bases = 0
        
        self.bms_truth = 0
        self.distance_max = 0
        self.distance_min = 0
        self.distance_avg = 0
        self.avg_len_maxcons = 0
        self.max_len_maxcons = 0
        self.min_len_maxcons = -1
        self.truth_in_mc = 0
        self.distance_una = 0
        self.truth_una = 0
        self.len_croyance_avg = 0
        self.taille_formule_avg = 0
        self.formulas_good = 0
        self.avg_good = 0
        
        # self.nb_true_found = 0
        # self.nb_false_found = 0
        # self.nb_true_total = 0
        # self.correct = 0
        # self.wrong = 0
        # self.nb_correct = 0
        # self.truth_found = 0
        # self.is_included = 0
        # self.precisionBM = 0
        # self.CSIBM = 0
        
        
        self.recall = 0
        self.accuracy = 0
        self.precision = 0
        self.csi = 0
        self.precision_formula_min = -1
        self.csi_formula_min = -1
        self.precision_formula_max = 0
        self.csi_formula_max = 0
        self.precision_formula_mean = 0
        self.csi_formula_mean = 0
        self.csi_formula_unanime = 0
        self.precision_formula_unanime = 0
        self.csi_formula_majority = 0
        self.precision_formula_majority = 0
        self.mem = []
        
        self.swap = 0
        self.swap_max = 0
        self.swap1 = False
        self.swap2 = False
        
        self.euclidean_d = 0
        self.euclidean_d_max = 0
        
        self.difference = 0
        self.diffbysrc = [0 for s in range(self.nbs)]
        
        self.true_world = 0
        self.ratio_true_world = 0
        self.nbanswers = 0

        self.iteration = self.G.iteration
        
        self.posteriori = deepcopy(self.rg.posteriori)
        
        self.posteriori.sort(reverse=True, key=itemgetter(1))
        groups = groupby(self.posteriori, itemgetter(1))
        self.posteriori = [[item[0] for item in data] for (key, data) in groups]
        
        #order with the trust
        self.ordre = self.G.get_rank_sources_name(True)
        # fact that won the vote
        self.best_f = []
        
    def gen_cpl_in(self, e, lst):
        """
        couple where e in lst
        """
        res = []
        for elt in lst:
            if e != elt:
                res.append((e,elt))
        return res

    def gen_cpl_out(self, e, lst):
        """
        couple where e not in lst
        """
        res = []
        for l in lst:
            for elt in l:
                res.append((e,elt))
        return res
        
    def gen_couple(self, lst):
        """
        generate every couple
        """
        res = []
        for i in range(len(lst)):
            l = lst[i]
            for e in l:
                res.extend(self.gen_cpl_in(e, l))
                res.extend(self.gen_cpl_out(e, lst[i+1:]))            
        return res

    def nb_swap2(self, lt, lp):
        """
        compute number of swaps when order is not strict
        [1,2] > [4,3] & 1 > 2 > 3 > 4 => 2
        [1,2] > [4,3] & 4 > 1 > 2 > 3 => 6
        """
        self.swap2 = True
        cpllt = self.gen_couple(lt)
        cpllp = self.gen_couple(lp)
        diff = set(cpllt).symmetric_difference(set(cpllp))
        return len(diff)
            
    def min_swap(self, lst, n):
        arrPos = [[0 for x in range(2)] for y in range(n)]
        for i in range(n):
            arrPos[i][0] = lst[i]
            arrPos[i][1] = i
        arrPos.sort()
    
        visited = [False] * (n)
        res = 0
        for i in range(n):
            if (visited[i] or arrPos[i][1] == i):
                continue
            cycle_size = 0
            j = i
            while (not visited[j]):	
                visited[j] = 1
                j = arrPos[j][1]
                cycle_size += 1
            res += (cycle_size - 1)
        return res
    
    def nb_swap1(self, lt, lp):
        """
        nb swap with strict order
        lt, lp same length
        """
        self.swap1 = True
        mp = {}
        for i in range(len(lt)):
            mp[lp[i]] = i
        #stock in lp the index where the element should be
        for i in range(len(lt)):
            lp[i] = mp[lt[i]]
        return self.min_swap(lp, len(lt))
    
    def nb_swap(self, lt, lp):
        """
        call the function
        """
        if len(lt) != self.nbs or len(lp) != self.nbs:
            return self.nb_swap2(lt, lp)
        return self.nb_swap1(list(np.array(lt).flatten()), list(np.array(lp).flatten()))
        
    def compute_swaps(self):
        """
        compute the nb swap between the trust (ordre) ranking and the a posteriori ranking
        
        if strict order -> swap
        else smt close to kendall rank
        """
        lt = deepcopy(self.ordre)
        lp = deepcopy(self.posteriori)
        
        self.swap = self.nb_swap(lt, lp)
        # self.swap_max = ((self.nbs-1) * self.nbs) / 2
        self.swap_max = ((self.nbs-1) * self.nbs)
        
    def compute_truth(self):
        for i in range(len(self.G.obj.of)):
            best = self.G.obj.get_best_fact(i)
            for f in self.G.obj.of[i].prec:
                if f in best:
                    if f.is_true:
                        self.TP += 1
                    else:
                        self.FP += 1
                else:
                    if f.is_true:
                        self.FN += 1
                    else:
                        self.TN += 1
    
    def compute_metrics(self):
        tmp = (self.TP+self.FP)
        self.precision = self.TP / tmp

        tmp = self.TP + self.FN + self.FP
        self.csi = (self.TP / tmp)

        tmp = (self.TP+self.FP+self.TN+self.FN)
        self.accuracy = (self.TP+self.TN) / tmp
        
        tmp = (self.TP+self.FN)
        if tmp > 0:
            self.recall = self.TP / tmp
            
    def compute_euclidean_distance(self):
        post = np.array(self.rg.posteriori_trust)
        trust = np.array(self.G.trust_s)
        self.euclidean_d = round(np.sqrt(np.sum(np.square(post-trust))),3)
        m = []
        for t in trust:
            if t < 0.5:
                m.append(1-t)
            else:
                m.append(t)
        m = np.array(m)
        zeros = np.zeros(self.rg.nbs)
        self.euclidean_d_max = round(np.sqrt(np.sum(np.square(zeros-m))),3)
        
    def compute_difference(self):
        for i in range(self.rg.nbs):    
            self.difference += abs(self.G.trust_s[i] - self.rg.posteriori_trust[i])
            self.diffbysrc[i] = abs(self.G.trust_s[i] - self.rg.posteriori_trust[i])
        self.difference /= self.rg.nbs
        
    def compute_formula_stats(self):
        if self.JAG != None:
            self.nbanswers = self.JAG.nbmax
            
            self.alg_consistent = int(self.JAG.alg_consistent)
            self.maj_consistent = int(self.JAG.maj_consistent)
            
            if self.JAG.truth_found:
                self.true_world = 1
                self.ratio_true_world = 1 / self.JAG.nbmax
            else:
                self.true_world = 0
                self.ratio_true_world = 0
            # print(self.JAG.__repr__, self.ratio_true_world, self.nbanswers)
            
            # On regarde toutes les réponses et on fait le calcul
            tmp = []
            
            for ans in self.JAG.answers:
                tmp.extend(ans)
                
                TP = 0
                TN = 0
                FP = 0
                FN = 0
                
                for i in range(len(ans)):
                    if ans[i] == self.JAG.truth_form[i]:
                        self.TP += 1
                        self.TN += 1
                        TP += 1
                        TN += 1
                    else:
                        self.FP += 1
                        self.FN += 1
                        FP += 1
                        FN += 1
                if TP == 0:
                    self.precision_formula_mean += 0
                    self.csi_formula_mean += 0
                else:
                    v = (TP / (TP+FP))
                    self.mem.append([v])
                    self.precision_formula_mean += v
                    if self.precision_formula_min == -1:
                        self.precision_formula_min = v
                    if v < self.precision_formula_min:
                        self.precision_formula_min = v
                    if v > self.precision_formula_max:
                        self.precision_formula_max = v
                        
                    v = (TP / (TP+FN+FP))
                    self.mem[-1].append(v)
                    self.csi_formula_mean += v
                    if self.csi_formula_min == -1:
                        self.csi_formula_min = v
                    if v < self.csi_formula_min:
                        self.csi_formula_min = v
                    if v > self.csi_formula_max:
                        self.csi_formula_max = v
            #     print(ans, ":", TP, "/", TP, "+", FP, "+", FN, "TP / TP + FP + FN")
            # print()
            
            if self.csi_formula_min == -1:
                self.csi_formula_min = 0
            if self.precision_formula_min == -1:
                self.precision_formula_min = 0
            
            self.precision_formula_mean /= len(self.JAG.answers)
            self.csi_formula_mean /= len(self.JAG.answers)

            cnt = Counter(tmp)

            TP = 0
            TN = 0
            FP = 0
            FN = 0
            TP2 = 0
            TN2 = 0
            FP2 = 0
            FN2 = 0
                
            for i in range(len(self.JAG.truth_form)):
                j = i+1
                # On prend que les formules ou on a une Unanimite sinon on considere la reponse 
                # comme fausse
                if f"{j}" in cnt and f"n{j}" in cnt:
                    FN2 += 1
                    FP2 += 1
                elif f"{j}" in cnt and f"n{j}" not in cnt:
                    if self.JAG.truth_form[i] == f"{j}":
                        TP2 += 1
                        TN2 += 1
                    else:
                        FP2 += 1
                        FN2 += 1
                elif f"{j}" not in cnt and f"n{j}" in cnt:
                    if self.JAG.truth_form[i] == f"n{j}":
                        TP2 += 1
                        TN2 += 1
                    else:
                        FP2 += 1
                        FN2 += 1
                # On prend que les formules majoritaire sinon on considere une reponse 
                # comme fausse et correcte
                if cnt[f"{i+1}"] > cnt[f"n{i+1}"]:
                    if self.JAG.truth_form[i] == f"{i+1}":
                        TP += 1
                        TN += 1
                    else:
                        FN += 1
                        FP += 1
                elif cnt[f"{i+1}"] < cnt[f"n{i+1}"]:
                    if self.JAG.truth_form[i] == f"n{i+1}":
                        TP += 1
                        TN += 1
                    else:
                        FN += 1
                        FP += 1
                else:
                    TP += 1
                    FP += 1
                    
            if TP == 0:
                self.precision_formula_majority += 0
                self.csi_formula_majority += 0
            else:
                self.precision_formula_majority = TP / (TP+FP)
                self.csi_formula_majority = TP / (TP+FN+FP)

   
            if TP2 == 0:
                self.precision_formula_unanime += 0
                self.csi_formula_unanime += 0
            else:
                self.precision_formula_unanime = TP2 / (TP2+FP2)
                self.csi_formula_unanime = TP2 / (TP2+FN2+FP2)
    
    def compute_proportion(self):
        """
        """
        if self.BMG != None:
            # vrai monde trouve
            self.true_world_guess = self.BMG.nb_true_found
            # mauvais monde classe comme vrai
            self.true_world_wrong = self.BMG.nb_false_found
            # autre monde correctement classe
            self.all_worlds_guess = 0
            #
            self.prc_claim_truth = self.BMG.nb_claim_truth / self.nbs
            #
            self.len_bases = sum(self.BMG.len_bases) / self.nbs
            
            for i in range(len(self.BMG.answers_wneg)):
                if self.BMG.answers_wneg[i] == self.BMG.truth_form_wneg[i]:
                    # self.correct += 1
                    self.all_world_guess += 1
                    # if self.BMG.answers_wneg[i] != self.BMG.truth_form[0]:
                    #     self.false_world_guess += 1
                # else:
                #     self.wrong += 1
                    
            #
            self.nb_answers = self.BMG.nb_total
            #
            self.precision_trust_un = ((self.all_world_guess/self.BMG.len_interpretation)*0.5) + (self.true_world_guess*0.5)
            #
            self.precision_trust_deux = self.true_world_guess / self.nb_answers
            #
            self.ham_hausdorff = self.BMG.ham_hausdorff
            self.avg_ham_hausdorff = self.BMG.avg_ham_hausdorff
            
    def compute_bms_metrics(self):
        if self.BMG != None:
            
            self.taille_formule_avg = self.BMG.taille_formule_avg
            self.len_croyance_avg = sum([sum(self.BMG.G.sf[i]) for i in range(len(self.BMG.G.sf))])/len(self.BMG.G.sf)
            
            if self.BMG.nb_total2 == 0:
                self.formulas_good = 0
            else:
                self.formulas_good = self.BMG.formulas_good / self.BMG.nb_total2
            
            if len(self.BMG.avg_score) == 0:
                self.avg_good = 0
            else:
                self.avg_good = sum(self.BMG.avg_score) / len(self.BMG.avg_score)
                
            
            self.nbanswers = self.BMG.nb_answers
            
            self.bms_truth = self.BMG.nb_true_found / self.BMG.nb_total
            
            if self.BMG.nbi_una > 0:
                self.truth_una = self.BMG.truth_una / self.BMG.nbi_una
                self.distance_una = (self.BMG.nb_literals - (self.BMG.distance_una / self.BMG.nbi_una)) / self.BMG.nb_literals
            
            # la distance la plus eloigne de la verite
            self.distance_max = (self.BMG.nb_literals - max(self.BMG.distance_intp)) / self.BMG.nb_literals
            # la distance la plus proche de la verite
            self.distance_min = (self.BMG.nb_literals - min(self.BMG.distance_intp)) / self.BMG.nb_literals
            # la distance moyenne par rapport a la verite
            self.distance_avg = (self.BMG.nb_literals - (sum(self.BMG.distance_intp) / len(self.BMG.distance_intp))) / self.BMG.nb_literals
            
            self.avg_len_maxcons = self.BMG.len_maxcons
            self.max_len_maxcons = self.BMG.max_len_maxcons
            self.min_len_maxcons = self.BMG.min_len_maxcons
            
            self.truth_in_mc = self.BMG.truth_in_mc
            
            # self.bms_truth = self.BMG.nb_true_found / self.BMG.nb_total
            # self.alg_consistent = self.BMG.consistant
            # self.nbanswers = self.BMG.nb_answers
            
            # self.bms_truth_una = self.BMG.nb_true_found_una / self.BMG.nb_total_una
    
    def run_all(self):
        """
        run all the metrics
        """
        if constants.FORMULA == constants.RUN_TD:
            self.compute_truth()
        elif constants.FORMULA == constants.RUN_JA:
            self.compute_formula_stats()
        elif constants.FORMULA == constants.RUN_BS:
            self.compute_bms_metrics()

        self.compute_swaps()
        self.compute_euclidean_distance()
        self.compute_difference()
        
        if constants.FORMULA not in [constants.RUN_BS]:
            self.compute_metrics()
    
# if __name__ == "__main__":
    # t = AttMetrics()
    # t.compute_swaps()
from v4.constants import constants

from v4.generation import spe_metrics as spm

class Metrics:
    def __init__(self, experience):
        """
        res : res for the metric in use
        exp : experience with all the graphs
        """
        self.nb_methods = constants.NB_METHODS
        self.res = []
        self.exp = experience
        if experience != None:
            #Change the number of sources (mandatory IF nvalue = SRC)
            self.exp.nbs = self.exp.graphes[0].nbs
        #id for the metrics in dict
        self.n_methods = constants.ID_METRICS
        #id in list for the metrics
        self.id_methods = list(self.n_methods.keys())
        
        self.n = -1
        self.mini = True
        
        self.spe_metric = None
        
        self.id_methods_sources = constants.ID_METHODS_SOURCES
        
        self.metrics = [self.swaps, self.swaps_norma, 
                        self.euclidean_distance, self.euclidean_distance_norma,
                        self.difference, self.metric_trust, self.ranking_order,
                        self.precision, self.accuracy, self.recall,
                        self.csi, self.iteration_avg, self.iteration_max,
                        self.number_answers,
                        self.precision_mean, self.precision_unanime,
                        self.csi_mean, self.csi_unanime,
                        self.csi_min, self.csi_max,
                        self.precision_min, self.precision_max,
                        self.csi_majorite, self.precision_majorite,
                        self.alg_consistent, self.maj_consistent, 
                        self.truth_eq_maj, self.same,
                        self.precision_trust_un, self.precision_trust_deux,
                        self.bm_nb_answers,
                        self.ham_hausdorff, self.avg_ham_hausdorff,
                        self.prc_claim_truth, self.len_bases,
                        self.number_truth, 
                        self.distance_max, self.distance_min, self.distance_avg, 
                        self.truth_in_mc,
                        self.len_avg_mc, self.len_min_mc, self.len_max_mc,
                        self.bm_unanime_distance, self.bm_unanime_truth,
                        self.taille_croyance, self.taille_formulas, self.number_truth2,
                        self.avg_truth3]
        
        #must be the same name in the file latex (used is latex.py)
        self.metrics_name = constants.METRICS_NAMES
        
    def __str__(self):
        if self.n == -1:
            return "No results"
        res = f"Results for {self.metrics[self.n].__name__} with {self.exp.graphes[0].rgs[0].nbs} sources, prior {self.exp.graphes[0].prior} and graph {self.exp.graphes[0].rgs[0].typeg}:\n"
        for i in range(len(constants.ORDER)):
            res += f"{constants.ORDER[i]} : {self.res[i]}\n"
        res += "\n"
        return res
    
    def execute(self):
        return self.n in list(constants.ID_METRICS_ACTIVE.values())
    
    def avg_truth3(self):
        self.mini = False
        self.n = self.n_methods["Bn3"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.avg_good
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def number_truth2(self):
        """sert a rien"""
        self.mini = False
        self.n = self.n_methods["Bn2"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.formulas_good
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
            
    def number_truth(self):
        """Bn1"""
        self.mini = False
        self.n = self.n_methods["Bnt"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.bms_truth
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]

    def taille_formulas(self):
        self.mini = False
        self.n = self.n_methods["Btf"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.taille_formule_avg
            self.res = [(r/self.exp.nb_exp) for r in self.res]
    
    def taille_croyance(self):
        self.mini = False
        self.n = self.n_methods["Btc"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.len_croyance_avg
            self.res = [(r/self.exp.nb_exp) for r in self.res]

    def bm_unanime_distance(self):
        self.mini = False
        self.n = self.n_methods["Bud"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.distance_una
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def bm_unanime_truth(self):
        self.mini = False
        self.n = self.n_methods["But"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.truth_una
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]

    def len_avg_mc(self):
        self.mini = False
        self.n = self.n_methods["Bla"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.avg_len_maxcons
            self.res = [(r/self.exp.nb_exp) for r in self.res]

    def len_max_mc(self):
        self.mini = False
        self.n = self.n_methods["Blh"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.max_len_maxcons
            self.res = [(r/self.exp.nb_exp) for r in self.res]
            
    def len_min_mc(self):
        self.mini = False
        self.n = self.n_methods["Bll"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.min_len_maxcons
            self.res = [(r/self.exp.nb_exp) for r in self.res]

    def truth_in_mc(self):
        self.mini = False
        self.n = self.n_methods["Btm"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.truth_in_mc
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]

    def distance_avg(self):
        self.mini = False
        self.n = self.n_methods["Bda"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.distance_avg
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]

    def distance_min(self):
        self.mini = False
        self.n = self.n_methods["Bdl"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.distance_min
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def distance_max(self):
        self.mini = False
        self.n = self.n_methods["Bdh"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.distance_max
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]

    # -----------------

    def len_bases(self):
        self.mini = False
        self.n = self.n_methods["Blb"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.len_bases
            self.res = [(self.res[0]/self.exp.nb_exp) for r in self.res]

    def prc_claim_truth(self):
        self.mini = False
        self.n = self.n_methods["Bpt"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.prc_claim_truth
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def precision_trust_un(self):
        self.mini = False
        self.n = self.n_methods["Btu"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.precision_trust_un
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def precision_trust_deux(self):
        self.mini = False
        self.n = self.n_methods["Btd"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.precision_trust_deux
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def bm_nb_answers(self):
        self.mini = True
        self.n = self.n_methods["Bna"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.nb_answers
            self.res = [(r/self.exp.nb_exp) for r in self.res]
    
    def ham_hausdorff(self):
        self.mini = False
        self.n = self.n_methods["Bhh"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.ham_hausdorff
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def avg_ham_hausdorff(self):
        self.mini = False
        self.n = self.n_methods["Bha"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.avg_ham_hausdorff
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def same(self):
        self.mini = False
        self.n = self.n_methods["Sam"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                if g.rgs[1].metric_att.JAG.answers == g.rgs[3].metric_att.JAG.answers:
                        self.res[0] += 1
                        self.res[1] += 1
                        self.res[3] += 1
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def truth_eq_maj(self):
        self.mini = False
        self.n = self.n_methods["Tem"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.truth_eq_maj
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]

    def alg_consistent(self):
        self.mini = False
        self.n = self.n_methods["Mca"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.alg_consistent
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def maj_consistent(self):
        self.mini = False
        self.n = self.n_methods["Mcm"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.maj_consistent
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]

    def csi_majorite(self):
        self.mini = False
        self.n = self.n_methods["Csm"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.csi_formula_majority
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def precision_majorite(self):
        self.mini = False
        self.n = self.n_methods["Prm"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.precision_formula_majority
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def csi_max(self):
        self.mini = False
        self.n = self.n_methods["Csh"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.csi_formula_max
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def precision_max(self):
        self.mini = False
        self.n = self.n_methods["Prh"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.precision_formula_max
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def csi_min(self):
        self.mini = False
        self.n = self.n_methods["Csl"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.csi_formula_min
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
            
    def precision_min(self):
        self.mini = False
        self.n = self.n_methods["Prl"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.precision_formula_min
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def csi_mean(self):
        self.mini = False
        self.n = self.n_methods["Csa"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.csi_formula_mean
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
    
    def precision_mean(self):
        self.mini = False
        self.n = self.n_methods["Pra"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.precision_formula_mean
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def csi_unanime(self):
        self.mini = False
        self.n = self.n_methods["Csu"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.csi_formula_unanime
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def precision_unanime(self):
        self.mini = False
        self.n = self.n_methods["Pru"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.precision_formula_unanime
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def number_answers(self):
         self.mini = True
         self.n = self.n_methods["Na"]
         self.res = [0 for i in range(self.nb_methods)]
         if self.execute():
             for g in self.exp.graphes:
                 for i in range(len(g.rgs)):
                     self.res[i] += g.rgs[i].metric_att.nbanswers
             self.res = [(r/self.exp.nb_exp) for r in self.res]  
    
    def ranking_order(self):
        """
        # Number of graph with the exact ranking i.e. nb_swap == 0
        """
        self.mini = False
        self.n = self.n_methods["RO"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in self.id_methods_sources:
                    self.res[i] += int(g.rgs[i].metric_att.swap == 0)
            self.res = [(r/self.exp.nb_exp) for r in self.res]
    
    def swaps(self):
        """
        Return the average number of swaps
        """
        self.mini = True
        self.n = self.n_methods["S"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in self.id_methods_sources:
                    self.res[i] += g.rgs[i].metric_att.swap
            self.res = [r/self.exp.nb_exp for r in self.res]
        
    def swaps_norma(self):
        """
        Return the normalize average number of swaps
        """
        self.mini = True
        self.n = self.n_methods["SN"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in self.id_methods_sources:
                    # maxi = ((g.rgs[i].nbs-1) * g.rgs[i].nbs) / 2
                    self.res[i] += (g.rgs[i].metric_att.swap/g.rgs[i].metric_att.swap_max)
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
            
    def euclidean_distance(self):
        """
        Return the average euclidean distance
        """
        self.mini = True
        self.n = self.n_methods["E"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in self.id_methods_sources:
                    self.res[i] += g.rgs[i].metric_att.euclidean_d
            self.res = [(r/self.exp.nb_exp) for r in self.res]
        
    def euclidean_distance_norma(self):
        """
        Return the normalize average euclidean distance
        """
        self.mini = True
        self.n = self.n_methods["EN"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in self.id_methods_sources:
                    self.res[i] += (g.rgs[i].metric_att.euclidean_d/g.rgs[i].metric_att.euclidean_d_max)        
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def difference(self):
        """
        Return the average difference between the a posteriori and trust
        """
        self.mini = True
        self.n = self.n_methods["D"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in self.id_methods_sources:
                    self.res[i] += g.rgs[i].metric_att.difference
            self.res = [(r/self.exp.nb_exp) for r in self.res]
                
    def precision(self):
        """
        Return the average precision
        """
        self.mini = False
        self.n = self.n_methods["P"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.precision
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def accuracy(self):
        """
        Return the average accuracy
        """
        self.mini = False
        self.n = self.n_methods["A"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.accuracy
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def recall(self):
        """
        Return the average recall
        """
        self.mini = False
        self.n = self.n_methods["R"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.recall
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def csi(self):
        """
        Return the average csi
        """
        self.mini = False
        self.n = self.n_methods["CSI"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.csi
            self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def iteration_avg(self):
        """
        Return the average number of iterations
        """
        self.mini = True
        self.n = self.n_methods["Ia"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.iteration
            self.res = [(r/self.exp.nb_exp) for r in self.res]
        
    def iteration_max(self):
        """
        Return the maximum number of iterations
        """
        self.mini = True
        self.n = self.n_methods["Im"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.execute():
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] = max(self.res[i], g.rgs[i].metric_att.iteration)
        
    def metric_trust(self):
        """
        """
        self.mini = True
        self.n = self.n_methods["Mt"]
        if self.execute():
            if self.spe_metric == None:
                self.spe_metric = spm.SpeMetrics(experience=self.exp)
        
        
from v4.vote import plurality as maj
from v4.vote import borda as bor

from v4.graph import derive, prio, mylog

from v4.constants import constants

from v4.other_methods import sums, usums, hna, truthfinder, voting_majo
from v4.other_methods import averagelog, pooledinvestment, investment

from v4.generation import random_graph as rg
from v4.generation import priors as pr

from v4.judag import sfsum, sfproduit, sfleximax, sfleximin
from v4.judag import RDH, RMCSA, RMSA, RMWA, RRA
from v4.judag import COUNTSUM, COUNTMAX, COUNTMIN
from v4.judag import baseVo

from v4.belms import sfleximin as sfleximinBM
from v4.belms import sfleximax as sfleximaxBM
from v4.belms import sfbmscavg, sfbmsum
from v4.belms import mcdrastic, mcintersect, mcsymm, mxc, mxcd

from copy import deepcopy

class GraphMethods:
    """
    Generate a graph for the 8 methods
    Run all the graph
    
    #use another class for metrics and get the results on the nb_exp graph
    """
    def __init__(self, prior, nbo=10, nbfl=3, nbfu=3, nbs=10, typeg='ncpu', min_fs=1, allg=False):
        self.rgs = []
        self.prior = prior
        self.nbo = nbo
        self.nbs = nbs
        self.nbfl = nbfl
        self.nbfu = nbfu
        self.typeg = typeg
        self.min_fs = min_fs
        self.graphes = []
        
        self.names_nonorma = constants.NAMES_NONORMA
        
        self.names = constants.NAMES
            
    def create_graph(self):
        """
        create graph with default para (Plurality - normaA)
        """
        vote = maj.Plurality
        option = 1
        norma = constants.NORMA_A
            
        return rg.randomGraph(voting_method=vote, 
                                       voting_parameters=option, 
                                       nbs=self.nbs, nbo=self.nbo, 
                                       nbfl=self.nbfl, nbfu=self.nbfu, 
                                       prior=self.prior, norma=norma, 
                                       typeg=self.typeg, min_fs=self.min_fs)
    
    def all_methods(self, i):        
        if constants.FORMULA == constants.RUN_BS:
            self.all_BS(i)
        elif constants.FORMULA == constants.RUN_JA:
            self.all_JA(i)
        elif constants.FORMULA == constants.RUN_TD:
            if constants.TD_TEST:
                self.all_TD_TEST(i)
            else:
                self.all_TD(i)
    
    def all_BS(self, i):
        rGA = deepcopy(self.rgs[0])
        option_vote = self.rgs[0].G.G.obj.voting_met.option
        # norma = constants.NORMA_O
        norma = constants.NORMA_A
        if constants.ORDER[i] == constants.NAMES[1]:
            rGA.G = mcdrastic.McDrastic(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, norma, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, relia=rGA.G.relia, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[2]:
            rGA.G = mcsymm.McSymm(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, norma, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, relia=rGA.G.relia, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[3]:
            rGA.G = mcintersect.McIntersect(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, norma, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, relia=rGA.G.relia, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[4]:
            rGA.G = sfleximinBM.SFLeximin(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, norma, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, relia=rGA.G.relia, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[5]:
            rGA.G = mxc.Mxc(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, norma, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, relia=rGA.G.relia, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[6]:
            rGA.G = mxcd.Mxcd(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, norma, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, relia=rGA.G.relia, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[7]:
            rGA.G = sfbmscavg.SFbmSCAvg(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_O, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[8]:
            rGA.G = sfbmscavg.SFbmSCAvg(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, norma, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, relia=rGA.G.relia, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[9]:
            rGA.G = sfbmsum.SFbmSSum(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, norma, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, formulas=rGA.G.formulas, table=rGA.G.maxcons_ind, maxcons=rGA.G.maxcons, agents=rGA.G.agents, distance=rGA.G.distance, relia=rGA.G.relia, agents_ind=rGA.G.agents_ind, formulas_chosed=rGA.G.formulas_chosed)
            self.rgs.append(rGA)
            
    
    def generate_other_methods(self):
        for i in range(len(constants.NAMES)):
            if constants.ORDER[i] in constants.RUN_METHODS:
                self.all_methods(i)
    
    def run_all(self, interp):
        for g in self.rgs:
            # if isinstance(g.G, graph.Graph):
            #     print(g.G.trust_s, g.G.trust_f)
            # else:
            #     print(g.G.G.trust_s, g.G.G.trust_f)
            if constants.FORMULA == constants.RUN_BS:
                g.G.decision()
            elif constants.FORMULA == constants.RUN_JA:
                g.G.aggr()
            elif constants.FORMULA == constants.RUN_TD:
                g.G.run_noprint()
            # if isinstance(g.G, graph.Graph):
            #     print(g.G.trust_s, g.G.trust_f)
            # else:
            #     print(g.G.G.trust_s, g.G.G.trust_f)
            # print()
            g.update_metric_att(interp)

    def all_BM(self, i):
        rGA = deepcopy(self.rgs[0])
        option_vote = self.rgs[0].G.G.obj.voting_met.option
        if constants.ORDER[i] == constants.NAMES[1]:
            rGA.G = sumbm.Sumbm(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, interp=rGA.G.interpretation, distance=rGA.G.distance, agents=rGA.G.agents, ind_int=rGA.G.ind_int, distance_drastic=rGA.G.distance_drastic)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[2]:
            rGA.G = leximaxbm.Leximaxbm(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, interp=rGA.G.interpretation, distance=rGA.G.distance, agents=rGA.G.agents, ind_int=rGA.G.ind_int, distance_drastic=rGA.G.distance_drastic)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[3]:
            rGA.G = drastic.Drastic(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.truth, Gr=rGA.G, nbl=rGA.G.nb_literals, interp=rGA.G.interpretation, distance=rGA.G.distance, agents=rGA.G.agents, ind_int=rGA.G.ind_int, distance_drastic=rGA.G.distance_drastic)
            self.rgs.append(rGA)
    
    def all_TD_TEST(self, i):
        option_vote = self.rgs[0].G.obj.voting_met.option
        rGA = deepcopy(self.rgs[0])
        if constants.ORDER[i] == constants.NAMES[1]:
            rGA.G = mylog.MyLog(G=rGA.G, voting_met=maj.Plurality, vote_para=option_vote, name_norma=constants.NORMA_A)
            # rGA.G = mylog.MyLog(G=rGA.G, voting_met=maj.Plurality, vote_para=option_vote, name_norma=constants.NORMA_A)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[2]:
            # norma O
            # rGA.change_norma(constants.NORMA_O)
            # rGA.G = derive.Derive(G=rGA.G, voting_met=maj.Plurality, vote_para=option_vote, name_norma=constants.NORMA_O)
            # norma A
            rGA.G = derive.Derive(G=rGA.G, voting_met=maj.Plurality, vote_para=option_vote, name_norma=constants.NORMA_A)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[3]:
            # norma O
            # rGA.change_norma(constants.NORMA_O)
            # rGA.G = prio.Prio(G=rGA.G, voting_met=maj.Plurality, vote_para=option_vote, name_norma=constants.NORMA_O)
            # norma A
            rGA.G = prio.Prio(G=rGA.G, voting_met=maj.Plurality, vote_para=option_vote, name_norma=constants.NORMA_A)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[4]:
            # rGA.change_norma(constants.NORMA_O)
            rGA.change_vote(bor.Borda, option_vote)
            self.rgs.append(rGA)
    
    def all_TD(self, i):
        option_vote = self.rgs[0].G.obj.voting_met.option
        rGA = deepcopy(self.rgs[0])
        if constants.ORDER[i] == constants.NAMES[1]:
            rGA.change_norma(constants.NORMA_O)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[2]:
            rGA.change_vote(bor.Borda, option_vote)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[3]:
            rGA.change_norma(constants.NORMA_O)
            rGA.change_vote(bor.Borda, option_vote)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[4]:
            rGA.G = sums.Sums(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[5]:
            rGA.G = usums.Usums(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[6]:
            rGA.G = hna.Hna(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[7]:
            rGA.G = truthfinder.Truthfinder(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[8]:
            rGA.G = voting_majo.VotingMajo(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[9]:
            rGA.G = averagelog.AverageLog(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[10]:
            rGA.G = investment.Investment(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[11]:
            rGA.G = pooledinvestment.PooledInvestment(rGA.G)
            self.rgs.append(rGA)
    
    def all_JA(self, i):
        # met de la litt start a l'ind 4
        ind_litt_met = 4
        option_vote = self.rgs[0].G.G.obj.voting_met.option
        if i <= ind_litt_met:
            numg = 0
        else:
            # On prend une methode avec baseVO
            numg = ind_litt_met
            if not isinstance(self.rgs[numg].G, baseVo.BaseVoting):
                print(f"Must be a baseVo class: {self.rgs[numg].G.__repr__} - {i} - {numg} - {[r.G.__repr__ for r in self.rgs]} - {self.rgs[0].nom_agenda}")
                raise(f"Must be a baseVo class: {self.rgs[numg].G.__repr__}")
        rGA = deepcopy(self.rgs[numg])
        if i == ind_litt_met:
            vect = None
            form = None
            revres = None
            maj_form = None
            maj_formSF = None
        else:
            vect = rGA.G.vect
            form = rGA.G.form
            revres = rGA.G.revres
            maj_form = rGA.G.maj_form
            maj_formSF = rGA.G.maj_formSF
        if constants.ORDER[i] == constants.NAMES[1]:
            # rGA.G = sfleximax.Leximax(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G.G, form=rGA.G.form, vect=rGA.G.vect, revres=rGA.G.revres, maj_form=rGA.G.maj_form)
            rGA.G = sfleximax.Leximax(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[2]:
            rGA.G = sfleximin.Leximin(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[3]:
            rGA.G = sfproduit.Produitsf(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[4]:
            rGA.G = RMSA.RMSA(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[5]:
            rGA.G = RMCSA.RMCSA(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[6]:
            rGA.G = RMWA.RMWA(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[7]:
            rGA.G = RRA.RRA(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[8]:
            rGA.G = RDH.RDH(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[9]:
            rGA.G = COUNTSUM.COUNTSUM(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[10]:
            rGA.G = COUNTMAX.COUNTMAX(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[11]:
            rGA.G = COUNTMIN.COUNTMIN(rGA.G.G.mat_fs, rGA.G.G.mat_of, maj.Plurality, option_vote, constants.NORMA_A, len(rGA.G.G.mat_fs[0]), len(rGA.G.G.mat_fs), truth=rGA.G.G.obj.truth, model=rGA.G.model, Gr=rGA.G, form=form, vect=vect, revres=revres, maj_form=maj_form, maj_formSF=maj_formSF)
            self.rgs.append(rGA)
            
    def add_rg(self, G):
        """
        G : random_graph
        """
        self.rgs.append(G)
        
    def gen_one_graph(self):
        self.add_rg(self.create_graph())
        self.generate_other_methods()
        self.run_all()
    
if __name__ == "__main__":    
    nbo = 2
    nbfl = 2
    nbfu = 2
    
    nbs = 10
    len_prior=10
    
    typeg = 'ncpr'
    
    min_fs=1
    
    bmin=10
    bmax=90
    
    priors = pr.Priors(len_prior=len_prior, nbo=nbo, bmin=bmin, bmax=bmax)
    prc = priors.rand_percent()
    prior = priors.rand_prior(prc)
    print(prc, prior)
    
    graphmet = GraphMethods(prior, nbo=nbo, nbfl=nbfl, nbfu=nbfu, nbs=nbs, typeg=typeg, min_fs=min_fs, allg=False)
    
    #graphmet.gen_one_graph()
    
    #print(graphmet.rgs[0].metric_att.__dict__)
    #print(graphmet.rgs[9].metric_att.__dict__)
    
    #print(graphmet.rgs[0].G.to_file())
    
    # rgs = graphmet.rgs
    
    # res = ""
    # res2 = ""
    # name=[f"pl{nm.Normalize.normaA_name()}", f"pl{nm.Normalize.normaO_name()}", f"bo{nm.Normalize.normaA_name()}", f"bo{nm.Normalize.normaO_name()}", "Sum", "Usum", "hna", "tf"]
    
    # for i in range(len(rgs)):
    #     if i < 4:
    #         print(rgs[i].voting_met, rgs[i].norma)
    #         G = rgs[i].G
    #     else:
    #         print(rgs[i].G)
    #         G = rgs[i].G.G
    #     bf = [[(n.id, n.trust) for n in l] for l in G.obj.get_best_facts_group()]
    #     bf2 = [(n.id, n.trust) for n in G.obj.get_best_facts()]
        
    #     #print("a posteriori name/proba", rgs[i].posteriori)
    #     #print("a posteriori ranking   ", rgs[i].metric_att.posteriori)
    #     #print("ranking with the trust ", rgs[i].metric_att.ordre)
    #     print("TP", rgs[i].metric_att.TP, "FP", rgs[i].metric_att.FP, "FN", rgs[i].metric_att.FN)
    #     print("Number of true facts   ", len(bf2))
    #     print(bf)
    #     print()
        
    #     res += f"{name[i]}:{round(rgs[i].metric_att.precision,2)} - "
    #     res2 += f"{name[i]}:{round(rgs[i].metric_att.csi,2)} - "
        
    # print("Precision", res)
    # print()
    # print("CSI", res2)
        
        

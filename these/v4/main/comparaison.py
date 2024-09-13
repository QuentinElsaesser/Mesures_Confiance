import os, sys

from v4.vote import plurality as voting
from v4.vote import borda as voting2

from v4.graph import graph
from v4.examples import read_file as rf
from v4.constants import constants

from v4.other_methods import sums, usums, hna, truthfinder, voting_majo, averagelog, investment, pooledinvestment


def noprint_G(G):
    print(G.obj.voting_met, G.normalizer.name)
    G.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_A
    G.change_norma(norma)
    G.change_vote(voting_method_b, para_b)
    print(G.obj.voting_met, G.normalizer.name)
    G.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = sums.Sums(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = usums.Usums(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = hna.Hna(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = truthfinder.Truthfinder(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = voting_majo.VotingMajo(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = averagelog.AverageLog(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = investment.Investment(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = pooledinvestment.PooledInvestment(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
def print_G(G):
    res = []
    
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    res.append(("SF^PA",G.get_winners(),[round(n,3) for n in G.trust_s], [round(n,3) for n in G.trust_f]))
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    res.append(("SF^PC",G.get_winners(),[round(n,3) for n in G.trust_s], [round(n,3) for n in G.trust_f]))
    
    norma = constants.NORMA_A
    G.change_norma(norma)
    G.change_vote(voting_method_b, para_b)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    res.append(("SF^BA",G.get_winners(),[round(n,3) for n in G.trust_s], [round(n,3) for n in G.trust_f]))
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    res.append(("SF^BC",G.get_winners(),[round(n,3) for n in G.trust_s], [round(n,3) for n in G.trust_f]))
    
    algo = sums.Sums(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(algo.G.str_trust())
    
    res.append(("SUMS ",algo.G.get_winners(),[round(n,3) for n in algo.G.trust_s], [round(n,3) for n in algo.G.trust_f]))

    algo = usums.Usums(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(algo.G.str_trust())
    
    res.append(("USUMS",algo.G.get_winners(),[round(n,3) for n in algo.G.trust_s], [round(n,3) for n in algo.G.trust_f]))

    algo = hna.Hna(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(algo.G.str_trust())
    
    res.append(("HNA  ",algo.G.get_winners(),[round(n,3) for n in algo.G.trust_s], [round(n,3) for n in algo.G.trust_f]))

    algo = truthfinder.Truthfinder(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(algo.G.str_trust())
    
    res.append(("TF   ",algo.G.get_winners(),[round(n,3) for n in algo.G.trust_s], [round(n,3) for n in algo.G.trust_f]))
    
    algo = voting_majo.VotingMajo(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(algo.G.str_trust())
    
    res.append(("VOTNG",algo.G.get_winners(),[round(n,3) for n in algo.G.trust_s], [round(n,3) for n in algo.G.trust_f]))
    
    algo = averagelog.AverageLog(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(algo.G.str_trust())
    
    res.append(("AV.LG",algo.G.get_winners(),[round(n,3) for n in algo.G.trust_s], [round(n,3) for n in algo.G.trust_f]))
    
    algo = investment.Investment(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(algo.G.str_trust())
    
    res.append(("INV  ",algo.G.get_winners(),[round(n,3) for n in algo.G.trust_s], [round(n,3) for n in algo.G.trust_f]))
    
    algo = pooledinvestment.PooledInvestment(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(algo.G.str_trust())
    
    res.append(("P-INV",algo.G.get_winners(),[round(n,3) for n in algo.G.trust_s], [round(n,3) for n in algo.G.trust_f]))
    
    for m in res:
        print(m)

if __name__ == "__main__":
    #Default parameters
    norma = constants.NORMA_A
    opt = 1
    #exmaple article
    # name = "examples/graphes/ce_compsrc.txt"
    
    name = "examples/graphes/capital.txt"
    
    para_b = 1
    voting_method_b = voting2.Borda
    
    para_m = 1
    voting_method_m = voting.Plurality
    
    for i in range(1, len(sys.argv)):
        if os.path.isfile(sys.argv[i]):
            name = sys.argv[i]
    
    mat_fs, mat_of, t = rf.read_file(name)
            
    G = graph.Graph(mat_fs, mat_of, voting_method_m, para_m, norma, len(mat_fs[0]), len(mat_fs))
    #print(G)
    
    print_G(G)
    # noprint_G(G)
    

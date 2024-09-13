import os, sys

from v4.vote import plurality as voting
from v4.vote import borda as voting2
from v4.vote import parameters_vote as pm

from v4.graph import graph
from v4.examples import read_file as rf
from v4.constants import constants

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
    
def print_G(G):
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_A
    G.change_norma(norma)
    G.change_vote(voting_method_b, para_b)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())

if __name__ == "__main__":
    #Default parameters
    norma = constants.NORMA_A
    opt = 3
    #exmaple article
    # name = "../examples/graphes/ce_norma_prop.txt"
    
    name = "v4/examples/graphes/graphe_diapo.txt"
    
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

    

from v4.vote import plurality as voting

from v4.belms import sfleximin, sfleximax, sfbmscavg, sfbmsum
from v4.belms import mcdrastic, mcintersect, mcsymm

from v4.constants import constants

from v4.examples import read_file as rf

import os, sys

if __name__ == "__main__":
    
    #Default parameters
    norma = constants.NORMA_A
    para = 1
    name = "v4/examples/bms/testbm.txt"

    voting_method = voting.Plurality
    
    for i in range(1, len(sys.argv)):
        if os.path.isfile(sys.argv[i]):
            name = sys.argv[i]
    
    print("file used :", name)

    mat_fs, mat_of, truth, nbintp, formulas, formulas_chosed = rf.read_file_bm(name)
    
    # nbintp = nb varaible
    
    interp = list(range(2**nbintp))
    
    if sys.argv[1] == "avgA":
        print("AVG norma A")
        G = sfbmscavg.SFbmSCAvg(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, nbl=nbintp, interp=interp, formulas=formulas, formulas_chosed=formulas_chosed)
    elif sys.argv[1] == "avgC":
        print("AVG norma C")
        G = sfbmscavg.SFbmSCAvg(mat_fs, mat_of, voting_method, para, constants.NORMA_O, len(mat_fs[0]), len(mat_fs), truth=truth, nbl=nbintp, interp=interp, formulas=formulas, formulas_chosed=formulas_chosed)
    elif sys.argv[1] == "sum":
        print("AVG norma A")
        G = sfbmsum.SFbmSSum(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, nbl=nbintp, interp=interp, formulas=formulas, formulas_chosed=formulas_chosed)
    elif sys.argv[1] == "max":
        print("Leximax")
        G = sfleximax.SFLeximax(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, nbl=nbintp, interp=interp, formulas=formulas, formulas_chosed=formulas_chosed)
    elif sys.argv[1] == "min":
        print("Leximin")
        G = sfleximin.SFLeximin(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, nbl=nbintp, interp=interp, formulas=formulas, formulas_chosed=formulas_chosed)
    elif sys.argv[1] == "dras":
        print("Drastic")
        G = mcdrastic.McDrastic(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, nbl=nbintp, interp=interp, formulas=formulas, formulas_chosed=formulas_chosed)
    elif sys.argv[1] == "symm":
        print("Symmetric")
        G = mcsymm.McSymm(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, nbl=nbintp, interp=interp, formulas=formulas, formulas_chosed=formulas_chosed)
    elif sys.argv[1] == "diff":
        print("Difference")
        G = mcintersect.McIntersect(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, nbl=nbintp, interp=interp, formulas=formulas, formulas_chosed=formulas_chosed)        
    else:
        print(f"ERROR {sys.argv[1]} n existe pas")

    for i in range(len(G.agents)):
        a = G.agents[i]
        print(f"Agents{i+1}", sorted(G.agents_to_interp(a)))
    G.decision()
    
    
    print("trust s : ", G.G.trust_s)
    for i in range(len(G.info)):
        #print(")))", G.info[i][0], "-", G.answers)
        print(f"Maxcons{i+1}", G.info[i][0] in G.answers ,[G.formulas_id[str(sorted(x))]+1 for x in G.info[i][0]], G.info[i][2], G.maxcons_to_interp([set(x) for x in G.info[i][0]]))
        print()
            
    print("Maxcons proposé(s):")
    for i in range(len(G.answers)):
        print(f"maxcons{i+1} : {[G.formulas_id[str(sorted(x))]+1 for x in G.answers[i]]} - {G.maxcons_to_interp(G.answers[i])}")
    print(G.G.obj.str_object())

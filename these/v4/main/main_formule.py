from v4.vote import plurality as voting

from v4.judag import sfsum, sfleximax, sfleximin, sfproduit
# from v4.judag import sfsrc
from v4.judag import RMSA, RMCSA, RMWA, RRA, RDH
from v4.judag import COUNTSUM, COUNTMAX, COUNTMIN

from v4.constants import constants

from v4.examples import read_file as rf

from v4.generation import generate_w_prop

import os, sys

if __name__ == "__main__":
    
    #Default parameters
    norma = constants.NORMA_A
    para = 1

    n = 6
    #name = f"v4/examples/formula/formula{n}.txt"
    
    # name = "v4/examples/formula/lang.txt"
    name = "v4/examples/formula/diff.txt"
    # name = "v4/examples/formula/majo.txt"
    
    print("file used :", name)

    voting_method = voting.Plurality
    
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == constants.NORMA_O:
            norma = constants.NORMA_O
        elif os.path.isfile(sys.argv[i]):
            name = sys.argv[i]
    
    mat_fs, mat_of, tmptruth, formula_file = rf.read_file_formula(name)
    truth = [0 for n in mat_fs]
    for i in range(len(tmptruth)):
        truth[tmptruth[i]-1] = 1
    #read file to get that
    #mat_fs_t = [np.array([0,1,0]), np.array([1,0,1]), np.array([0,0,0]), np.array([0,1,0]), np.array([1,0,1])]
    #mat_of_t = [np.array([1,1,1,0,0]), np.array([0,0,0,1,1])]
    
    generator = generate_w_prop.GenerateWProp(formula_file.split("/")[-1], 0, read_xp=True)
    model = generator.model

    if sys.argv[1] == "sum":
        print("SF-Sum")
        G = sfsum.Sumsf(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "max":
        print("Leximax")
        G = sfleximax.Leximax(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "min":
        print("Leximin")
        G = sfleximin.Leximin(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    # elif sys.argv[1] == "src":
    #     print("SF-Src")
    #     G = sfsrc.SFsrc(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "prod":
        print("SF-Product")
        G = sfproduit.Produitsf(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "rmsa":
        print("RMSA")
        G = RMSA.RMSA(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "rmcsa":
        print("RMCSA")
        G = RMCSA.RMCSA(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "rmwa":
        print("RMWA")
        G = RMWA.RMWA(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "rra":
        print("RRA")
        G = RRA.RRA(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "rdh":
        print("Rdh")
        G = RDH.RDH(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "csum":
        print("COUNTSUM")
        G = COUNTSUM.COUNTSUM(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "cmin":
        print("COUNTMIN")
        G = COUNTMIN.COUNTMIN(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    elif sys.argv[1] == "cmax":
        print("COUNTMAX")
        G = COUNTMAX.COUNTMAX(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    else:
        print(f"ERROR {sys.argv[1]} n existe pas")
    # elif sys.argv[1] == "ry":
        # print("Ry")
        # G = RY.RY(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    # elif sys.argv[1] == "rmnac":
        # print("RMNAC")
        # G = RMNAC.RMNAC(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model)
    
    G.aggr()
    print(G.G.mem_f[-1])
    for m in G.test:
        print(m)
    print("Ensemble de jugements choisis :")
    for a in G.answers:
        print(a)
    # print("RRA with G param")
    # G2 = RRA.RRA(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth, model=model, Gr=G)
    # G2.aggr()

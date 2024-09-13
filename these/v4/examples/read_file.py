import numpy as np

def read_file_bm(name):
    """
    OPERATEUR A FORMULE : SYNTAXIQUES
    return two Adjacency matrix
    1st : for each fact, which source claimed it
    2nd : for each object, which fact is linked to him
    
    files : 
        line with a # are ignored
        - is a delimiter to pass to the objects
        a empty line will be consider as an empty object except 
        at the end of the file, we ignored them
    """
    sf = []
    of = []
    truth = []
    s = 0
    o = 0
    src = True
    formulastmp = []
    formulas = dict()
    
    f = open(name, "r")
    lines = f.readlines()
    
    n=0
    while lines[n][0] == "#":
        n += 1
    
    #nb_s nb_o nb_f nb_l
    values = lines[n].split()
    
    nb_literals = int(values[3])
    
    formulas_chosed = [False for x in range(int(values[1])*2)]
    
    fs = [np.array([0 for j in range(int(values[0]))]) for i in range(int(values[2]))]

    #remove the empty lines at the end of the file
    j = 0
    for i in range(len(lines)-1, 2, -1):
        if not lines[i].strip():
            j += 1
        else:
            break
    if j > 0:
        lines = lines[:-j]
    
    for i in range(n+1, len(lines)):
        if lines[i][0] == '#':
            if lines[i].startswith("#truth :"):
                truth = lines[i]
            elif lines[i].startswith("#Formulae:"):
                formulastmp = lines[i]
            continue
        elif lines[i][0] == '-':
            src = False
            continue
        
        if "\n" in lines[i]:
            elts = lines[i][:-1].split(',')
            tmp_lines = lines[i][:-1]
        else:
            elts = lines[i][:].split(',')
            tmp_lines = lines[i][:]
        links = [0 for cpt in range(int(values[2]))]
        
        if tmp_lines.strip() != '' and tmp_lines != 'None':
            for e in elts:
                try:
                    links[int(e)-1] = 1
                except IndexError:
                    raise ValueError("Not enough facts in the file")
                if src:
                    try:
                        fs[int(e)-1][s] = 1
                        formulas_chosed[int(e)-1] = True
                    except IndexError:
                        raise ValueError("Not enough sources in the file")
        if src:
            sf.append(np.array(links))
            s += 1
        else:
            of.append(np.array(links))
            o += 1

    formulastmp = formulastmp.split(":")[1].strip().split("<")
    interpretations = list(range(2**int(values[3])))
    # formulas_chosed = [False for n in range(int(values[2]))]
    set_interpretation_sets = set([str(x) for x in interpretations])
    ind_f = 0
    
    for f in formulastmp:
        # print(f)
        lf = sorted(f.split(","))
        tmpvaluesx = list(formulas.values())
        to_add = True
        for ind_ici in range(len(tmpvaluesx)):
            if tmpvaluesx[ind_ici] == lf:
                # print(lf, "existe deja")
                # formulas_chosed[ind_ici] = True
                to_add = False
                # print("new chosed", formulas_chosed)
                break
        if to_add:
            # formulas_chosed.append(True)
            formulas[str(ind_f)] = lf
            # print("existe pas donc ajoute", lf, formulas_chosed)
            ind_f += 1
        negation = set_interpretation_sets.difference(lf)
        lf_neg = list(sorted(negation))
        tmpvaluesx = list(formulas.values())
        to_add = True
        for ind_ici in range(len(tmpvaluesx)):
            if tmpvaluesx[ind_ici] == lf_neg:
                # print(lf_neg, "neg existe deja")
                # formulas_chosed[ind_ici] = True
                to_add = False
                # print("new chosed", formulas_chosed)
                break
        if to_add:
            formulas[str(ind_f)] = lf_neg
            # formulas_chosed.append(False)
            # print("existe pas donc ajoute neg", lf_neg, formulas_chosed)
            ind_f += 1
    
    # print(formulas_chosed)
    # for i in range(len(formulas_chosed)):
    #     formulas_chosed[i] = True
    
    truth = truth.split(":")[1].strip()
    
    return fs,of,truth,nb_literals,formulas,formulas_chosed

def read_file_beliefm(name):
    """
    return two Adjacency matrix
    1st : for each fact, which source claimed it
    2nd : for each object, which fact is linked to him
    
    files : 
        line with a # are ignored
        - is a delimiter to pass to the objects
        a empty line will be consider as an empty object except 
        at the end of the file, we ignored them
    """
    sf = []
    of = []
    truth = []
    s = 0
    o = 0
    src = True
    
    f = open(name, "r")
    lines = f.readlines()
    
    n=0
    while lines[n][0] == "#":
        n += 1
    
    #nb_s nb_o nb_f nb_l
    values = lines[n].split()
    
    nb_literals = int(values[3])
    
    fs = [np.array([0 for j in range(int(values[0]))]) for i in range(int(values[2]))]

    #remove the empty lines at the end of the file
    j = 0
    for i in range(len(lines)-1, 2, -1):
        if not lines[i].strip():
            j += 1
        else:
            break
    if j > 0:
        lines = lines[:-j]
    
    for i in range(n+1, len(lines)):
        if lines[i][0] == '#':
            if "truth" in lines[i]:
                truth = lines[i]
            continue
        elif lines[i][0] == '-':
            src = False
            continue
        
        if "\n" in lines[i]:
            elts = lines[i][:-1].split(',')
            tmp_lines = lines[i][:-1]
        else:
            elts = lines[i][:].split(',')
            tmp_lines = lines[i][:]
        links = [0 for cpt in range(int(values[2]))]
        
        if tmp_lines.strip() != '' and tmp_lines != 'None':
            for e in elts:
                try:
                    links[int(e)-1] = 1
                except IndexError:
                    raise ValueError("Not enough facts in the file")
                if src:
                    try:
                        fs[int(e)-1][s] = 1
                    except IndexError:
                        raise ValueError("Not enough sources in the file")
        if src:
            sf.append(np.array(links))
            s += 1
        else:
            of.append(np.array(links))
            o += 1

    if type(truth) == str:
        truthtmp = truth.split(":")[1].strip()
        if truthtmp != '':
            truth = list(map(int, truthtmp.split("-")))
        else:
            truth = []
    
    return fs,of,truth,nb_literals

def read_file_formula(name):
    """
    return two Adjacency matrix
    1st : for each fact, which source claimed it
    2nd : for each object, which fact is linked to him
    
    files : 
        line with a # are ignored
        - is a delimiter to pass to the objects
        a empty line will be consider as an empty object except 
        at the end of the file, we ignored them
    """
    sf = []
    of = []
    truth = []
    formula_file = ""
    s = 0
    o = 0
    src = True
    
    f = open(name, "r")
    lines = f.readlines()
    
    n=0
    while lines[n][0] == "#":
        n += 1
    
    #nb_s nb_o nb_f
    values = lines[n].split()
    
    fs = [np.array([0 for j in range(int(values[0]))]) for i in range(int(values[2]))]

    #remove the empty lines at the end of the file
    j = 0
    for i in range(len(lines)-1, 2, -1):
        if not lines[i].strip():
            j += 1
        else:
            break
    if j > 0:
        lines = lines[:-j]
    
    for i in range(n+1, len(lines)):
        if lines[i][0] == '#':
            if "truth" in lines[i]:
                truth = lines[i]
            if "Formula:" in lines[i]:
                formula_file = lines[i].split(":")[1].split(".")[0]
            continue
        elif lines[i][0] == '-':
            src = False
            continue
        
        if "\n" in lines[i]:
            elts = lines[i][:-1].split(',')
            tmp_lines = lines[i][:-1]
        else:
            elts = lines[i][:].split(',')
            tmp_lines = lines[i][:]
        links = [0 for cpt in range(int(values[2]))]
        
        if tmp_lines.strip() != '' and tmp_lines != 'None':
            for e in elts:
                try:
                    links[int(e)-1] = 1
                except IndexError:
                    raise ValueError("Not enough facts in the file")
                if src:
                    try:
                        fs[int(e)-1][s] = 1
                    except IndexError:
                        raise ValueError("Not enough sources in the file")
        if src:
            sf.append(np.array(links))
            s += 1
        else:
            of.append(np.array(links))
            o += 1

    if type(truth) == str:
        truthtmp = truth.split(":")[1].strip()
        if truthtmp != '':
            truth = list(map(int, truthtmp.split("-")))
        else:
            truth = []
    
    return fs,of,truth,formula_file

def read_file(name):
    """
    return two Adjacency matrix
    1st : for each fact, which source claimed it
    2nd : for each object, which fact is linked to him
    
    files : 
        line with a # are ignored
        - is a delimiter to pass to the objects
        a empty line will be consider as an empty object except 
        at the end of the file, we ignored them
    """
    sf = []
    of = []
    truth = []
    s = 0
    o = 0
    src = True
    
    f = open(name, "r")
    lines = f.readlines()
    
    n=0
    while lines[n][0] == "#":
        n += 1
    
    #nb_s nb_o nb_f
    values = lines[n].split()
    
    fs = [np.array([0 for j in range(int(values[0]))]) for i in range(int(values[2]))]

    #remove the empty lines at the end of the file
    j = 0
    for i in range(len(lines)-1, 2, -1):
        if not lines[i].strip():
            j += 1
        else:
            break
    if j > 0:
        lines = lines[:-j]
    
    for i in range(n+1, len(lines)):
        if lines[i][0] == '#':
            if "truth" in lines[i]:
                truth = lines[i]
            continue
        elif lines[i][0] == '-':
            src = False
            continue
        
        if "\n" in lines[i]:
            elts = lines[i][:-1].split(',')
            tmp_lines = lines[i][:-1]
        else:
            elts = lines[i][:].split(',')
            tmp_lines = lines[i][:]
        links = [0 for cpt in range(int(values[2]))]
        
        if tmp_lines.strip() != '' and tmp_lines != 'None':
            for e in elts:
                try:
                    links[int(e)-1] = 1
                except IndexError:
                    raise ValueError("Not enough facts in the file")
                if src:
                    try:
                        fs[int(e)-1][s] = 1
                    except IndexError:
                        raise ValueError("Not enough sources in the file")
        if src:
            sf.append(np.array(links))
            s += 1
        else:
            of.append(np.array(links))
            o += 1

    if type(truth) == str:
        truthtmp = truth.split(":")[1].strip()
        if truthtmp != '':
            truth = list(map(int, truthtmp.split("-")))
        else:
            truth = []
    
    return fs,of,truth

def read_str_as_file(file):
    """
    return two Adjacency matrix
    1st : for each fact, which source claimed it
    2nd : for each object, which fact is linked to him
    
    files : 
        line with a # are ignored
        - is a delimiter to pass to the objects
        a empty line will be consider as an empty object except 
        at the end of the file, we ignored them
    """
    sf = []
    of = []
    truth = []
    s = 0
    o = 0
    src = True
    
    lines = file.split("\n")
    for i in range(len(lines)):
        lines[i] += "\n"
    
    n=0
    while lines[n][0] == "#":
        n += 1
    
    #nb_s nb_o nb_f
    values = lines[n].split()
    
    fs = [np.array([0 for j in range(int(values[0]))]) for i in range(int(values[2]))]

    #remove the empty lines at the end of the file
    j = 0
    for i in range(len(lines)-1, 2, -1):
        if not lines[i].strip():
            j += 1
        else:
            break
    if j > 0:
        lines = lines[:-j]
    
    for i in range(n+1, len(lines)):
        if lines[i][0] == '#':
            if "truth" in lines[i]:
                truth = lines[i]
            continue
        elif lines[i][0] == '-':
            src = False
            continue
        
        if "\n" in lines[i]:
            elts = lines[i][:-1].split(',')
            tmp_lines = lines[i][:-1]
        else:
            elts = lines[i][:].split(',')
            tmp_lines = lines[i][:]
        links = [0 for cpt in range(int(values[2]))]
        
        if tmp_lines.strip() != '' and tmp_lines != 'None':
            for e in elts:
                try:
                    links[int(e)-1] = 1
                except IndexError:
                    raise ValueError("Not enough facts in the file")
                if src:
                    try:
                        fs[int(e)-1][s] = 1
                    except IndexError:
                        raise ValueError("Not enough sources in the file")
        if src:
            sf.append(np.array(links))
            s += 1
        else:
            of.append(np.array(links))
            o += 1

    if type(truth) == str:
        truthtmp = truth.split(":")[1].strip()
        if truthtmp != '':
            idtruth = list(map(int, truthtmp.split("-")))
            tmptruth = [0 for n in fs]
            for i in range(len(idtruth)):
                tmptruth[idtruth[i]-1] = 1
        else:
            tmptruth = []
    else:
        tmptruth = []
 
    return fs,of,tmptruth

def read_file_app(name):
    """
    with ID for the app
    """
    id_src = []
    id_fct = []
    id_obj = []
    
    fs = []
    sf = []
    tmp_of = []
    of = []
    src = True
    
    f = open(name, "r")
    lines = f.readlines()
    
    n=0
    while lines[n][0] == "#":
        n += 1
        
    values = lines[n].split()
    fs = [np.array([0 for j in range(int(values[0]))]) for i in range(int(values[2]))]
    of = [np.array([0 for j in range(int(values[2]))]) for i in range(int(values[1]))]
    
    #remove the empty lines at the end of the file
    j = 0
    for i in range(len(lines)-1, 2, -1):
        if not lines[i].strip():
            j += 1
        else:
            break
    if j > 0:
        lines = lines[:-j]
        
    for i in range(n+1, len(lines)):
        if lines[i][0] == '#':
            continue
        elif lines[i][0] == '-':
            src = False
            continue
        
        ide = lines[i].split(":")
        if src:
            id_src.append(int(ide[0]))
            sf.append([])
            for e in ide[1].split(","):
                sf[-1].append(int(e))
        else:
            id_obj.append(int(ide[0]))
            tmp_of.append([])
            for e in ide[1].split(","):
                tmp_of[-1].append(int(e))
                id_fct.append(int(e))
    
    for i in range(len(sf)):
        for j in range(len(fs)):
            if id_fct[j] in sf[i]:
                fs[j][i] = 1
                
    for i in range(len(tmp_of)):
        for j in range(len(fs)):
            if id_fct[j] in tmp_of[i]:
                of[i][j] = 1
    
    return fs, of, id_src, id_fct, id_obj

def read_file_long(name):
    """
    return one Adjacency matrix
    1st : for each fact, which source claimed it
    2nd : the index of the fact link to the object
    
    files : 
        line with a # are ignored
        - is a delimiter to pass to the objects
        a empty line will be consider as an empty object except 
        at the end of the file, we ignored them
    """
    sf = []
    of = []
    s = 0
    o = 0
    src = True
    
    f = open(name, "r")
    lines = f.readlines()
    
    n=0
    while lines[n][0] == "#":
        n += 1
    
    #nb_s nb_o nb_f
    values = lines[n].split()
    
    fs = [np.array([0 for j in range(int(values[0]))]) for i in range(int(values[2]))]

    #remove the empty lines at the end of the file
    j = 0
    for i in range(len(lines)-1, 2, -1):
        if not lines[i].strip():
            j += 1
        else:
            break
    if j > 0:
        lines = lines[:-j]
    
    for i in range(n+1, len(lines)):
        if lines[i][0] == '#':
            continue
        elif lines[i][0] == '-':
            src = False
            continue
        
        if "\n" in lines[i]:
            elts = lines[i][:-1].split(',')
        else:
            elts = lines[i][:].split(',')
            
        if src:
            links = [0 for cpt in range(int(values[2]))]
        
            if lines[i][:-1].strip() != '' and lines[i][:-1] != 'None':
                for e in elts:
                    links[int(e)-1] = 1
                    if src:
                        fs[int(e)-1][s] = 1
        else:
            links = []
            if lines[i][:-1].strip() != '' and lines[i][:-1] != 'None':
                links = []
                for e in elts:
                    links.append(int(e)-1)
        if src:
            sf.append(np.array(links))
            s += 1
        else:
            of.append(np.array(links))
            o += 1
    
    return fs,of
    

if __name__ == "__main__":
    fs, of, truth, lit, formulas, formulas_chosed = read_file_bm("v4/examples/bms/testbm.txt")
    
    
    # fs, of, ids, idf, ido = read_file_app("../examples/graphes/graphe_3.txt")
    # fs, of = read_file("../examples/graphes/graphe_4.txt")
    # fs, of = read_file_long("../examples/graphes/graphe_3.txt")
    # print("\n")
    # print(fs, "\n")
    # print(of, "\n")
    # print(ids, "\n")
    # print(idf, "\n")
    # print(ido, "\n")
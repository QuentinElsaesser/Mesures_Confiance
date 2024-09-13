############################################
################ PARAMETERS ################
############################################

#Name of the normalizations
NORMA_A = 'A'
NORMA_O = 'C'
#ID norma in generation # not used ?
ID_NORMA_A = 'normaA'
ID_NORMA_O = 'normaO'

#PATH
PATH_PNG = "v4/png/"
PATH_XP = "v4/generation/xp/"
PATH_RESULTS = "v4/results/"
PRIOR_PATH  ="v4/priors_file/"
PROP_PATH  ="v4/prop_files/"

############ADD NEW METHOD############
### Add a new methods to test and generate Plot
####### in this file add the name in NAMES; ORDER; NAMES_NONORMA; ID_METHODS_SOURCES(if test on metrics src); 
####### PARA_PLOT: PLOT_ORDER; LEGEND_ORDER
####### in graph_method.py add the methods in the list to run the metrics on it

####################################
#### if we do not want to RUN a method, removes it from RUN_METHODS
#### if we do not want to PLOT the result of a method, removes it from PLOT_METHODS

RUN_METHODS = []
PLOT_METHODS = []
NAMES_NONORMA = []
NAMES = []
ORDER = []
PLOT_ORDER = []
LEGEND_ORDER = []
PARA_PLOT = []
ID_METHODS_SOURCES = []
NB_METHODS = len(RUN_METHODS)
NB_METHODS_SOURCES = len(ID_METHODS_SOURCES)

RUN_BS = "BS"
RUN_JA = "JA"
RUN_TD = "TD"

# Change nb src TD avec prc fixe
RUN_SRC = "SRC"
# Change nb obj TD avec prc fixe
RUN_OBJ = "OBJ"
# Change nb fct TD avec prc fixe
RUN_FCT = "FCT"
# Change variance TD
RUN_VRN = "VRN"
# Change pourcentage TD
RUN_PRC = "PRC"
# Change pourcentage TD pour test log
RUN_TDP = "TDP"

# Change pourcentage JA
RUN_PRP = "PRP"
# Change nb src JA avec prc fixe
RUN_SPR = "SPR"
# Change prc JA mais suit une distribution
RUN_SDR = "SDR"

# Syntactic Implique avec abstention BS
RUN_BIA = "BIA"
# Syntactic Implique sans abstention BS
RUN_BIF = "BIF"
# Syntactic Consistant aevc abstention BS
RUN_BCA = "BCA"
# Syntactic Consistant sans abstention BS
RUN_BCF = "BCF"
# BS chg nombre SRC
RUN_BSA = "BSA"
# BS chg nombre formules
RUN_BFA = "BFA"

# Truth Discovery
# FORMULA = RUN_TD
# TEST avec ou sans methode log
TD_TEST = False
# TD_TEST = True
# Judgment Aggregation
# FORMULA = RUN_JA
# Belief Merging Syntactic
FORMULA = RUN_BS

# FR = False
FR = True

LIST_RUN_NORMAL = [RUN_PRC, RUN_TDP, RUN_PRP, RUN_BIA, RUN_BIF, RUN_BCA, RUN_BCF]
LIST_RUN_SRC = [RUN_SRC, RUN_SPR, RUN_SDR, RUN_BSA, RUN_BFA]

def verif(run):
    if FORMULA == RUN_TD:
        if TD_TEST:
            return run in [RUN_TDP, RUN_PRC]
        return run in [RUN_SRC, RUN_OBJ, RUN_FCT, RUN_VRN, RUN_PRC]
    elif FORMULA == RUN_JA:
        return run in [RUN_PRP, RUN_SDR, RUN_SPR]
    elif FORMULA == RUN_BS:
        return run in [RUN_BIA, RUN_BIF, RUN_BCA, RUN_BCF, RUN_BSA, RUN_BFA]

if FORMULA == RUN_BS:
    # SFCA = average norma A
    # SFA = average norma C
    # SFC = leximin
    # SF = leximax
    # SFSUM = sum
    RUN_METHODS = ["SF", "Drastic", "Symmetric", "Intersect", "SFC", "Maxcons", "Maxcard", "SFA", "SFCA", "SFSUM"]
    PLOT_METHODS = ["SF", "Drastic", "Symmetric", "Intersect", "SFC", "Maxcons", "Maxcard", "SFA", "SFCA", "SFSUM"]
    NAMES_NONORMA = ["SF", "Drastic", "Symmetric", "Intersect", "SFC", "Maxcons", "Maxcard", "SFA", "SFCA", "SFSUM"]
    NAMES = ["SF", "Drastic", "Symmetric", "Intersect", "SFC", "Maxcons", "Maxcard", "SFA", "SFCA", "SFSUM"]
    ORDER = ["SF", "Drastic", "Symmetric", "Intersect", "SFC", "Maxcons", "Maxcard", "SFA", "SFCA", "SFSUM"]
    # "Maxcons", "Maxcard", , "SFSUM", "SFAC,
    # PLOT_ORDER = ["SF", "Drastic", "Symmetric", "Intersect", "SFC", "SFA", "SFCA", "SFSUM"]
    PLOT_ORDER = ["SF", "SFCA", "Drastic", "Symmetric", "Intersect"]
    LEGEND_ORDER = ["SF", "SFCA", "Drastic", "Symmetric", "Intersect", "SFC", "Maxcons", "Maxcard", "SFA", "SFSUM"]
    # same order as name
                        # ("--o", 'blue', r"$\triangle_{R}^{leximin}$"),
    PARA_PLOT = [("--o", 'blue', r"$Δ^{R_{leximax}}$"),
                 ("--x", 'black', r"$Δ^{D}$"),
                 ("-x", 'red', r"$Δ^{S,\sum}$"),
                 ("-o", 'forestgreen', r"$Δ^{\cap,\sum}$"),
                 ("-x", 'indianred', r"$SF^{leximin}$"),
                 ("--o", 'mediumslateblue', r"$maxcons$"),
                 ("-", 'orange', r"$maxcard$"),
                 ("--x", 'deepskyblue', r"$SF^{C}_{avg}$"),
                 (":x", 'cyan', r"$Δ^{R_{avg}}$"),
                 (":x", 'green', r"$SF^{A}_{\sum}$")]
    # PARA_PLOT = [("--o", 'blue', r"$SF^{leximax}$"),
    #              ("--x", 'black', r"$drastic$"),
    #              ("-x", 'red', r"$symmetric$"),
    #              ("-o", 'orange', r"$intersect$"),
    #              ("-x", 'indianred', r"$SF^{leximin}$"),
    #              ("--o", 'mediumslateblue', r"$maxcons$"),
    #              ("-", 'forestgreen', r"$maxcard$"),
    #              ("--x", 'deepskyblue', r"$SF^{C}_{avg}$"),
    #              (":x", 'fuchsia', r"$SF^{A}_{avg}$"),
    #              (":x", 'cyan', r"$SF^{A}_{\sum}$")]
    # Add another method and it will write the results for the sources metrics
    ID_METHODS_SOURCES = [ORDER.index(NAMES[0])]
    #Number of methods we test
    NB_METHODS = len(RUN_METHODS)
    #Number of methods that use the metrics for the sources
    NB_METHODS_SOURCES = len(ID_METHODS_SOURCES)
elif FORMULA == RUN_JA:
    RUN_METHODS = ["SFsum", "SFmax", "SFmin", "SFprod", 
                   "RMSA", "RMCSA", "RMWA", "RRA", "RDH",
                   "CSUM", "CMAX", "CMIN"]
    PLOT_METHODS = ["SFsum", "SFmax", "SFmin", "SFprod",
                    "RMSA", "RMCSA", "RMWA", "RRA", "RDH",
                    "CSUM", "CMAX"]
    NAMES_NONORMA = ["SFsum", "SFmax", "SFmin", "SFprod", 
                   "RMSA", "RMCSA", "RMWA", "RRA", "RDH",
                   "CSUM", "CMAX", "CMIN"]
    NAMES = ["SFsum", "SFmax", "SFmin", "SFprod", 
                   "RMSA", "RMCSA", "RMWA", "RRA", "RDH",
                   "CSUM", "CMAX", "CMIN"]
    ORDER = ["SFsum", "SFmax", "SFmin", "SFprod", 
                   "RMSA", "RMCSA", "RMWA", "RRA", "RDH",
                   "CSUM", "CMAX", "CMIN"]
    # PLOT_ORDER = ["RDH", "RMSA", "RMCSA", "RMWA", "RRA", "CMAX","CMIN", "CSUM",
                  # "SFsum", "SFmax", "SFmin", "SFprod"]
    PLOT_ORDER = ["SFsum",
                  "CMIN", "CMAX", "CSUM", 
                  "RRA", "RMWA", "RMCSA", "RMSA", "RDH"]
    # LEGEND_ORDER = ["SFsum", "SFmax", "SFmin", "SFprod", 
    #                "RMSA", "RMCSA", "RMWA", "RRA", "RDH",
    #                "CMIN", "CMAX", "CSUM"]
    LEGEND_ORDER = ["SFsum", "SFmax", "SFmin", "SFprod", 
                   "RMSA", "RMCSA", "RMWA", "RRA", "RDH",
                   "CMIN", "CMAX", "CSUM"]
    # same order as name
    #https://matplotlib.org/stable/gallery/color/named_colors.html
    #https://matplotlib.org/stable/api/markers_api.html
    #https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    PARA_PLOT = [("--o", 'blue', r"$R^{\times}$"), # r"$R^{\sum}$" C'EST SUM ICI
                 ("--o", 'black', r"$R^{leximax}$"),
                 ("--o", 'red', r"$R^{leximin}$"),
                 ("--o", 'orange', r"$R^{\times}$"),
                 (":o", 'forestgreen', r"$R_{MSA}$"),
                 ("-.o", 'lime', r"$R_{MCSA}$"),
                 ("-.o", 'fuchsia', r"$R_{MWA}$"),
                 (":o", 'cyan', r"$R_{RA}$"),
                 ("-o", 'deepskyblue', r"$R^{dH,max}$"),
                 (":o", 'mediumslateblue', r"$\delta^{sum}$"),
                 ("-o", 'indianred', r"$\delta^{leximax}$"),
                 ("-.o", 'goldenrod', r"$\delta^{leximin}$")]
    
    # Add another method and it will write the results for the sources metrics
    ID_METHODS_SOURCES = [ORDER.index(NAMES[i]) for i in range(len(NAMES))]
                          # ,ORDER.index(NAMES[12]),ORDER.index(NAMES[13]),ORDER.index(NAMES[14]),ORDER.index(NAMES[15])]
    #Number of methods we test
    # NB_METHODS = len(NAMES)
    NB_METHODS = len(RUN_METHODS)
    #Number of methods that use the metrics for the sources
    NB_METHODS_SOURCES = len(ID_METHODS_SOURCES)
elif FORMULA == RUN_TD:
    if TD_TEST:
        # Opti = Log
        # MAJ = Derive
        # Acti = Prio
        RUN_METHODS = ["Plurality", "Log", "Derive", "Prio", "BOA"]
        PLOT_METHODS = ["Plurality", "Log", "Derive", "Prio", "BOA"]
        NAMES_NONORMA = ["Plurality", "Log", "Derive", "Prio", "BOA"]
        NAMES = ["Plurality", "Log", "Derive", "Prio", "BOA"]
        ORDER = ["Plurality", "Log", "Derive", "Prio", "BOA"]
        # PLOT_ORDER = ["Plurality", "Log", "Derive", "Prio", "BOA"]
        PLOT_ORDER = ["Plurality", "Log"]
        LEGEND_ORDER = ["Plurality", "Log", "Derive", "Prio", "BOA"]
        # same order as name
        PARA_PLOT = [("--o", 'blue', r"$SF^{A}_{Pl}$"),
                     ("--o", 'black', r"$SFOP^{A}_{Pl}$"),
                     ("--o", 'red', r"$SFUC^{A}_{Pl}$"),
                     ("--o", 'darkgoldenrod', r"$SFAO^{A}_{Pl}$"),
                     ("--o", 'green', r"$SF^{A}_{Bo}$"),]
    else:
        RUN_METHODS = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_A}", f"Borda {NORMA_O}",
                 "Sums", "Usums", "H\&A", "TruthFinder", "Voting",
                 "AverageLog", "Investment", "PooledInvestment"]
        
        PLOT_METHODS = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_A}", f"Borda {NORMA_O}", 
                        "Sums", "Usums", "H\&A", "TruthFinder", "Voting",
                        "AverageLog", "Investment", "PooledInvestment"]
        
        #Names of the methods when graph is complete
        NAMES_NONORMA = ["Plurality", "Plurality", "Borda", "Borda", 
                         "Sums", "Usums", "H\&A", "TruthFinder", "Voting",
                         "AverageLog", "Investment", "PooledInvestment"]
                         # ,"Derive","Derive","Prio","Prio"]
        
        #Names of the methods
        NAMES = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_A}", f"Borda {NORMA_O}",
                 "Sums", "Usums", "H\&A", "TruthFinder", "Voting",
                 "AverageLog", "Investment", "PooledInvestment"]
                 # ,f"Derive {NORMA_A}", f"Derive {NORMA_O}", f"Prio {NORMA_A}", f"Prio {NORMA_O}"]
        
        #Order of the methods in the latex when we write the file
        ORDER = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_A}", f"Borda {NORMA_O}",
                 "Sums", "Usums", "H\&A", "TruthFinder", "Voting",
                 "AverageLog", "Investment", "PooledInvestment"]
                # ,f"Derive {NORMA_A}", f"Derive {NORMA_O}", f"Prio {NORMA_A}", f"Prio {NORMA_O}"]
        
        # #Order to plot the methods [0]=first ploted [-1]=last ploted
        # PLOT_ORDER = ["AverageLog", "Investment", "PooledInvestment",
        #               "TruthFinder", "H\&A", "Sums", "Usums", "Voting",
        #                 f"Borda {NORMA_A}", f"Borda {NORMA_O}",f"Plurality {NORMA_O}", f"Plurality {NORMA_A}"]
        #                 # ,f"Derive {NORMA_A}", f"Derive {NORMA_O}", f"Prio {NORMA_A}", f"Prio {NORMA_O}"]
        
        # PLOT_ORDER = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_O}",
        #                 "Sums", "Usums", "H\&A", "TruthFinder", 
        #                 f"Borda {NORMA_A}", "Voting",
        #                 "AverageLog", "Investment", "PooledInvestment"]
        
        # PLOT_ORDER = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_A}", f"Borda {NORMA_O}",
        #          "Sums", "Usums", "H\&A", "TruthFinder", "Voting",
        #          "AverageLog", "Investment", "PooledInvestment"]
        
        PLOT_ORDER = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_A}", f"Borda {NORMA_O}",]
        
        #Order for the legends in the plot [0]=highest [-1]=lowest
        # LEGEND_ORDER = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_O}",
        #                 "Sums", "Usums", "H\&A", "TruthFinder", 
        #                 f"Borda {NORMA_A}", "Voting",
        #                 "AverageLog", "Investment", "PooledInvestment"]
        LEGEND_ORDER = [f"Plurality {NORMA_A}", f"Plurality {NORMA_O}", f"Borda {NORMA_A}", f"Borda {NORMA_O}",
                 "Sums", "Usums", "H\&A", "TruthFinder", "Voting",
                 "AverageLog", "Investment", "PooledInvestment"]
        # f"Derive {NORMA_A}", f"Derive {NORMA_O}", f"Prio {NORMA_A}", f"Prio {NORMA_O}",
        
        #https://matplotlib.org/stable/gallery/color/named_colors.html
        #https://matplotlib.org/stable/api/markers_api.html
        #https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        PARA_PLOT = [("--d", 'blue', r"$SF^{A}_{Pl}$"), 
               ("-v", 'black', r"$SF^{C}_{Pl}$"),
               ("--s", 'red', r"$SF^{A}_{Bo}$"),
               ("-h", 'orange', r"$SF^{C}_{Bo}$"),
               ("-p", 'forestgreen', "Sums"),
               ("-p", 'lime', "Usums"),
               ("-p", 'fuchsia', "H&A"),
               ("-p", 'cyan', "TF"),
               (":*", 'deepskyblue', "Voting"),
               ("-p", 'darkviolet', "AL"),
               ("-p", 'mediumslateblue', "Inv"),
               ("-p", 'darkgoldenrod', "PInv")]
               # ,       
               # ("--*", 'darkviolet', f"drv{NORMA_A}"),
               # ("--*", 'mediumslateblue', f"drv{NORMA_O}"),
               # ("--*", 'darkgoldenrod', f"pio{NORMA_A}"),
               # ("--*", 'goldenrod', f"pio{NORMA_O}")]
           
    # Add another method and it will write the results for the sources metrics
    ID_METHODS_SOURCES = [ORDER.index(NAMES[i]) for i in range(len(NAMES))]
    # ID_METHODS_SOURCES = [ORDER.index(NAMES[0]),ORDER.index(NAMES[1]),ORDER.index(NAMES[2]),ORDER.index(NAMES[3]),
    #                       ORDER.index(NAMES[4]),ORDER.index(NAMES[5]),ORDER.index(NAMES[6]),ORDER.index(NAMES[7]),ORDER.index(NAMES[8]),
    #                       ORDER.index(NAMES[9]),ORDER.index(NAMES[10]),ORDER.index(NAMES[11])]
                          # ,ORDER.index(NAMES[12]),ORDER.index(NAMES[13]),ORDER.index(NAMES[14]),ORDER.index(NAMES[15])]
    #Number of methods we test
    # NB_METHODS = len(NAMES)
    NB_METHODS = len(RUN_METHODS)
    #Number of methods that use the metrics for the sources
    NB_METHODS_SOURCES = len(ID_METHODS_SOURCES)       
# return RUN_METHODS, PLOT_METHODS, NAMES_NONORMA, NAMES, ORDER, PLOT_ORDER, LEGEND_ORDER, PARA_PLOT

def is_tested(met):
    """
    met = ORDER
    """
    tmp = []
    for m in met:
        if m in RUN_METHODS:
            tmp.append(m)
    return tmp

def id_is_tested():
    """
    met = RUN_METHODS
    """
    tmp = []
    for m in NAMES:
        if m in RUN_METHODS:
            tmp.append(ORDER.index(m))
    return tmp

def plot_index_fct(list_met):
    """
    Return the list with the order of the legends for the plot
    """
    res = []
    for i in range(len(LEGEND_ORDER)):
        if LEGEND_ORDER[i] in list_met:
            res.append(list_met.index(LEGEND_ORDER[i]))
    return res

############ADD NEW METHOD############

############ADD NEW METRIC############
#In this file : METRICS_NAMES;PLOT_Y;PLOT_FILE;PLOT_YLIM; and in ID_METRICS_SRC or ID_METRICS_TD
#respect the order when you add a new metric
#In metrics.py : the function; in metrics
METRICS_NAMES = ["Swaps", "Normalize Swaps", 
                     "Euclidean distance", "Normalize euclidean distance",
                     "Difference", "Sources Reliability", 
                     "Ranking Order",
                     "Precision", "Accuracy", "Recall", "CSI", 
                     "Average iteration", "Max iteration",
                     "Number answers",
                     "Precision Mean", "Precision Unanimous",
                     "CSI Mean", "CSI Unanimous",
                     "CSI Min", "CSI Max",
                     "Precision Min", "Precision Max",
                     "CSI Majority", "Precision Majority",
                     "Majority Consistent ALGO", "Majority Consistent MAJO",
                     "Truth is majority", "Same outcome",
                     "Trust Un", "Trust Deux",
                     "Nb Answers",
                     "Hamming Hausdorff", "Avg Hamming Hausdorff",
                     "Percent Claim Truth", "Len Bases",
                     "Number Truth",
                     "Distance Max", "Distance Min", "Distance Avg",
                     "Truth In Maxcons", 
                     "Len Maxcons Avg", "Len Maxcons Min", "Len Maxcons Max",
                     "Unanime Distance", "Unanime Truth",
                     "Len Model", "Len Formulas", "V2Truth",
                     "V3AVGTRUTH"]

def PLOT_L(FR):
    if not FR:
        # Y Descrption of metrics in plot
        PLOT_Y = ["Number of swaps", "Percentage of swaps (divide by max)",
                        "Euclidean distance", "Euclidean distance (divide by max)", 
                        "Averaged difference", "Average reliability",
                        "Ranking",
                        "Precision (facts)", "Accuracy (facts)", "Recall (facts)", "CSI (facts)", 
                        "Average iterations", "Maximum iterations",
                        "Number of judgment proposed",
                        "Mean Precision on judgment", "Precision",# on unanimous judgment
                        "Mean CSI on judgment", "CSI on unanimous judgment",
                        "Min CSI on judgment", "Max CSI on judgment",
                        "Min Precision on judgment", "Max Precision on judgment",
                        "CSI on Majority", "Precision on Majority",
                        "Number of SF graphs that are majority-consistant", "Number of graphs with a consistent majority",
                        "Number of truth equal majority", "Same outcome methods 1,2,3",
                        "TP/nb_inpt * .5 + T*.5", "TP / TP + FP (only answers)",
                        "Number of answers",
                        "Distance Hausdorff (max Hamming)", "Distance Hausdorff (avg Hamming)",
                        "Percent Claim Truth", "Len Bases",
                        "strict_precision",
                        "Furthest distance to the truth(0=oppose truth)", "Closest distance to the truth", "Distance Avg",
                        "Truth in maxcons",
                        "Len Maxcons Avg", "Len Maxcons Min", "Len Maxcons Max",
                        "Unanime Distance", "Unanime Truth",
                        "Average number of formulae claimed", "Avg Len Formulas", "unanimous_precision",
                        "average_precision"]
        if FORMULA != RUN_TD:
            X_LABEL = "Average reliability of the agents (in percent)"
        else:
            X_LABEL = "Average reliability of the sources (in percent)"
    else:
        #PLOT FR
        PLOT_Y = ["Nombre de swaps", "Nombre de swaps (divisé par le max)",
                        "Distance euclidienne", "Distance euclidienne (divisé par le max)", 
                        "Différence moyenne", "Fiabilité moyenne",
                        "Classement",
                        "Precision (faits)", "Accuracy (faits)", "Recall (faits)", "CSI (faits)", 
                        "Itérations moyennes", "Itérations maximum",
                        "Nombre de jugements proposées",
                        "Precision moyenne", "Precision",# sur le choix unanime des agents
                        "CSI moyenne sur les jugements", "CSI sur l'unanimité des jugements",
                        "Minimum CSI", "Maximum CSI",
                        "Precision minimum", "Precision maximum ",
                        "CSI sur la Majorité", "Précision sur la Majorité",
                        "Nombre de graphes où SF est majority-consistant", "Nombre de graphes où la majorité est cohérente",
                        "Nombre de fois où la vérité est la majorité", "Même résultat methodes 1,2,3",
                        "TP/nb_inpt * .5 + T*.5", "TP / TP + FP (only answers)",
                        "Nombre de réponses",
                        "Distance Hausdorff (max Hamming)", "Distance Hausdorff (avg Hamming)",
                        "Pourcentage Verité affirmée", "Taille des Bases",
                        "precision_stricte",
                        "Distance max", "Distance min", "Distance moyenne",
                        "Vérité dans le maxcons", 
                        "Taille Maxcons Avg", "Taille Maxcons Min", "Taille Maxcons Max",
                        "Unanime Distance", "Unanime Truth",
                        "Nombre de formules affirmées en moyenne", "Taille moyenne formules", "precision_unanime",
                        "precision_moyenne"]
        
        if FORMULA != RUN_TD:
            X_LABEL = "Probabilité moyenne des agents (en pourcentage)"
        else:
            X_LABEL = "Probabilité moyenne des sources (en pourcentage)"
    return PLOT_Y, X_LABEL

PLOT_Y, X_LABEL = PLOT_L(FR)

def X_LABEL_SPE(label, nvalue, tmpsplit, FR):
    if nvalue == RUN_FCT:
        texte = tmpsplit[1:-1].split("-")
        if FR:
            return f"Nombre de faits (fiabilité moyenne entre {texte[0]} et {texte[1]})"
        else:
            return f"Number of facts (average reliability between {texte[0]} and {texte[1]})"
    elif nvalue == RUN_SRC:
        texte = tmpsplit[1:-1].split("-")
        if FR:
            return f"Nombre de sources (fiabilité moyenne entre {texte[0]} et {texte[1]})"
        else:    
            return f"Number of sources (average reliability between {texte[0]} and {texte[1]})"
    elif nvalue == RUN_SPR or nvalue == RUN_SDR or nvalue == RUN_BSA:
        if not FORMULA:
            if FR:
                return f"Nombre de sources {tmpsplit}"
            else:    
                return f"Number of sources {tmpsplit}"
        else:
            texte = tmpsplit[1:-1].split("-")
            if FR:
                return f"Nombre d'agents (fiabilité moyenne des profils entre {texte[0]} et {texte[1]})"
            else:    
                return f"Number of agents (average reliability of profiles between {texte[0]} and {texte[1]})"
    elif nvalue == RUN_OBJ:
        if FR:
            return f"Nombre d'objets {tmpsplit}"
        else:    
            return f"Number of objects {tmpsplit}"
    elif nvalue == RUN_BFA:
        if FR:
            return f"Nombre de formules {tmpsplit}"
        else:    
            return f"Number of formulae {tmpsplit}"
    elif nvalue == RUN_VRN:
        if FR:
            return f"Variance sur les affirmations des agents {tmpsplit}"
        else:    
            return f"Variance on agent's claims {tmpsplit}"
    else:
        return label

# name of the file 
PLOT_FILE = ["swp", "swn", 
                  "ecd", "edn", 
                  "dif", "ars",
                  "rnk",
                  "prc", "acc", "rec", "csi", 
                  "avi", "mxi",
                  "nba",
                  "pra", "pru",
                  "csa", "csu",
                  "csl", "csh",
                  "prl", "prh",
                  "csm", "prm",
                  "mca", "mcm",
                  "tem", "sam",
                  "btu", "btd",
                  "bna", 
                  "bhh", "bha",
                  "bpt", "blb",
                  "bn1",
                  "bdh", "bdl", "bda",
                  "btm",
                  "bla", "bll", "blh",
                  "bud", "but",
                  "bn0","btf", "bn2",
                  "bn3"]

# PLOT_YLIM = [[0], [0,100], 
#              [0], [0,100],
#              [0], [0],
#              [0],
#              [0,100], [0,100], [0,100], [0,100], 
#              [0], [0]]
#p = value must be min or max when you read the file
#100.1 to see the curve
PLOT_YLIM = [['m','m'], [0,'m'], 
             [0,'m'], [0,'m'],
             [0,'m'], [0,'m'],
             [0,'m'],
             ['m',100.1], ['m',100.1], ['m',100.1], ['m',100.1], 
             [0,'m'], [0,'m'],
             [0,'m'],
             ['m',100.1],['m',100.1],
             ['m',100.1],['m',100.1],
             ['m',100.1],['m',100.1],
             ['m',100.1],['m',100.1],
             ['m',100.1],['m',100.1],
             [0,'m'],[0,'m'],
             [0,'m'], [0,'m'],
             ['m','m'],['m','m'],
             ['m','m'], 
             ['m','m'], ['m','m'],
             ['m','m'], ['m','m'],
             ['m','m'],
             ['m','m'], ['m','m'], ['m','m'], 
             ['m','m'],
             ['m','m'], ['m','m'], ['m','m'],
             ['m','m'], ['m','m'],
             ['m','m'], ['m','m'], ['m','m'],
             ['m','m']]

ID_METRICS_SRC = {"S":METRICS_NAMES.index("Swaps"), "SN":METRICS_NAMES.index("Normalize Swaps"), 
                  "E":METRICS_NAMES.index("Euclidean distance"), "EN":METRICS_NAMES.index("Normalize euclidean distance"), 
                  "D":METRICS_NAMES.index("Difference"), "Mt":METRICS_NAMES.index("Sources Reliability"), 
                  "RO":METRICS_NAMES.index("Ranking Order")}

ID_METRICS_TD = {"P":METRICS_NAMES.index("Precision"), "A":METRICS_NAMES.index("Accuracy"),
                 "R":METRICS_NAMES.index("Recall"), "CSI":METRICS_NAMES.index("CSI")}

ID_METRICS_ALGO = {"Ia":METRICS_NAMES.index("Average iteration"), "Im":METRICS_NAMES.index("Max iteration")}

ID_METRICS_PRP = {"Na":METRICS_NAMES.index("Number answers"),
                  "Pra":METRICS_NAMES.index("Precision Mean"),"Pru":METRICS_NAMES.index("Precision Unanimous"),
                  "Csa":METRICS_NAMES.index("CSI Mean"),"Csu":METRICS_NAMES.index("CSI Unanimous"),
                  "Csl":METRICS_NAMES.index("CSI Min"),"Csh":METRICS_NAMES.index("CSI Max"),
                  "Prl":METRICS_NAMES.index("Precision Min"),"Prh":METRICS_NAMES.index("Precision Max"),
                  "Csm":METRICS_NAMES.index("CSI Majority"),"Prm":METRICS_NAMES.index("Precision Majority"),
                  "Mca":METRICS_NAMES.index("Majority Consistent ALGO"),"Mcm":METRICS_NAMES.index("Majority Consistent MAJO"),
                  "Tem":METRICS_NAMES.index("Truth is majority"), "Sam":METRICS_NAMES.index("Same outcome")}

ID_METRICS_BM = {"Btu":METRICS_NAMES.index("Trust Un"), "Btd":METRICS_NAMES.index("Trust Deux"),
                 "Bna":METRICS_NAMES.index("Nb Answers"), 
                 "Bhh":METRICS_NAMES.index("Hamming Hausdorff"), "Bha":METRICS_NAMES.index("Avg Hamming Hausdorff"),
                 "Bpt":METRICS_NAMES.index("Percent Claim Truth"), "Blb":METRICS_NAMES.index("Len Bases")}

ID_METRICS_BS = {"Bnt":METRICS_NAMES.index("Number Truth"), "Na":METRICS_NAMES.index("Number answers"), 
                 "Bdh":METRICS_NAMES.index("Distance Max"), "Bdl":METRICS_NAMES.index("Distance Min"), 
                 "Bda":METRICS_NAMES.index("Distance Avg"), "Btm":METRICS_NAMES.index("Truth In Maxcons"),
                 "Bla":METRICS_NAMES.index("Len Maxcons Avg"),"Bll":METRICS_NAMES.index("Len Maxcons Min"),
                 "Blh":METRICS_NAMES.index("Len Maxcons Max"),
                 "Bud":METRICS_NAMES.index("Unanime Distance"), "But":METRICS_NAMES.index("Unanime Truth"),
                 "Btc":METRICS_NAMES.index("Len Model"), "Btf":METRICS_NAMES.index("Len Formulas"), "Bn2":METRICS_NAMES.index("V2Truth"),
                 "Bn3":METRICS_NAMES.index("V3AVGTRUTH")}


ID_METRICS = {**ID_METRICS_SRC,**ID_METRICS_TD,**ID_METRICS_ALGO,**ID_METRICS_PRP,**ID_METRICS_BM,**ID_METRICS_BS}

if FORMULA == RUN_TD:
    ID_METRICS_ACTIVE = {**ID_METRICS_SRC,**ID_METRICS_TD,**ID_METRICS_ALGO}
elif FORMULA == RUN_JA:
    ID_METRICS_ACTIVE = {**ID_METRICS_SRC,**ID_METRICS_ALGO,**ID_METRICS_PRP}
elif FORMULA == RUN_BS:
    ID_METRICS_ACTIVE = {**ID_METRICS_SRC,**ID_METRICS_ALGO,**ID_METRICS_BS}

#Number of metrics for the sources
NB_METRICS_SOURCES = len(ID_METRICS_SRC)
############ADD NEW METRIC############

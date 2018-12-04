import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.results as res

pandas = pd.read_table("swissmetro.dat")
database = db.Database("swissmetro",pandas)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())

from headers import *

# Removing some observations can be done directly using pandas.
#remove = (((database.data.PURPOSE != 1) & (database.data.PURPOSE != 3)) | (database.data.CHOICE == 0))
#database.data.drop(database.data[remove].index,inplace=True)

# Here we use the "biogeme" way for backward compatibility
exclude = (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) +  ( CHOICE == 0 )) > 0
database.remove(exclude)


# Note that the default values are 0. Usually, simulation is performed on a model with the estimated values of the parameters. 

ASC_CAR = Beta('ASC_CAR',0,None,None,0)
ASC_TRAIN = Beta('ASC_TRAIN',0,None,None,0)
ASC_SM = Beta('ASC_SM',0,None,None,1)
B_TIME = Beta('B_TIME',0,None,None,0)
B_COST = Beta('B_COST',0,None,None,0)

MU_EXISTING = Beta('MU_EXISTING',1,1,None,0)
MU_PUBLIC = Beta('MU_PUBLIC',1,1,None,0)
ALPHA_EXISTING = Beta('ALPHA_EXISTING',0.5,0,1,0)
ALPHA_PUBLIC = 1 - ALPHA_EXISTING



SM_COST =  SM_CO   * (  GA   ==  0  ) 
TRAIN_COST =  TRAIN_CO   * (  GA   ==  0  )

TRAIN_TT_SCALED = TRAIN_TT / 100.0
TRAIN_COST_SCALED = DefineVariable('TRAIN_COST_SCALED',\
                                   TRAIN_COST / 100,database)
SM_TT_SCALED = SM_TT / 100.0
SM_COST_SCALED = DefineVariable('SM_COST_SCALED', SM_COST / 100,database)
CAR_TT_SCALED = CAR_TT / 100.0
CAR_CO_SCALED = DefineVariable('CAR_CO_SCALED', CAR_CO / 100,database)

V1 = ASC_TRAIN + \
     B_TIME * TRAIN_TT_SCALED + \
     B_COST * TRAIN_COST_SCALED
V2 = ASC_SM + \
     B_TIME * SM_TT_SCALED + \
     B_COST * SM_COST_SCALED
V3 = ASC_CAR + \
     B_TIME * CAR_TT_SCALED + \
     B_COST * CAR_CO_SCALED

# Associate utility functions with the numbering of alternatives
V = {1: V1,
     2: V2,
     3: V3}


# Associate the availability conditions with the alternatives
CAR_AV_SP =  DefineVariable('CAR_AV_SP',CAR_AV  * (  SP   !=  0  ),database)
TRAIN_AV_SP =  DefineVariable('TRAIN_AV_SP',TRAIN_AV  * (  SP   !=  0  ),database)

av = {1: TRAIN_AV_SP,
      2: SM_AV,
      3: CAR_AV_SP}

#Definition of nests:
alpha_existing = {1: ALPHA_EXISTING,
                  2:0.0,
                  3:1.0}

alpha_public = {1: ALPHA_PUBLIC,
                2: 1.0,
                3: 0.0}

nest_existing = MU_EXISTING, alpha_existing
nest_public = MU_PUBLIC, alpha_public
nests = nest_existing, nest_public
logprob = models.logcnl_avail(V,av,nests,CHOICE)
biogeme  = bio.BIOGEME(database,logprob)

# Instead of estimating the parameters, read the estimation
# results from the pickle file.
results = res.bioResults(pickleFile='11cnl.pickle')
print("Estimaton results: ",results)


# The choice model is a cross-nested logit, with availability conditions
prob1 = models.cnl_avail(V,av,nests,1)
prob2 = models.cnl_avail(V,av,nests,2)
prob3 = models.cnl_avail(V,av,nests,3)

genelas1 = Derive(prob1,'TRAIN_TT') * TRAIN_TT / prob1
genelas2 = Derive(prob2,'SM_TT') * SM_TT / prob2
genelas3 = Derive(prob3,'CAR_TT') * CAR_TT / prob3

simulate = {'Prob. train': prob1,
            'Prob. Swissmetro': prob2,
            'Prob. car':prob3,
            'Elas. 1':genelas1,
            'Elas. 2':genelas2,
            'Elas. 3':genelas3}

biosim  = bio.BIOGEME(database,simulate)
biosim.modelName = "11cnl_simul"
simresults = biosim.simulate(results.data.betaValues)
print(sum(simresults['Prob. train']))
print(sum(simresults['Elas. 1']))
#print("Results=",simresults.describe())



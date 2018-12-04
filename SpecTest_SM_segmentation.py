# Michel Bierlaire
# Thu Oct 25 13:49:48 2018

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio

pandas = pd.read_table("swissmetro.dat")
database = db.Database("swissmetro",pandas)
pd.options.display.float_format = '{:.3g}'.format

from headers import *

exclude = ((  PURPOSE   !=  1  ) * (  PURPOSE   !=  3  ) + (  CHOICE   ==  0  ) + (  AGE == 6  ))>0
database.remove(exclude)


#Parameters to be estimated
# Arguments:
#   1  Name for report. Typically, the same as the variable
#   2  Starting value
#   3  Lower bound
#   4  Upper bound
#   5  0: estimate the parameter, 1: keep it fixed
ASC_CAR	 = Beta('ASC_CAR',0,None,None,0)
ASC_SBB	 = Beta('ASC_SBB',0,None,None,1)
ASC_SM	 = Beta('ASC_SM',0,None,None,0)
B_CAR_COST	 = Beta('B_CAR_COST',0,None,None,0)
B_HE	 = Beta('B_HE',0,None,None,0)
B_SM_COST	 = Beta('B_SM_COST',0,None,None,0)
B_TIME	 = Beta('B_TIME',0,None,None,0)
B_TRAIN_COST	 = Beta('B_TRAIN_COST',0,None,None,0)
B_SENIOR	 = Beta('B_SENIOR',0,None,None,0)
B_GA	 = Beta('B_GA',0,None,None,0)

# Define here arithmetic expressions for name that are not directly 
# available from the data

SENIOR  = DefineVariable('SENIOR', AGE   ==  5 ,database)
CAR_AV_SP  = DefineVariable('CAR_AV_SP', CAR_AV    *  (  SP   !=  0  ),database)
SM_COST  = DefineVariable('SM_COST', SM_CO   * (  GA   ==  0  ),database)
TRAIN_AV_SP  = DefineVariable('TRAIN_AV_SP', TRAIN_AV    *  (  SP   !=  0  ),database)
TRAIN_COST  = DefineVariable('TRAIN_COST', TRAIN_CO   * (  GA   ==  0  ),database)

TRAIN_TT_SCALED = DefineVariable('TRAIN_TT_SCALED',\
                                 TRAIN_TT / 100.0,database)
TRAIN_COST_SCALED = DefineVariable('TRAIN_COST_SCALED',\
                                   TRAIN_COST / 100,database)
SM_TT_SCALED = DefineVariable('SM_TT_SCALED', SM_TT / 100.0,database)
SM_COST_SCALED = DefineVariable('SM_COST_SCALED', SM_COST / 100,database)
CAR_TT_SCALED = DefineVariable('CAR_TT_SCALED', CAR_TT / 100,database)
CAR_CO_SCALED = DefineVariable('CAR_CO_SCALED', CAR_CO / 100,database)
TRAIN_HE_SCALED = DefineVariable('TRAIN_HE_SCALED', TRAIN_HE / 100,database)
SM_HE_SCALED = DefineVariable('SM_HE_SCALED', SM_HE / 100,database)

#Utilities
Car_SP = ASC_CAR + B_TIME * CAR_TT_SCALED + B_CAR_COST * CAR_CO_SCALED + B_SENIOR * SENIOR
SBB_SP = ASC_SBB + B_TIME * TRAIN_TT_SCALED + B_TRAIN_COST * TRAIN_COST_SCALED + B_HE * TRAIN_HE_SCALED + B_GA * GA
SM_SP = ASC_SM + B_TIME * SM_TT_SCALED + B_SM_COST * SM_COST_SCALED + B_HE * SM_HE_SCALED + B_GA * GA + B_SENIOR * SENIOR

V = {3: Car_SP,1: SBB_SP,2: SM_SP}
av = {3: CAR_AV_SP,1: TRAIN_AV_SP,2: SM_AV}

# Duplicate the database
database_males = db.Database("airline_males",pd.DataFrame.copy(database.data))
database_females = db.Database("airline_females",pd.DataFrame.copy(database.data))
# Remove observations
database_males.remove(MALE   ==  0)
database_females.remove(MALE   ==  1)
print(f"Total number of observations: {database.getNumberOfObservations()}")
print(f"Females                     : {database_females.getNumberOfObservations()}")
print(f"Males                       : {database_males.getNumberOfObservations()}")

logprob = bioLogLogit(V,av,CHOICE)

biogeme_full  = bio.BIOGEME(database,logprob)
biogeme_full.modelName = "fullSample"
results_full = biogeme_full.estimate()
ll_full = results_full.data.logLike

biogeme_females  = bio.BIOGEME(database_females,logprob)
biogeme_females.modelName = "females"
results_females = biogeme_females.estimate()
ll_females = results_females.data.logLike

biogeme_males  = bio.BIOGEME(database_males,logprob)
biogeme_males.modelName = "males"
results_males = biogeme_males.estimate()
ll_males = results_males.data.logLike

print(f"LL full:    {ll_full:.3f}  Parameters: {results_full.data.nparam}")
print(f"LL females: {ll_females:.3f}  Parameters: {results_females.data.nparam}")
print(f"LL males:   {ll_males:.3f}  Parameters: {results_males.data.nparam}")
unrestricted = ll_females+ll_males
print(f"Sum LL :    {unrestricted:.3f}")
lr = -2 * (ll_full - unrestricted)
print(f"likelihood ratio: {lr:.3f}")

import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.distributions as dist
import pandas as pd
import unittest

from testheaders import *        


import biogeme.models as models


class testSwissmetro(unittest.TestCase):
    def setUp(self):
        longMessage = True
        self.formulas = {}
        self.models = {}
        pandas = pd.read_table("swissmetro.dat")
        self.database = db.Database("swissmetro",pandas)
        def theTriangularGenerator(size):
            return np.random.triangular(-1,0,1,size=size)

        myRandomNumberGenerators = {'TRIANGULAR':theTriangularGenerator}
        self.database.setRandomNumberGenerators(myRandomNumberGenerators)
        
        pandas = pd.read_table("swissmetro.dat")
        self.paneldatabase = db.Database("swissmetro",pandas)
        self.paneldatabase.panel("ID")

        pandas = pd.read_table("swissmetro.dat")
        self.binarydatabase = db.Database("swissmetro",pandas)
        
        # Exclude some observations
        exclude = (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) +  ( CHOICE == 0 )) > 0
        self.database.remove(exclude)
        self.paneldatabase.remove(exclude)

        CAR_AV_SP =  CAR_AV  * (  SP   !=  0  )
        TRAIN_AV_SP = TRAIN_AV  * (  SP   !=  0  )

        excludebinary = (TRAIN_AV_SP == 0) + (CAR_AV_SP == 0) + ( CHOICE == 2 ) + (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) + ( CHOICE == 0 )) > 0
        self.binarydatabase.remove(excludebinary)
        
        # Generic definitions
        ASC_CAR = Beta('ASC_CAR',1,None,None,0)
        ASC_TRAIN = Beta('ASC_TRAIN',1,None,None,0)
        ASC_SM = Beta('ASC_SM',1,None,None,1)
        B_TIME = Beta('B_TIME',1,None,None,0)
        B_COST = Beta('B_COST',1,None,None,0)

        SM_COST = SM_CO * ( GA == 0 ) 
        TRAIN_COST =  TRAIN_CO * ( GA == 0 )

        TRAIN_TT_SCALED = TRAIN_TT / 100.0
        TRAIN_COST_SCALED = TRAIN_COST / 100
        SM_TT_SCALED = SM_TT / 100.0
        SM_COST_SCALED = SM_COST / 100
        CAR_TT_SCALED = CAR_TT / 100
        CAR_CO_SCALED = CAR_CO / 100

        
        av = {1: TRAIN_AV_SP,
              2: SM_AV,
              3: CAR_AV_SP}


        modelNames = []
        V = {}
        loglike = {}
        # 01logit
        
        V["01logit"] = {1: ASC_TRAIN + 
                      B_TIME * TRAIN_TT_SCALED + 
                      B_COST * TRAIN_COST_SCALED,
                      2: ASC_SM + 
                      B_TIME * SM_TT_SCALED + 
                      B_COST * SM_COST_SCALED,
                      3: ASC_CAR + 
                      B_TIME * CAR_TT_SCALED + 
                      B_COST * CAR_CO_SCALED}

        loglike["01logit"] = bioLogLogit(V["01logit"],av,CHOICE)
        self.models["01logit"] = self.database,loglike["01logit"],-5331.252

                                
    def testEstimation(self):
        for k,f in self.models.items():
            logging.info("Estimate {}".format(k)) ;
            biogeme  = bio.BIOGEME(f[0],f[1],seed=10,numberOfDraws=5)
            biogeme.modelName = k
            biogeme.generateHtml = False
            results = biogeme.estimate()
            with self.subTest(msg="{}: check final log likelihhood".format(k)):
                self.assertAlmostEqual(results.data.logLike,f[2],2)

if __name__ == '__main__':
    unittest.main()

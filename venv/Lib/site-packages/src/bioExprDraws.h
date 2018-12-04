//-*-c++-*------------------------------------------------------------
//
// File name : bioExprDraws.h
// @date   Mon May  7 10:23:08 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#ifndef bioExprDraws_h
#define bioExprDraws_h

#include "bioExpression.h"
#include "bioString.h"

class bioExprDraws: public bioExpression {
 public:
  
  bioExprDraws(bioUInt drawId, bioString name) ;
  ~bioExprDraws() ;
  virtual bioDerivatives* getValueAndDerivatives(std::vector<bioUInt> literalIds,
						 bioBoolean gradient,
						 bioBoolean hessian) ;
  virtual bioString print() const ;
  virtual void setDrawIndex(bioUInt* d) ;
protected:
  bioUInt theDrawId ;
  bioString theName ;
  bioUInt* drawIndex ;
};


#endif

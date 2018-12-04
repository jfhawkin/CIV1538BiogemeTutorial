//-*-c++-*------------------------------------------------------------
//
// File name : bioExprRandomVariable.h
// @date   Wed May  9 17:15:40 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#ifndef bioExprRandomVariable_h
#define bioExprRandomVariable_h

#include "bioExpression.h"
#include "bioString.h"

class bioExprRandomVariable: public bioExpression {
 public:
  
  bioExprRandomVariable(bioUInt id, bioString name) ;
  ~bioExprRandomVariable() ;
  virtual bioDerivatives* getValueAndDerivatives(std::vector<bioUInt> literalIds,
						 bioBoolean gradient,
						 bioBoolean hessian) ;
  virtual bioString print() const ;
  virtual void setRandomVariableValuePtr(bioUInt id, bioReal* v) ;
protected:
  bioUInt rvId ;
  bioString theName ;
  bioReal* valuePtr ;
};


#endif

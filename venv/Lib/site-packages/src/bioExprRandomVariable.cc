//-*-c++-*------------------------------------------------------------
//
// File name : bioExprRandomVariable.cc
// @date   Wed May  9 17:17:32 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#include "bioExprRandomVariable.h"
#include <sstream>
#include "bioExceptions.h"
#include "bioDebug.h"

bioExprRandomVariable::bioExprRandomVariable(bioUInt id, bioString name) : bioExpression(), rvId(id), theName(name), valuePtr(NULL) {

}
bioExprRandomVariable::~bioExprRandomVariable() {
}


bioDerivatives* bioExprRandomVariable::getValueAndDerivatives(std::vector<bioUInt> literalIds,
						       bioBoolean gradient,
						       bioBoolean hessian) {

  if (!gradient && hessian) {
    throw bioExceptions(__FILE__,__LINE__,"If the hessian is needed, the gradient must be computed") ;
  }

  if (theDerivatives == NULL) {
    theDerivatives = new bioDerivatives(literalIds.size()) ;
  }
  else {
    if (gradient && theDerivatives->getSize() != literalIds.size()) {
      delete(theDerivatives) ;
      theDerivatives = new bioDerivatives(literalIds.size()) ;
    }
  }

  
  if (gradient) {
    if (hessian) {
      theDerivatives->setDerivativesToZero() ;
    }
    else {
      theDerivatives->setGradientToZero() ;
    }
  }

  if (valuePtr == NULL) {
      throw bioExceptNullPointer(__FILE__,__LINE__,"random variable value") ;
  }



  theDerivatives->f = *valuePtr ;
  return theDerivatives ;
}


bioString bioExprRandomVariable::print() const {
  std::stringstream str ;
  str << theName << "[" << rvId << "]" ;
  return str.str() ;
}

void bioExprRandomVariable::setRandomVariableValuePtr(bioUInt id, bioReal* v) {
  if (rvId == id) {
    valuePtr = v ;
  }
}

//-*-c++-*------------------------------------------------------------
//
// File name : bioExprGreater.cc
// @date   Thu Apr 19 07:27:30 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#include "bioExprGreater.h"
#include <sstream>
#include "bioDebug.h"
#include "bioExceptions.h"

bioExprGreater::bioExprGreater(bioExpression* l, bioExpression* r) :
  left(l), right(r) {

  listOfChildren.push_back(l) ;
  listOfChildren.push_back(r) ;
}

bioExprGreater::~bioExprGreater() {

}

bioDerivatives* bioExprGreater::getValueAndDerivatives(std::vector<bioUInt> literalIds,
						       bioBoolean gradient,
						   bioBoolean hessian) {

  if (theDerivatives == NULL) {
    theDerivatives = new bioDerivatives(literalIds.size()) ;
  }
  else {
    if (gradient && theDerivatives->getSize() != literalIds.size()) {
      delete(theDerivatives) ;
      theDerivatives = new bioDerivatives(literalIds.size()) ;
    }
  }

  if (gradient || hessian) {
    if (containsLiterals(literalIds)) {
      std::stringstream str ;
      str << "Expression Greater is not differentiable" << std::endl ; 
      throw bioExceptions(__FILE__,__LINE__,str.str())  ;
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

  
  if (left->getValue() > right->getValue()) {
    theDerivatives->f = 1.0 ;
  }
  else {
    theDerivatives->f = 0.0 ;
  }

  
  return theDerivatives ;
}

bioString bioExprGreater::print() const {
  std::stringstream str ;
  str << "(" << left->print() << ">" << right->print() << ")" ;
  return str.str() ;
}

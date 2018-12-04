//-*-c++-*------------------------------------------------------------
//
// File name : bioExprDraws.cc
// @date   Mon May  7 10:24:27 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#include "bioExprDraws.h"
#include <sstream>
#include "bioExceptions.h"
#include "bioDebug.h"

bioExprDraws::bioExprDraws(bioUInt drawId, bioString name) : bioExpression(), theDrawId(drawId), theName(name), drawIndex(NULL) {
  
}
bioExprDraws::~bioExprDraws() {
}


bioDerivatives* bioExprDraws::getValueAndDerivatives(std::vector<bioUInt> literalIds,
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

  if (draws == NULL) {
      throw bioExceptNullPointer(__FILE__,__LINE__,"draws") ;
  }


  if (sampleSize == 0) {
    throw bioExceptions(__FILE__,__LINE__,"Empty list of draws.") ;
  }
  if (numberOfDraws == 0) {
    throw bioExceptions(__FILE__,__LINE__,"Empty list of draws.") ;

  }
  if (numberOfDrawVariables == 0) {
    throw bioExceptions(__FILE__,__LINE__,"Empty list of draws.") ;
  }
  if (individualIndex == NULL) {
    throw bioExceptions(__FILE__,__LINE__,"Row index is not defined.") ;
  }
  if (*individualIndex >= sampleSize) {
    throw bioExceptOutOfRange<bioUInt>(__FILE__,__LINE__,*individualIndex,0,sampleSize-1) ;
  }
  if (drawIndex == NULL) {
    throw bioExceptions(__FILE__,__LINE__,"Draw index is not defined. It may be caused by the use of draws outside a Montecarlo statement.") ;
  }
  if (*drawIndex >= numberOfDraws) {
    throw bioExceptOutOfRange<bioUInt>(__FILE__,__LINE__,*drawIndex,0,numberOfDraws-1) ;
  }
  if (theDrawId == bioBadId || theDrawId >= numberOfDrawVariables) {
    throw bioExceptOutOfRange<bioUInt>(__FILE__,__LINE__,theDrawId,0,numberOfDrawVariables-1) ;
  }

  theDerivatives->f = (*draws)[*individualIndex][*drawIndex][theDrawId] ;
  return theDerivatives ;
}


bioString bioExprDraws::print() const {
  std::stringstream str ;
  str << theName << "[" << theDrawId << "]" ;
  return str.str() ;
}

void bioExprDraws::setDrawIndex(bioUInt* d) {
  drawIndex = d ;
}


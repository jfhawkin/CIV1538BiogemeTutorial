//-*-c++-*------------------------------------------------------------
//
// File name : bioExprLiteral.h
// @date   Thu Apr 12 11:31:11 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#ifndef bioExprLiteral_h
#define bioExprLiteral_h

#include "bioExpression.h"
#include "bioString.h"

class bioExprLiteral: public bioExpression {
 public:
  
  bioExprLiteral(bioUInt literalId, bioString name) ;
  ~bioExprLiteral() ;
  virtual bioDerivatives* getValueAndDerivatives(std::vector<bioUInt> literalIds,
						 bioBoolean gradient,
						 bioBoolean hessian) ;
  virtual bioString print() const ;
  // Returns true is the expression contains at least one literal in
  // the list. Used to simplify the calculation of the derivatives
  virtual bioBoolean containsLiterals(std::vector<bioUInt> literalIds) const ;
  virtual void setData(std::vector< std::vector<bioReal> >* d) ;
  virtual std::map<bioString,bioReal> getAllLiteralValues() ;

protected:
  enum literalType {
    bioParameter,
    bioFixedParameter,
    bioVariable,
    bioUnknown 
  };
  bioReal getLiteralValue()  ;
  bioUInt theLiteralId ;
  bioString theName ; 
  bioBoolean first ;
  bioUInt myId ;
  literalType theType ;
};


#endif

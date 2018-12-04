//-*-c++-*------------------------------------------------------------
//
// File name : bioConst.h
// @date   Fri Apr 13 08:44:55 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#ifndef bioConst_h
#define bioConst_h

#include "bioTypes.h"
#ifndef NULL
#define NULL 0L
#endif

#define PURE_VIRTUAL 0

const bioUInt bioBadId = static_cast<bioUInt>(-1) ;
const bioReal bioPi = 3.141592653589793238463 ;
const bioReal invSqrtTwoPi = 0.3989422804 ;

#endif

//-*-c++-*------------------------------------------------------------
//
// File name : bioString.cc
// @date   Tue Apr 10 17:10:47 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#include "bioString.h"
#include <vector>
#include <sstream>
#include "bioExceptions.h"
#include "bioTypes.h"
#include "bioDebug.h"


bioString extractParentheses(char openParen,
			     char closeParen,
			     bioString str) {

  std::size_t firstParen = str.find(openParen) ;
  if (firstParen == bioString::npos) {
    throw bioExceptions(__FILE__,__LINE__,"Open parenthesis not found") ;
  }

  if (openParen == closeParen) {
    std::size_t lastParen = str.rfind(openParen) ;
    return str.substr(firstParen+1,lastParen-firstParen-1) ;

  }
  bioUInt level = 0 ;
  for (std::size_t i = firstParen+1 ; i < str.length() ; ++i) {
    if (str[i] == openParen) {
      ++level ;
    }
    else if (str[i] == closeParen) {
      if (level == 0) {
	return str.substr(firstParen+1,i-1-firstParen) ;
      }
      else {
	--level ;
      }
    }
  }
  throw bioExceptions(__FILE__,__LINE__,"Close parenthesis not found") ;
}



std::vector<bioString> split(const bioString& s, char delimiter) {
   std::vector<bioString> tokens;
   bioString token;
   std::istringstream tokenStream(s);
   while (std::getline(tokenStream, token, delimiter))
   {
      tokens.push_back(token);
   }
   return tokens;
}

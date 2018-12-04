//-*-c++-*------------------------------------------------------------
//
// File name : bioString.h
// @date   Tue Apr 10 17:06:12 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#ifndef bioString_h
#define bioString_h

#include <string>
#include <vector>

typedef std::string bioString ;

// Extract the text between two parentheses, skipping some of them if required
// @param paren the character(s) that define 
// @param str the string to process
// Example: str = [ab[cd]][ef]
// extractParentheses('[',']',str) returns 'ab[cd]'
// extractParentheses('[',']',str,2) returns 'ef'
bioString extractParentheses(char openParen, char closeParen,  bioString str) ;

std::vector<bioString> split(const bioString& s, char delimiter) ;
 

#endif

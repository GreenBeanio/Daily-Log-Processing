from typing import List, Tuple

from src.parser import modes
from src.lexer import tokens

class ParserExpressionError(Exception):
    """Error for the parser"""
    pass

class ParserExpression:
    """Class for an expression for the parser to match"""
    def __init__(self, parser_expression: List[tokens.LexerTokenEnum], parser_mode: modes.ParserMode):
        self.parser_expression: List[tokens.LexerTokenEnum] = parser_expression
        self.parser_mode: modes.ParserMode = parser_mode

    def _checkInd(self, lexer_token: str, exp_pos: int) -> bool:
        """Method to check individual characters of the text and the token"""
        if lexer_token is self.parser_expression[exp_pos]:
            return True
        return False

    def checkExp(self, lexer_stack: List[tokens.Lexeme]) -> Tuple[modes.ParserMode, int]:
        """Method to check if the text matches a token"""        
        if len(lexer_stack) < len(self.parser_expression):
            raise ParserExpressionError("ParserExpression.checkExp() lexer_stack smaller than self.parser_expression")
        
        if len(lexer_stack) > 0 and len(lexer_stack) >= len(self.parser_expression):
            for exp_pos in range(len(self.parser_expression)):
                if not self._checkInd(lexer_stack[exp_pos].identifier, exp_pos):
                    raise ParserExpressionError("ParserExpression.checkExp() no match")
            return (self.parser_mode, len(self.parser_expression))
            #return self.parser_mode().build(self.parser_expression[0:len(self.parser_expression)])
        raise ParserExpressionError("ParserExpression.checkExp() no match")

class ParserExpressions:
    """Class to hold the expressions for the parser"""
    def __init__(self):
        self.exps: List[ParserExpression] = []
    
    def addExp(self, exp: ParserExpression):
        """Method to add expressions to the container"""
        if not isinstance(exp, ParserExpression):
            raise TypeError("ParserExpressions.addExp() token is not a ParserExpression")
        self.exps.append(exp)

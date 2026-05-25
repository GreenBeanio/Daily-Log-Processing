from enum import Enum
from typing import List

class LexerNoMatchError(Exception):
    """Error to handle a lexer token not matching"""
    pass

class LexerTokenEnum(Enum):
    """Enum of lexer token options"""
    ACTIVITY = 1
    COMMENT = 2
    TIME = 3
    SENTENCE = 4
    END_OF_INPUT = 5

class Lexeme:
    """Class to hold an extracted lexer element"""
    def __init__(self, identifier: LexerTokenEnum, text: str):
        self.identifier = identifier
        self.text = text
    
    def __repr__(self):
        return f"{self.identifier}\n{self.text}"

class LexerToken:
    """Class to define tokens"""
    def __init__(self, search_term: str, lexer_token: LexerTokenEnum):
        self.search_term = search_term
        self.lexer_token = lexer_token

    def _checkInd(self, lexer_char: str, check_pos: int) -> bool:
        """Method to check individual characters of the text and the token"""
        if lexer_char == self.search_term[check_pos]:
            return True
        return False

    def checkChar(self, lexer_str: str) -> Lexeme:
        """Method to check if the text matches a token"""        
        if len(lexer_str) < len(self.search_term):
            raise LexerNoMatchError("LexerLogic.checkChar() lexer_str smaller than self.search_term")
        
        if len(lexer_str) > 0 and len(lexer_str) >= len(self.search_term):
            for char_pos in range(len(self.search_term)):
                if not self._checkInd(lexer_str[char_pos], char_pos):
                    raise LexerNoMatchError("LexerLogic.checkChar() no match")
            return Lexeme(self.lexer_token, self.search_term)
        raise LexerNoMatchError("LexerLogic.checkChar() no match")
    
class LexerTokens:
    """Class to hold tokens for the lexer"""
    def __init__(self):
        self.tokens: List[LexerToken] = []
    
    def addToken(self, token: LexerToken):
        """Method to add tokens to the container"""
        if not isinstance(token, LexerToken):
            raise TypeError("LexerTokens.addToken() token is not a LexerToken")
        self.tokens.append(token)
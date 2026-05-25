from enum import Enum

class LexerTokenEnum(Enum):
    """Enum of lexer token options"""
    ACTIVITY = 1
    COMMENT = 2
    TIME = 3
    SENTENCE = 4
    END_OF_INPUT = 5

class LexerNoMatchError(Exception):
    """Error to handle a lexer token not matching"""
    pass

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
        self.tokens: list[LexerToken] = []
    
    def addToken(self, token: LexerToken):
        """Method to add tokens to the container"""
        if not isinstance(token, LexerToken):
            raise TypeError("LexerTokens.addToken() token is not a LexerToken")
        self.tokens.append(token)

class Lexer:
    """Class for the main lexer"""
    def __init__(self, lexer_tokens: LexerTokens):
        self.lexer_tokens: LexerTokens = lexer_tokens
        self.lexed: list[Lexeme] = []
        self.buffer: str = ""
        self.stack = ""

    def _itrChar(self):
        """Method to move 1 character from the stack to the buffer"""
        if len(self.stack) >= 1:
            self.buffer = "".join((self.buffer, self.stack[0]))
            self.stack = self.stack[1:]
        else:
            raise IndexError("Lexer._itrChar() there are no more characters in self.stack")
        
    def _addBuffer(self):
        """Method to add the buffer as a LexerTokenEnum.SENTENCE lexeme to self.lexed"""
        if len(self.buffer) == 0:
            raise IndexError("Lexer._addBuffer() self.buffer is out of characters")
        if len(self.buffer.strip()) > 0:
                self.lexed.append(Lexeme(LexerTokenEnum.SENTENCE, self.buffer.strip()))
                self.buffer = ""

    def _addLexeme(self, lexeme: Lexeme):
        """Method to add the matched Lexeme to to self.lexed"""
        if isinstance(lexeme, Lexeme):
            self.lexed.append(lexeme)
            self.stack = self.stack[len(lexeme.text):]
        raise TypeError("Lexer._addLexeme() lexeme is not a Lexeme")

    def _addMatch(self, lexeme: Lexeme):
        """Method to add lexemes to self.lexed after a token is matched"""
        self._addBuffer()
        self._addLexeme(lexeme)
        
    def _checkChar(self) -> Lexeme:
        """Method to check if the current stack position matches a token"""
        for token in self.lexer_tokens.tokens:
            try:
                return token.checkChar(self.stack)
            except:
                pass
        raise LexerNoMatchError("Lexer._checkChar() has no token match")
            
    def reset(self):
        """Method to reset the Lexer"""
        self.lexed = []
        self.buffer = ""
        self.stack = ""

    def searchLexer(self, src_txt: str):
        """Method to search the Lexer"""
        self.reset()
        self.stack = src_txt
        while True:
            try:
                self._addMatch(self._checkChar())
            except:
                if len(self.stack) != 0:
                    self._itrChar()
            if len(self.stack) == 0:
                if len(self.buffer) >= 1:
                    self._addBuffer()
                self.lexed.append(Lexeme(LexerTokenEnum.END_OF_INPUT, ""))
                break

    def removeLexeme(self, remove_len: int):
        """
        """
        if len(self.lexed) >= remove_len:
            self.lexed = self.lexed[remove_len:]
        else:
            raise ValueError("Lexer.removeLexeme() remove_len is larger than self.lexed")
from typing import List

from src.lexer import tokens

class Lexer:
    """Class for the main lexer"""
    def __init__(self, lexer_tokens: tokens.LexerTokens):
        self.lexer_tokens: tokens.LexerTokens = lexer_tokens
        self.lexed: List[tokens.Lexeme] = []
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
        """Method to add the buffer as a tokens.LexerTokenEnum.SENTENCE lexeme to self.lexed"""
        if len(self.buffer) != 0 and len(self.buffer.strip()) > 0:
                self.lexed.append(tokens.Lexeme(tokens.LexerTokenEnum.SENTENCE, self.buffer.strip()))
                self.buffer = ""

    def _addLexeme(self, lexeme: tokens.Lexeme):
        """Method to add the matched Lexeme to to self.lexed"""
        if isinstance(lexeme, tokens.Lexeme):
            self.lexed.append(lexeme)
            self.stack = self.stack[len(lexeme.text):]
        else:
            raise TypeError("Lexer._addLexeme() lexeme is not a tokens.Lexeme")

    def _addMatch(self, lexeme: tokens.Lexeme):
        """Method to add lexemes to self.lexed after a token is matched"""
        self._addBuffer()
        self._addLexeme(lexeme)
        
    def _checkChar(self) -> tokens.Lexeme:
        """Method to check if the current stack position matches a token"""
        for token in self.lexer_tokens.tokens:
            try:
                return token.checkChar(self.stack)
            except:
                pass
        raise tokens.LexerNoMatchError("Lexer._checkChar() has no token match")
            
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
                self.lexed.append(tokens.Lexeme(tokens.LexerTokenEnum.END_OF_INPUT, ""))
                break

    def removeLexeme(self, remove_len: int):
        """
        """
        if len(self.lexed) >= remove_len:
            self.lexed = self.lexed[remove_len:]
        else:
            raise ValueError("Lexer.removeLexeme() remove_len is larger than self.lexed")
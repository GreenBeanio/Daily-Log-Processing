import sys
from typing import List

from src.parser import expressions, nodes, modes
from src.lexer import lexer

class ParserNoMatchError(Exception):
    """Error for the parser"""
    pass

class Parser:
    """Class for the Parser"""
    def __init__(self, lexer: lexer.Lexer, parser_exps: expressions.ParserExpressions):
        self.lexer: lexer.Lexer = lexer
        self.parser_exps: expressions.ParserExpressions = parser_exps
        self.parsed: List[nodes.AST] = []

    def _checkMatch(self):
        """Method to check if the tokens match an expression"""
        for exp in self.parser_exps.exps:
            try:
                return exp.checkExp(self.lexer.lexed)
            except:
                pass
        raise ParserNoMatchError("Parser._checkMatch() has no expression match")

    def reset(self):
        """Method to reset the Parser"""
        self.lexer.reset()
        self.ast = []

    def searchParser(self, src_txt: str):
        """Method to search the Parser"""
        self.reset()
        self.lexer.searchLexer(src_txt)
        i = 0
        while i < 20: #True:
            try:
                matched = self._checkMatch()
                built_AST = matched[0].build(self.lexer.lexed[0:matched[1]])
                self.lexer.removeLexeme(matched[1])
                self.parsed.append(built_AST)
                if len(self.lexer.lexed) == 0:
                    break
            except modes.ParserEOIFlag:
                break
            except Exception as e:
                sys.exit((
                    f"{e}\n"
                    f"{self.lexer.lexed[0:matched[1]]}"
                ))
            i = i + 1
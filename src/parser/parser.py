from __future__ import annotations

from enum import Enum
from abc import ABC, abstractmethod
import re
import datetime
import sys

from src.lexer import lexer
class NodeError(Exception):
    """Error for the nodes"""
    pass

class Node(ABC):
    """Class for a basic node for the AST"""
    def __init__(self):
        self.children: list[Node] = []
    
    def addChild(self, child: Node):
        """Method to add a child to the node"""
        if not isinstance(child, Node):
            raise NodeError("Node.addChild() child is not a Node")
        self.children.append(child)

    def removeChild(self, pos: int = 0):
        if not len(self.children) >= pos + 1:
            raise IndexError("Node.removeChild() pos is larger than self.children")
        del self.children[pos]

    @abstractmethod
    def build(self):
        """Method to build the Node output"""
        pass

class TimeNode(Node):
    """Class for storing the Time data"""
    def __init__(self, contents: datetime.datetime):
        super().__init__()
        self.contents: datetime.datetime = contents
    
    def build(self):
        """Method to build the Time Node output"""
        pass

class ActivityNode(Node):
    """Class for storing the Activity data"""
    def __init__(self, contents: str):
        super().__init__()
        self.contents: str = contents
    
    def build(self):
        """Method to build the Activity Node output"""
        pass

class CommentNode(Node):
    """Class for storing the Comment data"""
    def __init__(self, contents: str):
        super().__init__()
        self.contents: str = contents
    
    def build(self):
        """Method to build the Comment Node output"""
        pass

class AST:
    """Class for something resembling an AST, but not really"""
    def __init__(self, root: Node):
        self.root: Node = root

class ParserNoMatchError(Exception):
    """Error for the parser"""
    pass

class ParserModeError(Exception):
    """Error for the Parser Modes"""
    pass

class ParserMode(ABC):
    """Class for the Parser modes"""
    def __init__(self):
        pass

    @abstractmethod
    def build(self, lexer_stack: list[lexer.Lexeme]) -> AST:
        """A method to build the node from a Parser mode"""
        pass

class ParserTimeMode(ParserMode):
    """Class for the Parser time mode"""
    def __init__(self):
        super().__init__()

    def _validateTime(self, source_str: str) -> datetime.datetime:
        """Get the times from a input_text string"""
        time_pattern = r"^[0-9]{1,2}:[0-9]{1,2}$"
        matches = re.match(time_pattern, source_str)
        if matches is None:
            raise ValueError("ParserTimeMode._validateTime() source_str is not a valid time")
        #return time.strptime(matches.group(), "%H:%M")
        return datetime.datetime.strptime(matches.group(), "%H:%M")

    def _validateDateTime(self, source_str: str) -> datetime.datetime:
        """Get the times from a input_text string"""
        time_pattern = r"^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{1,2}:[0-9]{1,2}$"
        matches = re.match(time_pattern, source_str)
        if matches is None:
            try:
                return self._validateTime(source_str)
            except:
                raise ValueError("ParserTimeMode._validateDateTime() source_str is not a valid time")
        return datetime.datetime.strptime(matches.group(), "%Y-%m-%d %H:%M")
    
    def build(self, lexer_stack: list[lexer.Lexeme]) -> AST:
        """Method to build the Node output"""
        try:
            processed_time = self._validateDateTime(lexer_stack[0].text)
            return AST(TimeNode(processed_time))
        except:
            raise ParserModeError("ParserTimeMode.build() time is not valid")

class ParserSentenceMode(ParserMode):
    """Class for the Parser sentence mode"""
    def __init__(self):
        super().__init__()
    
    def build(self, lexer_stack: list[lexer.Lexeme]) -> AST:
        """Method to build the Node output"""
        if lexer_stack[0].identifier is lexer.LexerTokenEnum.SENTENCE:
            return AST(ActivityNode(lexer_stack[0].text))
        if lexer_stack[0].identifier is lexer.LexerTokenEnum.COMMENT:
            return AST(CommentNode(lexer_stack[1].text))
        
class ParserActivityCommentMode(ParserMode):
    """Class for the Parser activity comment mode"""
    def __init__(self):
        super().__init__()
    
    def build(self, lexer_stack: list[lexer.Lexeme]) -> AST:
        """Method to build the Node output"""
        activity = ActivityNode(lexer_stack[0].text)
        activity.addChild(CommentNode(lexer_stack[2].text))
        return(AST(activity))
    
class ParserEOIFlag(Exception):
    """Error to track the parser reaching the end of input token"""
    pass

class ParserEOIMode(ParserMode):
    """Class for the Parser End of Input mode"""
    def __init__(self):
        super().__init__()
    
    def build(self, lexer_stack: list[lexer.Lexeme]) -> AST:
        """Method to build the Node output"""
        raise(ParserEOIFlag("End of Input reached"))
        
class ParserExpression:
    """Class for an expression for the parser to match"""
    def __init__(self, parser_expression: list[lexer.LexerTokenEnum], parser_mode: ParserMode):
        self.parser_expression: list[lexer.LexerTokenEnum] = parser_expression
        self.parser_mode: ParserMode = parser_mode

    def _checkInd(self, lexer_token: str, exp_pos: int) -> bool:
        """Method to check individual characters of the text and the token"""
        if lexer_token is self.parser_expression[exp_pos]:
            return True
        return False

    def checkExp(self, lexer_stack: list[lexer.Lexeme]) -> tuple[ParserMode, int]:
        """Method to check if the text matches a token"""        
        if len(lexer_stack) < len(self.parser_expression):
            raise ParserNoMatchError("ParserExpression.checkExp() lexer_stack smaller than self.parser_expression")
        
        if len(lexer_stack) > 0 and len(lexer_stack) >= len(self.parser_expression):
            for exp_pos in range(len(self.parser_expression)):
                if not self._checkInd(lexer_stack[exp_pos].identifier, exp_pos):
                    raise ParserNoMatchError("ParserExpression.checkExp() no match")
            return (self.parser_mode, len(self.parser_expression))
            #return self.parser_mode().build(self.parser_expression[0:len(self.parser_expression)])
        raise ParserNoMatchError("ParserExpression.checkExp() no match")

class ParserExpressions:
    """Class to hold the expressions for the parser"""
    def __init__(self):
        self.exps: list[ParserExpression] = []
    
    def addExp(self, exp: ParserExpression):
        """Method to add expressions to the container"""
        if not isinstance(exp, ParserExpression):
            raise TypeError("ParserExpressions.addExp() token is not a ParserExpression")
        self.exps.append(exp)

class Parser:
    """Class for the Parser"""
    def __init__(self, lexer: lexer.Lexer, parser_exps: ParserExpressions):
        self.lexer: lexer.Lexer = lexer
        self.parser_exps: ParserExpressions = parser_exps
        self.parsed: list[AST] = []

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
            except ParserEOIFlag:
                break
            except Exception as e:
                sys.exit((
                    f"{e}\n"
                    f"{self.lexer.lexed[0:matched[1]]}"
                ))
            i = i + 1
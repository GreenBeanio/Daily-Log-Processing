from abc import ABC, abstractmethod
import datetime
import re
from typing import List

from src.parser import nodes
from src.lexer import tokens

class ParserModeError(Exception):
    """Error for the Parser Modes"""
    pass

class ParserEOIFlag(Exception):
    """Error to track the parser reaching the end of input token"""
    pass

class ParserMode(ABC):
    """Class for the Parser modes"""
    def __init__(self):
        pass

    @abstractmethod
    def build(self, lexer_stack: List[tokens.Lexeme]) -> nodes.AST:
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
    
    def build(self, lexer_stack: List[tokens.Lexeme]) -> nodes.AST:
        """Method to build the Node output"""
        try:
            processed_time = self._validateDateTime(lexer_stack[0].text)
            return nodes.AST(nodes.TimeNode(processed_time))
        except:
            raise ParserModeError("ParserTimeMode.build() time is not valid")

class ParserSentenceMode(ParserMode):
    """Class for the Parser sentence mode"""
    def __init__(self):
        super().__init__()
    
    def build(self, lexer_stack: List[tokens.Lexeme]) -> nodes.AST:
        """Method to build the Node output"""
        if lexer_stack[0].identifier is tokens.LexerTokenEnum.SENTENCE:
            return nodes.AST(nodes.ActivityNode(lexer_stack[0].text))
        if lexer_stack[0].identifier is tokens.LexerTokenEnum.COMMENT:
            return nodes.AST(nodes.CommentNode(lexer_stack[1].text))
        
class ParserActivityCommentMode(ParserMode):
    """Class for the Parser activity comment mode"""
    def __init__(self):
        super().__init__()
    
    def build(self, lexer_stack: List[tokens.Lexeme]) -> nodes.AST:
        """Method to build the Node output"""
        activity = nodes.ActivityNode(lexer_stack[0].text)
        activity.addChild(nodes.CommentNode(lexer_stack[2].text))
        return(nodes.AST(activity))

class ParserEOIMode(ParserMode):
    """Class for the Parser End of Input mode"""
    def __init__(self):
        super().__init__()
    
    def build(self, lexer_stack: List[tokens.Lexeme]) -> nodes.AST:
        """Method to build the Node output"""
        raise(ParserEOIFlag("End of Input reached"))
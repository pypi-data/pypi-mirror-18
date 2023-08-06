"""
This library contains a set of utilities for building probabilistic
context-free grammars (:class:`kasami.TreeScorer`) from parsed sentence
trees and then using those PCFGs to score new sentence trees.
"""
from .tree_scorer import TreeScorer
from .productions import Production, SymbolProduction, TerminalProduction
from .nodes import Node, SymbolNode, TerminalNode
from .about import (__name__, __version__, __author__, __author_email__,
                    __description__, __license__, __url__)

__all__ = [TreeScorer,
           Production, SymbolProduction, TerminalProduction,
           Node, SymbolNode, TerminalNode,
           __name__, __version__, __author__, __author_email__,
           __description__, __license__, __url__]

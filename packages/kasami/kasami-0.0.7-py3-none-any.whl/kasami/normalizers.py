from .nodes import SymbolNode, TerminalNode


def bllip(bllip_tree):
    if len(bllip_tree.subtrees()) == 0:
        return TerminalNode(bllip_tree.label, str(bllip_tree.token))
    else:

        produces = tuple(bllip(sub_tree)
                         for sub_tree in bllip_tree.subtrees())
        return SymbolNode(bllip_tree.label, produces)


def spacy(spacy_doc):
    roots = [t for t in spacy_doc if t.head is t]

    if len(roots) == 0:
        return TerminalNode("EMPTY", "EMPTY")
    elif len(roots) == 1:
        return _spacy_treeify_at(roots[0], spacy_doc)
    else:
        return SymbolNode("SENTENCES", tuple(_spacy_treeify_at(root, spacy_doc)
                                             for root in roots))


def _spacy_treeify_at(token, spacy_doc):
    if token.left_edge == token.right_edge:
        return TerminalNode(spacy_doc.vocab.strings[token.tag], str(token))
    else:
        root = TerminalNode(spacy_doc.vocab.strings[token.tag], str(token))
        sorted_i_trees = sorted([(child.i, _spacy_treeify_at(child, spacy_doc))
                                 for child in token.children] +
                                [(token.i, root)])

        return SymbolNode(spacy_doc.vocab.strings[token.dep],
                          tuple(tree for _, tree in sorted_i_trees))

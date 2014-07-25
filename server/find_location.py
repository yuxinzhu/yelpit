from bs4 import BeautifulSoup
import cities
import nltk

PAGE_RANK = []

def find_location(html):
    html = BeautifulSoup(html)

def _find_named_entities(query):
    try:
        named_entities, definitive_results = [], []
        tokens = nltk.word_tokenize(query)
        pos_tags = nltk.pos_tag(tokens)
        chunks = nltk.ne_chunk(pos_tags, binary=True)
        for subtree in chunks.subtrees(filter=lambda t: t.node == "NE"):
            named_entities.append(" ".join([word for word, pos in subtree.leaves()]))
        for ne in named_entities:
            if ne.title() in world_cities:
                definitive_results.append(ne)
        return ne
    except Exception as e:

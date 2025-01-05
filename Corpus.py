# correction des profs

import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import csr_matrix


from Classes import Author, RedditDocument, ArxivDocument


class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.vocab = {}

    #ajout de doc au corpus
    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    #affiche les docs du corpus triés
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values()) #récupère tous les docs
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri chronologique
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
    
    def organisation(self, saved_corpus):
        # Organisation des documents dans le corpus
        for doc in saved_corpus.id2doc.values():  # Parcours les documents
            # Vérification que le document possède un texte valide
            if not hasattr(doc, "texte") or not isinstance(doc.texte, str) or not doc.texte.strip():
                continue  # Ignore les docs sans texte valide

            # Classe les docs selon l'origine(reddit, arxiv)
            if "reddit" in doc.url.lower():  # Identifie comme Reddit
                # reddit_doc = RedditDocument(len(doc.texte.split()))  # Init avec un count exemple
                reddit_doc = RedditDocument(comments=0)
                reddit_doc.titre = doc.titre
                reddit_doc.auteur = doc.auteur
                reddit_doc.date = doc.date
                reddit_doc.url = doc.url
                reddit_doc.texte = doc.texte
                self.add(reddit_doc)
                
            elif "arxiv" in doc.url.lower():  # Identifie comme ArXiv
                arxiv_doc = ArxivDocument(doc.auteur)
                arxiv_doc.titre = doc.titre
                arxiv_doc.auteur = doc.auteur
                arxiv_doc.date = doc.date
                arxiv_doc.url = doc.url
                arxiv_doc.texte = doc.texte
                self.add(arxiv_doc)
        
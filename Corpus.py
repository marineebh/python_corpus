# correction des profs

import re
import panda as pd



from Classes import Author

# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
    
# ----------------- question 1.1 TD6 --------------------
# texte = compilation des textes
    def search(self, texte, keyword):
        res = []
        matches = re.finditer('\b{}\b'.format(re.escape(keyword)), texte, flags=re.IGNORECASE)
        passages = [match.group(0) for match in matches]
        if passages:
            res.append({'passages': passages})
        return res
        
    def concorde(self, texte, keyword, concorde=15):
        res = []
        matches = re.finditer('\b{}\b'.format(re.escape(keyword)), texte, flags=re.IGNORECASE)
        for m in matches :
            start = min(0, m.start()-concorde)
            end = max(len(m), m.end()+concorde)
            contexte = texte[start:end]
            res.append({
                'contexte_avant': contexte[:concorde],
                'motif' : m.match(0),
                'contexte_après' : contexte[concorde:]
            })
            df = pd.DataFrame(res)
            return df

    def nettoyer_texte(texte):
        texte = texte.lower().sub('[^\w\s\n]', '', texte)

    def creation_vocabulaire(self):
        vocabulaire = set()
        for doc in self.id2doc.values() :
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = [mot for mot in re.split('\s+|[.,;:\'"!,()/]', texte_nettoye) if mot]
            vocabulaire.update(mots)
        return vocabulaire

from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import display
import ipywidgets as widgets
import pandas as pd
import re

class SearchEngine:
    def __init__(self, corpus):
        try:
            self.corpus = corpus
            self.vocab, self.mat_TF, self.mat_TFxIDF, self.freq = self.creer_vocabulaire()
        except Exception as e:
            print(f"Erreur dans SearchEngine.__init__: {e}")
            import traceback
            traceback.print_exc()

    def nettoyer_texte(self, text):
        """Nettoyage du texte : minuscule et suppression de la ponctuation."""
        text = text.texte.lower() 
        if not isinstance(text, str):
            text = str(text)
        # text = re.sub(r'[^\w\s]', '', text)  # Supprime la ponctuation
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text



    def search(self, keywords, top_k=5):
        """Recherche les documents correspondants et retourne des résultats formatés."""
        vecteur_requete = [0] * len(self.vocab)
        for mot in keywords:
            if mot in self.vocab:
                vecteur_requete[self.vocab[mot]] = 1

        vecteur_requete = csr_matrix(vecteur_requete).toarray()
        scores = cosine_similarity(vecteur_requete, self.mat_TFxIDF.toarray()).flatten()

        meilleurs_scores = sorted(
            [(doc_id, score) for doc_id, score in enumerate(scores)],
            key=lambda x: x[1], reverse=True
        )[:top_k]

        resultats = []
        for doc_id, score in meilleurs_scores:
            # Utilise l'attribut `id2doc` pour accéder aux documents
            doc = list(self.corpus.id2doc.values())[doc_id]  # Utilise id2doc pour récupérer le document
            extrait = self.concorde(doc, keywords[0])[:1]  # Extrait le contexte autour du premier mot-clé
            resultats.append({
                'Source': 'Reddit' if 'reddit' in doc.url else 'Arxiv',
                'Titre': doc.titre,
                'Auteur': doc.auteur,
                'Date': doc.date,
                'Extrait': extrait,
                'Pertinence': score
            })
        return resultats


    def concorde(self, doc, keyword, concorde=15):
        """Recherche un mot-clé et extrait le contexte avant et après."""
        texte = doc.texte  # Texte du document
        res = []
        matches = re.finditer(r'\b{}\b'.format(re.escape(keyword)), texte, flags=re.IGNORECASE)
        for m in matches:
            start = max(0, m.start() - concorde)
            end = min(len(texte), m.end() + concorde)
            contexte_avant = texte[start:m.start()]
            contexte_apres = texte[m.end():end]
            res.append({
                'contexte_avant': contexte_avant.strip(),
                'motif': m.group(0),
                'contexte_apres': contexte_apres.strip()
            })
        return res  # Retourne une liste de résultats

    def creer_vocabulaire(self):
        """Crée le vocabulaire, les matrices TF et TF-IDF et calcule les fréquences."""
        vocabulaire = set()
        occurrences = {}
        mot_par_doc = {}
        row, col, data = [], [], []

        # Assure-toi que `corpus.id2doc.values()` renvoie une liste de documents
        for doc_id, doc in enumerate(self.corpus.id2doc.values()):
            texte_nettoye = self.nettoyer_texte(doc)
            mots = [mot for mot in re.split(r'\s+|[.,;\'"!?()]', texte_nettoye) if mot]  # Nettoyage des mots

            for mot in mots:
                if mot not in occurrences:
                    occurrences[mot] = 0
                occurrences[mot] += 1
                if mot not in mot_par_doc:
                    mot_par_doc[mot] = set()
                mot_par_doc[mot].add(doc_id)

                vocabulaire.add(mot)
                row.append(doc_id)
                col.append(mot)  # Ajouter le mot brut ici
                data.append(1)

        # Création du dictionnaire vocabulaire avec index
        vocab = {mot: i for i, mot in enumerate(sorted(vocabulaire))}

        # Filtrer les mots dans col pour s'assurer qu'ils sont bien dans vocab
        col_indices = [vocab[mot] for mot in col if mot in vocab]

        # Construire la matrice creuse
        mat_TF = csr_matrix((data, (row, col_indices)), shape=(len(self.corpus.id2doc), len(vocab)))

        tfidf_transformer = TfidfTransformer()
        mat_TFxIDF = tfidf_transformer.fit_transform(mat_TF)

        freq = pd.DataFrame([
            {'Mot': mot, 'Occurrences': occurrences[mot], 'Nombre de documents': len(mot_par_doc[mot])}
            for mot in vocab
        ])

        return vocab, mat_TF, mat_TFxIDF, freq





        
    # Modification de la fonction de recherche
    def on_search_clicked(self, b, output, keyword, top_k):
        with output:  
            output.clear_output()
        
            if not keyword:
                print("Veuillez entrer un mot-clé.")
                return
            
            try:
                resultats = self.search([keyword], top_k=top_k)
                if not resultats:
                    print("Aucune correspondance trouvée.")
                    return
                
                formatted_results = []
                for res in resultats:
                    extrait = res.get("Extrait", [])
                    if extrait:
                        extraitdeux = extrait[0]
                        formatted_results.append({
                            "Source": res.get("Source", "Inconnu"),
                            "Titre": res.get("Titre", ""),
                            "Auteur": res.get("Auteur", ""),
                            "Date": res.get("Date", ""),
                            "Extrait avant": f"...{extraitdeux.get('contexte_avant', '')} ",
                            "Motif": extraitdeux.get('motif', ''),
                            "Extrait après": f"{extraitdeux.get('contexte_apres', '')}...",
                            "Pertinence": round(res.get("Pertinence", 0), 2)
                        })
                
                if formatted_results:
                    resultats_df = pd.DataFrame(formatted_results)
                    display(resultats_df)
                else:
                    print("Aucun extrait trouvé.")
            
            except Exception as e:
                print(f"Erreur lors de la recherche : {e}")

# version corrigée partagée

# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"



# =============== 2.4 : La classe Author ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
# =============== 2.5 : ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    


# ========== td5 1.1 ======================
class RedditDocument(Document):
    '''
    nombre de commentaires postés 
    
    '''
    def __init__(self, comments):
        super().__init__(titre="", auteur="", date="", url="", texte="")
        self.comments = comments

    def getComments(self):
        return self.comments
    def setComments(self, comments):
        self.comments = comments

    def __str__(self):
        return (f"Le Document est un élément Reddit publié par {self.auteur} le {self.date} avec {self.comments} commentaires et ayant pour titre {self.titre} -- {self.texte} // url : {self.url}")


class ArxivDocument(Document):
    """Classe pour représenter un document ArXiv."""
    def __init__(self, auteur=""):
        super().__init__(titre="", auteur="", date="", url="", texte="")
        self.auteur = auteur

    def getAuteur(self):
        return self.auteur

    def setAuteur(self, author):
        if isinstance(author, list):
            self.auteur = [a for a in author if isinstance(a, Author)]
        elif isinstance(author, Author):
            self.auteur = [author]

    def __str__(self):
        return (f"Le Document est un élément ArXiv publié par {self.auteur} le {self.date} "
                f"ayant pour titre {self.titre} -- {self.texte} // url : {self.url}")

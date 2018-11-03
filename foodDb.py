from neo4j import GraphDatabase, basic_auth

class FoodDb():

    def __init__ (self):
        self._driver = GraphDatabase.driver("bolt://localhost:11004", auth=("neo4j", "dblocal"))
        self._session = self._driver.session()

    def addManga (self, manga_name, editor_name, type_name, author):
        '''Allows you to add a manga with its editor, type and author
        
        Arguments:
            manga_name {string} -- defines the name of the manga (unique)
            editor_name {string} -- defines the editor of the editor (unique)
            type_name {string} -- defines the type of the editor (unique)
            author {dictionnary} -- defines the author's firstname (unique) and author's lastname of the editor
        '''

        try:
            author_firstname = author['firstname']
            author_lastname = author['lastname']

            try:
                request = 'CREATE (:Manga {name: {manga_name}})'
                self._session.run(request, {'manga_name': manga_name})        
            except:
                pass

            try:
                request = 'CREATE (:Editor {name: {editor_name}})'
                self._session.run(request, {'editor_name': editor_name})        
            except:
                pass
            
            try:
                request = 'CREATE (:Type {name: {type_name}})'
                self._session.run(request, {'type_name': type_name})        
            except:
               pass
            
            try:
                request = 'CREATE (:Author {firstname: {author_firstname}, lastname: {author_lastname}})'
                self._session.run(request, {'author_firstname': author_firstname, 'author_lastname': author_lastname})        
            except:
                pass

            try:
                #Manga-[TYPE]->Type
                request = "MATCH (m:Manga) WHERE m.name = '{}' MATCH (t:Type) WHERE t.name = '{}' CREATE (m) -[r:TYPE]-> (t)".format(manga_name, type_name)
                self._session.run(request)

                #Author-[CREATE]->Manga
                request = "MATCH (a:Author) WHERE a.firstname = '{}' AND a.lastname = '{}' MATCH (m:Manga) WHERE m.name = '{}' CREATE (a) -[r:CREATE]-> (m)".format(author_firstname, author_lastname, manga_name)
                self._session.run(request)

                #Editor-[EDITS]->Manga
                request = "MATCH (e:Editor) WHERE e.name = '{}' MATCH (m:Manga) WHERE m.name = '{}' CREATE (e) -[r:EDITS]-> (m)".format(editor_name, manga_name)
                self._session.run(request)
            except:
                pass
        
        except:
            print("Verify the autor's parameters")


    def addTom (self, manga_name, tom_title, tom_closingDate, tom_price, tom_possessed):
        '''Allows to add a tom to a manga
        
        Arguments:
            manga_name {string} -- name to which the tom is added
            tom_title {string} -- title of the tom (unique)
            tom_closingDate {string} -- closing date of the tom
            tom_price {float} -- price of the tom
            tom_possessed {boolean} -- possessed of the tom
        '''

        try:
            request = 'MATCH (m:Manga {name: {manga_name}}) RETURN m'
            result = self._session.run(request, {'manga_name': manga_name})   

            #Verify if the manga exists
            if (result.single() == None):
                raise Exception('The manga does not exist')    
            
            try:
                request = 'CREATE (:Tom {title: {tom_title}, closingDate: {tom_closingDate}, price: {tom_price}, possessed: {tom_possessed}})'
                self._session.run(request, {'tom_title': tom_title, 'tom_closingDate': tom_closingDate, 'tom_price': tom_price, 'tom_possessed': tom_possessed})        
            except:
                pass
            
            try:
                #TODO arranger l'ajout du lien s'il est déjà existant

                #Manga-[CONTAINS]->Tom
                request = "MATCH (m:Manga) WHERE m.name = '{}' MATCH (t:Tom) WHERE t.title = '{}' CREATE (m) -[r:CONTAINS]-> (t)".format(manga_name, tom_title)
                self._session.run(request)
            except:
                pass

        except Exception as e:
            print(e)
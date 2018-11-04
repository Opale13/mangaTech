from neo4j import GraphDatabase, basic_auth

class FoodDb():    
    #TODO arranger l'ajout du lien s'il est déjà existant

    def __init__ (self):
        self._driver = GraphDatabase.driver("bolt://localhost:11004", auth=("neo4j", "dblocal"))
        

    def addManga (self, manga_name, editor_name, type_name, author_firstname, author_lastname):
        '''Allows you to add a manga with its editor, type and author
        
        Arguments:
            manga_name {string} -- defines the name of the manga (unique)
            editor_name {string} -- defines the editor of the editor (unique)
            type_name {string} -- defines the type of the editor (unique)
            author_firstname {string} -- defines the author's firstname (unique)
            author_lastname {string} -- defines the author's lastname 
        '''

        try:
            session = self._driver.session()

            try:
                request = 'CREATE (:Manga {name: {manga_name}})'
                session.run(request, {'manga_name': manga_name})        
            except:
                pass

            try:
                request = 'CREATE (:Editor {name: {editor_name}})'
                session.run(request, {'editor_name': editor_name})        
            except:
                pass
            
            try:
                request = 'CREATE (:Type {name: {type_name}})'
                session.run(request, {'type_name': type_name})        
            except:
               pass
            
            try:
                request = 'CREATE (:Author {firstname: {author_firstname}, lastname: {author_lastname}})'
                session.run(request, {'author_firstname': author_firstname, 'author_lastname': author_lastname})        
            except:
                pass          
            
            try:
                #Manga-[TYPE]->Type
                request = "MATCH (m:Manga) WHERE m.name = '{}' MATCH (t:Type) WHERE t.name = '{}' CREATE (m) -[r:TYPE]-> (t)".format(manga_name, type_name)
                session.run(request)
            except:
                pass        
            
            try:
                #Author-[CREATE]->Manga
                request = "MATCH (a:Author) WHERE a.firstname = '{}' AND a.lastname = '{}' MATCH (m:Manga) WHERE m.name = '{}' CREATE (a) -[r:CREATE]-> (m)".format(author_firstname, author_lastname, manga_name)
                session.run(request)
            except:
                pass

            try:
                #Editor-[EDITS]->Manga
                request = "MATCH (e:Editor) WHERE e.name = '{}' MATCH (m:Manga) WHERE m.name = '{}' CREATE (e) -[r:EDITS]-> (m)".format(editor_name, manga_name)
                session.run(request)
            except:
                pass

            session.close()
        
        except:
            session.close()


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
            session = self._driver.session()

            request = 'MATCH (m:Manga {name: {manga_name}}) RETURN m'
            result = session.run(request, {'manga_name': manga_name})   

            #Verify if the manga exists
            if (result.single() == None):
                raise Exception('The manga does not exist') 
            
            try:
                request = 'CREATE (:Tom {title: {tom_title}, closingDate: {tom_closingDate}, price: {tom_price}, possessed: {tom_possessed}})'
                session.run(request, {'tom_title': tom_title, 'tom_closingDate': tom_closingDate, 'tom_price': tom_price, 'tom_possessed': tom_possessed})        
            except:
                pass
            
            try:
                #Manga-[CONTAINS]->Tom
                request = "MATCH (m:Manga) WHERE m.name = '{}' MATCH (t:Tom) WHERE t.title = '{}' CREATE (m) -[r:CONTAINS]-> (t)".format(manga_name, tom_title)
                session.run(request)
            except:
                pass
            
            session.close()

        except Exception as e:
            print(e)
            session.close()
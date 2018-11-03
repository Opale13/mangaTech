from neo4j import GraphDatabase, basic_auth

class FoodDb():

    def __init__ (self):
        self.__driver = GraphDatabase.driver("bolt://localhost:11004", auth=("neo4j", "dblocal"))
        self.__session = self.__driver.session()

    def addManga (self, manga_name, editor_name, type_name, author):
        '''[summary]
        
        Arguments:
            manga_name {string} -- [defines the name of the manga]
            editor_name {string} -- [defines the editor of the editor]
            type_name {string} -- [defines the type of the editor]
            author {dictionnary} -- [defines the author's firstname and author's lastname of the editor]
        '''

        try:
            author_firstname = author['firstname']
            author_lastname = author['lastname']

            try:
                request = 'CREATE (:Manga {name: {manga_name}})'
                self.__session.run(request, {'manga_name': manga_name})        
            except:
                pass

            try:
                request = 'CREATE (:Editor {name: {editor_name}})'
                self.__session.run(request, {'editor_name': editor_name})        
            except:
                pass
            
            try:
                request = 'CREATE (:Type {name: {type_name}})'
                self.__session.run(request, {'type_name': type_name})        
            except:
               pass
            
            try:
                request = 'CREATE (:Author {firstname: {author_firstname}, lastname: {author_lastname}})'
                self.__session.run(request, {'author_firstname': author_firstname, 'author_lastname': author_lastname})        
            except:
                pass

            try:
                #Manga-[TYPE]->Type
                request = "MATCH (m:Manga) WHERE m.name = '{}' MATCH (t:Type) WHERE t.name = '{}' CREATE (m) -[r:TYPE]-> (t)".format(manga_name, type_name)
                self.__session.run(request)

                #Author-[CREATE]->Manga
                request = "MATCH (a:Author) WHERE a.firstname = '{}' AND a.lastname = '{}' MATCH (m:Manga) WHERE m.name = '{}' CREATE (a) -[r:CREATE]-> (m)".format(author_firstname, author_lastname, manga_name)
                self.__session.run(request)

                #Editor-[EDITS]->Manga
                request = "MATCH (e:Editor) WHERE e.name = '{}' MATCH (m:Manga) WHERE m.name = '{}' CREATE (e) -[r:EDITS]-> (m)".format(editor_name, manga_name)
                self.__session.run(request)
            except:
                pass
        
        except:
            raise Exception("Verify the autor's parameters")


    def addTom (self, manga_name, title, closingDate, price, possessed):
        pass
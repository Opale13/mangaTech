from neo4j import GraphDatabase, basic_auth
import re

class FoodDb():    

    def __init__ (self, localhost, login, password):
        self._driver = GraphDatabase.driver(localhost, auth=(login, password))
        self.regexDate = re.compile(r"[\d]{2}/[\d]{2}/[\d]{4}")

        try:
            request = "CREATE CONSTRAINT ON (a:Author) ASSERT a.firstname IS UNIQUE"
            session = self._driver.session()
            session.run(request)
            session.close()    
        except:
            session.close()

        try:
            request = "CREATE CONSTRAINT ON (e:Editor) ASSERT e.name IS UNIQUE"
            session = self._driver.session()
            session.run(request)
            session.close()    
        except:
            session.close()
        
        try:
            request = "CREATE CONSTRAINT ON (m:Manga) ASSERT m.name IS UNIQUE"
            session = self._driver.session()
            session.run(request)
            session.close()    
        except:
            session.close()
        
        try:
            request = "CREATE CONSTRAINT ON (s:Store) ASSERT s.name IS UNIQUE"
            session = self._driver.session()
            session.run(request)
            session.close()    
        except:
            session.close()
        
        try:
            request = "CREATE CONSTRAINT ON (t:Tom) ASSERT t.title IS UNIQUE"
            session = self._driver.session()
            session.run(request)
            session.close()    
        except:
            session.close()

        try:
            request = "CREATE CONSTRAINT ON (t:Type) ASSERT t.name IS UNIQUE"
            session = self._driver.session()
            session.run(request)
            session.close()    
        except:
            session.close()
        

    def addManga (self, manga_name, editor_name, type_name, author):
        '''Allows you to add a manga with its editor, type and author
        
        Arguments:
            manga_name {string} -- defines the name of the manga (unique)
            editor_name {string} -- defines the editor of the editor (unique)
            type_name {string} -- defines the type of the editor (unique)
            author {dictionnary} -- firstname: defines the author's firstname (unique) {string}
                                    lastname: defines the author's lastname {string}
        '''
        author_firstname = ''
        author_lastname = ''

        try:
            if not isinstance(manga_name, str):
                raise Exception("manga_name is not a string")

            if not isinstance(editor_name, str):
                raise Exception("editor_name is not a string")
            
            if not isinstance(type_name, str):
                raise Exception("type_name is not a string")

            if 'firstname' not in author:
                raise Exception("firstname is not in author dictionnary")
            elif not isinstance(author['firstname'], str):
                raise Exception("author_firstname is not a string")            
            else:
                author_firstname = author['firstname']
            
            if 'lastname' not in author:
                raise Exception("lastname is not in author dictionnary")
            elif not isinstance(author['lastname'], str):
                raise Exception("author_lastname is not a string")            
            else:
                author_lastname = author['lastname']

            try:
                request = 'CREATE (:Manga {name: {manga_name}})'
                session = self._driver.session()
                session.run(request, {'manga_name': manga_name})  
                session.close()    
            except:
                session.close()

            try:
                request = 'CREATE (:Editor {name: {editor_name}})'
                session = self._driver.session()
                session.run(request, {'editor_name': editor_name})
                session.close()    
            except:
                session.close()
            
            try:
                request = 'CREATE (:Type {name: {type_name}})'
                session = self._driver.session()
                session.run(request, {'type_name': type_name}) 
                session.close()   
            except:
               session.close()
            
            try:
                request = 'CREATE (:Author {firstname: {author_firstname}, lastname: {author_lastname}})'
                session = self._driver.session()
                session.run(request, {'author_firstname': author_firstname, 'author_lastname': author_lastname}) 
                session.close()    
            except:
                session.close()          
            
            try:
                request = "MATCH (m:Manga) -[r:TYPE]-> (t:Type) WHERE m.name='{}' AND t.name='{}' RETURN r".format(manga_name, type_name)
                session = self._driver.session()
                result = session.run(request)
                session.close()

                if (result.single() == None):     
                    try:               
                        #Manga-[TYPE]->Type
                        request = "MATCH (m:Manga) WHERE m.name = '{}' MATCH (t:Type) WHERE t.name = '{}' CREATE (m) -[r:TYPE]-> (t)".format(manga_name, type_name)
                        session = self._driver.session()
                        session.run(request)
                        session.close()
                    except:
                        session.close()

            except:
                session.close()        
            
            try:
                request = "MATCH (a:Author) -[r:CREATE]-> (m:Manga) WHERE a.firstname = '{}' AND a.lastname = '{}' AND m.name = '{}' RETURN r".format(author_firstname, author_lastname, manga_name)
                session = self._driver.session()
                result = session.run(request)
                session.close()

                if (result.single() == None):  
                    try:
                        #Author-[CREATE]->Manga
                        request = "MATCH (a:Author) WHERE a.firstname = '{}' AND a.lastname = '{}' MATCH (m:Manga) WHERE m.name = '{}' CREATE (a) -[r:CREATE]-> (m)".format(author_firstname, author_lastname, manga_name)
                        session = self._driver.session()
                        session.run(request)
                        session.close()
                    except:
                        session.close()
            except:
                session.close()

            try:
                request = "MATCH (e:Editor) -[r:EDITS]-> (m:Manga) WHERE e.name = '{}' AND m.name = '{}' RETURN r".format(editor_name, manga_name)
                session = self._driver.session()
                result = session.run(request)
                session.close()

                if (result.single() == None): 
                    try:
                        #Editor-[EDITS]->Manga
                        request = "MATCH (e:Editor) WHERE e.name = '{}' MATCH (m:Manga) WHERE m.name = '{}' CREATE (e) -[r:EDITS]-> (m)".format(editor_name, manga_name)
                        session = self._driver.session()
                        session.run(request)
                        session.close()
                    except:
                        session.close()
            except:
                session.close()
        
        except Exception as e:
            print(e)

  
    def addTom (self, manga_name, tom_title, tom_closingDate, tom_price, tom_possessed, store_name=None, purchase_date=None):
        '''Allows to add a tom to a manga
        
        Arguments:
            manga_name {string} -- name to which the tom is added
            tom_title {string} -- title of the tom (unique)
            tom_closingDate {string} -- closing date of the tom
            tom_price {float} -- price of the tom
            tom_possessed {boolean} -- possessed of the tom
            store_name {string} -- store where we buy the manga (unique), optional if we have bought the tom
            purchase_date {string} -- date of purchase, optional if we have bought the tom
        '''

        try:      
            if not isinstance(manga_name, str):
                raise Exception("manga_name is not a string")
            
            if not isinstance(tom_title, str):
                raise Exception("tom_title is not a string")
            
            if not isinstance(tom_closingDate, str):
                raise Exception("tom_closingDate is not a string")
            elif self.regexDate.match(tom_closingDate) == None:
                raise Exception("tom_closingDate has not the good format: dd/mm/yy")
            
            if not isinstance(tom_price, float):
                raise Exception("tom_price is not a float")
            elif tom_price < 0:
                raise Exception("tom_price must be greater than 0")
            
            if not isinstance(tom_possessed, bool):
                raise Exception("tom_possessed is not a boolean")

            if tom_possessed == True:
                if not isinstance(store_name, str):
                    raise Exception("store_name is not a string")

                if not isinstance(purchase_date, str):
                    raise Exception("purchase_date is not a string")
                elif self.regexDate.match(purchase_date) == None:
                    raise Exception("purchase_date has not the good format: dd/mm/yy")

            try:
                request = 'MATCH (m:Manga {name: {manga_name}}) RETURN m'
                session = self._driver.session()
                result = session.run(request, {'manga_name': manga_name}) 
                session.close() 
            except:
                session.close() 

            #Verify if the manga exists
            if (result.single() == None):
                raise Exception('The manga does not exist')             
            else:
                try:
                    request = 'CREATE (:Tom {title: {tom_title}, closingDate: {tom_closingDate}, price: {tom_price}, possessed: {tom_possessed}})'
                    session = self._driver.session()
                    session.run(request, {'tom_title': tom_title, 'tom_closingDate': tom_closingDate, 'tom_price': tom_price, 'tom_possessed': tom_possessed})        
                    session.close()
                except:
                    session.close()
                
                try:
                    request = "MATCH (m:Manga) -[r:CONTAINS]-> (t:Tom) WHERE m.name = '{}' AND t.title = '{}' RETURN r".format(manga_name, tom_title)
                    session = self._driver.session()
                    result = session.run(request)
                    session.close()
                
                    if (result.single() == None): 
                        try:
                            #Manga-[CONTAINS]->Tom
                            request = "MATCH (m:Manga) WHERE m.name = '{}' MATCH (t:Tom) WHERE t.title = '{}' CREATE (m) -[r:CONTAINS]-> (t)".format(manga_name, tom_title)
                            session = self._driver.session()
                            session.run(request)              
                            session.close()
                        except:
                            session.close()                
                except:
                    session.close()

                if (tom_possessed == True):                  
                    self.addStore(tom_title, store_name, purchase_date)  

        except Exception as e:
            print(e)


    def addStore (self, tom_title, store_name, purchase_date):
        '''Add a store at one tom
        
        Arguments:
            tom_title {string} -- title of the tom (unique)
            store_name {string} -- name of the store (unique)
            purchase_date {string} -- purchase date
        '''

        try:
            if not isinstance(tom_title, str):
                raise Exception("tom_title is not a string")

            if not isinstance(store_name, str):
                raise Exception("store_name is not a string")

            if not isinstance(manga_name, str):
                raise Exception("manga_name is not a string")
            
            if not isinstance(purchase_date, str):
                    raise Exception("purchase_date is not a string")
            elif self.regexDate.match(purchase_date) == None:
                raise Exception("purchase_date has not the good format: dd/mm/yy")

            try:
                request = 'CREATE (:Store {name: {store_name}})'
                session = self._driver.session()
                session.run(request, {'store_name': store_name})        
                session.close()
            except:
                session.close()

            try:
                request = "MATCH (t:Tom) -[r:PURCHASED]-> (s:Store) WHERE t.title = '{}' AND s.name = '{}' RETURN r".format(tom_title, store_name)
                session = self._driver.session()
                result = session.run(request)
                session.close()

                if (result.single() == None): 
                    try:
                        #Tom-[PURCHASED]->Store
                        request = "MATCH (s:Store) WHERE s.name = '{}' MATCH (t:Tom) WHERE t.title = '{}' CREATE (t) -[r:PURCHASED]-> (s) SET r.purchaseDate='{}'".format(store_name, tom_title, purchase_date)
                        session = self._driver.session()
                        session.run(request)              
                        session.close()
                    except:
                        session.close()

            except:
                session.close()    

        except Exception as e:
            print(e)      

    def getDriver (self):
        return self._driver   
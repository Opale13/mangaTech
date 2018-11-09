from neo4j import GraphDatabase, basic_auth

def searchManga(manga_type, author):
    try:
        driver = GraphDatabase.driver("bolt://localhost:11004", auth=("neo4j", "dblocal"))

        request = "MATCH (t:Type) <-[r:TYPE]- (m:Manga) <-[s:CREATE]- (a:Author) WHERE t.name={manga_type} AND a.firstname={author_firstname} AND a.lastname={author_lastname} RETURN m"
        session = driver.session()
        result = list(session.run(request, {'manga_type': manga_type, 'author_firstname': author['firstname'], 'author_lastname': author['lastname']}))
        session.close()      

        # If the author does not exist, we send all manga for the type
        if (len(result) == 0):
            try:
                request = "MATCH (t:Type) <-[r:TYPE]- (m:Manga) WHERE t.name={manga_type} RETURN m"
                session = driver.session()
                result = list(session.run(request, {'manga_type': manga_type}))
                session.close()        
                
                if (len(result) > 0):
                     for i in range(len(result)):
                        print(result[i]['m']['name'])
                
                else:
                    print("No manga found for {}".format(manga_type))

            except Exception as e:
                print(e)   

        else:  
            for i in range(len(result)):
                print(result[i]['m']['name'])

    except Exception as e:
        print(e)
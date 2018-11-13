from neo4j import GraphDatabase, basic_auth

def searchManga(driver, manga_type, author):
    '''This function found one or many manga in function of a type and a author.
       If the author does not exist, the function return the manga link at the type.
    
    Arguments:
        manga_type {string} -- The type
        author {dictionnary} -- a dictionnary with two key, firstname and lastname
    '''
    author_firstname = ''
    author_lastname = ''

    if not isinstance(manga_type, str):
        raise Exception("manga_type is not a string")

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
        request = "MATCH (t:Type) <-[r:TYPE]- (m:Manga) <-[s:CREATE]- (a:Author) WHERE t.name={manga_type} AND a.firstname={author_firstname} AND a.lastname={author_lastname} RETURN m"
        session = driver.session()
        result = list(session.run(request, {'manga_type': manga_type, 'author_firstname': author_firstname, 'author_lastname': author_lastname}))
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

            except:
                session.close() 

        else:  
            for i in range(len(result)):
                print(result[i]['m']['name'])
    
    except:
        session.close()   


def calculPrice(driver, manga_name):
    '''For a given manga, calculate the price that remains to be paid to have the mangas 
       that are not in our possession and the price that we have already paid.
    
    Arguments:
        manga_name {string} -- the manga's name
    '''

    try:
        if not isinstance(manga_name, str):
            raise Exception("manga_name is not a string")

        total_price = 0
        price_possessed = 0
        price_to_paye = 0
        
        try:
            request = "MATCH (to:Tom) <-[r:CONTAINS]- (m:Manga) WHERE m.name={manga_name} RETURN to ORDER BY to.title"
            session = driver.session()
            result = list(session.run(request, {'manga_name': manga_name}))
            session.close()
        except:
            session.close()

        if (len(result) > 0):
            for i in range(len(result)):
                manga = result[i]['to']
                total_price += manga['price']

                if (manga['possessed']):
                    price_possessed += manga['price']
                    price_to_paye = total_price - price_possessed            
            
            print("For {}:".format(manga_name))
            print("    The total price is equal to {}\u20ac".format(total_price))
            print("    You have already paid: {}\u20ac".format(price_possessed))
            print("    You still have to pay: {}\u20ac".format(price_to_paye))
        
        else:
            print("Manga not found")

    except Exception as e:
        print(e)


def calculStat(driver):
    pass
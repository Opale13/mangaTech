from foodDb import FoodDb
from useDatabase import *
#localhost: bolt://localhost:11004

#searchManga(driver, 'Seinen', {'firstname': 'ss', 'lastname': 'Ishida'})
#calculPrice(driver, 'Blue Exorcist')

#calculStat(driver)

db = None
driver = None
print(">In first enter the login command")
while True:
    mode = input(">Enter an operating mode (for commands type 'help'):")

    if mode == 'login':
        localhost = input("\t>Enter the localhost: ")
        login = input("\t>Enter the login (by default: neo4j): ")
        password = input("\t>Enter the password: ")

        db = FoodDb(localhost, login, password)
        driver = db.getDriver()
    
    elif mode == 'logout':
        print('>logout')
        break

    elif mode == 'addmanga':
        print(">Create manga:")
        manga_name = input("\t>Enter manga's name (like One Piece): ")
        editor_name = input("\t>Enter editor's name (like Glenat): ")
        type_name = input("\t>Enter type's name (like Shonen): ")
        author_firstname = input("\t>Enter author's firstname (like Eiichirō): ")
        author_lastname = input("\t>Enter author's lastname (like Oda): ")

        try:
            db.addManga(manga_name.title(), editor_name.title(), type_name.title(), {
                'firstname': author_firstname.title(),
                'lastname': author_lastname.title()
            })

            print('\t>Manga created')

        except Exception as e:
            print(e)
    
    elif mode == 'addtom':
        print(">Create tom:")
        manga_name = input("\t>Enter manga's name (like One Piece): ")
        tom_title = input("\t>Enter tom's title (like One Piece T.1): ")
        tom_closingDate = input("\t>Enter tom's closing date (like 13/11/2018): ")
        tom_price = float(input("\t>Enter tom's price (like 7.20): "))
        tom_possessed = input("\t>Enter if you have the tom (like True): ")

        if tom_possessed.title() == 'True':
            store_name = input("\t>Enter store's name (like Club): ")
            purchase_date = input("\t>Enter tom's purchase date (like 13/11/2018): ")

            try:
                db.addTom(manga_name.title(), tom_title.title(), tom_closingDate, tom_price, True, store_name.title(), purchase_date.title())
                print('\t>Tom created')
            except Exception as e:
                print(e)
        
        else:
            try:
                db.addTom(manga_name.title(), tom_title.title(), tom_closingDate.title(), tom_price, False)
                print('\t>Tom created')
            except Exception as e:
                print(e)        

    elif mode == 'addstore':        
        print(">Create tom:")
        tom_title = input("\t>Enter tom's title (like One Piece T.1): ")
        store_name = input("\t>Enter store's name (like Club): ")
        purchase_date = input("\t>Enter tom's purchase date (like 13/11/2018): ")

        try:
            db.addStore(tom_title.title(), store_name.title(), purchase_date.title())
            print('Store added')
        
        except Exception as e:
            print(e)
        
    elif mode == 'searchmanga':
        print(">Search manga:")
        type_name = input("\t>Enter type's name (like Shonen): ")
        author_firstname = input("\t>Enter author's firstname (like Eiichirō): ")
        author_lastname = input("\t>Enter author's lastname (like Oda): ")

        try:
            searchManga(driver, type_name, {
                'firstname': author_firstname,
                'lastname': author_lastname
            })
        
        except Exception as e:
            print(e)

    elif mode =='help':
        print('>All function:')
        print('\tlogin: connect at the database')
        print('\tlogout: desconnect at the database')
        print('\taddmanga: add manga in database')
        print('\taddtom: add tom in database')
        print('\taddstore: if you have bought a tom, you can add a store')
        print('\tsearchmanga: ')
    
    else:
        print('>Command not found')
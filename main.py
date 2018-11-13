from foodDb import FoodDb
from useDatabase import *

db = FoodDb("bolt://localhost:11004", "neo4j", "dblocal")
driver = db.getDriver()

#db.addManga('Blue Exorcist', 'Kaze', 'Shonen', {'firstname': 'Kazue', 'lastname':'Kato'})
#db.addTom('Blue Exorcist', "Blue Exorcist T.1", '08/08/2015', 7.20, True, 'Carrefour', '10/08/2018')
#db.addTom('One Piece', "One Piece T.2", '05/08/2015', 7.50, False)
#db.addTom('One Piece', "One Piece T.3", '05/08/2015', 7.50, False)

#searchManga(driver, 'Seinen', {'firstname': 'ss', 'lastname': 'Ishida'})
#calculPrice(driver, 'Blue Exorcist')

#calculStat(driver)
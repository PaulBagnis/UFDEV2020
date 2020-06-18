import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", db="doom")
mycursor = mydb.cursor()

def collide(obj1, obj2):
    # Fonction qui vérifie si des sprites se chevauchent
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def updateCredits(number) :
    strNumber = '\'' + str(number) + '\''
    query = "UPDATE credits SET credits =" + strNumber + "WHERE id = 1"
    mycursor.execute(query)
    return 0

def getCredits() :
    # Fonction qui récupère les crédits en BDD
    mycursor.execute("SELECT credits from credits")
    result = mycursor.fetchall()
    return result[0][0]

def updateBonus(number, numberTwo) :
    strNumber = '\'' + str(number) + '\''
    strNumberTwo = '\'' + str(numberTwo) + '\''
    query = "UPDATE save_bonus SET vel =" + strNumber + "WHERE id = 1"
    mycursor.execute(query)
    query = "UPDATE save_bonus SET life =" + strNumberTwo + "WHERE id = 1"
    mycursor.execute(query)
    return 0

def getBonusVel() :
    # Fonction qui récupère les crédits en BDD
    mycursor.execute("SELECT vel from save_bonus")
    result = mycursor.fetchall()
    return result[0][0]

def getBonusLife() :
    # Fonction qui récupère les crédits en BDD
    mycursor.execute("SELECT life from save_bonus")
    result = mycursor.fetchall()
    return result[0][0]
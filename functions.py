import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", db="doom")
mycursor = mydb.cursor()

def collide(obj1, obj2):
    # Fonction qui vérifie si des sprites se chevauchent
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def getScores() :
    # Fonction qui récupère les scores en BDD
    mycursor.execute("SELECT score,ship from scores")
    result = mycursor.fetchall()
    resultList = []
    for i in result:
        resultList.append(i)
    return resultList

def updateScores(number) :
    strNumber = '\'' + str(number) + '\''
    query = "UPDATE credits SET credits =" + strNumber + "WHERE id = 1"
    mycursor.execute(query)
    return 0

def getCredits() :
    # Fonction qui récupère les crédits en BDD
    mycursor.execute("SELECT credits from credits")
    result = mycursor.fetchall()
    return result[0][0]
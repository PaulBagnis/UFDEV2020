import mysql.connector

# def collide(obj1, obj2):
#     offset_x = obj2.x - obj1.x
#     offset_y = obj2.y - obj1.y
#     return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def getScores() :
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="", db="doom")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT score from scores")
    result = mycursor.fetchall()
    resultList = []
    for i in result:
        resultList.append(i[0])
    return resultList
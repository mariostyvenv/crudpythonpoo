from connections.Main import ConexionSqlite

class Word(ConexionSqlite):

    def __init__(self):
        super(Word, self).__init__()

    def startDatabase(self):
        state = False

        cursor = self.conexion.cursor()

        sql = '''CREATE TABLE IF NOT EXISTS words(
                LETRA VARCHAR(100),
                INGLES VARCHAR(100),
                NO_APRENDIDO INT,
                REFORZAR INT,
                APRENDIDA INT,
                ORACION VARCHAR(100));
                '''
        try:

            cursor.execute(sql)
            self.conexion.commit()

            if self.__validatePopulate():

                if self.__populateTable():
                    state = True
                else:
                    print("Errores presentados al momento de preparar la base de datos")
                    state = False
            else:
                state = True

        except self.conexion.Error as e:
            print("Error en la consulta sql: {}".format(e))
            state = False

        except Exception as e:
            print("Error provocado en : {}".format(e))
            state = False
        
        return state

    def getAllResult(self):
        
        cursor = self.conexion.cursor()
        sql = '''SELECT rowid, INGLES, NO_APRENDIDO, REFORZAR, APRENDIDA, ORACION FROM words'''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conexion.commit()
        
        return result

    def getLearned(self):

        cursor = self.conexion.cursor()
        sql = '''SELECT rowid, INGLES, ORACION FROM words WHERE APRENDIDA = 1'''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conexion.commit()
        
        return result

    def getNotLearned(self):

        cursor = self.conexion.cursor()
        sql = '''SELECT rowid, INGLES FROM words WHERE NO_APRENDIDO = 1'''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conexion.commit()
        
        return result

    def startLearn(self):

        cursor = self.conexion.cursor()
        sql = '''SELECT rowid, INGLES FROM `words` WHERE APRENDIDA = 0 ORDER BY RANDOM() LIMIT 100'''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conexion.commit()

        return result
    
    def saveSentence(self, id, sentence):

        state = False

        try:
            cursor = self.conexion.cursor()
            sql = '''UPDATE words SET NO_APRENDIDO = 0, REFORZAR = 1, APRENDIDA = 1, ORACION = ? WHERE rowid = ?'''
            cursor.execute(sql, (sentence, id))
            state = True
            self.conexion.commit()

        except Exception:
            state = False

        return state

    def getReview(self):
        cursor = self.conexion.cursor()
        sql = '''SELECT rowid, INGLES, ORACION FROM `words` WHERE REFORZAR = 1 ORDER BY RANDOM() LIMIT 100'''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conexion.commit()

        return result

    def confirmReview(self, id, sentence):

        state = False

        try:
            cursor = self.conexion.cursor()
            sql = '''UPDATE words SET NO_APRENDIDO = 0, REFORZAR = 0, APRENDIDA = 1, ORACION = ? WHERE rowid = ?'''
            cursor.execute(sql, (sentence, id))
            state = True
            self.conexion.commit()

        except Exception:
            state = False

        return state

    def resetDatabase(self):

        state = False

        try:
            cursor = self.conexion.cursor()
            sql = '''UPDATE words SET NO_APRENDIDO = 1, REFORZAR = 0, APRENDIDA = 0, ORACION = '' '''
            cursor.execute(sql)
            state = True
            self.conexion.commit()

        except Exception:
            state = False

        return state

    def __validatePopulate(self):
        
        state = False

        cursor = self.conexion.cursor()

        sql = '''SELECT rowid FROM words'''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conexion.commit()

        if len(result) > 0:
            state = False

        else:
            state = True

        return state

    def __populateTable(self):

        state = False

        try:
            file = open("./db/words.sql")
            sql = file.read().replace("\n", " ")
            file.close()

            cursor = self.conexion.cursor()
            cursor.executescript(sql)
            self.conexion.commit()
            state = True
            self.conexion.commit()

        except self.conexion.Error as e:
            print("Error al poblar la tabla en la consulta: {}".format(e))
            state = False

        except Exception as e:
            print("Error al poblar la tabla : {}".format(e))
            state = False
        
        return state
        

    def __del__(self):
        self.conexion.close()
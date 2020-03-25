import sqlite3

class dbLib:
    def __init__(self):
        self.conn = sqlite3.connect("hz.db")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("SELECT * FROM appointment LIMIT 1")
            self.cursor.fetchall()
        except sqlite3.OperationalError:
            self.cursor.execute("""CREATE TABLE appointment ( 
                                       id INTEGER PRIMARY KEY,
                                       fio TEXT NOT NULL,
                                       date TEXT NOT NULL,
                                       distr TEXT,
                                       addr TEXT,
                                       phone TEXT NOT NULL,
                                       diag TEXT,
                                       create_date TEXT NOT NULL,
                                       create_time TEXT NOT NULL,
                                       del INTEGER DEFAULT 0
                                   );""")

			
	
    def addRecord(self, name, birthdate, distr, addresses, phone, diagn):
        mkrec = """INSERT INTO appointment (fio, date, distr, addr, phone, diag, create_date, create_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', date('now'), time('now'));"""
        self.cursor.execute(mkrec % (name, birthdate, distr, addresses, phone, diagn))
        self.conn.commit()
        mkrec = """SELECT * FROM appointment ORDER BY id DESC LIMIT 0"""
        self.cursor.execute(mkrec)
        return self.cursor.fetchall()
        
		
    def getAllRecords(self, limit=(False, 0, 0)):
        if not limit[0]:
            req = """SELECT * FROM appointment ORDER BY id DESC;"""
        else:
            req = """SELECT * FROM appointment ORDER BY id DESC LIMIT %d, %d;""" % (limit[1], limit[2])
        self.cursor.execute(req)
        x = self.cursor.fetchall()
        return x
        
    def getNotDeleted(self, limit=(False, 0, 0)):
        if not limit[0]:
            req = """SELECT * FROM appointment WHERE del = 0 ORDER BY id DESC;"""
        else:
            req = """SELECT * FROM appointment WHERE del = 0 ORDER BY id DESC LIMIT %d, %d;""" % (limit[1], limit[2])
        self.cursor.execute(req)
        x = self.cursor.fetchall()
        return x

    def deleteRecord(self, idr):
        req = """UPDATE appointment SET del = 1 WHERE id = %d;""" % (int(idr))
        self.cursor.execute(req)
        self.conn.commit()
        req = """SELECT * from appointment WHERE id = %d ORDER BY id DESC;""" % (int(idr))
        self.cursor.execute(req)
        return self.cursor.fetchall()
    
    def search(self, idr, name, birthdate, distr, addresses, phone, diagn):
        if idr == "-1":
            idr = "(\n"
        else:
            idr = """(id LIKE %s\nAND""" % (idr)
        req = """
		SELECT * FROM appointment 
		    WHERE 
		        %s(fio LIKE '%%%s%%'
		        AND date LIKE '%%%s%%'
		        AND addr LIKE '%%%s%%'
                        AND disrt LIKE '%%%s%%'
		        AND phone LIKE '%%%s%%'
                        AND diag LIKE '%%%s%%'
                        fio TEXT NOT NULL,
		        )) AND del = 0
		 ORDER BY id DESC;
		""" % (idr, name, birthdate, distr, addresses, phone, diagn)
        print(req)
        self.cursor.execute(req)
        return self.cursor.fetchall()
		
if __name__ == '__main__':
	db = dbLib()
	db.addRecord(
	    input("fio:"), 
	    input("Datebirth:"),
	    input("distr:"),
	    input("addr"),
            input("phone"),
            input("diagn"),
            


	)
	print(db.getNotDeleted())

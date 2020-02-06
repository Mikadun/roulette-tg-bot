import os
import urllib.parse as up
import psycopg2



class Roulette():
    def __init__(self):
        self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_NAME'), 
                                    password=os.getenv('DB_PASSWORD'), 
                                    host=os.getenv('DB_HOST'))
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def add(self, ref_id, good = "#fio# win", bad = "#fio# lose"):
        try:
            self.cur.execute('''INSERT INTO "Roulette" ("Reference_ID", "Good", "Bad") VALUES (%s, %s, %s)''', (ref_id, good, bad))
        except:
            return False
        else:
            self.conn.commit()
            return True

    def add_user(self, ref_id, user_id, f_name, s_name):
        try:
            self.cur.execute('''INSERT INTO "Roulette_users" ("Reference_ID", "Tg_ID", "F_name", "S_name") VALUES (%s, %s, %s, %s)''', (ref_id, user_id, f_name, s_name))
        except:
            return False
        else:
            self.conn.commit()
            return True

    def delete(self, ref_id):
        try:
            self.cur.execute('''DELETE FROM "Roulette_users" WHERE ("Reference_ID" = %s)''', (ref_id, ))
        except:
            return False
        else:
            self.conn.commit()
        
        try:
            self.cur.execute('''DELETE FROM "Roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
        except:
            return False
        else:
            self.conn.commit()
            return True

    def get_user(self, user_id):
        try:
            self.cur.execute('''SELECT "F_name", "S_name" FROM "Roulette_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
        except Exception as e:
            print(e)
            return False
        else:
            return self.cur.fetchall()

    def get_users(self, ref_id):
        try:
            self.cur.execute('''SELECT "Tg_ID" FROM "Roulette_users" WHERE ("Reference_ID" = %s)''', (ref_id, ))
        except:
            return False
        else:
            return [i[0] for i in self.cur.fetchall()]

    def get_info(self, ref_id):
        try:
            self.cur.execute('''SELECT "Good", "Bad" FROM "Roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
        except Exception as e:
            print(e)
            return False
        else:
            return list(self.cur.fetchall()[0])

    def check(self, ref_id):
        try:
            self.cur.execute('''SELECT "Reference_ID" FROM "Roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
        except Exception as e:
            print(e)
            return False
        else:
            return not(self.cur.fetchall()==[])

    def check_user(self, user_id):
        try:
            self.cur.execute('''SELECT "Reference_ID" FROM "Roulette_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
        except:
            return False
        else:
            temp = self.cur.fetchall()
            if len(temp) >= 1:
                return [i[0] for i in temp]
            else:
                return []

roulette = Roulette()

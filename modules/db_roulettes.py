import os
import urllib.parse as up
import psycopg2



class Russian_roulette():
	def __init__(self):
		self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_NAME'), 
									password=os.getenv('DB_PASSWORD'), 
									host=os.getenv('DB_HOST'))
		self.cur = self.conn.cursor()

	def __del__(self):
		self.cur.close()
		self.conn.close()

	def add(self, ref_id, magazine, misfire):
		try:
			self.cur.execute('''INSERT INTO "Russian_roulette" ("Reference_ID", "Magazine", "Shoots", "Misfire") VALUES (%s, %s, %s, %s)''', (ref_id, magazine, 0, misfire))
			self.conn.commit()
			return True
		except:
			return False

	def make_shoot(self, ref_id):
		try:
			self.cur.execute('''SELECT * FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
			temp = self.cur.fetchall()[0][2]
			self.cur.execute('''UPDATE "Russian_roulette" SET "Shoots" = %s where "Reference_ID" = %s''', (temp+1, ref_id))
			self.conn.commit()
			return temp+1
		except:
			return False	

	def get_info(self, ref_id):
		try:
			self.cur.execute('''SELECT * FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
			return self.cur.fetchall()[0][2:] #return magazine, shoots and misfire only
		except:
			return False

	def delete(self, ref_id):
		try:
			self.cur.execute('''DELETE FROM "Russian_roulette" WHERE ("Reference_ID = %s")''', (ref_id, ))
			self.conn.commit()
			return True
		except:
			return False
			
russian_roulette = Russian_roulette()
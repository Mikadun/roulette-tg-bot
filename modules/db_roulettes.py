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

	def add(self, ref_id, magazine, bullet, misfire):
		try:
			if (self.check_ref_id(ref_id)):
				self.cur.execute('''INSERT INTO "Russian_roulette" ("Reference_ID", "Magazine", "Shoots", "Bullet", "Misfire") VALUES (%s, %s, %s, %s, %s)''', (ref_id, magazine, 0, bullet, misfire))
			else:
				return False
		except:
			return False
		else: 
			self.conn.commit()
			return True
	
	def check_ref_id(self, ref_id):
		try:
			self.cur.execute('''SELECT * FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id,))
			return (self.cur.fetchall() == [])
		except:
			return -1

	def shoot(self, ref_id):
		try:
			self.cur.execute('''SELECT * FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
			temp = self.cur.fetchall()[0]

			if (temp[3]+1 == temp[4]):
				self.cur.execute('''DELETE FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
			else:
				self.cur.execute('''UPDATE "Russian_roulette" SET "Shoots" = %s where "Reference_ID" = %s''', (temp[3]+1, ref_id))
		except:
			return False	
		else:
			self.conn.commit()
			return [(temp[3]+1 == temp[4]), temp[5]]

	def delete(self, ref_id):
		try:
			self.cur.execute('''DELETE FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def clear(self):
		try:
			self.cur.execute('''DELETE FROM "Russian_roulette"''')
		except:
			return False
		else:
			self.conn.commit()
			return True

russian_roulette = Russian_roulette()
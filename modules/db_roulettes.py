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
			self.cur.execute('''INSERT INTO "Russian_roulette" ("Reference_ID", "Magazine", "Shoots", "Bullet", "Misfire") VALUES (%s, %s, %s, %s, %s)''', (ref_id, magazine, 0, bullet, misfire))
			self.conn.commit()
			return True
		except:
			return False

	def shoot(self, ref_id):
		try:
			self.cur.execute('''SELECT * FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
			temp = self.cur.fetchall()[0]
		except Exception as e:
			print(1, e)
			return False

		try:
			if (temp[3]+1 == temp[4]):
				self.cur.execute('''DELETE FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
			else:
				self.cur.execute('''UPDATE "Russian_roulette" SET "Shoots" = %s where "Reference_ID" = %s''', (temp[3]+1, ref_id))

			self.conn.commit()
			return [(temp[3]+1 == temp[4]), temp[5]]
		except Exception as e:
			print(2, e)
			return False	

	def delete(self, ref_id):
		try:
			self.cur.execute('''DELETE FROM "Russian_roulette" WHERE ("Reference_ID" = %s)''', (ref_id, ))
			self.conn.commit()
			return True
		except:
			return False

	def clear(self):
		try:
			self.cur.execute('''DELETE FROM "Russian_roulette"''')
			self.conn.commit()
			return True
		except:
			return False

russian_roulette = Russian_roulette()
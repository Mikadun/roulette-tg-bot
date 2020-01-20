import os
import urllib.parse as up
import psycopg2



class Classic_roulette():
	def __init__(self):
		self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_NAME'), 
									password=os.getenv('DB_PASSWORD'), 
									host=os.getenv('DB_HOST'))
		self.cur = self.conn.cursor()

	def __del__(self):
		self.cur.close()
		self.conn.close()

	def add(self, ref_id, user_id, bet, value):
		try:
			self.cur.execute('''INSERT INTO "Russian_roulette" ("Reference_ID", "Tg_ID", "Bet", "Value") VALUES (%s, %s, %s, %s)''', (ref_id, user_id, bet, value))
			self.conn.commit()
			return True
		except:
			return False

	def delete(self, ref_id, user_id):
		try:
			self.cur.execute('''DELETE FROM "Classic_roulette" WHERE ("Reference_ID = %s" AND "Tg_ID = %s")''', (ref_id, user_id))
			self.conn.commit()
			return True
		except:
			return False

classic_roulette = Classic_roulette()
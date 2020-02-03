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

	def add(self, ref_id, user_id, place, bet):
		try:
			self.cur.execute('''INSERT INTO "Classic_roulette" ("Reference_ID", "Tg_ID", "Place", "Bet") VALUES (%s, %s, %s, %s)''', (ref_id, user_id, place, bet))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def delete(self, ref_id, user_id):
		try:
			self.cur.execute('''DELETE FROM "Classic_roulette" WHERE ("Reference_ID = %s" AND "Tg_ID = %s")''', (ref_id, user_id))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def get_bet(self, ref_id, user_id, place):
		try:
			self.cur.execute('''SELECT "Bet" FROM "Classic_roulette" WHERE ("Reference_ID" = %s AND "Tg_ID" = %s AND "Place" = %s)''', (ref_id, user_id, place))
		except:
			return False
		else:
			temp = self.cur.fetchall()

			if (temp == []):
				return False
			else:
				return temp[0][0]

classic_roulette = Classic_roulette()
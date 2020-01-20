import os
import urllib.parse as up
import psycopg2

class Admin_list():
	def __init__(self):
		self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_NAME'), 
									password=os.getenv('DB_PASSWORD'), 
									host=os.getenv('DB_HOST'))
		self.cur = self.conn.cursor()

	def __del__(self):
		self.cur.close()
		self.conn.close()

	def add(self, user_id):
		try:
			self.cur.execute('''INSERT INTO "Admin_list" ("Tg_ID") VALUES (%s)''', (user_id,))
			return True
		except:
			return False

	def check(self, user_id):
		try:
			self.cur.execute('''SELECT * FROM "Admin_list" WHERE ("Tg_ID" = %s)''', (user_id,))
			return not(self.cur.fetchall() == [])
		except:
			return -1

admin_list = Admin_list()
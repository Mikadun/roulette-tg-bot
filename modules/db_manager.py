import os
import urllib.parse as up
import psycopg2

class Unauthenticated_users():
	def __init__(self):
		self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_NAME'), 
									password=os.getenv('DB_PASSWORD'), 
									host=os.getenv('DB_HOST'))
		self.cur = self.conn.cursor()

	def __del__(self):
		self.cur.close()
		self.conn.close()

	def get_info(self, user_id):
		try:
			self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
			return self.cur.fetchall()[0]	
		except:
			return False

	def check_email(self, email):
		try:
			self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Email" = %s)''', (email,))
			return not(self.cur.fetchall() == [])
		except:
			return -1

	def check_user_id(self, user_id):
		try:
			self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id,))
			return not(self.cur.fetchall() == [])
		except:
			return -1

	def show_all(self):
		try:
			self.cur.execute('''SELECT * FROM "Unauthenticated_users"''')
			return self.cur.fetchall()
		except:
			return False

	def add(self, user_id):
		try:
			self.cur.execute('''INSERT INTO "Unauthenticated_users" ("Tg_ID", "State") VALUES (%s, %s)''', (user_id, 1))
			self.conn.commit()
		except:
			return False
		else:
			return True

	def update_name(self, user_id, f_name, m_name, l_name):

		try:
			state = self.get_state(user_id)
			self.cur.execute('''UPDATE "Unauthenticated_users" SET "F_name" = %s,"M_name" = %s, "L_name" = %s, "State" = %s where "Tg_ID" = %s''', 
				(f_name, m_name, l_name, state+1, user_id))

		except:
			return False
		else:
			self.conn.commit()
			return True

	def update_email(self, user_id, email, code):
		try:
			state = self.get_state(user_id)
			self.cur.execute('''UPDATE "Unauthenticated_users" SET "Email" = %s, "Code" = %s, "State" = %s where "Tg_ID" = %s''', (email, code, state+1, user_id))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def update_code(self, user_id, code):
		try:
			self.cur.execute('''UPDATE "Unauthenticated_users" SET "Code" = %s where "Tg_ID" = %s''', (code, user_id))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def update_group(self, user_id, group):
		try:
			self.cur.execute('''UPDATE "Unauthenticated_users" SET "Group" = %s where "Tg_ID" = %s''', (group, user_id))
		except:
			return False
		else:
			self.conn.commit()
			return True


	def delete(self, user_id):
		try:
			self.cur.execute('''DELETE FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def get_code(self, user_id):
		try:
			self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
			return self.cur.fetchall()[0][7]
		except:
			return False

	def get_email(self, user_id):
		try:
			self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
			return self.cur.fetchall()[0][6]
		except:
			return False

	def get_state(self, user_id):
		try:
			self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
			return self.cur.fetchall()[0][-1]
		except:
			return False

	def next_state(self, user_id):
		try:
			state = self.get_state(user_id)
			self.cur.execute('''UPDATE "Unauthenticated_users" SET "State" = %s where "Tg_ID" = %s''', (state+1, user_id))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def previous_state(self, user_id):
		try:
			state = self.get_state(user_id)
			self.cur.execute('''UPDATE "Unauthenticated_users" SET "State" = %s where "Tg_ID" = %s''', (state-1, user_id))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def clear(self):
		try:
			self.cur.execute('''DELETE FROM "Unauthenticated_users"''')
		except:
			return False
		else:
			self.conn.commit()
			return True



class Authenticated_users():
	def __init__(self):
		self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_NAME'), 
									password=os.getenv('DB_PASSWORD'), 
									host=os.getenv('DB_HOST'))
		self.cur = self.conn.cursor()

	def __del__(self):
		self.cur.close()
		self.conn.close()
	
	def show_all(self):
		try:
			self.cur.execute('''SELECT * FROM "Authenticated_users"''')
			return self.cur.fetchall()
		except:
			return False

	def check_email(self, email):
		try:
			self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Email" = %s)''', (email,))
			return not(self.cur.fetchall() == [])
		except:
			return -1

	def check_group(self, group):
		try:
			self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Group" = %s)''', (group,))
			return not(self.cur.fetchall() == [])
		except:
			return -1

	def check_user_id(self, user_id):
		try:
			self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id,))
			return not(self.cur.fetchall() == [])
		except:
			return -1

	def add(self, user_id, f_name, m_name, l_name, group, email):
		try:
			self.cur.execute('''INSERT INTO "Authenticated_users" ("Tg_ID", "F_name", "M_name", "L_name", "Group", "Points", "Email") 
				VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
				(user_id, f_name, m_name, l_name, group, 0, email))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def delete(self, user_id):
		try:
			self.cur.execute('''DELETE FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def add_points(self, user_id, points):
		try:
			self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
			temp = self.cur.fetchall()[0][6]
			self.cur.execute('''UPDATE "Authenticated_users" SET "Points" = %s where "Tg_ID" = %s''', (temp+points, user_id))
		except Exception as e:
			return e
		else:
			self.conn.commit()
			return True

	def remove_points(self, user_id, points):
		try:
			self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
			temp = self.cur.fetchall()[0][6]
			self.cur.execute('''UPDATE "Authenticated_users" SET "Points" = %s where "Tg_ID" = %s''', (temp-points, user_id))
		except:
			return False
		else:
			self.conn.commit()
			return True

	def get_users_by_group(self, group):
		try:
			self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Group" = %s)''', (group, ))
			return self.cur.fetchall()
		except:
			return False

	def get_info(self, user_id):
		try:
			self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
			return self.cur.fetchall()[0]
		except:
			return False

	def clear(self):
		try:
			self.cur.execute('''DELETE FROM "Authenticated_users"''')
		except:
			return False
		else:
			self.conn.commit()
			return True

	def get_points(self, user_id):
		try:
			if self.check_user_id(user_id):
				self.cur.execute('''SELECT "Points" FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
				return self.cur.fetchall()
			else:
				return -1
		except:
			return False

	def get_groups(self):
		try:
			self.cur.execute('''SELECT DISTINCT "Group" FROM "Authenticated_users"''')
			return self.cur.fetchall()
		except:
			return False

unauth_users = Unauthenticated_users()
auth_users = Authenticated_users()

if __name__ == '__main__':
	unauth_users.clear()
import os
import urllib.parse as up
import psycopg2

class Unauthenticated_users():
	def __init__(self):

		self.conn = psycopg2.connect(dbname='***REMOVED***', user='***REMOVED***', 
									password='***REMOVED***', 
									host='***REMOVED***')
		self.cur = self.conn.cursor()

	def __del__(self):
		self.cur.close()
		self.conn.close()

	def get_info(self, user_id):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		return self.cur.fetchall()[0]	

	def check_email(self, email):
		self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Email" = %s)''', (email,))

		return not(self.cur.fetchall() == [])

	def check_user_id(self, user_id):
		self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id,))

		return not(self.cur.fetchall() == [])

	def show_all(self):
		self.cur.execute('''SELECT * FROM "Unauthenticated_users"''')
		return self.cur.fetchall()

	def add(self, user_id):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''INSERT INTO "Unauthenticated_users" ("Tg_ID", "State") VALUES (%s, %s)''', (user_id, 0))
		self.conn.commit()
		return 0

	def update_name(self, user_id, f_name, m_name, l_name):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''UPDATE "Unauthenticated_users" SET "F_name" = %s where "Tg_ID" = %s''', (f_name, user_id))
		self.cur.execute('''UPDATE "Unauthenticated_users" SET "M_name" = %s where "Tg_ID" = %s''', (m_name, user_id))
		self.cur.execute('''UPDATE "Unauthenticated_users" SET "L_name" = %s where "Tg_ID" = %s''', (l_name, user_id))
		self.conn.commit()
		return 0

	def update_email(self, user_id, email):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''UPDATE "Unauthenticated_users" SET "Email" = %s where "Tg_ID" = %s''', (email, user_id))
		self.conn.commit()
		return 0

	def update_code(self, user_id, code):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''UPDATE "Unauthenticated_users" SET "Code" = %s where "Tg_ID" = %s''', (code, user_id))
		self.conn.commit()
		return 0

	def update_group(self, user_id, group):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''UPDATE "Unauthenticated_users" SET "Group" = %s where "Tg_ID" = %s''', (group, user_id))
		self.conn.commit()
		return 0


	def delete(self, user_id):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''DELETE FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		self.conn.commit()
		return 0

	def get_code(self, user_id):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		return self.cur.fetchall()[0][7]

	def get_email(self, user_id):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		return self.cur.fetchall()[0][6]

	def get_state(self, user_id):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''SELECT * FROM "Unauthenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		return self.cur.fetchall()[0][8]

	def next_state(self, user_id):
		if not(self.check_user_id(user_id)):
			return -1

		state = self.get_state(user_id)

		self.cur.execute('''UPDATE "Unauthenticated_users" SET "State" = %s where "Tg_ID" = %s''', (state+1, user_id))
		self.conn.commit()
		return 0

	def clear(self):
		self.cur.execute('''DELETE FROM "Unauthenticated_users"''')
		return 0



class Authenticated_users():
	def __init__(self):
		self.conn = psycopg2.connect(dbname='***REMOVED***', user='***REMOVED***', 
									password='***REMOVED***', 
									host='***REMOVED***')
		self.cur = self.conn.cursor()

	def __del__(self):
		self.cur.close()
		self.conn.close()
	
	def show_all(self):
		self.cur.execute('''SELECT * FROM "Authenticated_users"''')
		return self.cur.fetchall()

	def check_email(self, email):
		self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Email" = %s)''', (email,))

		return not(self.cur.fetchall() == [])
	
	def check_group(self, group):
		self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Group" = %s)''', (group,))

		return not(self.cur.fetchall() == [])

	def check_user_id(self, user_id):
		self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id,))

		return not(self.cur.fetchall() == [])

	def add(self, user_id, f_name, m_name, l_name, group, email):
		if self.check_email(email) or self.check_user_id(user_id):
			return -1

		self.cur.execute('''INSERT INTO "Authenticated_users" ("Tg_ID", "F_name", "M_name", "L_name", "Group", "Points", "Email") VALUES ()''', 
						(user_id, f_name, m_name, l_name, group, 0, email))

		self.conn.commit()
		return 0

	def delete(self, user_id):
		self.cur.execute('''DELETE FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		self.conn.commit()
		return 0

	def add_points(self, user_id, points):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		temp = self.cur.fetchall()[0][6]
		self.cur.execute('''UPDATE "Authenticated_users" SET "Points" = %s where "Tg_ID" = %s''', (temp+points, user_id))
		self.conn.commit()
		return 0

	def remove_points(self, user_id, points):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		temp = self.cur.fetchall()[0][6]
		self.cur.execute('''UPDATE "Authenticated_users" SET "Points" = %s where "Tg_ID" = %s''', (temp-points, user_id))
		self.conn.commit()
		return 0

	def get_users_by_group(self, group):
		if not(self.check_group(group)):
			return -1

		self.cur.execute('''SELECT "Tg_ID" FROM "Authenticated_users" WHERE ("Group" = %s)''', (group, ))
		return [i[0] for i in self.cur.fetchall()]

	def get_info(self, user_id):
		if not(self.check_user_id(user_id)):
			return -1

		self.cur.execute('''SELECT * FROM "Authenticated_users" WHERE ("Tg_ID" = %s)''', (user_id, ))
		return self.cur.fetchall()[0]

	def clear(self):
		self.cur.execute('''DELETE FROM "Authenticated_users"''')
		return 0

unauth_users = Unauthenticated_users()
auth_users = Authenticated_users()

if __name__ == '__main__':
	unauth_users.clear()
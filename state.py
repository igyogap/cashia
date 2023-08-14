from dbinterface import *


class State:
	db = DBInterface()
	idle = 0
	start = 1
	inputName = 2
	inputPhone = 3
	inputSaldoUtama = 4
	inputTransaction = 5
	inputDescriptionTrx = 6
	inputPemasukan = 7
	inputPengeluaran = 8
	getLaporan = 9

	def getState(self, chatid):
		sql = "SELECT state FROM users WHERE chatid = '%s'"% (chatid) 
		result = self.db.queries(sql)
		print (result)
		return result[0]

	def setStateUser(self, chatid, state):
		#check
		check_sql = "SELECT id FROM users WHERE chatid = %s" % (chatid)
		check = self.db.queries(check_sql)
		sql = "update users set state=%s WHERE chatid=%s" % (state, chatid)
		self.db.commands(sql)
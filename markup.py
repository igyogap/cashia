from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from telebot import apihelper
import json

from dbinterface import *

db = DBInterface()
class Markup:

	def confirmName(self, name):
		data = {}
		dataButtonName = []
		dataCallbackData = []
		rowWidth = 2
		markup = InlineKeyboardMarkup()
		markup.row_width = rowWidth
		btnYes = "Ya"
		dataButtonName.append(btnYes)
		btnNo = "Tidak"
		dataButtonName.append(btnNo)
		cbNo = "CONFIRMNAME NO "+ name.replace(" ", "_")
		cbYes = "CONFIRMNAME YES "+ name.replace(" ", "_")
		dataCallbackData.append(cbNo)
		dataCallbackData.append(cbYes)
		markup.add(InlineKeyboardButton(btnNo, callback_data=cbNo), InlineKeyboardButton(btnYes, callback_data=cbYes))
		data['Width'] = rowWidth
		data['ButtonName'] = dataButtonName
		data['CallbackData'] = dataCallbackData
		jsonData = json.dumps(data)
		return markup, jsonData

	def confirmPhone(self, phone):
		data = {}
		dataButtonPhone = []
		dataCallbackData = []
		rowWidth = 2
		markup = InlineKeyboardMarkup()
		markup.row_width = rowWidth
		btnYes = "Ya"
		dataButtonPhone.append(btnYes)
		btnNo = "Tidak"
		dataButtonPhone.append(btnNo)
		cbNo = "CONFIRMPHONE NO "+ phone
		cbYes = "CONFIRMPHONE YES "+ phone
		dataCallbackData.append(cbNo)
		dataCallbackData.append(cbYes)
		markup.add(InlineKeyboardButton(btnNo, callback_data=cbNo), InlineKeyboardButton(btnYes, callback_data=cbYes))
		data['Width'] = rowWidth
		data['ButtonName'] = dataButtonPhone
		data['CallbackData'] = dataCallbackData
		jsonData = json.dumps(data)
		return markup, jsonData

	def confirmTrx(self,cat, trx):
		data = {}
		dataButtonTrx = []
		dataCallbackData = []
		rowWidth = 2
		markup = InlineKeyboardMarkup()
		markup.row_width = rowWidth
		btnYes = "Ya"
		dataButtonTrx.append(btnYes)
		btnNo = "Tidak"
		dataButtonTrx.append(btnNo)
		cbNo = "CONFIRMTRX NO "+cat+" "+ trx
		cbYes = "CONFIRMTRX YES "+cat+" "+ trx
		dataCallbackData.append(cbNo)
		dataCallbackData.append(cbYes)
		markup.add(InlineKeyboardButton(btnNo, callback_data=cbNo), InlineKeyboardButton(btnYes, callback_data=cbYes))
		data['Width'] = rowWidth
		data['ButtonName'] = dataButtonTrx
		data['CallbackData'] = dataCallbackData
		jsonData = json.dumps(data)
		return markup, jsonData
	
	def getCategories(self):
		sql = "SELECT * FROM categories"
		result = db.queries(sql)
		data = {}
		dataButtonName = []
		dataCallbackData = []
		rowWidth = 2
		markup = InlineKeyboardMarkup()
		markup.row_width = rowWidth
		for row in result:
			buttonName = row[1]
			cbData = "CATEGORIES %s" % row[0]
			markup.add(InlineKeyboardButton(buttonName, callback_data=cbData))
			dataButtonName.append(buttonName)
			dataCallbackData.append(cbData)
		data['Width'] = rowWidth
		data['ButtonName'] = dataButtonName
		data['CallbackData'] = dataCallbackData
		jsonData = json.dumps(data)
		return markup, jsonData

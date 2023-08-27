import telebot
import datetime
# import locale
from babel.numbers import format_currency

from dbinterface import *

TOKEN = '6608670146:AAGcW-a8YOWAJQTC0K5glGFybQssSTwdEVU'
bot = telebot.TeleBot(token=TOKEN)
db = DBInterface()

class App:

    def filterInputCharacter(self, text):
        values = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !#$%&()*+,-./:;<=>?@[\]^_{|}~")
        if text != '':
            try:
                text = text.encode('utf-8')
                for character in text:
                    print(character)
                    if character not in values:
                        print(character)
                        text = text.replace(character, "")
                        # print(text)
            except:
                text = ""

        return text

    def sendMessage(self, chatid, text, replyMarkup=None, jsonDataMarkup=None):
        try:
            if replyMarkup is not None:
                message = bot.send_message(chatid, text, reply_markup=replyMarkup, parse_mode='Markdown')
            else:
                message = bot.send_message(chatid, text, parse_mode='Markdown')
        except:
            if replyMarkup is not None:
                message = bot.send_message(chatid, text, reply_markup=replyMarkup, parse_mode='HTML')
            else:
                message = bot.send_message(chatid, text, parse_mode='HTML')
        return message

    def editMessage(self, chatid, messageid, text, replyMarkup=None, jsonDataMarkup=None):
        try:
            if replyMarkup is not None:
                message = bot.edit_message_text(chat_id=chatid, message_id=messageid, text=text, reply_markup=replyMarkup, parse_mode="MARKDOWN")
            else:
                message = bot.edit_message_text(chat_id=chatid, message_id=messageid, text=text, parse_mode="MARKDOWN")
        except:
            if replyMarkup is not None:
                message = bot.edit_message_text(chat_id=chatid, message_id=messageid, text=text, reply_markup=replyMarkup, parse_mode="HTML")
            else:
                message = bot.edit_message_text(chat_id=chatid, message_id=messageid, text=text, parse_mode="HTML")
        # self.insertLogBot(chatid, text, raw_message=message.json, message_id=messageid, button_data=jsonDataMarkup) if jsonDataMarkup is not None else self.insertLogBot(chatid, text, raw_message=message, message_id=messageid)
        return message

    def getMessage(self, idMessage):
        sql = "SELECT text FROM message WHERE id = '%s'" % (idMessage)
        result = db.queries(sql)
        if len(result) > 0:
            return str(result[0][0])

    def insertGuest(self,chatid):
        sql = "INSERT INTO guest(chatid) VALUES ('%s')"% (chatid)
        db.commands(sql)

    def insertUser(self, chatid):
        sql = "SELECT * FROM users WHERE chatid = '%s'"% (chatid)
        result = db.queries(sql)
        if len(result) == 0:
            sql = "INSERT INTO users(chatid) VALUES ('%s')"% (chatid)
            db.commands(sql)

    def updateName(self, chatid, name):
        sql = "UPDATE users SET nama = '%s' WHERE chatid = '%s'"% (name, chatid)
        db.commands(sql)

    def updatePhone(self, chatid, phone):
        sql = "UPDATE users SET phone = '%s' WHERE chatid = '%s'"% (phone, chatid)
        db.commands(sql)

    def userActive(self, chatid):
        sql = "UPDATE users SET is_active = '1' WHERE chatid = '%s'"% (chatid)
        db.commands(sql)

    def cekUser(self, chatid):
        found = False
        results =""
        sql = "SELECT * FROM users WHERE chatid='%s' AND is_active ='1'" % str(chatid)
        results = db.queries(sql)
        
        if len(results) > 0 :
            found = True
        else:
            found = False
        return results, found

    # TRANSACTION
    def inputTransaction(self, chatid, cat_id, trx):
        sql = "SELECT id FROM users WHERE chatid = '%s'"%(chatid)
        user_id = db.queries(sql)
        sql = "INSERT INTO transaction(user_id, cat_id, trx) VALUES ('%s','%s','%s' )"%(user_id[0][0], cat_id, trx)
        db.commands(sql)

    def inputDescriptionTransaction(self, chatid, desc):
        sql = "SELECT MAX(a.id) FROM transaction a LEFT JOIN users b ON a.user_id = b.id WHERE b.chatid = '%s'"%(chatid)
        results = db.queries(sql)
        id_trx = results[0][0]
        sql = "UPDATE transaction SET description = '%s' WHERE id='%s'"%(desc, id_trx)
        db.commands(sql)
    
    def getKas(self, chatid):
        dataUser, found = self.cekUser(chatid)
        id_user = dataUser[0][0]
        sql = "SELECT SUM(CASE WHEN cat_id = '1' THEN trx ELSE 0 END) AS pemasukan, SUM(CASE WHEN cat_id ='2' THEN trx ELSE 0 END) AS pengeluaran FROM `transaction` WHERE user_id = '%s'"%(id_user)
        result = db.queries(sql)
        if len(result) > 0:
            total_kas=int(float(result[0][0])- float(float(result[0][1])))
        else:
            total_kas = 0
        return total_kas

    def format_rupiah(self, amount):
        formatted_amount = format_currency(amount, 'IDR', locale='id_ID')

        return formatted_amount
# Close function Apps
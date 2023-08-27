from app import *
from state import *
from markup import *
markup = Markup()
state = State()
app =App()
DEBUG_MODE = True

def debugFunction(text):
    if DEBUG_MODE:
        print (str(text))
# Command
@bot.message_handler(commands=['start'])
def start(message):
    chatid = str(message.from_user.id)
    users, found = app.cekUser(chatid)
    userState = str(state.getState(chatid)[0])
    if found:
        if userState == str(state.inputSaldoUtama):
            text = "Silahkan masukan saldo utama kamu"
            app.sendMessage(chatid,text)
        else:
            text = app.getMessage('7')
            markupConfirm, jsonData = markup.getCategories()
            app.sendMessage(chatid, text,markupConfirm, jsonData)
    else:
        app.insertGuest(chatid)
        app.insertUser(chatid)
        text = app.getMessage('1')
        app.sendMessage(chatid, text)
        state.setStateUser(chatid, state.inputName)
        
        
# close command

# Message Handler
@bot.message_handler(func=lambda message: True)
def response_chat(message):
    if message.chat.type == "private":
        chatid = str(message.chat.id)
        inputTextUser = message.text
        userState = str(state.getState(chatid)[0])

        if userState == str(state.inputName):
            name = inputTextUser
            markupConfirm, jsonData = markup.confirmName(inputTextUser)
            text = app.getMessage('2') %(inputTextUser)
            userInput = str(inputTextUser)
            app.sendMessage(chatid, text, markupConfirm, jsonData)

        elif userState == str(state.inputPhone):
            markupConfirm, jsonData = markup.confirmPhone(inputTextUser)
            text = app.getMessage('3')%(inputTextUser)
            userInput = str(inputTextUser)
            app.sendMessage(chatid, text, markupConfirm, jsonData)

        elif userState == str(state.inputSaldoUtama):
            app.inputTransaction(chatid, '1', inputTextUser)
            app.inputDescriptionTransaction(chatid, "Saldo Utama")
            nominal =app.format_rupiah(int(inputTextUser))
            text = app.getMessage('8')%(nominal)
            app.sendMessage(chatid, text)
            state.setStateUser(chatid, state.idle)

        elif userState == str(state.inputPemasukan):
            markupConfirm, jsonData = markup.confirmTrx('1', inputTextUser)
            text = "Apakah transaksi yang anda masukan sebesar "+ str(inputTextUser)
            app.sendMessage(chatid, text, markupConfirm, jsonData)

        elif userState == str(state.inputPengeluaran):
            markupConfirm, jsonData = markup.confirmTrx('2',inputTextUser)
            text = "Apakah transaksi yang anda masukan sebesar "+ str(inputTextUser)
            app.sendMessage(chatid, text, markupConfirm, jsonData)

        elif userState == str(state.inputDescriptionTrx):
            app.inputDescriptionTransaction(chatid, inputTextUser)
            kas = app.getKas(chatid)
            kas_rupiah = app.format_rupiah(kas)
            text = app.getMessage('12')%(kas_rupiah)
            app.sendMessage(chatid, text)
            state.setStateUser(chatid, state.idle)
            


@bot.callback_query_handler(func=lambda call: True)
def response_button(call):
    chatid = str(call.from_user.id)
    buttonData = call.data
    debugFunction(buttonData)
    menu = buttonData.split()
    messageID = call.message.message_id
    
    if len(menu) == 1:
        # step confirm name
        print("test")
    else:
        cbButton = menu[0]
        if cbButton == "CONFIRMNAME":
            if menu[1] == "YES":
                name = menu[2].replace("_", " ")
                app.updateName(chatid, name)
                text = app.getMessage('4')
                app.editMessage(chatid,messageID,text)
                state.setStateUser(chatid, state.inputPhone)
            else:
                text = app.getMessage('5')
                app.editMessage(chatid, messageID, text)

        elif cbButton == "CONFIRMPHONE":
            if menu[1] == "YES":
                phone = menu[2]
                app.updatePhone(chatid, phone)
                app.userActive(chatid)
                text = app.getMessage('7')
                app.editMessage(chatid,messageID,text)
                state.setStateUser(chatid, state.inputSaldoUtama)
            else:
                text = app.getMessage('6')
                app.editMessage(chatid,messageID,text)
                state.setStateUser(chatid, state.inputPhone)

        elif cbButton == "CATEGORIES":
            if menu[1] == "1":
                text = app.getMessage('9')% ("pemasukan")
                app.editMessage(chatid,messageID, text)
                text = app.getMessage('10')% ("pemasukan")
                app.sendMessage(chatid,text)
                state.setStateUser(chatid, state.inputPemasukan)
            elif menu[1] == "2":
                text = app.getMessage('9')% ("pengeluaran")
                app.editMessage(chatid,messageID, text)
                text = app.getMessage('10')% ("pengeluaran")
                app.sendMessage(chatid,text)
                state.setStateUser(chatid, state.inputPengeluaran)
            else:
                app.editMessage(chatid,messageID,"Fitur Belum Tersedia")

        elif cbButton == "CONFIRMTRX":
            if menu[1] == "YES":
                if menu[2] == "1":
                    trx = menu[3]
                    app.inputTransaction(chatid, '1', trx)
                    text = app.getMessage('11')% ("pemasukan")
                    app.editMessage(chatid, messageID,text)
                    state.setStateUser(chatid, state.inputDescriptionTrx)
                else:
                    trx = menu[3]
                    app.inputTransaction(chatid, '2', trx)
                    text = app.getMessage('11')% ("pengeluaran")
                    app.editMessage(chatid, messageID,text)
                    state.setStateUser(chatid, state.inputDescriptionTrx)
            else:
                if menu[2] == "1":
                    text = app.getMessage('10')% ("pemasukan")
                    app.editMessage(chatid,messageID,text)
                    state.setStateUser(chatid, state.inputPemasukan)
                else:
                    text = app.getMessage('10')% ("pengeluaran")
                    app.editMessage(chatid,messageID,text)
                    state.setStateUser(chatid, state.inputPengeluaran)
# BOT Run
bot.polling(True)
    

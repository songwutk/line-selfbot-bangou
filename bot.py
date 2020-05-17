# -*-coding: utf-8 -*-
from Linephu.linepy import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import requests
from bs4 import BeautifulSoup
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, timeit
from gtts import gTTS
from googletrans import Translator
#==============================================================================#
botStart = time.time()
cl = LINE("")

#ki = LINE()
#ki.log("Auth Token : " + str(ki.authToken))

#k1 = LINE()
#k1.log("Auth Token : " + str(k1.authToken))

#k2 = LINE()
#k2.log("Auth Token : " + str(k2.authToken))

clMID = cl.profile.mid
#AMID = ki.profile.mid
#BMID = k1.profile.mid
#CMID = k2.profile.mid

#KAC = [cl,ki,k1,k2]
#Bots = [clMID,AMID,BMID,CMID]

clProfile = cl.getProfile()
#kiProfile = ki.getProfile()
#k1Profile = k1.getProfile()
#k2Profile = k2.getProfile()
lineSettings = cl.getSettings()
#kiSettings = ki.getSettings()
#k1Settings = k1.getSettings()
#k2Settings = k2.getSettings()

oepoll = OEPoll(cl)
#oepoll1 = OEPoll(ki)
#oepoll2 = OEPoll(k1)
#oepoll3 = OEPoll(k2)
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
banOpen = codecs.open("ban.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)
ban = json.load(banOpen)

msg_dict = {}
bl = [""]

#==============================================================================#
####################################################
mulai = time.time()
####################################################
def Runtime(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours, 24)
    return '%02d 天\n%02d 小時\n%02d 分鐘\n%02d 秒\n以上為半垢運行時間\n半垢 運行時間測試' % (days, hours, mins, secs)
def Runtimeself(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours, 24)
    return '%02d天%02d小時%02d分鐘%02d秒' % (days, hours, mins, secs)
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = ban
        f = codecs.open('ban.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
def logError(text):
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = ""
    if mids == []:
        raise Exception("Invaliod mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
            textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    cl.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
def helpmessage():
    helpMessage = """—〘 指令分類 〙—
【Sn:Help】 Command Help 查看指令面板
【Help1】 System Comm. 查看系統指令
【Help2】 Machine settings. 查看機器設定
【Help3】 Information. 查看資料訊息
【Help4】 Blacklist func. 查看黑單功能
【Help5】 Group func. 查看群組功能
【Help6】 Other features. 查看其他功能
【Help7】 kick func. 查看踢人功能
【Help8】 Invite feature. 查看邀請功能
— Thanks for use〘無名半垢感謝使用 〙—"""
    return helpMessage
def helpmessagebot():
    helpMessageBOT = """♨━狀態━♨
 Restart 重新啟動
 Save 儲存設定
 Runtime 運作時間
 Speed 速度
 /Sp 統整速度
 Set 設定
 About 關於本帳"""
    return helpMessageBOT
def helpmessageset():
    helpMessageSET = """♨━設定━♨
 Add On/Off 自動加友
 Join On/Off 自動進群
 Leave On/Off 離開副本
 Read On/Off 自動已讀
 Share On/Off 權限公開
 Game On/Off 遊戲開啟
 sl On/Off 入群通知
 sj On/Off 退群通知
 kc On/Off 踢人通知
 ReRead On/Off 查詢收回
 Pro On/Off 所有保護
 pr On/Off 踢人保護
 qr On/Off 網址保護
 ip On/Off 邀請保護
 Getmid On/Off 取得mid
 Detect On/Off 標註偵測
 Timeline On/Off 文章網址 """
    return helpMessageSET
def helpmessageme():
    helpMessageME = """♨━資訊━♨
 Me 我的連結
 MyMid 我的mid
 MyName 我的名字
 MyBio 個簽
 MyPicture 我的頭貼
 myvid 我的影片
 MyCover 我的封面
 Contact @ 標註取得連結
 Mid @ 標註查mid
 Name @ 查看名字"""
    return helpMessageME
def helpmessageban():
    helpMessageBAN = """♨━權黑指令━♨
 addop @ 新增權限
 delop @ 刪除權限
 Ban @ 加入黑單
 Unban @ 取消黑單
 Nkban 踢除黑單
 CleanBan 清空黑單
 oplist 查看權限表
 Banlist 查看黑單"""
    return helpMessageBAN
def helpmessagegrp():
    helpMessageGRP = """♨━群組━♨
 Group 創群者
 GroupId 群組ID
 GroupName 群組名稱
 GroupPicture 群組圖片
 GroupLink 群組網址
 Link On/Off網址開/關
 Lg 所有群組列表
 Gb 成員名單
 Ginf 群組資料
 Gn (文字) 更改群名
 Cancel 取消所有邀請"""
    return helpMessageGRP
def helpmessageatl():
    helpMessageATL = """♨━其他━♨
 Tagall 標註全體
 Zc 發送0字元友資
 SR 已讀點設置
 CR 取消偵測
 LR 已讀偵測"""
    return helpMessageATL
def helpmessagemin():
    helpMessageMIN = """♨━踢人━♨
 Nk Kick alot.@ 單、多踢
 Zk Kick all. 踢出0字元
 Byeall翻群
 Ri @ 來回機票"""
    return helpMessageMIN
def helpmessageadd():
    helpMessageADD = """♨━邀請━♨
 Botsadd Join invit. @ 加入自動邀請
 Botsdel Cancel invit. @ 取消自動邀請
 Botslist Inv list. 自動邀請表
 Join 自動邀請
 Inv (mid) 透過mid邀請
 Inv @ 標註多邀"""
    return helpMessageADD
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

admin=[]
owners=["","",clMID]
#if clMID not in owners:
#    python = sys.executable
#    os.execl(python, python, *sys.argv)
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                cl.sendMessage(op.param1, "Thanks for add me friend.感謝您加我為好友w".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 1:
            print ("[ 1 ] 個簽鎖定")
            if cl.getProfile().mid != admin:
                if op.param1 == "16":
                    _name = "✎﹏ Anonymous bot running 無名 Bøt 運行中...\n\n"
                    _name += "✔ʙᴏᴛ ʀᴜɴɴɪɴɢ.....\n\n"
                    _name += "✔已運行③⑨ʜʀ...\n\n"
                    _name += "✔ʙᴏᴛ ʀᴜɴɴɪɴɢᴀ ᴇᴠᴇʀᴅᴀʏ....\n\n"
                    _name += "使用者：UNKNOWN\n\n"
                    _name += "✔Line : \n\n"
                    contact = cl.getProfile()
                    status = contact.statusMessage
                    if _name not in  cl.getProfile().statusMessage:
                        profile = cl.getProfile()
                        profile.statusMessage =  _name + status
                        cl.updateProfile(profile)
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            if settings["qrprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"]:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            if clMID in op.param3:
                group = cl.getGroup(op.param1)
                if settings["autoJoin"] == True:
                    cl.acceptGroupInvitation(op.param1)
                    cl.sendMessage(op.param1,"☰☱☲☳ Auto join group 自動入群☴☵☶☷\nSilent Bøt自動入群\n使用者：錒勛\nline://au/q/Ol8azIc66Lc29GyUwKEEhzAus3S5bvnW\n☰☱☲☳通知完畢☴☵☶☷")
            elif settings["invprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"]:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1,[op.param3])
            else:
                group = cl.getGroup(op.param1)
                gInviMids = []
                for z in group.invitee:
                    if z.mid in ban["blacklist"]:
                        gInviMids.append(z.mid)
                if gInviMids == []:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1, gInviMids)
                    cl.sendMessage(op.param1,"Invitee Black List. 被邀請者黑單中...")
        if op.type == 15:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            if settings["seeLeave"] == True:
                try:
                    arrData = ""
                    text = "%s "%('默哀 ')
                    arr = []
                    mention = "@x "
                    slen = str(len(text))
                    elen = str(len(text) + len(mention) - 1)
                    arrData = {'S':slen, 'E':elen, 'M':op.param2}
                    arr.append(arrData)
                    text += mention + "\n水煮蛋變成茶葉蛋了ಥ_ಥ"
                    cl.sendMessage(op.param1,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                except Exception as error:
                    print(error)
        if op.type == 17:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            if settings["seeJoin"] == True:
                try:
                    arrData = ""
                    text = "%s "%('歡迎')
                    arr = []
                    mention = "@x "
                    slen = str(len(text))
                    elen = str(len(text) + len(mention) - 1)
                    arrData = {'S':slen, 'E':elen, 'M':op.param2}
                    arr.append(arrData)
                    text += mention + "\n加入群組 ヾ(＾∇＾) "
                    cl.sendMessage(op.param1,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                except Exception as error:
                    print(error)
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            contact2 = cl.getContact(op.param3)
            if settings["protect"] == True:
                if op.param2 in admin:
                    pass
                else:
                    if settings["kickContact"] == True:
                        try:
                            arrData = ""
                            text = "%s " %('')
                            arr = []
                            mention1 = "@arasi "
                            slen = str(len(text))
                            elen = str(len(text) + len(mention1) - 1)
                            arrData = {'S':slen, 'E':elen, 'M':op.param2}
                            arr.append(arrData)
                            text += mention1 + '把 '
                            mention2 = "@kick "
                            sslen = str(len(text))
                            eelen = str(len(text) + len(mention2) - 1)
                            arrdata = {'S':sslen, 'E':eelen, 'M':op.param3}
                            arr.append(arrdata)
                            text += mention2 + '\n拖出去煎了Σ(･口･)'
                            cl.kickoutFromGroup(op.param1,[op.param2])
                            settings["blacklist"][op.param2] = True
                            cl.sendMessage(op.param1,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                        except Exception as error:
                            print(error)
                    else:
                        cl.kickoutFromGroup(op.param1,[op.param2])
                        settings["blacklist"][op.param2] = True
            else:
                if settings["kickContact"] == True:
                    try:
                        arrData = ""
                        text = "%s " %('')
                        arr = []
                        mention1 = "@arasi "
                        slen = str(len(text))
                        elen = str(len(text) + len(mention1) - 1)
                        arrData = {'S':slen, 'E':elen, 'M':op.param2}
                        arr.append(arrData)
                        text += mention1 + '把 '
                        mention2 = "@kick "
                        sslen = str(len(text))
                        eelen = str(len(text) + len(mention2) - 1)
                        arrdata = {'S':sslen, 'E':eelen, 'M':op.param3}
                        arr.append(arrdata)
                        text += mention2 + '\n拖出去煎了Σ(･口･)'
                        cl.sendMessage(op.param1,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                    except Exception as error:
                        print(error)
                else:
                     pass
        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 25 or op.type == 26:
            K0 = admin
            msg = op.message
            if settings["share"] == True:
                K0 = msg._from
            else:
                K0 = admin
#        if op.type == 25 :
#            if msg.toType ==2:
#                g = cl.getGroup(op.message.to)
#                print ("sended:".format(str(g.name)) + str(msg.text))
#            else:
#                print ("sended:" + str(msg.text))
#        if op.type == 26:
#            msg =op.message
#            pop = cl.getContact(msg._from)
#            print ("replay:"+pop.displayName + ":" + str(msg.text))
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in sender:
                if text.lower() == '遊戲':        
                    if settings["newGame"] == True:
                        cl.sendReplyMessage(msg.id, to,"[遊戲內容]\n\n》猜拳《\n\n》運勢《\n\n[感謝使用]")
            if sender in sender:
                if text.lower() == '運勢':        
                    if settings["newGame"] == True:
                        data = random.choice(['[運勢結果]\n小吉～有點手氣！','[運勢結果]\n末吉～運氣可以^_^','[運勢結果]\n兇～有點不好...','[運勢結果]\n大兇～慘了慘了...','[運勢結果]\n大吉～手氣旺旺！'])
                        cl.sendReplyMessage(msg.id, to,str(data))
            if sender in sender:
                if text.lower() == '猜拳':
                    if settings["newGame"] == True:
                        cl.sendReplyMessage(msg.id, to, "[猜拳遊戲]\n輸入：\n剪刀，石頭，布\n\n來一決高下吧！")
            if sender in sender:
                if text.lower() == '剪刀':        
                    if settings["newGame"] == True:
                        data = random.choice(['[猜拳結果]\n你出剪刀✌\n我出石頭👊\n\n👻你輸了！👻','[猜拳結果]\n你出剪刀✌\n我出布✋\n\n🎉你贏了！🎉','[猜拳結果]\n你出剪刀✌\n我出剪刀✌\n\n👏平手！👏'])
                        cl.sendReplyMessage(msg.id, to,str(data))
            if sender in sender:
                if text.lower() == '石頭':        
                    if settings["newGame"] == True:
                        data = random.choice(['[猜拳結果]\n你出石頭👊\n我出石頭👊\n\n👏平手！👏','[猜拳結果]\n你出石頭👊\n我出布✋\n\n👻你輸了！👻','[猜拳結果]\n你出石頭👊\n我出剪刀✌\n\n🎉你贏了！🎉'])
                        cl.sendReplyMessage(msg.id, to,str(data))  
            if sender in sender:
                if text.lower() == '布':        
                    if settings["newGame"] == True:
                        data = random.choice(['[猜拳結果]\n你出布✋\n我出石頭\n\n🎉你贏了！🎉','[猜拳結果]\n你出布✋\n我出布✋\n\n👏平手！👏','[猜拳結果]\n你出布✋\n我出剪刀✌\n\n👻你輸了！👻'])
                        cl.sendReplyMessage(msg.id, to,str(data))
                
#==============================================================================#
            if sender in K0 or sender in owners:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendReplyMessage(msg.id, to, str(helpMessage))
                if text.lower() == 'help1':
                    helpMessageBOT = helpmessagebot()
                    cl.sendReplyMessage(msg.id, to, str(helpMessageBOT))
                if text.lower() == 'help2':
                    helpMessageSET = helpmessageset()
                    cl.sendReplyMessage(msg.id, to, str(helpMessageSET))
                if text.lower() == 'help3':
                    helpMessageME = helpmessageme()
                    cl.sendReplyMessage(msg.id, to, str(helpMessageME))
                if text.lower() == 'help4':
                    helpMessageBAN = helpmessageban()
                    cl.sendReplyMessage(msg.id, to, str(helpMessageBAN))
                if text.lower() == 'help5':
                    helpMessageGRP = helpmessagegrp()
                    cl.sendReplyMessage(msg.id, to, str(helpMessageGRP))
                if text.lower() == 'help6':
                    helpMessageATL = helpmessageatl()
                    cl.sendReplyMessage(msg.id, to, str(helpMessageATL))
                if text.lower() == 'help7':
                    helpMessageMIN = helpmessagemin()
                    cl.sendReplyMessage(msg.id, to, str(helpMessageMIN))
                if text.lower() == 'help8':
                    helpMessageADD = helpmessageadd()
                    cl.sendReplyMessage(msg.id, to, str(helpMessageADD))
            
#==============================================================================#
                elif text.lower() == 'spt':
                    cl.sendReplyMessage(msg.id, to,"結果約為\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=100)) + "秒")
                elif text.lower() == '/sp':
                    ret_ = "［ 反應速度 ］"
                    ret_ += "\n第一次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n第二次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n第三次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n第四次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n第五次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n［ 處理速度 ］"
                    ret_ += "\n第一次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n第二次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n第三次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n第四次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n第五次:\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000))
                    ret_ += "\n［ 以上是速度測試 ］"
                    cl.sendReplyMessage(msg.id, to, str(ret_))
                elif text.lower() == 'sp':
                    cl.sendReplyMessage(msg.id, to,"Find results. 查詢結果\n"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000)) + "秒")
                elif text.lower() == 'save':
                    backupData()
                    cl.sendReplyMessage(msg.id, to,"Storage is successful. 儲存設定成功!")
                elif text.lower() == 'restart':
                    cl.sendReplyMessage(msg.id, to, "重新啟動中...")
                    time.sleep(5)
                    cl.sendReplyMessage(msg.id, to, "重新啟動成功\n\n重新啟動版本《V2.0》")
                    restartBot()
                elif text.lower() == 'runtime':
                    eltime = time.time() - mulai
                    bot = "運行時間長達\n" + Runtime(eltime)
                    cl.sendReplyMessage(msg.id, to,bot)    
                elif "cp:" in msg.text:
                    path = text.replace("cp:","")
                    cl.updateProfilePicture(path)    
                elif "youtube:" in msg.text:
                    number = text.replace("youtube:","")
                    url = "https://m.youtube.com/results?search_query={}".format(number)
                    request = requests.get(url)
                    content = request.content
                    soup = BeautifulSoup(content, "html.parser")
                    ret_ = "—YouTube search result 搜尋結果—"
                    no = 0 + 1
                    for all_mv in soup.select(".yt-lockup-video"):
                         name = all_mv.select("a[rel='spf-prefetch']")
                         ret_ += "\n\n =====[ {} ]====={}\n\n https://www.youtube.com{}".format(str(no), str(name[0].get("title")), str(name[0].get("href")))
                         no += 1
                    cl.sendReplyMessage(msg.id, to, str(ret_))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner =""
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        clProfile = cl.getProfile()
                        clSetting = cl.getSettings()
                        eltime = time.time() - mulai
                        timeNow = datetime.now()
                        timE = datetime.strftime(timeNow,"%H:%M:%S")
                        bot = "" + Runtimeself(eltime)
                        ret_ = "☰☱☲☳帳號名稱☴☵☶☷"
                        ret_ += "\n【{}】".format(contact.displayName)
                        ret_ += "\n☰☱☲☳帳號MID.☴☵☶☷"
                        ret_ += "\n【{}】".format(contact.mid)
                        ret_ += "\n☰☱☲☳帳號資訊☴☵☶☷"
                        ret_ += "\n 群組數 : 【{}】".format(str(len(grouplist)))
                        ret_ += "\n 好友數 : 【{}】".format(str(len(contactlist)))
                        ret_ += "\n 已封鎖 : 【{}】".format(str(len(blockedlist)))
                        ret_ += "\n☰☱☲☳輔助設定☴☵☶☷"
                        if settings["autoAdd"] == True: ret_ += "\n 自動加友 ✅"
                        else: ret_ += "\n 自動加友 ❌"
                        if settings["autoJoin"] == True: ret_ += "\n 自動入群 ✅"
                        else: ret_ += "\n 自動入群 ❌"
                        if settings["autoLeave"] == True: ret_ += "\n 自離副本 ✅"
                        else: ret_ += "\n 自離副本 ❌"
                        if settings["autoRead"] == True: ret_ += "\n 自動已讀 ✅"
                        else: ret_ += "\n 自動已讀 ❌"
                        if settings["newGame"] ==True: ret_+="\n 遊戲公開 ✅"
                        else: ret_ += "\n 遊戲公開 ❌"
                        ret_ += "\n☰☱☲☳通知設定☴☵☶☷"
                        if settings["seeJoin"] == True: ret_ += "\n 入群通知 ✅"
                        else: ret_ += "\n 入群通知 ❌"
                        if settings["poilfe"] == True: ret_ += "\n 入群頭貼 ✅"
                        else: ret_ += "\n 入群頭貼 ❌"
                        if settings["seeLeave"] == True: ret_ += "\n 退群通知 ✅"
                        else: ret_ += "\n 退群通知 ❌"
                        if settings["kickContact"] == True: ret_ += "\n 踢人通知 ✅"
                        else: ret_ += "\n 踢人通知 ❌"
                        ret_ += "\n☰☱☲☳關於作者☴☵☶☷"
                        ret_ += "\n 使用者 : 無名"
                        ret_ += "\n 作者I'd：你不配"
                        ret_ += "\n 作者網址：\n擊敗你不配"
                        ret_ += "\n☰☱☲☳關於bot☴☵☶☷"
                        ret_ += "\n 版本 : 【半垢v1.0】"
                        ret_ += "\n 預備線程數 : 【10】"
                        ret_ += "\n 連線線程數 : 【1】"
                        ret_ += "\n 半垢反應速度：\n【{}】".format(str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000)))
                        ret_ += "\n 運行時間長達：\n【{}】".format(str(bot))
                        ret_ += "\n 查詢時間：【{}】".format(str(timE))
                        ret_ += "\n☰☱☲☳作者友資☴☵☶☷"
                        cl.sendReplyMessage(msg.id, to, str(ret_))
                        cl.sendContact(to, "u3d07fc517427da2f8dff71630873ee4f")
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == 'set':
                    try:
                        ret_ = "[ 狀態 ]"
                        if settings["autoAdd"] == True: ret_ += "\n 自動加友 ✅"
                        else: ret_ += "\n 自動加友 ❌"
                        if settings["autoJoin"] == True: ret_ += "\n 自動入群 ✅"
                        else: ret_ += "\n 自動入群 ❌"
                        if settings["autoLeave"] == True: ret_ += "\n 自離副本 ✅"
                        else: ret_ += "\n 自離副本 ❌"
                        if settings["autoRead"] == True: ret_ += "\n 自動已讀 ✅"
                        else: ret_ += "\n 自動已讀 ❌"
                        if settings["protect"] ==True: ret_+="\n 群組保護 ✅"
                        else: ret_ += "\n 群組保護 ❌"
                        if settings["qrprotect"] ==True: ret_+="\n 網址保護 ✅"
                        else: ret_ += "\n 網址保護 ❌"
                        if settings["invprotect"] ==True: ret_+="\n 邀請保護 ✅"
                        else: ret_ += "\n 邀請保護 ❌"
                        if settings["detectMention"] ==True: ret_+="\n 標註回覆 ✅"
                        else: ret_ += "\n 標註回覆 ❌"
                        if settings["reread"] ==True: ret_+="\n 查詢收回 ✅"
                        else: ret_ += "\n 查詢收回 ❌"
                        if settings["seeJoin"] == True: ret_ += "\n 入群通知 ✅"
                        else: ret_ += "\n 入群通知 ❌"
                        if settings["poilfe"] == True: ret_ += "\n 入群頭貼 ✅"
                        else: ret_ += "\n 入群頭貼 ❌"
                        if settings["seeLeave"] == True: ret_ += "\n 退群通知 ✅"
                        else: ret_ += "\n 退群通知 ❌"
                        if settings["kickContact"] == True: ret_ += "\n 踢人通知 ✅"
                        else: ret_ += "\n 踢人通知 ❌"
                        if settings["newGame"] ==True: ret_+="\n 遊戲公開 ✅"
                        else: ret_ += "\n 遊戲公開 ❌"
                        if settings["share"] ==True: ret_+="\n 權限公開 ✅"
                        else: ret_ += "\n 權限公開 ❌"
                        ret_ += "\n[ Finish ]"
                        cl.sendReplyMessage(msg.id, to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'add on':
                    settings["autoAdd"] = True
                    cl.sendReplyMessage(msg.id, to, "自動加入好友已開啟")
                elif text.lower() == 'add off':
                    settings["autoAdd"] = False
                    cl.sendReplyMessage(msg.id, to, "自動加入好友已關閉")
                elif text.lower() == 'join on':
                    settings["autoJoin"] = True
                    cl.sendReplyMessage(msg.id, to, "自動加入群組已開啟")
                elif text.lower() == 'join off':
                    settings["autoJoin"] = False
                    cl.sendReplyMessage(msg.id, to, "自動加入群組已關閉")
                elif text.lower() == 'leave on':
                    settings["autoLeave"] = True
                    cl.sendReplyMessage(msg.id, to, "自動離開副本已開啟")
                elif text.lower() == 'leave off':
                    settings["autoLeave"] = False
                    cl.sendReplyMessage(msg.id, to, "自動離開副本已關閉")
                elif text.lower() == 'read on':
                    settings["autoRead"] = True
                    cl.sendReplyMessage(msg.id, to, "自動已讀已開啟")
                elif text.lower() == 'read off':
                    settings["autoRead"] = False
                    cl.sendReplyMessage(msg.id, to, "自動已讀已關閉")
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendReplyMessage(msg.id, to, "查詢收回開啟")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendReplyMessage(msg.id, to, "查詢收回關閉")
                elif text.lower() == 'pr on':
                    settings["protect"] = True
                    cl.sendReplyMessage(msg.id, to, "踢人保護開啟")
                elif text.lower() == 'pr off':
                    settings["protect"] = False
                    cl.sendReplyMessage(msg.id, to,"踢人保護關閉")
                elif text.lower() == 'game on':
                    settings["newGame"] = True
                    cl.sendReplyMessage(msg.id, to, "已開啟遊戲")
                elif text.lower() == 'game off':
                    settings["newGame"] = False
                    cl.sendReplyMessage(msg.id, to, "已關閉遊戲")
                elif text.lower() == 'share on':
                    settings["share"] = True
                    cl.sendReplyMessage(msg.id, to, "已開啟分享")
                elif text.lower() == 'share off':
                    settings["share"] = False
                    cl.sendReplyMessage(msg.id, to, "已關閉分享")
                elif text.lower() == 'detect on':
                    settings["detectMention"] = True
                    cl.sendReplyMessage(msg.id, to, "已開啟標註偵測")
                elif text.lower() == 'detect off':
                    settings["detectMention"] = False
                    cl.sendReplyMessage(msg.id, to, "已關閉標註偵測")
                elif text.lower() == 'qr on':
                    settings["qrprotect"] = True
                    cl.sendReplyMessage(msg.id, to, "網址保護開啟")
                elif text.lower() == 'qr off':
                    settings["qrprotect"] = False
                    cl.sendReplyMessage(msg.id, to, "網址保護關閉")
                elif text.lower() == 'ip on':
                    settings["invprotect"] = True
                    cl.sendReplyMessage(msg.id, to, "邀請保護開啟")
                elif text.lower() == 'ip off':
                    settings["invprotect"] = False
                    cl.sendReplyMessage(msg.id, to, "邀請保護關閉")
                elif text.lower() == 'getmid on':
                    settings["getmid"] = True
                    cl.sendReplyMessage(msg.id, to, "mid獲取開啟")
                elif text.lower() == 'getmid off':
                    settings["getmid"] = False
                    cl.sendReplyMessage(msg.id, to, "mid獲取關閉")
                elif text.lower() == 'timeline on':
                    settings["timeline"] = True
                    cl.sendReplyMessage(msg.id, to, "文章預覽開啟")
                elif text.lower() == 'timeline off':
                    settings["timeline"] = False
                    cl.sendReplyMessage(msg.id, to, "文章預覽關閉")
                elif text.lower() == 'sj on':
                    settings["seeJoin"] = True
                    cl.sendReplyMessage(msg.id, to, "入群通知已開啟")
                elif text.lower() == 'sj off':
                    settings["seeJoin"] = False
                    cl.sendReplyMessage(msg.id, to, "入群通知已關閉")
                elif text.lower() == 'sp on':
                    settings["poilfe"] = True
                    cl.sendReplyMessage(msg.id, to, "入群頭貼已開啟")
                elif text.lower() == 'sp off':
                    settings["poilfe"] = False
                    cl.sendReplyMessage(msg.id, to, "入群頭貼已關閉")
                elif text.lower() == 'sl on':
                    settings["seeLeave"] = True
                    cl.sendReplyMessage(msg.id, to, "退群通知已開啟")
                elif text.lower() == 'sl off':
                    settings["seeLeave"] = False
                    cl.sendReplyMessage(msg.id, to, "退群通知已關閉")
                elif text.lower() == 'kc on':
                    settings["kickContact"] = True
                    cl.sendReplyMessage(msg.id, to, "踢人標註已開啟")
                elif text.lower() == 'kc off':
                    settings["kickContact"] = False
                    cl.sendReplyMessage(msg.id, to, "踢人標註已關閉")
                elif text.lower() == 'pro on':
                    settings["protect"] = True
                    settings["qrprotect"] = True
                    settings["invprotect"] = True
                    cl.sendMessage(to, "踢人保護開啟")
                    cl.sendMessage(to, "網址保護開啟")
                    cl.sendMessage(to, "邀請保護開啟")
                elif text.lower() == 'pro off':
                    settings["protect"] = False
                    settings["qrprotect"] = False
                    settings["invprotect"] = False
                    cl.sendMessage(to, "踢人保護關閉")
                    cl.sendMessage(to, "網址保護關閉")
                    cl.sendMessage(to, "邀請保護關閉")
#==============================================================================#
                elif msg.text.lower().startswith("addop "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    admin.append(str(inkey))
                    cl.sendReplyMessage(msg.id, to, "已獲得權限！")
                elif msg.text.lower().startswith("delop "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    admin.remove(str(inkey))
                    cl.sendReplyMessage(msg.id, to, "已取消權限！")
                elif text.lower() == 'oplist':
                    if admin == []:
                        cl.sendReplyMessage(msg.id, to,"無擁有權限者!")
                    else:
                        mc = "[ Admin List ]"
                        for mi_d in admin:
                            mc += "\n ➥"+cl.getContact(mi_d).displayName
                        cl.sendReplyMessage(msg.id, to,mc + "\n[ Finish ]")
                elif msg.text.lower().startswith("invite "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    G = cl.getGroup
                    cl.inviteIntoGroup(to,targets)
                elif ("Say " in msg.text):
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        cl.sendMessage(to,x[1])
                elif msg.text.lower().startswith("tag "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        sendMessageWithMention(to, inkey)
                elif ("Rex " in msg.text):
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        cl.sendReplyMessage(msg.id, to,x[1])
                elif msg.text.lower().startswith("mex "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        cl.sendReplyMessage(msg.id, to, inkey)
                elif msg.text.lower().startswith("tex "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    x = text.split(' ',2)
                    c = int(x[2])
                    for c in range(c):
                        cl.sendReplyMessageWithMention(msg.id, to, inkey)
                elif msg.text.lower().startswith("botsadd "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].append(str(inkey))
                    cl.sendReplyMessage(msg.id, to, "已加入分機！")
                elif msg.text.lower().startswith("botsdel "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].remove(str(inkey))
                    cl.sendReplyMessage(msg.id, to, "已取消分機！")
                elif text.lower() == 'botslist':
                    if ban["bots"] == []:
                        cl.sendMessage(to,"無分機!")
                    else:
                        mc = "╔══[ Inviter List ]"
                        for mi_d in ban["bots"]:
                            mc += "\n╠ "+cl.getContact(mi_d).displayName
                        cl.sendReplyMessage(msg.id, to,mc + "\n╚══[ Finish ]")
                elif text.lower() == 'join':
                    if msg.toType == 2:
                        G = cl.getGroup
                        cl.inviteIntoGroup(to,ban["bots"])
                elif msg.text.lower().startswith("ii "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.createGroup("fuck",[inkey])
                    cl.leaveGroup(op.param1)
#==============================================================================#
                elif text.lower() == 'me':
                    if msg.toType == 2 or msg.toType == 1:
                        sendMessageWithMention(to, sender)
                        cl.sendContact(to, sender)
                    else:
                        cl.sendContact(to,sender)
                elif "c:" in msg.text:
                    number = text.replace("c:","")
                    cl.sendContact(msg.to,number)
                elif text.lower() == 'mymid':
                    cl.sendReplyMessage(msg.id, to, sender)
                elif text.lower() == 'myname':
                    me = cl.getContact(sender)
                    cl.sendReplyMessage(msg.id, to, me.displayName)
                elif text.lower() == 'mybio':
                    me = cl.getContact(sender)
                    cl.sendReplyMessage(msg.id, to,"[個人簽名]\n" + me.statusMessage)
                elif text.lower() == 'mypicture':
                    me = cl.getContact(sender)
                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvid':
                    me = cl.getContact(sender)
                    cl.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = cl.getContact(sender)
                    cover = cl.getProfileCoverURL(sender)
                    cl.sendImageWithURL(msg.to, cover)
                elif "gc " in msg.text:
                    if msg.toType == 2:
                        key = eval(msg.contentMetadata["MENTION"])
                        u = key["MENTIONEES"][0]["M"]
                        contact = cl.getContact(u)
                        cu = cl.getProfileCoverURL(mid=u)
                        try:
                            cl.sendMessage(msg.to,"名字:\n" + contact.displayName + "\n\n系統識別碼:\n" + contact.mid + "\n\n個性簽名:\n" + contact.statusMessage + "\n\n頭貼網址 :\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n\n封面網址 :\n" + str(cu))
                        except:
                            cl.sendMessage(msg.to,"名字:\n" + contact.displayName + "\n\n系統識別碼:\n" + contact.mid + "\n\n個性簽名:\n" + contact.statusMessage + "\n\n封面網址:\n" + str(cu))
                elif msg.text.lower().startswith("contact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            mi_d = contact.mid
                            cl.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += "" + ls
                        cl.sendReplyMessage(msg.id, to, str(ret_))
                elif msg.text.lower().startswith("name "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendReplyMessage(msg.id, to, "[ 名字 ]\n" + contact.displayName)
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendReplyMessage(msg.id, to, "[ 個簽 ]\n" + contact.statusMessage)
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus
                            cl.sendImageWithURL(msg.to, str(path))
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = cl.getProfileCoverURL(ls)
                                cl.sendImageWithURL(msg.to, str(path))
                elif "sc:" in msg.text:
                    ggid = msg.text.replace("sc:","")
                    group = cl.getGroup(ggid)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    else:
                        gQr = "開啟"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔════[群組資料]"
                    ret_ += "\n╠顯示名稱 Name : {}".format(str(group.name))
                    ret_ += "\n╠群組ＩＤ : {}".format(group.id)
                    ret_ += "\n╠群組作者 Creator : {}".format(str(gCreator))
                    ret_ += "\n╠成員數量 Members : {}".format(str(len(group.members)))
                    ret_ += "\n╠邀請數量 Pending : {}".format(gPending)
                    ret_ += "\n╠群組網址 QR : {}".format(gQr)
                    ret_ += "\n╠群組網址 Ticket : {}".format(gTicket)
                    ret_ += "\n╚═══[完]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
#==============================================================================#
                elif msg.text.startswith("Cn:"):
                    curryname = msg.text.replace("Cn:","")
                    profile = cl.getProfile()
                    profile.displayName = curryname
                    cl.updateProfile(profile)
                    cl.sendReplyMessage(msg.id,to,"名稱更改為：" + profile.displayName)
                elif msg.text.startswith("Cb:"):
                    currybio = msg.text.replace("Cb:","")
                    profile = cl.getProfile()
                    profile.statusMessage = currybio
                    cl.updateProfile(profile)
                    cl.sendReplyMessage(msg.id,to,"個簽更改為：" + profile.statusMessage)
                elif msg.text.startswith("我是默沁的奴隸"):
                    curryname = msg.text.replace("我是默沁的奴隸","默沁的奴隸")
                    profile = cl.getProfile()
                    profile.displayName = curryname
                    cl.updateProfile(profile)
                    path = "C:\\Users\\sen1213\\Desktop\\botfin\\vpc.jpg"
                    cl.updateProfilePicture(path)
                elif text.lower().startswith('send-tw '):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh-tw'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    cl.sendAudio(to,"hasil.mp3")
                elif text.lower().startswith('send-en '):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    cl.sendAudio(to,"hasil.mp3")
                elif text.lower().startswith('send-jp '):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ja'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    cl.sendAudio(to,"hasil.mp3")
                elif text.lower().startswith('send-id '):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'id'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    cl.sendAudio(to,"hasil.mp3")
                elif text.lower().startswith('tr-tw '):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='zh-tw')
                    A = hasil.text
                    cl.sendMessage(to, A)
                elif text.lower().startswith('tr-en '):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='en')
                    A = hasil.text
                    cl.sendMessage(to, A)
                elif text.lower().startswith('tr-jp '):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ja')
                    A = hasil.text
                    cl.sendMessage(to, A)
                elif text.lower().startswith('tr-id '):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='id')
                    A = hasil.text
                    cl.sendMessage(to, A)
#==============================================================================#
                elif text.lower() == 'group':
                    group = cl.getGroup(to)
                    GS = group.creator.mid
                    cl.sendContact(to, GS)
                elif text.lower() == 'groupid':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[ID Group : ]\n" + gid.id)
                elif text.lower() == 'grouppicture':
                    group = cl.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'groupname':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[群組名稱 : ]\n" + gid.name)
                elif text.lower() == 'grouplink':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = cl.reissueGroupTicket(to)
                            cl.sendMessage(to, "[ 群組網址 ]\nhttps://line.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            cl.sendMessage(to, "Grouplink未開啟 {}openlink".format(str(settings["keyCommand"])))
                elif text.lower() == 'link on':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            cl.sendReplyMessage(msg.id, to, "群組網址已開")
                        else:
                            group.preventedJoinByTicket = False
                            cl.updateGroup(group)
                            cl.sendReplyMessage(msg.id, to, "開啟成功")
                elif text.lower() == 'link off':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            cl.sendReplyMessage(msg.id, to, "群組網址已關")
                        else:
                            group.preventedJoinByTicket = True
                            cl.updateGroup(group)
                            cl.sendReplyMessage(msg.id, to, "關閉成功")
                elif text.lower() == 'ginfo':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "無"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "[ Group Info ]"
                    ret_ += "\n 群組名稱 Group name : {}".format(str(group.name))
                    ret_ += "\n 群組 Id : {}".format(group.id)
                    ret_ += "\n 創建者 Creator : {}".format(str(gCreator))
                    ret_ += "\n 群組人數 Members : {}".format(str(len(group.members)))
                    ret_ += "\n 邀請中 Pending : {}".format(gPending)
                    ret_ += "\n 網址狀態 QR : {}".format(gQr)
                    ret_ += "\n 群組網址 Ticket : {}".format(gTicket)
                    ret_ += "\n[ 完 ]"
                    cl.sendReplyMessage(msg.id, to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'gb':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "[ 成員名單 ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n {}. 名稱：{}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n[ 全部成員共 {} 人]".format(str(len(group.members)))
                        cl.sendReplyMessage(msg.id, to, str(ret_))
                elif text.lower() == 'lg':
                        groups = cl.groups
                        ret_ = "[ GroupList ]"
                        no = 0 + 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n {}.群名 {} | {} 人".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n[ 共有 {} 的群組 ]".format(str(len(groups)))
                        cl.sendReplyMessage(msg.id, to, str(ret_))
                elif msg.text.lower().startswith("nk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"Fuck you")
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.sendMessage(to,"規制中")
                            
                elif msg.text.lower().startswith("tk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.sendMessage(to,"規制中")
                
                elif "Zk" in msg.text:
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in admin:
                                pass
                            else:
                                try:
                                    cl.kickoutFromGroup(to,[target])
                                except:
                                    pass

                elif msg.text.lower().startswith("ri "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"來回機票一張")
                            cl.kickoutFromGroup(msg.to,[target])
                            cl.inviteIntoGroup(to,[target])
                        except:
                            cl.sendMessage(to,"規制中")
                            
                elif msg.text.lower().startswith("rk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.kickoutFromGroup(msg.to,[target])
                            cl.inviteIntoGroup(to,[target])
                        except:
                            cl.sendMessage(to,"規制中")
                elif text.lower() == 'byeall':
                    if msg.toType == 2:
                        print ("[ 19 ] KICK ALL MEMBER")
                        _name = msg.text.replace("Byeall","")
                        gs = cl.getGroup(msg.to)
                        cl.sendMessage(msg.to,"破壞降臨")
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"指令錯誤")
                        else:
                            for target in targets:
                                try:
                                    cl.kickoutFromGroup(msg.to,[target])
                                    print (msg.to,[g.mid])
                                except:
                                    cl.sendMessage(msg.to,"")
                elif ("Gn " in msg.text):
                    if msg.toType == 2:
                        X = cl.getGroup(msg.to)
                        X.name = msg.text.replace("Gn ","")
                        cl.updateGroup(X)
                    else:
                        cl.sendMessage(msg.to,"It can't be used besides the group.")
                elif text.lower() == 'cancel':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.invitee]
                    for _mid in gMembMids:
                        cl.cancelGroupInvitation(msg.to,[_mid])
                    cl.sendReplyMessage(msg.id, to,"已取消所有邀請!")
                elif ("Inv " in msg.text):
                    if msg.toType == 2:
                        midd = msg.text.replace("Inv ","")
                        cl.findAndAddContactsByMid(midd)
                        cl.inviteIntoGroup(to,[midd])
                elif msg.text.lower().startswith("mall "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    x = text.split(' ',2)
                    c = int(x[2])
                    group = cl.getGroup(to)
                    gMembMids = [contact.mid for contact in group.members]
                    for c in range(c):
                        cl.inviteIntoGroupCall(to.inkey,gMembMid,1)
                elif text.lower().startswith('call:'):
                    if msg.toType == 2:
                        number = msg.text.replace("call:","")
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        num = int(number)
                        for var in range(0,num):
                            cl.inviteIntoGroupCall(to,gMembMids,1)
                elif text.lower().startswith('rall:'):
                    if msg.toType == 1:
                        number = msg.text.replace("rall:","")
                        room = cl.getRoom(to)
                        rMembMids = [contact.mid for contact in room.contacts]
                        num = int(number)
                        for var in range(0,num):
                            cl.inviteIntoGroupCall(to,rMembMids,1)
#==============================================================================#
                elif text.lower() == 'tagall':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//20
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*20 : (a+1)*20]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                elif text.lower() == 'zt':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            sendMessageWithMention(to,target)
                elif text.lower() == 'zm':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for mi_d in targets:
                           cl.sendContect(to,mi_d)
                elif msg.text in ["SR","Setread"]:
                    cl.sendReplyMessage(msg.id, to, "設置已讀點 ✔")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M:%H")
                    wait2['ROM'][msg.to] = {}
                    print ("設置已讀點")
                elif msg.text in ["DR","Delread"]:
                    cl.sendReplyMessage(msg.id, to, "刪除已讀點 ✘")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                elif msg.text in ["LR","Lookread"]:
                    if msg.to in wait2['readPoint']:
                        print ("查詢已讀")
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendReplyMessage(msg.id, to, "[已讀順序]:%s\n\n[已讀過的人]:\n%s\n查詢時間:[%s]" % (wait2['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        cl.sendReplyMessage(msg.id, to, "請輸入SR設置已讀點")

#==============================================================================#
                elif msg.text.lower().startswith("ban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["blacklist"][target] = True
                            cl.sendReplyMessage(msg.id, to,"Ok")
                            break
                        except:
                            cl.sendReplyMessage(msg.id, to,"Nobe")
                            break
                elif "Ban:" in msg.text:
                    mmtxt = text.replace("Ban:","")
                    try:
                        ban["blacklist"][mmtext] = True
                        cl.sendReplyMessage(msg.id, to,"已加入黑單!")
                    except:
                        cl.sendReplyMessage(msg.id, to,"Ok")
                elif msg.text.lower().startswith("unban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del ban["blacklist"][target]
                            cl.sendReplyMessage(msg.id, to,"刪除成功 !")
                            break
                        except:
                            cl.sendReplyMessage(msg.id, to,"刪除失敗 !")
                            break
                elif text.lower() == 'banlist':
                    if ban["blacklist"] == {}:
                        cl.sendReplyMessage(msg.id, to,"無黑單成員!")
                    else:
                        mc = "[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n "+cl.getContact(mi_d).displayName
                        cl.sendReplyMessage(msg.id, to,mc + "\n[ Finish ]")
                elif msg.text.lower().startswith("k "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ban["kill"][target] = True
                            cl.sendReplyMessage(msg.id, to,"Ok")
                            break
                        except:
                            cl.sendReplyMessage(msg.id, to,"Nobe")
                            break
                elif text.lower().startswith("kn "):
                    if msg.toType == 2:
                        _name = msg.text.replace("kn ","")
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"Not Found")
                        else:
                            for target in targets:
                                try:
                                    ban["kill"][target] = True
                                    cl.sendReplyMessage(msg.id, to,"已經新增自預備名單")
                                    break
                                except:
                                    cl.sendReplyMessage(msg.id, to,"Nobe")
                                    break
                elif msg.text.lower().startswith("unk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del ban["kill"][target]
                            cl.sendReplyMessage(msg.id, to,"刪除成功 !")
                            break
                        except:
                            cl.sendReplyMessage(msg.id, to,"刪除失敗 !")
                            break
                elif text.lower() == 'klist':
                    if ban["kill"] == {}:
                        cl.sendReplyMessage(msg.id, to,"無預備成員!")
                    else:
                        mc = "[ 預備踢人名單 ]"
                        for mi_d in ban["kill"]:
                            mc += "\n "+cl.getContact(mi_d).displayName
                        cl.sendReplyMessage(msg.id, to,mc + "\n[ 已經幫你查詢完畢 ]")
                elif text.lower() == 'killgo':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in ban["kill"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"已經踢出預備名單")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                elif text.lower() == 'nkban':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in ban["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendMessage(msg.to,"Blacklist kicked out")
                elif text.lower() == 'cleankill':
                    for mi_d in ban["kill"]:
                        ban["kill"] = {}
                    cl.sendReplyMessage(msg.id, to, "已清空預備踢人")
                elif text.lower() == 'killlist':
                    if ban["kill"] == {}:
                        cl.sendReplyMessage(msg.id, to,"無預備成員")
                    else:
                        mc = "[ 預備成員mid ]"
                        for mi_d in ban["kill"]:
                            mc += "\n "+mi_d
                        cl.sendReplyMessage(msg.id, to,mc + "\n[ 已經幫你查詢完畢 ]")
                elif text.lower() == 'cleanban':
                    for mi_d in ban["blacklist"]:
                        ban["blacklist"] = {}
                    cl.sendReplyMessage(msg.id, to, "已清空黑名單")
                elif text.lower() == 'banmidlist':
                    if ban["blacklist"] == {}:
                        cl.sendReplyMessage(msg.id, to,"無黑單成員!")
                    else:
                        mc = "[ Black List ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n "+mi_d
                        cl.sendReplyMessage(msg.id, to,mc + "\n[ Finish ]")


#==============================================================================#
                elif "好友廣播：" in msg.text:
                    bctxt = text.replace("好友廣播：","")
                    t = cl.getAllContactIds()
                    for manusia in t:
                        cl.sendMessage(manusia,(bctxt))
                elif "群組廣播：" in msg.text:
                    bctxt = text.replace("群組廣播：","")
                    n = cl.getGroupIdsJoined()
                    for manusia in n:
                        cl.sendMessage(manusia,(bctxt))
                elif "Copy " in msg.text:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            contact = cl.getContact(target)
                            X = contact.displayName
                            profile = cl.getProfile()
                            profile.displayName = X
                            cl.updateProfile(profile)
                            cl.sendMessage(to, "Success...")
                            Y = contact.statusMessage
                            lol = cl.getProfile()
                            lol.statusMessage = Y
                            cl.updateProfile(lol)
                            path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                            P = contact.pictureStatus
                            cl.updateProfilePicture(P)
                        except Exception as e:
                            cl.sendMessage(to, "Failed!")
            if text.lower() == 'cc9487':
                if sender in ['uff33d3a90dccdb748b92e35003eb54f1']:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                else:
                    pass
#==============================================================================#
            if msg.contentType == 13:
                if settings["getmid"] == True:
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        cl.sendMessage(msg.to,"[mid]:\n" + msg.contentMetadata["mid"])
                    else:
                        cl.sendMessage(msg.to,"[mid]:\n" + msg.contentMetadata["mid"])
            elif msg.contentType == 16:
                if settings["timeline"] == True:
                    msg.contentType = 0
                    msg.text = "文章網址：\n" + msg.contentMetadata["postEndUrl"]
                  #  detail = cl.downloadFileURL(to,msg,msg.contentMetadata["postEndUrl"])
                    cl.sendMessage(msg.to,msg.text)
#==============================================================================#
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in ban["mimic"]["target"] and ban["mimic"]["status"] == True and ban["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        cl.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = cl.getContact(sender)
                                    cl.sendMessage(to, "找我嗎？\n有事請私我")
                                break
            try:
                msg = op.message
                if settings["reread"] == True:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                    elif msg.contentType == 7:
                        stk_id = msg.contentMetadata['STKID']
                        msg_dict[msg.id] = {"text":"貼圖id:"+str(stk_id),"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(e)

#==============================================================================#
        if op.type == 65:
            print ("[ 65 ] REREAD")
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            timeNow = datetime.now()
                            timE = datetime.strftime(timeNow,"(%y-%m-%d %H:%M:%S)")
                            try:
                                strt = int(3)
                                akh = int(3)
                                akh = akh + 8
                                aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(msg_dict[msg_id]["from"])+"},"""
                                aa = (aa[:int(len(aa)-1)])
                                cl.sendMessage(at, "收回訊息者 @wanping ", contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                            except Exception as e:
                                print(str(e))
                            cl.sendMessage(at,"[收回訊息者]\n%s\n[訊息內容]\n%s\n[完]"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            cl.sendMessage(at,"/n發送時間/n"+strftime("%y-%m-%d %H:%M:%S")+"/n收回時間/n"+timE)
                            
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print (e)
#==============================================================================#
        if op.type == 55:
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[※]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[※]" + Name
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)

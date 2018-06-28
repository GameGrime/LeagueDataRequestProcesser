#*****************************************************************************************
# Script made to process account data from riot support. Throw it into excel, or CSV files.
# Feel free to edit and change the script as much as you want. This script was made for 3.6
# This was made in free time, support may be limited. and It will not be updated past verion 8.13
# It should have support for using the riot API instead of downloaded files. I created the data Json files from riot api. But got rate limited. HAHA
# Feel free to fork if you want to add API support. to Auto update. Also Maybe make a database of ID's for hextech items/summoner spells. also mission items.
#*****************************************************************************************

import os, csv, json, datetime, re

developerModeSetupSkins = False

def loadInfo(fileName):
    with open(fileName,'r') as data:
        loaded = json.load(data)
    return loaded
    
def fixTime(time):
    timeFixed = str(time)[:-3]
    timeFixed = int(timeFixed)
    return timeFixed
    
def championSkinID():
    if developerModeSetupSkins:
        with open('data\\championSkinID.json','w') as champSkin:
            champSkin.write('{\n')
            champSkin.write('  "Skin" : {\n')
            counter = 0
            for file in os.listdir("champion"):
                if file.endswith(".json"):
                    json = loadInfo("champion\\"+ file)
                    championName = re.sub('.json','',file)
                    try:
                        skinsJson = json['data'][championName]['skins']
                    except:
                        skinsJson = json['skins']
                    skinCount = 0
                    counter += 1
                    for skin in skinsJson:
                        champSkin.write('    "%s" : {\n' % (skin['id']))
                        champSkin.write('      "{0}" : "{1}",\n'.format('id', skin['id']))
                        champSkin.write('      "{0}" : "{1}",\n'.format('champion', championName))
                        champSkin.write('      "{0}" : "{1}",\n'.format('num', skin['num']))
                        try:
                            champSkin.write('      "{0}" : "{1}",\n'.format('chromas', skin['chromas']))
                        except:
                            pass
                        champSkin.write('      "{0}" : "{1}"\n'.format('name', skin['name']))
                        
                        skinCount += 1
                        if counter == len(os.listdir('champion')) and skinCount == len(skinsJson):
                            champSkin.write('    }\n')
                        else:
                            champSkin.write('    },\n')


                    # champskin.write("{\n")
                    # champSkin.write('  "%s" : \{ \n' % championName)
                    # champSkin.write(skinsJson)
            champSkin.write('}}')
    else:
        pass
            
    
def findItemName(item):
    if 'champions' in item and not 'championsskin' in item:
        champions = loadInfo('data\\champions.json')
        championID = re.sub('champions_', '', item)
        championName = champions['keys'][championID]
        return championName
    elif 'championsskin' in item:
        skins = loadInfo('data\\championSkinID.json')
        skinID = re.sub('championsskin_','',item)
        try:
            skinName = skins['Skin'][skinID]['name']
            return skinName
        except:
            errorOfSkin = True
        try:
            
            skinIDStr = str(skinID)[:-2]
            skinIDStr = int(skinIDStr)
            skinIDStr = 100 * skinIDStr
            skinName = 'Chroma Skin for: {0}'.format(skins['Skin'][str(skinIDStr)]['champion'])
            return skinName
        except:
            print('Error, Champion Json File Missing, contact /u/Lil_Jening with this skin id. {}'.format(skinID))
        
    elif 'hextech' in item:
        hextechTypes = {
            'hextech_crafting_7' : 'Key Fragment'
            }
        try:
            itemName = hextechTypes[item]
            return itemName
        except:
            itemName = 'Hextech item not added: {}'.format(item)
            return itemName
    else:
    # This is really hard, i have to make this up myself. No API found here.
        return item
    
    
def accountData():
    aDJson = loadInfo('accountData.json')
    with open('accountData.csv','w') as csvFile:
        dataFile = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        dataFile.writerow(['Username', 'Summoner Name', 'Phone Number', 'Email', 'Date of Birth'])
        dataFile.writerow([aDJson['username'],aDJson['summonerName'],aDJson['phoneNumber'],aDJson['email'],aDJson['dateOfBirth']])
        csvFile.close()

def accountEvents():
    aEJson = loadInfo('accountEvents.json')
    with open('accountEvents.csv','w') as csvFile:
        dataFile = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        dataFile.writerow(['Please give info to /u/lil_jening on what actually goes here, His account events is blank.'])
        csvFile.close()

def groupedReports():
    gRJson = loadInfo('groupedReports.json')
    dataRR = gRJson['reportsReceived']
    dataRM = gRJson['reportsMade']
    reportDict={
        'HATE_SPEECH' : 'Hate Speech',
        'LEAVING_AFK' : 'Leaving/AFK', 
        'VERBAL_ABUSE' : 'Verbal Abuse',
        'NEGATIVE_ATTITUDE' : 'Negative Attitude',
        'ASSISTING_ENEMY_TEAM' : 'Assisting Enemy Team',
        'THIRD_PARTY_TOOLS' : 'Third Party Tools/Cheats',
        'INAPPROPRIATE_NAME' : 'Inappropriate Name'
    }
    reRe = ['']
    reReNumb = ['Reports Recieved']
    for eachType in dataRR:
        reRe.append(reportDict[eachType])
        reReNumb.append(dataRR[eachType])
    reMa = ['']
    reMaNumb = ['Reports Made']
    for eachType in dataRM:
        reMa.append(reportDict[eachType])
        reMaNumb.append(dataRM[eachType])
    with open('groupedReports.csv','w') as csvFile:
        dataFile = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        dataFile.writerow(reRe)
        dataFile.writerow(reReNumb)
        dataFile.writerow(reMa)
        dataFile.writerow(reMaNumb)
        csvFile.close()
        
def loginEvents():
    lEJson = loadInfo('loginEvents.json')
    loginType = {
    'LOGOUT_DEADPOOL' : 'Logout Deadpool',
    'DISCONNECT' : 'Disconnect',
    'AUTHENTICATION' : 'Authentication',
    'LOGIN' : 'Login',
    'LOGOUT_USER' : 'Logout User',
    'LOGIN_KICK' : 'Login Kick',
    'LOGOUT_KICK' : 'Logout Kick'
    }
    with open('loginEvents.csv','w') as csvFile:
        dataFile = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        dataFile.writerow(['Date', 'Username', 'IP Address', 'Login Type'])
        for loginEvent in lEJson:
            row = [
                datetime.datetime.fromtimestamp(fixTime(loginEvent['dateTime'])).strftime('%Y-%m-%d %H:%M:%S'),
                loginEvent['userName'],
                loginEvent['ipAddress'],
                loginType[loginEvent['eventType']],
            ]
            dataFile.writerow(row)
        csvFile.close()

def rpPurchases():
    rpPJson = loadInfo('rpPurchases.json')
    with open('rpPurchases.csv','w') as csvFile:
        dataFile = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        dataFile.writerow(['Date', 'Amount', 'ID', 'IP Address', 'Store Account ID', 'Transaction ID', 'Transaction Number', 'Currency Type', 'Payment Type'])
        for purchase in rpPJson:
            row = [
                datetime.datetime.fromtimestamp(fixTime(purchase['created'])).strftime('%Y-%m-%d %H:%M:%S'),
                purchase['amount'],
                purchase['id'],
                purchase['userIp'],
                purchase['storeAccountId'],
                purchase['transactionId'],
                purchase['transactionNumber'],
                purchase['currencyType'],
                purchase['paymentType']
            ]
            dataFile.writerow(row)

def storeTransactions():
    stJson = loadInfo('storeTransactions.json')
    with open('storeTransactions.csv','w') as csvFile:
        dataFile = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        dataFile.writerow(['Date', 'Item', 'Blue Essence/IP', 'RP', 'Transaction ID', 'Refunded', 'IP Address', 'Source', 'Type'])
        
        for purchase in stJson:
            row = [
                datetime.datetime.fromtimestamp(fixTime(purchase['millis'])).strftime('%Y-%m-%d %H:%M:%S'),
                findItemName(purchase['itemId']),
                purchase['ip'],
                purchase['rp'],
                purchase['transactionId'],
                purchase['refunded'],
                purchase['ipAddress'],
                purchase['source'],
                purchase['type']
            ]
            dataFile.writerow(row)
            
#-----------------------------------------------------------------------------
# Commenting will be sparce, close to non existent, This below sets the working directory to the same location as the .py file.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

championSkinID()
accountData()
accountEvents()
groupedReports()
loginEvents()
rpPurchases()
storeTransactions()

print("Output should be created. Heres hopin.")
input('press enter to exit...')

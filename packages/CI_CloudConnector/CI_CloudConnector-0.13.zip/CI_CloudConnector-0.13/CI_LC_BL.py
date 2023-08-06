#remarks test
import httplib, urllib , json , requests , urllib2, logging , time, datetime ,sys, os , threading , socket, ConfigParser ,random
#import pkg_resources  # part of setuptools
import cpppo
from cpppo.server.enip import address, client

TagsDefenitionFileName = 'TagsDefenition.txt'
TagsValuesFileName = '[NEW]TagsValues'
TagsValueDir = 'TagValues'
HomeDir = 'CI_LC'
HTTP_PREFIX = 'http' # https / http
#HTTP_PREFIX = 'https'

#config
cfg_serverAddress = ''
cfg_userName = ''
cfg_passWord = ''
cfg_plcMode = ''
        
#VER = pkg_resources.require("CI_LocalConnector")[0].version
VER = '0.13'
sugestedUpdateVersion = ''
configFile = 'config.ini'
ScanRateLastRead = {}
currentToken=''
g_connectorTypeName = ''

# ============================
# general Functions
# ============================    
def initLog():
    logging.basicConfig(filename='CI_CloudConnector.log',level=logging.INFO , format='%(asctime)s %(message)s')    
    logging.info('===============================')
    logging.info('CI_CloudConnector Init')

# ============================    
def ci_print(msg , level = ''):
    try:
        if level=='info':
            logging.info(msg)
        else:
            logging.warning(msg)
            
        #print(msg)
    except Exception as inst:
        logging.warning('Main Exception :: ' + inst)
        
# ============================
def handleError(message,err):
    try:
        err_desc = str(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(message, err_desc, exc_type, fname, exc_tb.tb_lineno)
        logging.Error('Error in MainLoop :: ' + str(inst))
    except Exception as errIgnore:
        ci_print ("Error in handleError " + str(errIgnore))
        
# ============================
def initConfig(overwrite = False):
    global cfg_serverAddress
    global cfg_userName
    global cfg_passWord
    global cfg_plcMode
    #check if config exists
    try:
        filePath = "/" + HomeDir + "/" +configFile
        exists = os.path.exists(filePath)
        strPlcModeOptions = ' , other options (Simulation , ModbucTCP , EtherNetIP)'
        if exists == True:
            ci_print ("Found config in " + filePath)
            Config = ConfigParser.ConfigParser()
            d = Config.read(filePath)
            cfg_serverAddress = Config.get("Server", "Address")
            cfg_userName = Config.get("Server", "username")
            cfg_passWord = Config.get("Server", "password")
            cfg_plcMode = Config.get("Server", "plcMode")
            #single = Config.getboolean("Server", "Address")
            ci_print ("serverAddress:" + cfg_serverAddress)
            ci_print ("userName:" + cfg_userName)
            ci_print ("password:" + cfg_passWord)
            ci_print ("plcMode:" + cfg_plcMode + strPlcModeOptions)
        if exists == False or overwrite==True:
            ci_print ("config not found , creating new one in " + filePath)
            config = ConfigParser.RawConfigParser()
            config.add_section('Server')
            var = raw_input("Enter Server Address: F.E: localhost:63483/ ")
            if var!="":
                config.set('Server', 'Address', var)
            else:
                config.set('Server', 'Address', 'localhost')

            var = raw_input("Enter username:")
            config.set('Server', 'username', var)

            var = raw_input("Enter password:")
            config.set('Server', 'password', var)
            
            var = raw_input("Enter plcMode:" + strPlcModeOptions)
            config.set('Server', 'plcMode', var)

            with open(filePath, 'wb') as configfileTmp:
                config.write(configfileTmp)
                ci_print ("Config Settings updated.")
    except Exception as inst:
        ci_print('initConfig Exception :: ' + str(inst))
        
# ============================
# Cloud Functions
# ============================
def getCloudToken():
    ci_print ("start getCloudToken")
    global cfg_serverAddress
    token=''
    url = ''
    try:
        ci_print ("About to get token from cloud")
        host = cfg_serverAddress
        url = HTTP_PREFIX + '://'+ cfg_serverAddress +'/token'
        ci_print ("url= "+url)
        response = requests.get(url,
                                data = {
                                    'grant_type' : 'password',
                                    'username' : cfg_userName ,
                                    'password' : cfg_passWord ,
                                    },
                                headers = {
                                    'User-Agent': 'python',
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                    })
        data = response.text

        #ci_print ('Token Data:' + data)
        jsonData = json.loads(data)
        token = jsonData[u'access_token']
        ci_print ("recieved Token ")# + token
    except Exception as inst:
        ci_print('URL :: ' + str(url))
        ci_print('Error getting Token :: ' + str(inst))
        token = ''
    return token

# ============================
# make http request to cloud if fails set currentToken='' so it will be initialized next time
def ciRequest(url , data , postGet='get', method ='', token=''):
    ans = {}
    ans["isOK"] = False
    global currentToken
    ansIsSucessful=False    
    try:
        #ci_print('url=' + url + ' ,postGet=' + postGet+ ' ,method=' + method)
        if token=='':
            ci_print("Skipping "+method+" - no Token")
            return ""            
        else:
            ci_print('Got Token Using Bearer auth')
            if postGet=='post':
                response = requests.post(url,
                                        data,
                                        headers={'Content-Type':"application/json",'Accept':'text/plain','Authorization': 'bearer %s' % token})
            else:
                response = requests.get(url,
                                        data = None,
                                        headers={'Authorization': 'bearer %s' % token})
            #ci_print('response='+str(response))
            if response.status_code==403:
                currentToken=''
            ansIsSucessful = True            
    except Exception as err:
        ci_print('Error in ciRequest '+method +" : "+ str(err))
        currentToken = ''
        ansIsSucessful = False
        
    ans["isOK"] = ansIsSucessful
    ans["response"] = response
    return ans
        
    
# ============================
def getCloudVersion():
    global currentToken
    if currentToken=='':
        currentToken = getCloudToken()    
    token = currentToken
    #initConfig()
    #token = getCloudToken()
    global sugestedUpdateVersion
    ci_print ("start getCloudVersion")
    tags= None
    try:        
        IpAddress = socket.gethostbyname(socket.gethostname())
        url = HTTP_PREFIX + '://'+ cfg_serverAddress + '/api/CloudConnector/GetVersion/?version='+ VER +'&IpAddress='+IpAddress
        
        ret = ciRequest(url , None , 'get', 'getCloudVersion', token)
        response = ret["response"]            
        if ret["isOK"]==False:
            return ""  
        #if token=='':
        #    ci_print("Skipping getCloudVersion - no Token")
        #    return ""            
        #else:
        #    ci_print('Got Token Using Bearer auth')
        #    response = requests.get(url,
        #                            data = None,
        #                            headers={'Authorization': 'bearer %s' % token})
        ci_print ('gettags response=' + response.text)
        ans = json.loads(response.text)
        updateToVersion = ans[0]
        serverTime = ans[1]
        #ci_print (serverTime)
        
        sugestedUpdateVersion = updateToVersion
        if updateToVersion!= VER:
            ci_print('! > Local Version : ' + str(VER) + ' But Server suggest Other Version : ' + str(updateToVersion))        

        #printTags(tags)
    except Exception as err:
        ci_print ("Error getting Version from cloud ::" + str(err))
        sugestedUpdateVersion = ""
        
    return sugestedUpdateVersion
# ============================
def getCloudTags(token=''):
    #initConfig()
    #token = getCloudToken()
    ci_print ("start getCloudTags")
    tags= None
    try:        
        IpAddress = socket.gethostbyname(socket.gethostname())
        url = HTTP_PREFIX + '://'+ cfg_serverAddress +'/api/CloudConnector/GetTags/'
        #ci_print(token)
        tags = None
        ret = ciRequest(url , None , 'get', 'getCloudTags', token)
        response = ret["response"]
        if ret["isOK"]==True:
            #if token=='':
            #    ci_print("Skipping getCloudTags - no Token")            
            #else:
            #    ci_print('Got Token Using Bearer auth')
            #    response = requests.get(url,
            #                            data = None,
            #                            headers={'Authorization': 'bearer %s' % token})
        
            #ci_print ('gettags response=' + response.text)
            ans = json.loads(response.text)
            #g_connectorTypeName = ans["connectorTypeName"]
            printTags(ans["Tags"])
            arangedTags = arrangeTagsByScanTime(ans["Tags"])
            tags = {}
            tags["Tags"] = arangedTags
            tags["connectorTypeName"] = ans["connectorTypeName"]
            tags["PlcIpAddress"] = ans["PlcIpAddress"]
            #write tags to file
            f = open(TagsDefenitionFileName, 'w')
            json.dump(tags, f)
            f.close()
            
            ci_print ("Get Cloud Counters recieved " + str(len(tags)) + " Tags")
    except Exception as err:
        handleError("Error getting tags from cloud", err)
        tags = None
        
    if tags == None:
        tags = getTagsDefenitionFromFile()
    return tags

# ============================
def arrangeTagsByScanTime(tags):
    ans={}
    try:
        ci_print("arrangeTagsByScanTime")
        
        for index in range(len(tags)):
            scanRate = tags[index][u'ScanRate']
            #ci_print("scanRate=" + str(scanRate))
            if scanRate in ans:
                tagsListPerScanRate = ans[scanRate]
            else:
                ans[scanRate]=[]

            #ci_print(ans[scanRate])
            ans[scanRate].append(tags[index])
    except Exception as err:
        handleError("arrangeTagsByScanTime", err)
    #ci_print(ans)
    return ans
# ============================
def printTags(tags):
    try:
        ci_print ("Print Tags : List Contains " + str(len(tags)) + " Tags")
        ci_print (tags)
        for index in range(len(tags)):
            msg = 'Tag Id: ' + str(tags[index][u'TagId']) + ' ,TagName: '+ str(tags[index][u'TagName']) + ' ,TagAddress: '+ str(tags[index][u'TagAddress'])
            msg = msg + ' ,ScanRate: '+ str(tags[index][u'ScanRate'])
            ci_print (msg)
            #print 'CounterId : ' + str(tags[index])
    except Exception as inst:
        handleError("Error in printTags", err)
        
# ============================        
def setCloudTags(tagValues , token=''):
    ci_print ("start setCloudTags")
    updatedSuccessfully = False
    try:
        url = HTTP_PREFIX + '://'+cfg_serverAddress+'/api/CloudConnector/SetCounterHistory/'
        
        payload = []
        for index in range(len(tagValues)):            
            TagId = tagValues[index][u'TagId']
            timeStamp = str(tagValues[index][u'time'])
            value = tagValues[index][u'value']
            status = 2 #1 = Invalid , 2 = Valid
            ci_print ('TagId = ' + str(TagId) + ' : ' + str(value))

            #{"TagId":5,"Value":"8.2","TimeStmp":"2016-06-21 11:25:56","StatusCE":""}
            tagVal = {
                'TagId':TagId
                 ,'TimeStmp':timeStamp
                 ,'StatusCE':status
                 ,'Value':value
                 }
            payload.append(tagVal)
                
        ci_print (str(payload))
        ret = ciRequest(url , json.dumps(payload) , 'post', 'setCloudTags', token)
        response = ret["response"]            
        #if token=='':
        #    ci_print("Skipping setCloudTags - no Token")
        #    return False
        #else:
        #    ci_print('Got Token Using Bearer auth')
        #    response = requests.post(url,
        #                             data = json.dumps(payload),
        #                             headers={'Content-Type':"application/json",'Accept':'text/plain','Authorization': 'bearer %s' % token})

        ci_print (response)
        ci_print (response.text)
        logging.info('setCloudTags response = ' + str(response) + ' : ' + response.text )
        #print '==' + str(response.status_code)
        updatedSuccessfully = response.status_code == 200

    except Exception as inst:
        handleError("Error setting tags in cloud", err)
        return False

    return updatedSuccessfully

# ============================
# PLC Functions
# ============================

def readEtherNetIP_Tags(tagsDefenitions, plcAddress):
    ci_print("start readEtherNetIP_Tags")
    ans  = []    
    try:
        maxOffset=0
        for index in range(len(tagsDefenitions)):
            try:
                offset = int(tagsDefenitions[index][u'TagAddress'])
            except ValueError:
                offset = 0
            maxOffset = max(maxOffset,offset)

        strTags = "Data_Array[0-" + str(maxOffset) + "]"   
        host                        = plcAddress    # Controller IP address
        port                        = address[1]    # default is port 44818
        depth                       = 1             # Allow 1 transaction in-flight
        multiple                    = 0             # Don't use Multiple Service Packet
        fragment                    = False         # Don't force Read/Write Tag Fragmented
        timeout                     = 1.0           # Any PLC I/O fails if it takes > 1s
        printing                    = False         # Print a summary of I/O
        #tags                        = ["Data_Array[0]","Data_Array[1]"]
        #tags                        = ["Tag[0-9]+16=(DINT)4,5,6,7,8,9", "@0x2/1/1", "Tag[3-5]"]
        tags                        = [strTags]
        with client.connector( host=host, port=port, timeout=timeout ) as connection:
            operations              = client.parse_operations( tags )
            failures,transactions   = connection.process(
                operations=operations, depth=depth, multiple=multiple,
                fragment=fragment, printing=printing, timeout=timeout )

        ci_print("transactions " + str(transactions))
        ci_print("failures " + str(failures))
        #client.close()
        #sys.exit( 1 if failures else 0 )

        for index in range(len(tagsDefenitions)):
            try:
                offset = int(tagsDefenitions[index][u'TagAddress'])
                TagId = int(tagsDefenitions[index][u'TagId'])
          
                value = transactions[0][offset]
                ci_print ('get register offset=' + str(offset) + ' value=' + str(value))
                val= {'offset':offset,'TagId':TagId,'time': str(datetime.datetime.now()), 'value': value}
                ans.append(val)
            except ValueError:
                ci_print ('Wrong offset (not int) ' + tagsDefenitions[index][u'TagAddress'])
                
        ci_print("End Read readEtherNetIP Tag")
        return ans
    except Exception as inst:
        handleError("Error in readEtherNetIP_Tags", inst)
        return ans

# ============================   
def readModBusTags(tagsDefenitions, plcAdress):
    ans  = []    
    try:       
        maxOffset=0
        for index in range(len(tagsDefenitions)):
            offset = int(tagsDefenitions[index][u'TagAddress'])
            maxOffset = max(maxOffset,offset)    
        
        ci_print ("Start Read ModBus Tag")
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient
        client = ModbusClient(plcAdress, port=502)
        client.connect()
        rr = client.read_holding_registers(1,1+maxOffset)
        ci_print (rr.registers)
        for index in range(len(tagsDefenitions)):
            offset = int(tagsDefenitions[index][u'TagAddress'])
            TagId = int(tagsDefenitions[index][u'TagId'])
          
            value = rr.registers[offset]
            ci_print ("get register offset=" + str(offset) + ' value=' + str(value))
            val= {'offset':offset,'TagId':TagId,'time': str(datetime.datetime.now()), 'value': value}
            ans.append(val)
            #ans.update({offset:[offset,CounterId,datetime.datetime.now(),value]})   
        
        client.close()
        logging.info('readModBusTags ')
        logging.info('readModBusTags = ' + str(ans) )
        ci_print ("End Read ModBus Tag")
        return ans
    except Exception as inst:
        handleError("error reading modbus", inst)
        return ans

# ============================
def readSimulation_Tags(tagsDefenitions):
    ci_print("start readSimulation_Tags")
    ans  = []    
    try:
        for index in range(len(tagsDefenitions)):
            try:
                TagId = int(tagsDefenitions[index][u'TagId'])
                value = random.uniform(-10, 10);
                #ci_print ('get register offset=' + str(offset) + ' value=' + str(value))
                val= {'TagId':TagId,'time': str(datetime.datetime.now()), 'value': value}
                ans.append(val)
            except ValueError:
                ci_print ('ValueError error ')
                
        ci_print("End Read readSimulation_Tags")
        return ans
    except Exception as inst:
        ci_print("Error in readSimulation_Tags " + str(inst))
        return ans

# ============================  
def printTagValues(tagValues):
    ci_print ("Count " + str(len(tagValues)) + " Tags")
    for index in range(len(tagValues)):
        ci_print (str(tagValues[index]))
     
def getLocalVersion():
    return VER
def getServerSugestedVersion():
    return sugestedUpdateVersion

# ============================
# Tag Files Functions
# ============================ 
def getTagsDefenitionFromFile():
    try:
        ci_print ('Start getTagsDefenitionFromFile ')  
        f2 = open(TagsDefenitionFileName, 'r')
        tags = json.load(f2)
        f2.close()
        ci_print ("Got " + str(len(tags)) + " Tags From File")
        #print tags
        return tags
    except Exception as inst:
        ci_print('Error in getTagsDefenitionFromFile :: ' + str(inst))

def getTagsValuesFromFile(fileName):
    try:
        ci_print ('Start get Values From File ' + fileName ) 
        f2 = open(fileName, 'r')
        vals = json.load(f2)
        f2.close()
        ci_print ("Got " + str(len(vals)) + " Values From File ")      
        return vals
    except Exception as inst:
        ci_print('Error in getTagsValuesFromFile :: ' + str(inst))

def saveValuesToFile(values , fileName):
    try:
        if fileName=='':
            fileName = TagsValuesFileName + datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")+ '.txt'
        #fileName = "./" + TagsValueDir + '/' + fileName
        fileName = "/" + HomeDir + "/" + TagsValueDir + '/' + fileName
        ci_print ('Start save Values To File ' + fileName ) 
        #write tags to file
        f = open(fileName, 'w')
        json.dump(values, f)
        f.close()
        time.sleep(1) # prevent two files in same ms
    except Exception as inst:
        ci_print('Error in saveValuesToFile :: ' + str(inst))

def handleValuesFile(fileName, token=''):
    try:
        ci_print("start handleValuesFile " + fileName)
        values = getTagsValuesFromFile(fileName)
        ci_print ('-----------')
        errFile = '[ERR]' + fileName[5:]
        isOk = setCloudTags(values,token)
        if isOk :
            os.remove(fileName)
            ci_print("file removed " + fileName)
            return True
        else:
            os.rename(fileName, errFile)
            ci_print('Error Handling File ' + errFile)
    except Exception as inst:
        ci_print('Error in handleValuesFile :: ' + str(inst))
    return False  

def handleAllValuesFiles(token=''):
    try:
        ci_print ('started handleAllValuesFiles')
        #if token=='':
        #    token = getCloudToken()
        i=0
        dirpath = "/" + HomeDir + "/" + TagsValueDir + "/"
        filesSortedByTime = [s for s in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, s))]
        filesSortedByTime.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
        ci_print ('in Dir ' + dirpath + " Found " + str(len(filesSortedByTime)) + " files")
        for file in filesSortedByTime:
            if file.endswith(".txt") and file.startswith('[NEW]'):
                i=i+1
                ci_print ('about to process file:' + file)
                handleValuesFile("/" + HomeDir +"/" +TagsValueDir + '/' + file, token)
        
        if i>0:
            ci_print (str(i) + ' Files handled')
    except Exception as inst:
        ci_print ("Error handleAllValuesFiles " + str(inst))

def createLibIfMissing():
    try:
        dirName = "/" + HomeDir + "/"
        d = os.path.dirname(dirName)
        if not os.path.exists(d):
            os.makedirs(dirName)
            ci_print ('Home DIR  Created :: ' + dirName)
            
        dirName = "/" + HomeDir + "/" + TagsValueDir + "/"
        d = os.path.dirname(dirName)
        if not os.path.exists(d):
            os.makedirs(dirName)
            ci_print ('TagsValueDir Created')
    except Exception as inst:
        ci_print ("Error createLibIfMissing " + str(inst))        

# ============================
# Main Loop 
# ============================ 
def Main():
    global ScanRateLastRead
    global currentToken
    try:    
        ci_print('Loop started at ' + str(datetime.datetime.now()))
        if (currentToken==''):
            currentToken = getCloudToken()
        # currently must get tags from cloud to init server before setting values
        tagsDefScanRatesAns = getCloudTags(currentToken)
        plcMode = tagsDefScanRatesAns["connectorTypeName"]
        tagsDefScanRates = tagsDefScanRatesAns["Tags"]
        plcAdress = tagsDefScanRatesAns["PlcIpAddress"]
        
        for scanRate in tagsDefScanRates:
            diff = 0
            if scanRate in ScanRateLastRead:
                now = datetime.datetime.now()                
                diff = (now - ScanRateLastRead[scanRate]).total_seconds()
                #print ('diff = -------' + str(diff))

            if diff+1 > scanRate or diff==0:
                
                ci_print("Get Tag Values For Scan Rate " + str(scanRate) + " ' time Form Last Run:" + str(diff) + " Sec")
                tagsDef = tagsDefScanRates[scanRate]
                #printTags(tagsDef)
                values = None
                if plcMode=='Simulation':
                    values = readSimulation_Tags(tagsDef) 
                if plcMode=='Modbus':
                    values = readModBusTags(tagsDef, plcAdress)
                if plcMode=='Ethernet/IP':
                    values = readEtherNetIP_Tags(tagsDef, plcAdress)

                printVal = " Val=" + str(values[0]["value"]) +" " + str( len(values)) + " Tags"
                print (str(datetime.datetime.now()) + ' Send Vals:' + str(scanRate) + " diff " + str(diff) + printVal)
                
                now = datetime.datetime.now()    
                ScanRateLastRead[scanRate] = now
                
                #printTagValues(values)
                if values:
                    saveValuesToFile(values,'')
        if currentToken!='':
            handleAllValuesFiles(currentToken)
        else:
            ci_print("No Token , skipping upload step")
    except Exception as inst:
        handleError("Error in Main", inst)     
        logging.Error('Error in MainLoop :: ' + str(inst))
        currentToken=''

    ci_print('===============================')
    ci_print('CI_CloudConnector Ended')
    
#initConfig()
#Main()

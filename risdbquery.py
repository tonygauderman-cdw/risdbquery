import sys, getopt
import json, csv
import configparser
import os, logging, logging.handlers
import urllib3
sys.path.insert(1,'../python-ucmapi/build/lib/')

from ucmapi import Axl, Ris

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

configfile = 'cucmconfig.ini'
delimiter = 'comma'
deviceclass = ''
outfile = ''
version = ''
cucmserver = ''
username = ''
password = ''
checkforhttp = False
checkfirmware = False
firmware = ''
phonemodel = ''
comparestatus = False
devices = ''
file1 = ''
axl = ''
getmodel = True
allphones = ''
phonereport = ''

def main(argv):
       global deviceclass, outfile, version, delimiter, logger, checkforhttp, checkfirmware, firmware, phonemodel, comparestatus, file1, getmodel
       comparestatus = False
       file1 = ''

       logging.captureWarnings(True)
       logger = logging.getLogger()
       logging.basicConfig(handlers=[logging.handlers.RotatingFileHandler('risdbquery.log', maxBytes=1000000, backupCount=10)],
              format='%(asctime)s %(levelname)s:%(message)s', level=logging.ERROR)
       logger.critical("risdbquery version 1.0.1")
       sys.stdout.write("risdbquery version 1.0.1\n")
       logger.critical('log level set to ERROR')
       sys.stdout.write("log level set to ERROR\n")

       #consolelog = logging.getLogger('console')
       sys.stdout.write("Getting configuration information from " + configfile + '\n')

       try:
              opts, args = getopt.getopt(argv,"hc:o:v:d:l:n:f:p:s:g",["help","deviceclass=","out=","version=","delimiter=","loglevel=","nohttp",
                     "firmware=","phonemodel=","comparestatus", "file1=", "getmodel"])
       except:
              logger.critical('FATAL ERROR Invalid Options')
              sys.stdout.write('FATAL ERROR Invalid Options\n')
              logger.critical('risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>')
              sys.stdout.write('risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>\n')
              sys.exit()
       else:
              for opt, arg in opts:
                     if opt in ('-h', "--help"):
                            logger.critical(
                                   'risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>')
                            sys.stdout.write('risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>\n')
                            sys.exit()
                     elif opt in ("-c", "--deviceclass"):
                            deviceclass = arg
                            if deviceclass.upper() == 'PHONE':
                                   deviceclass = 'Phone'
                            elif deviceclass.upper() == 'GATEWAY':
                                   deviceclass = 'Gateway'
                            elif deviceclass.upper() == 'H323':
                                   deviceclass = 'H323'
                            elif deviceclass.upper() == 'CTI':
                                   deviceclass = 'Cti'
                            elif deviceclass.upper() == 'VOICEMAIL':
                                   deviceclass = 'Voicemail'
                            elif deviceclass.upper() == 'MEDIARESOURCES':
                                   deviceclass = 'MediaResources'
                            elif deviceclass.upper() == "SIPTRUNK":
                                   deviceclass = 'SIPTrunk'
                            elif devicelcass.upper() == 'HUNTLIST':
                                   deviceclass = 'HuntList'
                            else:
                                   logger.critical('Supported deviceclass values are Phone, Gateway, H323, Cti, Voicemail, MediaResources, SIPTrunk, and HuntList')
                                   sys.stdout.write('Supported deviceclass values are Phone, Gateway, H323, Cti, Voicemail, MediaResources, SIPTrunk, and HuntList\n')

                                   sys.exit()
                            logger.critical('deviceclass is ' + deviceclass)
                     elif opt in ("-o", "--out"):
                            outfile = arg
                            logger.critical('output file is ' + outfile)
                     elif opt in ("v", "--version"):
                            version = arg
                            logger.critical('version is ' + version)
                     elif opt in ("-d", "--delimiter"):
                            delimiter = arg
                     elif opt in ("-l", "--loglevel"):
                            loglevel = arg.upper()
                            logger.critical('log level requested is ' + loglevel)
                            if loglevel == 'DEBUG':
                                   logger.setLevel(logging.DEBUG)
                            elif loglevel == 'INFO':
                                   logger.setLevel(logging.INFO)
                            elif loglevel == 'WARNING':
                                   logger.setLevel(logging.WARNING)
                            elif loglevel == 'ERROR':
                                   logger.setLevel(logging.ERROR)
                            elif loglevel == 'CRITICAL':
                                   logger.setLevel(logging.CRITICAL)
                            else:
                                   logger.critical('FATAL ERROR')
                                   logger.critical('valid log level values are DEBUG, INFO, WARNING, ERROR, and CRITICAL')
                                   sys.stdout.write('FATAL ERROR\n')
                                   sys.stdout.write('valid log level values are DEBUG, INFO, WARNING, ERROR, and CRITICAL\n')
                                   sys.exit()
                            logger.critical('log level changed to ' + loglevel)
                            sys.stdout.write('log level changed to ' + loglevel + '\n')

                     elif opt in ("-n", "--nohttp"):
                            checkforhttp = True
                            logger.critical('checking for phones without http server enabled')
                     elif opt in ("-f", "--firmware"):
                            checkfirmware = True
                            firmware = arg
                            logger.critical("checkfirmware = " + str(checkfirmware))
                            logger.critical("Firmware = " + firmware)
                     elif opt in ("-p", "--phonemodel"):
                            phonemodel = arg
                            logger.critical("Phone Model = " + arg)
                     elif opt in ("-s", "--comparestatus"):
                            comparestatus = True
                            logger.critical("comparestatus set to " + str(comparestatus))
                     elif opt in ("--file1"):
                            file1 = arg
                            logger.critical("Source file for comparison is " + file1)
                     elif opt in ('-g', "--getmodel"):
                            getmodel = True
                            logger.critical("Getting Phone Model")
                     else:
                            logger.critical('FATAL ERROR Invalid Options')
                            sys.stdout.write('FATAL ERROR Invalid Options\n')
                            logging.critical('risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>')
                            sys.stdout.write('risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>\n')
                            sys.exit()
       if deviceclass != '' and outfile != '':
              if os.path.isfile(configfile):
                     readconfigfile(configfile)
                     if cucmserver != '' and username != '' and password != '':
                            #file = open(sqlfile, "r")
                            #sqlquery = file.read()
                            sendrisdbquery()
                     else:
                            logger.critical('config cucmconfig.ini file required as below')
                            logger.critical('')
                            logger.critical('[cucm]')
                            logger.critical('server = cucmaxlserver.domain.suffix')
                            logger.critical('username = cucmaxluser')
                            logger.critical('password = cucmaxlpassword')
                            sys.stdout.write('config cucmconfig.ini file required\n')

              else:
                     logger.critical('config cucmconfig.ini file required as below')
                     logger.critical('')
                     logger.critical('[cucm]')
                     logger.critical('server = cucmaxlserver.domain.suffix')
                     logger.critical('username = cucmaxluser')
                     logger.critical('password = cucmaxlpassword')
                     sys.stdout.write('config cucmconfig.ini file required\n')

       else:
              logger.critical('risdbquery.exe --version <cucmversion> --sql <sqlfile.txt> --out <outfile.txt>')
              sys.stdout.write('risdbquery.exe --version <cucmversion> --sql <sqlfile.txt> --out <outfile.txt>\n')

       #sendrisdbquery()

def sendrisdbquery():
       global cucmserver, username, password, checkforhttp, checkfirmware, firmware, phonemodel, comparestatus, devices, axl, \
              getmodel, allphones, phonereport

       logger.critical("Device Class = " + deviceclass)
       sys.stdout.write("Device Class = " + deviceclass + '\n')

       ris = Ris(host=cucmserver, user=username, password=password, verify=False)

       if deviceclass == 'Phone':
              sys.stdout.write("Sending AXL query\n")
              wsdlpath = 'wsdl/cucmversion/' + version + '/AXLAPI.wsdl'
              #sys.stdout.write("wsdl " + wsdlpath)
              axl = Axl(host=cucmserver, user=username, password=password, wsdl=wsdlpath, verify=False)
              searchcriteria = {'name': '%'}
              returntags = {'name': '', 'model': ''}
              allphones = axl.list('phone', searchcriteria, rt=returntags)
              #sys.stdout.write("Assigning AXL output to list\n")
              fivek_names = [(p.name) for p in allphones][:10000]
              sys.stdout.write("Sending RisDB query\n")
              devices = ris.select_phones_by_name(fivek_names, status = 'Any')
              #for future version converting to dictionaries to make code faster and easier to follow
              #phonereport = {p.name: {'ip address': 'Unknown', 'status': 'Not in RisDB'} for p in allphones}
       else:
              sc = dict(DeviceClass=deviceclass, Status='Any', SelectBy='Name', SelectItems={'item': [{'Item': '*'}]})
              devices = ris.SelectCmDeviceResult(selection_criteria=sc)


       numdevices = str(len(devices))
       logger.critical('Number of Devices ' + numdevices)
       sys.stdout.write('Number of Devices ' + numdevices + '\n')

       logger.debug(devices)
       file_out = open(outfile,'w', newline='')

       if delimiter == 'tab':
              logger.critical('Writing tab delimited file')
              sys.stdout.write('Writing tab delimited file\n')
              outwriter = csv.writer(file_out, delimiter='\t')
       else:
              logger.critical('Writing csv file')
              sys.stdout.write('Writing csv file\n')
              outwriter = csv.writer(file_out)
       devicenum = 0

       if comparestatus != True:
              statusindicator = 0
              for device in devices:
                     #if (getmodel == True):
                     #       if (statusindicator < 80):
                     #              sys.stdout.write('!')
                     #              statusindicator += 1
                     #       else:
                     #              statusindicator = 0
                     #              sys.stdout.write('!\n')


                     if len(device.IPAddress) > 0:
                            deviceIPAddressObject = device.IPAddress[0]
                            deviceIPAddress = deviceIPAddressObject.IP
                            logger.debug("Device IP Address is " + deviceIPAddress)
                     else:
                            logger.debug("Device has no IP Address")
                            deviceIPAddress = ''

                     if devicenum == 0:

                            if deviceclass == 'Phone':
                                   logger.critical("Device Class is Phone")
                                   if (getmodel == True):
                                          outwriter.writerow(["Device Class", "Model", "Name", "IP", "Protocol", "Status", "Description", "Number",
                                                 "Number Of Lines", "Web Server","CTI Controllable", "Log In UserID", "Active Load", "Inactive Load",
                                                 "Download Server", "Download Status", "Download Failure Reason"])

                                          namesandmodels = [(p.name, p.model) for p in allphones][:10000]
                                   else:
                                          outwriter.writerow(["Device Class", "Name", "IP", "Protocol", "Status", "Description", "Number",
                                                 "Number Of Lines", "Web Server","CTI Controllable", "Log In UserID", "Active Load", "Inactive Load",
                                                 "Download Server", "Download Status", "Download Failure Reason"])
                                   if checkfirmware == True and (firmware == '' or phonemodel ==''):
                                          logger.critical("Cannot Check Firmware without setting firmware value and firmware prefix")
                                          sys.stdout.write("Cannot Check Firmware without setting firmwre value and firmware prefix\n")
                                          sys.exit()
                                   elif (checkfirmware == False):
                                          logger.debug("Not Checking Firmware")

                            else:
                                   outwriter.writerow(["Device Class", "Name", "IP", "Status", "Description", "Number"])\

                                   outwriter.writerow([device.DeviceClass, device.Name, deviceIPAddress, device.Protocol, device.Status,
                                          device.Description, device.DirNumber])

                            devicenum += 1
                     #else:
                     if deviceclass == 'Phone':
                            #logger.debug('check firmware = ' + str(checkfirmware) + ' phonemodel = ' + phonemodel
                             #      + ' axlphonemodel = ' + axlphonemodel + ' firmware = ' + firmware + 'device.ActiveLoadID = ' + str(device.ActiveLoadID))
                            if (getmodel == True):
                                   axlphone = list(filter(lambda x: device.Name in x, namesandmodels))
                                   axlphonemodel = axlphone[0][1]
                            else:
                                   axlphonemodel = ''

                            if ((checkforhttp == True and device.Httpd == 'No' and device.Name[:3] == 'SEP')
                                   or (checkfirmware == True and axlphonemodel == phonemodel and device.ActiveLoadID != firmware)
                                   or (checkfirmware == False and checkforhttp == False)):

                                   #sys.stdout.write('inside loop where info doesn\'t match')

                                   if (checkfirmware == True):
                                          logger.info("firmware = " + firmware + " Active Load = " + str(
                                                 device.ActiveLoadID))
                                          logger.info("phonemodel = " + str(phonemodel) + " axlphonemodel = " + str(
                                                 axlphonemodel))

                                   if (getmodel == True):
                                          axlphone = list(filter(lambda x: device.Name in x, namesandmodels))
                                          axlphonemodel = axlphone[0][1]

                                          outwriter.writerow(
                                                 [device.DeviceClass, axlphonemodel, device.Name, deviceIPAddress, device.Protocol,
                                                  device.Status, device.Description, device.DirNumber, device.NumOfLines,
                                                  device.Httpd,device.IsCtiControllable, device.LoginUserId, device.ActiveLoadID,
                                                  device.InactiveLoadID, device.DownloadServer, device.DownloadStatus,
                                                  device.DownloadFailureReason])
                                   else:
                                          outwriter.writerow(
                                                 [device.DeviceClass, device.Name, deviceIPAddress, device.Protocol,
                                                  device.Status, device.Description, device.DirNumber, device.NumOfLines,
                                                  device.Httpd, device.IsCtiControllable, device.LoginUserId, device.ActiveLoadID,
                                                  device.InactiveLoadID, device.DownloadServer, device.DownloadStatus,
                                                  device.DownloadFailureReason])




                     else:
                            outwriter.writerow([device.DeviceClass, device.Name, deviceIPAddress, device.Protocol, device.Status,
                                   device.Description, device.DirNumber])


                     #logger.critical("LineStatus " + str(device.LinesStatus))
       else:
              comparestatusfromfile()


def comparestatusfromfile():
       global file1, devices, phonereport
       logger.critical("Opening " + file1 + " For Comparison with current status")
       sys.stdout.write("Opening " + file1 + " for Comparison with current status\n")
       originalfile = open(file1,'r', newline='')
       if delimiter == 'tab':
              logger.critical('Reading and Writing tab delimited file')
              sys.stdout.write('Reading and Writing tab delimited file\n')
              reader = csv.DictReader(originalfile, delimiter='\t')
       else:
              logger.critical('Reading and Writing csv file')
              sys.stdout.write('Readig and Writing csv file\n')
              reader = csv.DictReader(originalfile)
       devicenum = 0
       #logger.critical(reader)

       file_out = open(outfile,'w', newline='')
       if delimiter == 'tab':
              #logger.critical('Writing tab delimited file')
              #sys.stdout.write('Writing tab delimited file\n')
              outwriter = csv.writer(file_out, delimiter='\t')
       else:
              #logger.critical('Writing csv file')
              #sys.stdout.write('Writing csv file\n')
              outwriter = csv.writer(file_out)
       devicenum = 0
       logger.info(devices)
       currentdevices = [(d.Name, d.Status) for d in devices][:10000]

       logger.info("current devices")
       logger.info(currentdevices)
       phoneloopcount = 0
       sys.stdout.write("Comparing Reading Status From File To Comparing To Current Status\n")
       for phone in reader:

              #if (phoneloopcount < 80):
              #       sys.stdout.write('!')
              #       phoneloopcount += 1
              #else:
              #       sys.stdout.write('!\n')
              #       phoneloopcount = 1

              #logger.critical("Device Name " + phone["Name"] + " Status " + phone["Status"])
              if (devicenum == 0):
                     outwriter.writerow(["Original Name", "Original Status", "Matching Name", "Current Status"])
              devicefound = False

              currentdevice = list(filter(lambda x: phone["Name"] in x, currentdevices))
              #logger.critical("lambda output")
              logger.critical(currentdevice)
              if currentdevice != []:
                     logger.info("Current Device Status is " + str(currentdevice[0][1]))
                     devicename = currentdevice[0][0]
                     devicestatus = currentdevice[0][1]
                     devicefound == True
              else:
                     devicename = 'Not Found'
                     devicestatus = 'Unknown'
                     devicefound == False

              logger.info("Comparison Data: Original Device " + phone["Name"] + ' Original Status ' + phone["Status"] + ' Found Device Name ' +
                     devicename +  'Current Status ' + devicestatus)

              if ((phone["Status"] == "Registered") and (devicestatus == "UnRegistered")):
                     logger.info("Original Device Name " + phone["Name"] + " Original Status " + phone["Status"] +
                                 " Current Device name " + devicename + " Current Device Status " + devicestatus)
                     outwriter.writerow([phone["Name"], phone["Status"], devicename, devicestatus])


              #for device in devices:
              #       if (phone["Name"] == device.Name):
              #              devicefound = True
              #              logger.info("Comparison Data " + phone["Name"] + ' ' + device.Name + ' ' + phone[
              #                     "Status"] + ' ' + device.Status)
              #              if ((phone["Status"] == "Registered") and (device.Status == "UnRegistered")):
              #                     logger.info("Original Device Name " + phone["Name"] + " Original Status " + phone["Status"] +
              #                            " Current Device name " + device.Name + " Current Device Status " + device.Status)
              #                     outwriter.writerow([phone["Name"], phone["Status"], device.Name, device.Status])
              #              break
              #if (devicefound == False and phone["Status"] == 'Registered'):
              #       outwriter.writerow([phone["Name"], phone["Status"], 'Not in RIS DB', 'Unregistered'])

              devicenum += 1

       logger.critical("Processed " + str(devicenum) + " Phones")
       sys.stdout.write("Processed " + str(devicenum) + " Phones\n")




def readconfigfile(configfile):
       global cucmserver, username, password
       config = configparser.ConfigParser()
       config.read('cucmconfig.ini')
       cucmserver = config['cucm']['server']
       username = config['cucm']['username']
       password = config['cucm']['password']
       logger.critical('cucmserver = ' + cucmserver)
       logger.critical('username = ' + username)
       logger.critical('password = ' + password)


if __name__ == "__main__":
       main(sys.argv[1:])

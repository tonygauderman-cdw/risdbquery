import sys, getopt
import json, csv
import configparser
import os, logging, logging.handlers

sys.path.insert(1,'../python-ucmapi/build/lib/')
from ucmapi import Ris


configfile = 'cucmconfig.ini'
delimiter = 'comma'
deviceclass = ''
outfile = ''
version = ''
cucmserver = ''
username = ''
password = ''

def main(argv):
       global deviceclass, outfile, version, delimiter, logger
       logger = logging.getLogger()
       logging.basicConfig(handlers=[logging.handlers.RotatingFileHandler('risdbquery.log', maxBytes=1000000, backupCount=10)],
              format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
       consolelog = logging.StreamHandler()
       consolelog.setLevel(logging.CRITICAL)
       logger.addHandler(consolelog)
       logger.critical("risdbquery version 1.00")
       logger.critical('log level set to INFO')

       logger = logging.getLogger()
       #consolelog = logging.getLogger('console')

       try:
              opts, args = getopt.getopt(argv,"hc:d:l",["help","deviceclass=","out=","delimiter=","loglevel="])
       except:
              logger.critical('FATAL ERROR')
              logging.critical('risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>')
              sys.exit()
       else:
              for opt, arg in opts:
                     if opt in ('-h', "--help"):
                            logger.critical('FATAL ERROR')
                            logging.critical(
                                   'risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>')
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
                                   sys.exit()
                            logger.info('deviceclass is ' + deviceclass)
                     elif opt in ("-o", "--out"):
                            outfile = arg
                            logger.info('output file is ' + outfile)
                     elif opt in ("-d", "--delimiter"):
                            delimiter = arg
                     elif opt in ("-l", "--loglevel"):
                            loglevel = arg.upper()
                            logger.info('log level requested is ' + loglevel)
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
                                   sys.exit()
                            logger.critical('log level changed to ' + loglevel)
                     else:
                            logger.critical('FATAL ERROR')
                            logging.critical(
                                   'risdbquery.exe --deviceclass <deviceclass> --out <outfile.txt>')
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
              else:
                     logger.critical('config cucmconfig.ini file required as below')
                     logger.critical('')
                     logger.critical('[cucm]')
                     logger.critical('server = cucmaxlserver.domain.suffix')
                     logger.critical('username = cucmaxluser')
                     logger.critical('password = cucmaxlpassword')

       else:
              logger.critical('risdbquery.exe --version <cucmversion> --sql <sqlfile.txt> --out <outfile.txt>')
       #sendrisdbquery()

def sendrisdbquery():
       global cucmserver, username, password
       from ucmapi import Ris
       wsdlpath = 'wsdl/' + cucmserver + '.wsdl'
       logger.critical("Device Class = " + deviceclass)
       logger.info('wsdlpath = ' + wsdlpath)
       ris = Ris(host=cucmserver, user=username, password=password, verify=False)
       sc = dict(DeviceClass=deviceclass, Status='Any', SelectBy='Name', SelectItems={'item': [{'Item': '*'}]})
       devices = ris.SelectCmDeviceResult(selection_criteria=sc)
       file_out = open(outfile,'w', newline='')
       if delimiter == 'tab':
              logger.critical('Writing tab delimited file')
              outwriter = csv.writer(file_out, delimiter='\t')
       else:
              logger.critical('Writing csv file')
              outwriter = csv.writer(file_out)
       devicenum = 0
       for device in devices:
              if len(device.IPAddress) > 0:
                     #logger.info("phone ip " + phone.IPAddress[0])
                     logger.info(device.IPAddress[0])
                     deviceIPAddressObject = device.IPAddress[0]
                     deviceIPAddress = deviceIPAddressObject.IP
              else:
                     deviceIPAddress = ''

              if devicenum == 0:

                     if deviceclass == 'Phone':
                            outwriter.writerow(["Device Class", "Name", "IP", "Protocol", "Status", "Description", "Number", "Number Of Lines", "Web Server",
                                   "CTI Controllable", "Log In UserID", "Active Load", "Inactive Load", "Download Server", "Download Status", "Download Failure Reason"])

                            outwriter.writerow([device.DeviceClass, device.Name, deviceIPAddress, device.Protocol, device.Status, device.Description, device.DirNumber,
                                   device.NumOfLines, device.Httpd, device.IsCtiControllable, device.LoginUserId, device.ActiveLoadID, device.InactiveLoadID,
                                   device.DownloadServer, device.DownloadStatus, device.DownloadFailureReason])
                     else:
                            outwriter.writerow(["Device Class", "Name", "IP", "Status", "Description", "Number"])\

                            outwriter.writerow([device.DeviceClass, device.Name, deviceIPAddress, device.Protocol, device.Status,
                                   device.Description, device.DirNumber])

                     devicenum += 1
              else:
                     if deviceclass == 'Phone':
                            outwriter.writerow([device.DeviceClass, device.Name, deviceIPAddress, device.Protocol, device.Status, device.Description, device.DirNumber,
                                   device.NumOfLines, device.Httpd, device.IsCtiControllable, device.LoginUserId, device.ActiveLoadID, device.InactiveLoadID,
                                   device.DownloadServer, device.DownloadStatus, device.DownloadFailureReason])
                     else:
                            outwriter.writerow([device.DeviceClass, device.Name, deviceIPAddress, device.Protocol, device.Status,
                                   device.Description, device.DirNumber])

              logger.info(device.IPAddress)

              logger.info("LineStatus " + str(device.LinesStatus))
              logger.info("DownloadServer " + str(device.DownloadServer))


def readconfigfile(configfile):
       global cucmserver, username, password
       config = configparser.ConfigParser()
       config.read('cucmconfig.ini')
       cucmserver = config['cucm']['server']
       username = config['cucm']['username']
       password = config['cucm']['password']
       logger.info('cucmserver = ' + cucmserver)
       logger.info('username = ' + username)
       logger.info('password = ' + password)


if __name__ == "__main__":
       main(sys.argv[1:])

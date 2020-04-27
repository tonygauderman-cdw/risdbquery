risdbquery Version 1.00

Released 4/26/2020

This command line tool allows you to send a risdbquery to a CUCM cluster and log the output to a csv or tab delimited file

Supported CUCM Versions:
10.0, 10.5, 11.0, 11.5, 12.0, 12.5


Required Parameters:
--deviceclass (-c)	Reduired - Device to run against.  Can be Phone, Gateway, H323, Cti, Voicemail, MediaResources, SIPTrunk, or HuntList
--out (-o)          	Required - Output file

Optional Paramegers:
--delimiter (-d)    Optional - delimiter - tab or comma
--loglevel (-l)     Optional - loglevel DEBUG, INFO, WARNING, ERROR
Use:
risdbquery.exe --deviceclass <device_class> --out <file_to_write_to>

Config File Required:
cucmconfig.ini must exist and contain the hostname/ip of an AXL server as well as axl username and password in the following format

[cucm]
server = cucmaxlserver.domain.suffix
username = cucmaxluser
password= cucmaxlpassword

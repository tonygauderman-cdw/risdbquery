risdbquery Version 1.00

Released 4/26/2020

This command line tool allows you to send a risdbquery to a CUCM cluster and log the output to a csv or tab delimited file

Supported CUCM Versions:
10.0, 10.5, 11.0, 11.5, 12.0, 12.5


Required Parameters:
--deviceclass (-c)	Reduired - Device to run against.  Can be Phone, Gateway, H323, Cti, Voicemail, MediaResources, SIPTrunk, or HuntList
--out (-o)          Required - Output file
--version           Required - Major CUCM Version

Optional Paramegers:
--delimiter (-d)    Optional - delimiter - tab or comma
--loglevel (-l)     Optional - loglevel DEBUG, INFO, WARNING, ERROR
--comparision       Optional - Used with --file1 to compare states to a previous file
--file1             Optional - Used with --comparison to compare states to a previous file
--getmodel          Optional - Uses AXL to get phone model from CUCM
--phonemodel        Optional - ex. "Cisco 8841" - Used with --firmware to get list of phones that don't have specific firmware
--firmware          Optional - ex. "sip88xx.12-6-1-0101-692" - Used with --phonemodel to get list of phones that don't match specific firmware

Use:

Get RisDB List of All Phones
risdbquery.exe --deviceclass <device_class> --out <file_to_write_to>

Get list of phones by model who are not using specified firmware
risdbquery --deviceclass Phone --version 10.5 --getmodel --firmware "sip88xx.12-6-1-0101-692" --phonemodel "Cisco 8841" --out risdb-out.csv

Compare current status to previous status in a file
risdbquery --deviceclass Phone --version 10.5 --comparestatus --file1 risdb-20200528-164855.csv --out risdb-out.csv


Config File Required:
cucmconfig.ini must exist and contain the hostname/ip of an AXL server as well as axl username and password in the following format

[cucm]
server = cucmaxlserver.domain.suffix
username = cucmaxluser
password= cucmaxlpassword

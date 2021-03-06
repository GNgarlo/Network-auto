#/usr/bin/python3.9
from netmiko.ssh_dispatcher import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException, NetmikoTimeoutException
import os
import re

from getpass import getpass

from netmiko.nokia.nokia_sros_ssh import NokiaSrosSSH

with open("inventario.txt") as olts:
    for IP in olts:
        olts = {
            'device_type' : 'nokia_sros',
            'host' : IP,
            'username' : 'xxxx',
            'password' : 'xxxxx' 
        }
        print('Connecting to:' + IP )
        net_connect = ConnectHandler(**olts)
        Outname = net_connect.send_command('info configure system | match exact:name | match before exact:map')
        Outid = net_connect.send_command('info configure system | match exact:id | match before exact:loop')
        Outwelcome = net_connect.send_command ('info configure system | match exact:welcome')

        print('For the: ',IP)
        print('Systema name: ',Outname)
        print('System id: ',Outid)
        print('Banner: ',Outwelcome)

        BKP = open('BackupNamesOLTs.txt','a')
        print(IP,'\nSystem name: ',Outname,'\nSystem ID: ',Outid, '\nBanner: ',Outwelcome,'\n','#'*80, file=BKP)
        BKP.close()

        print('#'*50)

        if Outname == '':
            name = input("The Systema name is empty, please type the correct name: ")
            Inname = net_connect.send_config_set('configure system name' + name, cmd_verify=True)
            print('Done')
        else:
            pass

        if Outid == '':
            idval = input("The System id is empty, please type the correct id: ")
            Inval = net_connect.send_config_set('configure system id ' + idval, cmd_verify=True)
            print('Done')
        else:
            pass
        
        lid = Outid.rsplit()
        lname = Outname.rsplit()

        if lid[1] != lname[1]:
            dif = input("The System Id and name are different, please type the correct one: ")
            indif = net_connect.send_config_set('configure system id ' + dif, cmd_verify=True)
            print('Done')
        else:
            pass

        if Outwelcome == '':
            welval = input("The welcome baner is empty, please type the correct one: ")
            inwel = net_connect.send_config_set('configure system security welcome-banner ' + welval, cmd_verify=True)
            print('Done')
        else:
            pass
    
    print('/'*50,'\nConfig complete\n','/'*50)
    
    net_connect.disconnect()


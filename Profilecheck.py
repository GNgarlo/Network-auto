#/usr/bin/python3.9
from netmiko.ssh_dispatcher import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException, NetmikoTimeoutException
import os

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
        output = net_connect.send_command('info configure qos profiles scheduler-node flat | match exact:down')
        output2 = net_connect.send_command('info configure qos profiles shaper flat | match exact:shaper')

        print('QoS Shaper profile:\n',output2)
        temp2 = open('temp-shaper.txt', 'w')
        print(output2, file=temp2)
        temp2.close()

        print('#'*10)

        resultadoshaper = output2.splitlines()
        x2 = (len(resultadoshaper))
        print(x2)

        print('#'*10)

        if x2 < 13:

            print('The shaper profile is not complete \n' 'The line missing is: \n')

            with open('shapertemplate.txt', 'r') as file1:
                with open('temp-shaper.txt', 'r') as file2:
                    same = set(file1).difference(file2)
                       
                same.discard('\n')

            with open('salida.txt', 'w') as fileout:
                for line in same:
                    fileout.write(line)
                    print(line)
            
            fileout.close()
            file1.close()
            file2.close()
        
            print('Saving the config... \n')

            archivo = open('backup.txt', 'a')
            print("Backup of "+ IP,"\n", output, file=archivo)
            archivo.close()

            print('Applying config profiles')
            conff = open('salida.txt')
            conffset = conff.read()
            line = net_connect.send_config_set(conffset, cmd_verify=False)
            print(line)
            conff.close()
            print(':'*20, '\n Config Applied \n', ':'*20)
                
        else:
             pass

        print('QoS profile scheduler-node:\n',output)
        temp = open('temp.txt', 'w')
        print(output, file=temp)
        temp.close()

        print('#'*10)

        resultado = output.splitlines()
        x = (len(resultado))
        print(x)

        print('#'*10)


        if x < 13:

            print('The scheduler-node profile is not complete \n' 'The line missing is: \n')

            with open('schedulerTemplate.txt', 'r') as file1:
                with open('temp.txt', 'r') as file2:
                    same = set(file1).difference(file2)
                       
                same.discard('\n')

            with open('salida.txt', 'w') as fileout:
                for line in same:
                    fileout.write(line)
                    print(line)
            
            fileout.close()
            file1.close()
            file2.close()
        
            print('Saving the config... \n')

            archivo = open('backup.txt', 'a')
            print("Backup of "+ IP,"\n", output, file=archivo)
            archivo.close()

            print('Applying config profiles')
            conff = open('salida.txt')
            conffset = conff.read()
            line = net_connect.send_config_set(conffset, cmd_verify=False)
            print(line)
            conff.close()
            print(':'*20, '\n Config Applied \n', ':'*20)
                
        else:
             pass

    print('*'*100)

net_connect.disconnect()

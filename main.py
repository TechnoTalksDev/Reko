import os
from colorama import Fore
#try getting bot
try:
    from src.bot import bot
except Exception as e:
    if e == KeyboardInterrupt:
        pass
    else:
        print(Fore.RED+"[Error] Something fatal occured in the bot."+Fore.RESET)
        print(e)
#dotenvs
from dotenv import load_dotenv

#Load Token
try: 
    load_dotenv("src\secrets\.env")
except: 
    pass
token = os.getenv("TOKEN")
#Run bot
if __name__ == "__main__":
    try: 
        bot.run(token)
    except:
        pass
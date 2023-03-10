import os, coloredlogs, logging, traceback
from colorama import Fore

#Setup logging so we know what the fuck is going on
coloredlogs.install(level="INFO", fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s")
logger = logging.getLogger("Reko")
file_handler = logging.FileHandler("SEVERE.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"))
logger.addHandler(file_handler)

#try getting bot
try:
    from src.bot import bot
except Exception as e:
    if e == KeyboardInterrupt:
        pass
    else:
        logging.critical("Something fatal occured in the bot")
        logger.error(traceback.format_exc())
#dotenvs
from dotenv import load_dotenv

#Load Token
load_dotenv("src/secrets/.env")
token = os.getenv("TOKEN")

#Run bot
if __name__ == "__main__":
    try:
        bot.run(token)
    except:
        pass
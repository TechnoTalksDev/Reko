<p align="center">
  <img width="700" src="https://www.technotalks.net/static/main/images/rekobanner.png" alt="Reko Banner">
</p>
<h1 align="center">
	Reko (Formerly: Project MSS) 
</h1>


<p align="center">
	<strong>A Minecraft Server Status discord bot! WIP!</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/docker/v/technotalks/reko?color=blue">
  <img src="https://img.shields.io/github/issues/technotalksdev/reko">
  <img src="https://img.shields.io/github/last-commit/technotalksdev/reko">
</p>

> I'm back!

## Key Features
- Get **player count**, **online players** (To-Do), **server version**, and **motd**
- Get **latency** to server (ping from bot to server)
- Get the **approximate location**
- Set a server for your **guild to track**
- **Updating Chart** of player count and other info (To-Do)
- **Player stats** (Planned)
- Track when **players join and leave** (To-Do)
- **@Online Players role** automatically assigned to online players on the server (To-Do)
- _Hack Minecraft Servers_ (_This is a joke...I think_)
## To-Do list
If you would like to **contribute**, or just want to see **upcoming features**, then take a look at the [To-do](https://github.com/users/TechnoTalksDev/projects/3) list!
## Website
**Reko has a website now!** Go check it out! [Link](https://reko.technotalks.net/)
## Setup
I request that if you want to test the main bot that you don't run a seperate instance of the bot and instead just [invite](https://reko.technotalks.net/) it. If your are developing or contributing to the bot then please go ahead!

**Dependencies** and **enviroment variables**:
1. Installing dependencies (Really quite simple because of... you guessed it! **_Poetry_**!)
	- You do need to **[install poetry](https://python-poetry.org/docs/#installation)** first!
	- Then simply run `poetry install`!
	- Poetry will then do all the work and install all the packages and their dependencies for you!
	- **Note:** If your using an editor like VSCode and don't want to manually change the venv path then you can look into [this poetry config option](https://python-poetry.org/docs/configuration/#virtualenvsin-project) which creates the **venv in the project directory** simplifying things
2. Setting up **enviroment variables**
	- Please create and .env file in the secrets folder with the variable TOKEN
	- And a [proper connection uri](https://pymongo.readthedocs.io/en/4.1.1/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient) in the MONGO_LINK variable. 
	- Please do not include quotes around the variables.
```
TOKEN=A123C456B7890
MONGO_LINK=localhost:27017
```

## Licence/Terms of use
I present to you the **GNU Affero General Public License**! Please browse through the license for basic info. If you plan on publishing your forked version (with valid and extensive changes), please make sure to run it by me once (You can contact me through my [Discord Server](https://discord.gg/8vNHAA36fR)), I would love to see what you've done with the bot!.
## Thanks
Thanks for viewing the repo I will update the bot (and this readme) and make it better in the future! 

PS: Go add the bot! Link on the [website](https://reko.technotalks.net/)!

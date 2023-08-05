# Dirvish Telegram Bot
This is a simple telegram-bot for the backupsoftware [dirvish](http://www.dirvish.org/) that will notify you if a backup has failed.

## Features
- Register with the bot
- add user to the bot (unregistered users are not able to do anything)
- subscribe/unsubscribe to failed backup notification
- show the current backup status

## Installation
To install this bot you have to run one of the following commands:
```
pip install dirvishbot
```
or
```
git clone https://github.com/jkuettner/dirvishbot.git && cd dirvishbot && pip install .
```

## Update
To update simply run
```
pip install --upgrade dirvishbot
```
or
```
git clone https://github.com/jkuettner/dirvishbot.git && cd dirvishbot && pip install --upgrade .
```

## Configuration
### 1. Create a new telegram bot
- Start conversation with `@botfather`
- Send `/newbot` and follow the instructions of `@botfather` until you got your bot token.

Further informations about how to create a new bot: https://core.telegram.org/bots#create-a-new-bot
### 2. Create `config.json`
You have to create a config.json with the telegram bot token in it. To do this you could copy the `config.example.json` to `/etc/dirvishbot/config.json` and replace the example `api_token` with yours:
```
cp /etc/dirvishbot/config.example.json /etc/dirvishbot/config.json
```
The `config.json` should look like the following:
```
{
    "api_token": "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
}

```
### 3. Trigger dirvishbot after the backup-process
The dirvishbot listens to the signal `SIGUSR1` to check the state of all backups and informs all subscribers if one of the backups has failed.

With the following line the dirvishbot will be notified:
```
bash -c 'kill -s SIGUSR1 $(< /var/run/dirvishbot.pid)'
```
You can put this line just before `exit $rc` in `/etc/dirvish/dirvish-cronjob` to start the backup-check after dirvish has finished.


## Run
If you have systemd installed the `dirvishbot.service` file will be placed to `/etc/systemd/system/dirvishbot.service` and you can start it with:
```
systemctl start dirvishbot
```
To check the status run
```
systemctl status dirvishbot
```

If you do not use `systemd` you can start this bot by running
```
dirvishbot &
```

## Usage
### First start
If you start the dirvishbot for the first time you have to register your telegram-user as admin.
To do this you need a token that will be saved in `/etc/dirvishbit/register`:

```
cat /etc/dirvishbot/register
```
```
This is your first start of the Bot.
Please register your admin-user within the next hour by sending the following to this Bot:
    /register <TOKEN>
```

After the first start you have one hour to register an admin-user with this bot until the token invalidates and you have to restart the bot to get a new token.

**Note that the first user that will send the `/register <TOKEN>` to your bot will become the administrator.**

To reset the bot simple stop it, delete the `config.json`-file and restart the bot.

### Commands
To run a command, send one of the following messages to your telegram-bot from your telegram-client:
- `/start`: Sends you a welcome message with an introduction (every user)
- `/register <TOKEN>`: registers the sender with this bot if `<TOKEN>` is valid. (every user)
- `/adduser`: generates a token for your contact that will be able to run the `/register`-command. The token invalidates after 24 hours. (only admins)
- `/subscribe`: enable notification of failed backups (every registered user)
- `/unsubscribe`: disable notification of failed backups (every registered user)
- `/status`: show the current status of all backups (every registered user)

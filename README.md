# sc3_bot_twitter
A bot tweeting SC3 helpfiles

Twitter account: [@sc3_bot](https://twitter.com/sc3_bot)

## Basic info and features
* The data are in `./bot-data/` and were copied from `/usr/share/SuperCollider/HelpSource`.  I deleted all other file extensions other than `*.schelp`.
* `sc3-bot.py` reads a random SC3 helpfile and tweets based on a cron task every 6 hours.
    * It reads the title and summary of the `schelp` file and tweets using the following format:
      * `<class OR title>: <summary> http://doc.sccode.org/<schelp-file-name>.html`
    * It keeps a log of posted help files in `./bot-data/history-sc3-bot.txt`, in order to secure unique posts.
    * It follows back new followers, and unfollows non-followers.
    * Tweets a single line sc-tweet from UGen help files, right after the help file tweet.

## TODO
* Write a function to update the weights in random selection based on history log file.

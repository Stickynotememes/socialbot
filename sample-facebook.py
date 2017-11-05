import sys, os, json
import logging as lg
import socialbot

basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
bot_type = basename.split("-")[1]

action = "posts"
if len(sys.argv) > 1:
    action = sys.argv[1]

with open("%s-targets.json" % basename, "r") as f:
    targets = json.load(f)

with open("%s-credentials.json" % basename, "r") as f:
    credentials = json.load(f)

cookies = None
try:
    with open("%s-cookies.json" % basename, "r") as f:
        cookies = json.load(f)
except:
    print("No cookie found")

whitelist = []
try:
    with open("%s-whitelist.json" % basename, "r") as f:
        whitelist = json.load(f)
except:
    print("No whitelist found")

blacklist = []
try:
    with open("%s-blacklist.json" % basename, "r") as f:
        blacklist = json.load(f)
except:
    print("No blacklist found")

# Instance bot

if bot_type == "twitter":
    bot = socialbot.Twitter(log_name=basename)
elif bot_type == "instagram":
    bot = socialbot.Instagram(log_name=basename)
else:
    bot = socialbot.Facebook(log_name=basename)

bot.record(True, "%s.log" % basename)
handler = lg.StreamHandler()
handler.setFormatter(bot.formatter)
handler.setLevel(lg.DEBUG)
bot.log.addHandler(handler)

# Login or use cookie

username = credentials["username"]

if cookies is not None:
    bot.set_cookies(cookies, bot_type)
else:
    bot.login(username, credentials["password"])

# Actions

if bot.logged():
    try:
        if action == "posts":
            # Display posts
            username = sys.argv[2]
            posts = bot.get_posts(username, max=1000)
            print(posts)

    except Exception as ex:
        print(ex)

# Save cookie

cookies = bot.browser.get_cookies()
with open("%s-cookies.json" % basename, "w") as f:
    json.dump(cookies, f)

# Quit

bot.quit()
print("Done")
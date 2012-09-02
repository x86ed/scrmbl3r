DOMAIN = 'encom511.local'
INSTALL = 'https://%s/' % DOMAIN
 # HTTPS is highly recommended! Using Cryptocat without HTTPS
 # in a production environment is a recipe for disaster.
 # You are severely warned against deploying Cryptocat
 # without HTTPS, unless the deployment is occurring as
 # a Tor Hidden Service.
SSL = True # formerly HTTPS
 # Chat storage directory. Needs to be writable by web server.
CHAT_LOGS = '/Users/laszlototh/Desktop/repos/git/cryptocat/data' #formerly data
 # directory for ssl certs
CERT_DIR = '/Users/laszlototh/Desktop/repos/git/cryptocat/certs'
# directory for sessions
SESSION_DIR = '/Users/laszlototh/Desktop/repos/git/cryptocat/sessions'
# directory for templates
TEMPLATE_DIR = '/Users/laszlototh/Desktop/repos/git/scrmbl3r/src/server/templates'
# session secret
SESSION_SECRET = "somethingreallyawesome"
 # session random number seed length (not currently used)
SESSION_ENTROPY_LENGTH = 1024
 # Maximum users in a chat. Untested above 10.
MAXIMUM_USERS = 12
 # Maximum characters per line (soft limit.)
MAXIMUM_MESSAGE_LENGTH = 256
 # Maximum encrypted file size in kilobytes (soft limit.)
 # Seems not to work above 700kb.
MAXIMUM_FILE_SIZE = 600
 # Time limit in seconds before overwriting chat.
TIME_LIMIT = 3600
 # Set to 0 to disable automatic URL linking.
AUTO_GENERATE_URLS = True
 # Default Nicknames
NICKNAMES = ['bunny', 'kitty', 'pony', 'puppy', 'squirrel', 'sparrow', 'turtle', 'kiwi', 'fox', 'owl', 'raccoon', 'koala', 'echidna', 'panther', 'sprite', 'ducky']
 # Timeout rate. You probably shouldn't touch this.
TIMEOUT = 80
 # regexp used for isaying if user is in chat or no
INFO_REG_EX = '(\>|\<)\s[a-z]{1,12}\shas\s(arrived|left)'
import yaml
from lookerapi import LookerApi
from datetime import datetime, timedelta
from pprint import pprint
import email.message
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

host = 'localhost'

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host, token=my_token, secret = my_secret)

# Build function for sending an email with a list of unused Looks to a user
def send_email(user_id,looker_email):
    # Search Looks for a particular user
    data = looker.search_looks(user_id)
    # Set number of days that Look hasn't been accessed
    n_days = 90
    date_n_days_ago = datetime.now() - timedelta(days=n_days)

    # Create the beginings of a table
    strTable = """
      <html>
        <head>
            <style type="text/css">
	            html { width: 100%; }
                p {font-family: "Arial"}
                th, td {padding: 5px;}
                table {table-layout: fixed; width: 70%; border-collapse: collapse; border: 1px solid purple;}
            </style>
          <body>
                <p>Hello Looker User,
                <p>Add something here to cajole the user to delete some redundant Looks...</p>
                <br>
                  <center>
                <table style="border: blue 1px solid;"><tr><th>Look Title</th><th>URL</th><th>Last Accessed</th></tr>
        """

    # initialize counter for loop
    i = 0

    # Build a simple HTML table to send with the email
    for x in data:
        url = 'https://<< hostname >>looker.com' + str(data[i]['short_url'])
        last_accessed_at_show = data[i]['last_accessed_at']
        last_accessed_at = data[i]['last_accessed_at']
        title = str(data[i]['title'])
        apply_style = ''
        if last_accessed_at is None:
            #if type(NoneType) change to an arbitray date string
            last_accessed_at = '2018-01-01T00:00:00.000+00:00'
        # convert str to datetime
        dt_obj = datetime.strptime(last_accessed_at, '%Y-%m-%dT%H:%M:%S.%f+00:00')
        if (dt_obj < date_n_days_ago):
            # Apply styling to the row if the Look hasn't been accessed in 90 days
            apply_style = ' bgcolor="#ff8080" '
        strRW = "<tr"+apply_style+"><td>"+title+"</td><td>"+url+ "</td><td>"+str(last_accessed_at_show)+"</td></tr>"
        strTable = strTable+strRW
        i += 1

    strTable = strTable+"""</table></body></html>"""

    # Construct an email
    msg = email.message.Message()
    msg['Subject'] = 'Looker FIX-UP'
    msg['From'] = '<<email address>>'
    msg['To'] = looker_email

    # Set credentials of Google "app" required for insecure application sending emails from the Google account
    password = "<<credentials for Google>>"

    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(strTable)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    # s.set_debuglevel(True) # show communication with the server
    s.starttls()

    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    # Send email
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    # Quit session
    s.quit()

# Replace this with a lsit of looker_user_id's to send an email to. This is to prevent emailing all users accidentally
looker_user_ids = '1,2,3'

# /GET search_users()
users = looker.get_all_users(looker_user_ids)

# Initialize counter for the loop as I didn't know a better way
n = 0

for x in users:
    looker_email = str(users[n]['email'])
    looker_user_id = str(users[n]['id'])
    display_name = str(users[n]['display_name'])
    # pass the user_id and email into send_email()
    send_email(looker_user_id,looker_email)
    n += 1

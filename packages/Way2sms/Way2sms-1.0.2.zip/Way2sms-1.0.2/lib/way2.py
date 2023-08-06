import urllib2
import cookielib
import csv
from os import path
file_path = path.expanduser('~')+r'\abook.csv'

class Way2sms:

    def __init__(self):
        self.cookies = cookielib.CookieJar()
        self.jession_id = ''
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

    def login(self, username, password):
        login_url = 'http://site24.way2sms.com/Login1.action?'
        params ='username='+username+'&password='+password
        headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64')]
        self.opener.addheaders=headers
        try:
            self.opener.open(login_url, params)

        except IOError:
            pass
        else:
            return True

    def send_sms(self, message, receipent):
        self.jession_id = str(self.cookies).split('~')[1].split(' ')[0]
        sms_url = 'http://site24.way2sms.com/smstoss.action?'
        sms_data = 'ssaction=ss&Token='+self.jession_id+'&mobile='+receipent+'&message='+message+'&msgLen=0'
        headers = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+self.jession_id)]
        self.opener.addheaders = headers
        try:
            sms_page = self.opener.open(sms_url, sms_data)
        except IOError:
            pass
        else:
            if 'Message has been submitted successfully' in sms_page.read():
                return 'Sms Sent'
            else:
                return 'Sms Sending Failed'

    def contacts(self, method, data=None):
        if 'GET' in method and path.exists(file_path):
            with open(file_path, 'rb') as fp:
                reader = csv.reader(fp)
                contacts = {item[0]: item[1] for item in reader}
            return contacts
        elif 'ADD' in method:
            with open(file_path, 'ab') as fp:
                w = csv.writer(fp)
                for keys in data:
                    w.writerow([keys, data[keys]])
        else:
            return {}


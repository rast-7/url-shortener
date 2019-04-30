from flask import Flask, render_template, request, redirect, url_for
from model import *
import string
import base64
from math import floor



try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

host = 'http://localhost:5000/'
short_url = ''
app = Flask(__name__)

def toBase62(num, b=62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + string.lowercase + string.uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res
    
def toBase10(num, b=62):
    base = string.digits + string.lowercase + string.uppercase
    limit = len(num)
    res = 0
    for i in xrange(limit):
        res = b * res + base.find(num[i])
    return res

@app.route('/',methods=['POST','GET'])
def home():
	if request.method == 'POST':
		db.connect()
		db.create_tables([weburls],safe=True)
		ourl = request.form.get('ur')
		if urlparse(ourl).scheme == '':
			ourl = 'http://'+ourl
		u = weburls.create(url = ourl)
		db.close()
		return render_template('back.html',short_url = host + toBase62(u.id))
	return render_template('home.html')
	 
@app.route('/<short_url>')
def redirect_short_url(short_url):
	x = str(short_url)
	decoded = toBase10(x)
	print( decoded)
	db.connect()
	u = weburls.select().where(weburls.id == decoded).get()
	ur = u.url
	db.close()
	return redirect(ur)
  
  
if __name__ == '__main__':
	app.run(debug=True)

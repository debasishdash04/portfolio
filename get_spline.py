import urllib.request
import re

url = 'https://my.spline.design/circularsolarcopycopy-XZDpjllJtCU8Z9kwvzv32doD-P74/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    print('HTML end snippet:', html[-2000:])
except Exception as e:
    print('Error:', e)

import http.client #minimum python v3 required

conn = http.client.HTTPConnection("localhost:5000")

payload = '''
{
    "Latitude": 6440041.1,
    "Issue time": 1515.0,
    "Agency": 2.0, 
    "Longitude": 1802686.2, 
    "Color": "WH", 
    "Body Style": "PA" 
}
'''

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

conn.request("POST", "/model", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
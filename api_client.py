import http.client #minimum python v3 required

conn = http.client.HTTPConnection("localhost:5000")

payload = '''
{
    "Color": "GR",
    "Latitude": 63453.0
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
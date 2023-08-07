import requests

url = "http://itashomolog02.jofege.com.br:8057/wsReport/IwsReport"

payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tot=\"http://www.totvs.com/\">\n   <soapenv:Header/>\n   <soapenv:Body>\n      <tot:GetFileChunk>\n         <!--Optional:-->\n         <tot:guid>89a89484-55a4-4813-b9d9-f8519300ebaf</tot:guid>\n         <!--Optional:-->\n         <tot:offset>0</tot:offset>\n         <!--Optional:-->\n         <tot:length>999999</tot:length>\n      </tot:GetFileChunk>\n   </soapenv:Body>\n</soapenv:Envelope>"
headers = {
  'Content-Type': 'text/xml',
  'SOAPAction': "http://www.totvs.com/IwsReport/GetFileChunk",
  'Authorization': 'Basic YW5kcmUubmlzaGlkYToxMjM0NTY='
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
z
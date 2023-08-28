import requests
import json

version = "v17.0"
phone_number_id = "110839738782292"
token = ("EAAEXLUUzmaoBO1ZALwUFZCkgAGmCyr88NGZCyzfRIZAGIvHmnyp7ofKNVKqE8j8YAiFfJlS8UcPYT0jx0JqOZBq0ZBFcZAOmWqLU0NGLXuO"
         "myxDoz4ZBh3JBVWpepUzlLzmM5m5DG7kIk8s1IWQODjAmKN2WKlgQ0gstHszrCWlgKxmLgma6QK0ha4DYzpWlIOFd12vRqBdGVrp8OpNbzrU"
         "ZD")

url = "https://graph.facebook.com/{version}/{phone_number_id}/messages".format(version=version,
                                                                               phone_number_id=phone_number_id)


class WhatsAppApi(object):
    def __init__(self, version=version, phone_number_id=phone_number_id, token=token):
        self.version = version
        self.phone_number_id = phone_number_id

        self.headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer %s" % token
        }

    def send_message(self, phone_number, message):
        data = {
            "messaging_product": "whatsapp",
            "to": "+55" + phone_number,
            "type": "template",
            "template": {
                "name": "hello_world5",
                "language": {
                    "code": "en_US"
                }
            }
        }
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()


if __name__ == "__main__":
    api = WhatsAppApi()
    r = api.send_message(phone_number="63992492893", message="Teste")
    print(r)

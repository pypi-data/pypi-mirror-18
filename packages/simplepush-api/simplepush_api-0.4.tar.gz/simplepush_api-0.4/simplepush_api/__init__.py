import os


class Phone:
    def __init__(self, key=None, title="Title", msg="Contents"):
        self.key = key
        self.default_title = title
        self.default_msg = msg
        if not key:
            print("Error, key not setup")

    def send(self, title=None, msg=None):
        if not title:
            title = self.default_title

        if not msg:
            msg = self.default_msg
        os.system("curl --data 'key=%s&title=%s&msg=%s' https://api.simplepush.io/send"
                  % (self.key, title, msg))

    def set_title(self, title):
        self.default_title = title

    def set_msg(self, msg):
        self.default_msg = msg

    def set_key(self, key):
        self.key = key

if __name__ == "__main__":
    p = Phone(key="rgde4C", title="Test", msg="This is a test")
    p.send()

class User:
    def __init__(self, data, id):
        self.first_name = data["first-name"]
        self.last_name = data["last-name"]
        self.email = data["email"]
        self.key = data["api-key"]
        self.type = data["account-type"]
        self.id = id

    def __repr__(self):
        return str(self.first_name + " " + self.last_name)

    def __str__(self):
        return str(self.first_name)

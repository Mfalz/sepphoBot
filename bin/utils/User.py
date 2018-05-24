class User:
    userID = 0
    Secret = 0

    def __int__(self, secret):
        self.Secret = secret

    def setUser(self, user_id):
        self.userID = user_id
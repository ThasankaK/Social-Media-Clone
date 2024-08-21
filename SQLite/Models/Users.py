class Users:
    def __init__(self, usr: int, pwd: str, name: str, email: str, city: str, timezone: float):
        self.usr = usr
        self.pwd = pwd
        self.name = name
        self.email = email
        self.city = city
        self.timezone = timezone
    
    def get_usr(self):
        return self.usr
    
    def get_pwd(self):
        return self.pwd
    
    def save_user(self):
        pass
    
    def get_name(self):
        return self.name
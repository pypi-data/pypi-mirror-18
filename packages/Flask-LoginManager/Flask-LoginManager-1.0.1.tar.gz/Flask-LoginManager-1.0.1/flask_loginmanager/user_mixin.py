class UserMixin(object):
    
    def __init__(self):
        self.__uid = 0
        self.__password = ''
        
    def get_id(self):
        return self.__uid

    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password

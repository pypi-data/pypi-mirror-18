class UserMixin(object):
    
    def __init__(self):
        self.__uid = 0
        self.__password = ''
        self.__permissions = 0
        
    def get_id(self):
        return self.__uid

    @property
    def permissions(self):
        return self.__permissions

    @permissions.setter
    def permissions(self, permissions):
        self.__permissions = permissions

    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password

class User:
    def __init__(self, id, fullname,role_id,email, username, password):
        self.id = id
        self.fullname = fullname
        self.role_id= role_id
        self.email=email
        self.username = username
        self.password=password
        
    
class Profile(User):
    def __init__(self, id, fullname, role_id, email, username, password, mobile, age, gender, weight):
        super().__init__(id, fullname, role_id, email, username, password)
        self.mobile = mobile
        self.age = age
        self.gender = gender
        self.weight = weight

    def __iter__(self):
        attributes = ['id', 'fullname', 'role_id', 'email', 'username', 'password', 'mobile', 'age', 'gender', 'weight']
        for attr in attributes:
            yield attr, getattr(self, attr)

    def __str__(self) -> str:
        return f"Name: {self.fullname}, Role: {self.get_role()}, Email: {self.email}, Username: {self.username}"

    def get_role(self):
        if self.role_id == 1:
            return "super_user"
        elif self.role_id == 2:
            return "admin"
        elif self.role_id == 3:
            return "consultant"
        elif self.role_id == 4:
            return "member"
        else:
            return "Invalid role"

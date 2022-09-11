from enum import Enum
class AuthLevel(Enum):
    Student = 0,
    Teacher = 1,
    Admin = 3
    def from_int(i: int):
        match i:
            case 0: return AuthLevel.Student
            case 1: return AuthLevel.Teacher
            case 3: return AuthLevel.Admin
    def to_int(al):
        match al:
            case AuthLevel.Student: return 0
            case AuthLevel.Teacher: return 1
            case AuthLevel.Admin: return 3

def str_auth_level(auth_level: int):
    match auth_level:
        case 0: return "Student"
        case 1: return "Teacher"
        case 3: return "Admin"

def check_auth_level(required: AuthLevel, auth_level: int):
    return auth_level >= AuthLevel.to_int(required)
from enum import Enum


class UserType(Enum):
    ADMIN = 0x7
    REGULAR_USER = 0x1

    @classmethod
    def all_values(cls):
        return [m.value for m in cls]

    @staticmethod
    def get_as_dic_list(roles):
        return list(map(
            lambda x: {
                'id': x.value,
                'name': x.name
            },
            filter(lambda x: x.value & roles != 0 and x.value <= roles, list(UserType))
        ))

import hashlib
from utils.config import CODE


class AuthSystem:
    def __init__(self):
        self.code_hash = CODE  # храним как строку

    def check_code(self, input_code):
        input_hash = hashlib.sha256(input_code.encode()).hexdigest()
        return input_hash == self.code_hash  # сравниваем строки
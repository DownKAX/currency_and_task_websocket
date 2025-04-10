import datetime
from pydantic import BaseModel, model_validator, SecretStr
from fastapi import WebSocket, HTTPException


class User(BaseModel):
    username: str
    password: str
    register_date: datetime.datetime

class UserRegistrationForm(BaseModel):
    username: str
    password: SecretStr
    confirm_password: SecretStr

    @model_validator(mode='after')
    def validate_passwords_match(self):
        if 8 > (password := len(str(self.password.get_secret_value()))) or password > 64: #метод позволяет получить реальное значение пароля, а не звёзды для проверки, потому что без метода пароль любой длинны будет отображаться как 10 *
            raise HTTPException(401, 'Length must be between 8 and 64')
        if self.password != self.confirm_password:
            raise HTTPException(401, detail='Passwords do not match')
        return self

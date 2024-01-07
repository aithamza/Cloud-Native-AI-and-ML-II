
'''from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

external_data = {
 'id': '1',
 'signup_ts': '2019-06-01 12:22',
 'friends': [1, 2, '5'],
}
user = User(**external_data)
print(user.id)
#> 123
print(repr(user.signup_ts))
#> datetime.datetime(2019, 6, 1, 12, 22)
print(user.friends)
#> [1, 2, 3]
print(user.dict())

from typing import List
from pydantic import BaseModel
class Foo(BaseModel):
 count: int
 size: float = None
 
class Bar(BaseModel):
 apple: str = 'x'
 banana : str = 'y'
class Spam(BaseModel):
 foo: Foo
 bars: List[Bar]
m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'},
{'apple': 'x2'}])
print(m)
print(m.dict())
'''

from pydantic import BaseModel, ValidationError, validator
class UserModel(BaseModel):
 name: str
 username: str
 password1: str
 password2: str
 @validator('name')
 def name_must_contain_space(cls, v):
   if ' ' not in v:
    raise ValueError('must contain a space')
   return v.title()
 @validator('password2')
 def passwords_match(cls, v, values, **kwargs):
   if 'password1' in values and v != values['password1']:
    raise ValueError('passwords do not match')
   return v
 @validator('username')
 def username_alphanumeric(cls, v):
   assert v.isalnum(), 'must be alphanumeric'
   return v
user = UserModel(
 name='samuel colvin',
 username='scolvin',
 password1='zxcvbn',
 password2='zxcvbn',
)
print(user)
try:
 UserModel(
 name='samuel ',
 username='scolvin',
 password1='zxcvbn',
 password2='zxcvbn2',
 )
except ValidationError as e:
 print(e)
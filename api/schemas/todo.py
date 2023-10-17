from pydantic import BaseModel,Field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.todo import List,Task

GetList = pydantic_model_creator(List,name="list")
GetTask = pydantic_model_creator(Task,name="task")


class PostList(BaseModel):
    name:str = Field(...,max_length=100)
    
class PutList(BaseModel):
    name:Optional[str] = Field(None,max_length=100)
    
class PostTask(BaseModel):
    list_id:int
    task:str = Field(...,max_length=100)

class PutTask(BaseModel):
    task:Optional[str] = Field(None,max_length=200)
    done:Optional[bool]

from fastapi import APIRouter,HTTPException,status
from api.schemas.todo import GetList,GetTask,PostList,PostTask,PutList,PutTask
from api.models.todo import Task,List

router = APIRouter(prefix='/api',tags=['Todo'])

@router.get('/my-lists/')
async def getlists():
    all = List.all()
    return await GetList.from_queryset(all)

@router.post('/create-list/')
async def createlist(body:PostList):
    row =  await List.create(**body.model_dump(exclude_unset=True))
    return await GetList.from_tortoise_orm(row)

@router.put('/update-list/{id}/')
async def updatelist(id:int,body:PutList):
    data = body.model_dump(exclude_unset=True)
    exists = await List.filter(id = id).exists()
    if exists:
        new = await List.filter(id = id).update(**data)
        print(new)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Todo not found')
    return await GetList.from_queryset_single(List.get(id=id))

@router.delete('/delete-list/{id}/')
async def deletelist(id:int):
    if await List.filter(id = id).exists():
       await List.filter(id = id).delete()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Todo not found')
    return "List deleted successfully"

@router.get('/tasks/{id}/')
async def tasks_list(id:int):
    if await List.filter(id = id).exists():
        base_list = await List.get(id = id)
        tasks = Task.filter(list = base_list.id)
        return await GetTask.from_queryset(tasks)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='List Not Found')


@router.post('/create-task/')
async def create_task(body:PostTask):
    data = body.model_dump(exclude_unset=True)
    base_list = await List.get(id = data['list_id'])
    task = await Task.create(list_id = base_list.id,task = data['task'])
    return await GetTask.from_tortoise_orm(task)

@router.put('/update-task/{id}/')
async def update_task(id:int,body:PutTask):
    data = body.model_dump(exclude_unset=True)
    if await Task.filter(id = id).exists():
        await Task.filter(id = id).update(**data)
        task = Task.get(id = id)
        return await GetTask.from_queryset_single(task)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task Not Found")

@router.delete('/delete-task/{id}/')
async def delete_task(id:int):
    if await Task.filter(id = id).exists():
        await Task.filter(id = id).delete()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    return "Task Deleted successfully"
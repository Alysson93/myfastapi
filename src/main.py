import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

import uvicorn
from fastapi import FastAPI

from routers import auth, users, todos

app = FastAPI()


@app.get('/')
def root():
    return {'msg': 'Hello, World!'}


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)

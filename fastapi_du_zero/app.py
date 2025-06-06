from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_du_zero.database import get_session
from fastapi_du_zero.models import User
from fastapi_du_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='API FastAPI Kanban')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, Mundo!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def html_page():
    return """
        <html>
            <head>
                <title>Página do Olá, Mundo!</title>
            </head>
            <body>
                <h1>Chega mais, Mundão!</h1>
            </body>
        </html>"""


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Este nome de usuário já está sendo usado! '
                'Favor, defina outro.',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Este endereço de e-mail já está sendo usado! '
                'Favor, digite outro.',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    skip: int = 0,
    session: Session = Depends(get_session)
):

    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


# @app.get(
#     '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
# )
# def read_user(user_id: int, session: Session = Depends(get_session)):

#     users = session.scalars(select(User))
#     if user_id > len(users) or user_id < 1:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail='Usuário não encontrado!'
#         )

#     user = session.scalar(select(User).where(user_id - 1))

#     return user


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado!'
        )

    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            detail='Nome de usuário ou endereço de e-mail \
                já está sendo usado!',
            status_code=HTTPStatus.CONFLICT
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado!'
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'Usuário excluído!'}

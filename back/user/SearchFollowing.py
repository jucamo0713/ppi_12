import re

from bson import ObjectId
from fastapi import APIRouter, Request, Header

from db.PaginatedSearch import paginated_search
from jwt_utils.Guard import validate_token
from user.User import User

SEARCH_FOLLOWING = APIRouter()


@SEARCH_FOLLOWING.get("/following",
                      response_description="List all users following")
def search_following(request: Request, authentication: str = Header(...),
                     limit=15, page=1, search_param=''):
    token_data = validate_token(authentication)
    user_id = token_data['id']
    users = list(request.app.database["follows"].aggregate(
        paginated_search(
            page=int(page) if page is not None else None, limit=int(limit) if
            limit is not None else None,
            query={
                '$or': [
                    {'name': re.compile(f'{search_param}', re.IGNORECASE)},
                    {'user': re.compile(f'{search_param}', re.IGNORECASE)},
                    {'email': re.compile(f'{search_param}', re.IGNORECASE)},
                ]
            },
            pre_query=
            [
                {
                    '$match': {
                        '$or': [
                            {
                                'user2_id': ObjectId(user_id),
                                'follow_back': True
                            }, {
                                'user1_id': ObjectId(user_id),
                                'follow': True
                            }
                        ]
                    }
                },
                {
                    '$project': {
                        'user': {
                            '$cond': [
                                {
                                    '$eq': ['$user1_id', ObjectId(
                                        user_id)]
                                }, '$user2_id', '$user1_id'
                            ]
                        }
                    }
                },
                {
                    '$lookup': {
                        'from': 'users',
                        'localField': 'user',
                        'foreignField': '_id',
                        'as': 'user'
                    }
                },
                {
                    '$unwind': {
                        'path': '$user'
                    }
                },
                {
                    '$project': {
                        '_id': '$user._id',
                        'name': '$user.name',
                        'user': '$user.user',
                        'password': '$user.password',
                        'email': '$user.email',
                        'burn_date': '$user.burn_date',
                        'registered_date': '$user.registered_date'
                    }
                }
            ]
        )))
    # Si se encuentran usuarios, se crea una respuesta con los datos y
    # metadatos
    response = users[0] if len(users) > 0 else {'data': [], 'metadata': {
        'total': 0,
        'page': 0,
        'total_pages': 0,
    }}
    response['data'] = list(map(lambda x: User(**x), response["data"]))
    return response

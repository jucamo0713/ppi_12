from bson import ObjectId
from fastapi import APIRouter, Request, Header

from db.PaginatedSearch import paginated_search
from jwt_utils.Guard import validate_token
from notifications.Notification import Notification

SEARCH_ALL_NOTIFICATIONS = APIRouter()


@SEARCH_ALL_NOTIFICATIONS.get("/all")
def search_all_notifications(request: Request, limit: int = 15, page: int = 1,
                             authentication: str = Header(...)):
    # Validar el token de autenticación utilizando la función
    # validate_token
    token_data = validate_token(authentication)
    user_id = ObjectId(token_data['id'])
    response = list(request.app.database['notifications'].aggregate(
        paginated_search(
            page=int(page), limit=int(limit),
            query={
                "user_id": user_id
            }
        )))
    if len(response) > 0:
        response = response.pop()
    else:
        return {
            'data': [],
            "metadata": {

            }
        }
    response["data"] = [Notification(**x) for x in response["data"]]
    return response

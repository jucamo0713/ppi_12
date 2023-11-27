from bson import ObjectId
from fastapi import APIRouter, Request, Header

from jwt_utils.Guard import validate_token

DELETE_NOTIFICATION = APIRouter()


@DELETE_NOTIFICATION.delete("/delete")
def search_all_notifications(request: Request, id: str,
                             authentication: str = Header(...)):
    # Validar el token de autenticación utilizando la función
    # validate_token
    validate_token(authentication)
    request.app.database['notifications'].find_one_and_delete({
        "_id": ObjectId(id)
    })
    return {"success": True}

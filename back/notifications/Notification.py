# Importaciones de librerías necesarias
from datetime import datetime
from typing import Literal

from bson import ObjectId
from pydantic import BaseModel, Field

# Definición de un tipo literal para el campo 'type' de Notification
types_notification = Literal[
    "NEW_FOLLOWER",
    "NEW_FOLLOW_OF_FOLLOWER",
    "RESPONSE_IN_COMMENT",
    "NEW_BOOK_OF_FOLLOWER",
    "FOLLOWER_UNFOLLOW"
]


class Notification(BaseModel):
    """
    Modelo Pydantic para representar una notificación.

    Atributos:
    - id (ObjectId): Identificador único de la notificación.
    - message (str): Mensaje de la notificación.
    - user_id (ObjectId): Identificador del usuario al que va dirigida la
    notificación.
    - type (types_notification): Tipo de la notificación.
    - created_at (datetime): Fecha de creación de la notificación.
    - data_id (ObjectId): Identificador del comentario, usuario o libro
    relacionado a la notificación.

    Config:
    - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios.
    - json_encoders (dict): Diccionario de codificadores JSON personalizados.
    """
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    message: str = Field(..., description="Mensaje de la Notificación")
    user_id: ObjectId = Field(..., description="Id del usuario al que va "
                                               "dirigida la Notificación")
    type: types_notification = Field(..., description="Tipo de la "
                                                      "Notificación")
    created_at: datetime = Field(..., description="Fecha de creación de la "
                                                  "notificación")
    data_id: ObjectId = Field(..., description="Id del Comentario, "
                                               "usuario o libro relacionado a "
                                               "la notification")

    class Config:
        """
        Configuración del modelo `User`.

        Atributos:
        - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios.
        - json_encoders (dict): Diccionario de codificadores JSON
        personalizados.
        """
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_jsonable(self, **kwargs) -> dict:
        """
        Convierte el objeto `Notification` a un diccionario JSON.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Un diccionario JSON que representa el objeto `Notification`.
        """
        notification_dict = self.model_dump(**kwargs)
        notification_dict['id'] = str(notification_dict['id'])
        notification_dict['user_id'] = str(notification_dict['user_id'])
        notification_dict['data_id'] = str(notification_dict['data_id'])
        notification_dict['created_at'] = self.registered_date.isoformat()
        return notification_dict

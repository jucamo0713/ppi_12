# Importaciones de librerías de terceros
from bson import ObjectId
from pydantic import BaseModel, Field


class Follow(BaseModel):
    """
    Modelo que representa la relación de seguimiento entre dos usuarios.

    Atributos:
    - id (ObjectId): Identificador único de la relación.
    - user1_id (ObjectId): ID del primer usuario en la relación.
    - user2_id (ObjectId): ID del segundo usuario en la relación.
    - follow (bool): Indica si el primer usuario sigue al segundo.
    - follow_back (bool): Indica si el segundo usuario sigue al primero.

    Config:
    - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios.
    - json_encoders (dict): Diccionario de codificadores JSON personalizados.
    """

    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user1_id: ObjectId = Field(default_factory=ObjectId)
    user2_id: ObjectId = Field(default_factory=ObjectId)
    follow: bool = Field(...)
    follow_back: bool = Field(...)

    class Config:
        """
        Configuración del modelo `Follow`.

        Atributos:
        - arbitrary_types_allowed (bool): Permite tipos de datos arbitrarios.
        - json_encoders (dict): Diccionario de codificadores JSON
        personalizados.

        Args:
            arbitrary_types_allowed (bool): Permite tipos de datos
            arbitrarios en el modelo.
            json_encoders (dict): Diccionario de codificadores JSON
            personalizados.
        """
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_jsonable(self, **kwargs):
        """
        Convierte el objeto `Follow` a un diccionario JSON.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Un diccionario JSON que representa el objeto `Follow`.
        """
        follow_dict = self.model_dump(**kwargs)
        follow_dict['id'] = str(follow_dict['id'])
        follow_dict['user1_id'] = str(follow_dict['user1_id'])
        follow_dict['user2_id'] = str(follow_dict['user2_id'])
        return follow_dict


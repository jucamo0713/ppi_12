def paginated_search(query=None, sort=None, page=0, limit=0, project=None):
    """
    Función que construye una consulta de MongoDB para realizar una búsqueda
    paginada.

    Parámetros:
    - query (dict): Diccionario con las condiciones de búsqueda.
    - sort (dict): Diccionario con las condiciones de ordenamiento.
    - page (int): Número de página.
    - limit (int): Cantidad máxima de resultados por página.
    - project (List[dict]): Lista de proyecciones.

    Retorna:
    - List[dict]: Consulta de MongoDB construida para búsqueda paginada.

    La función toma los parámetros de consulta, ordenamiento y paginación y
    construye una consulta de MongoDB que incluye saltos de página, límites,
    metadatos de paginación y ordenamiento. Esta consulta es útil para realizar
    búsquedas paginadas en una colección de MongoDB.

    Ejemplo de uso:
    ```
    query = {'field': 'value'}
    sort = {'_id': 1}
    page = 1
    limit = 10
    project = [{'$project': {'field1': 1, 'field2': 1}}]

    consulta = paginated_search(query, sort, page, limit, project)
    results = collection.aggregate(consulta)
    ```

    Args:
    - query (dict): Diccionario que contiene las condiciones de búsqueda en
    MongoDB.
    - sort (dict): Diccionario que contiene las condiciones de ordenamiento
    en MongoDB.
    - page (int): Número de página para la paginación.
    - limit (int): Cantidad máxima de resultados por página.
    - project (List[dict]): Lista de proyecciones a aplicar.

    Returns:
    - List[dict]: Una consulta de MongoDB lista para ser utilizada en la
    función `aggregate`.

    La función permite realizar búsquedas en una colección de MongoDB de
    forma paginada, aplicando condiciones de búsqueda, ordenamiento y
    proyecciones personalizadas. Además, proporciona información de
    paginación como el número total de páginas y la página actual.

    Ejemplo de uso:
    - `query`: Un diccionario de condiciones de búsqueda.
    - `sort`: Un diccionario de condiciones de ordenamiento.
    - `page`: Número de página para la paginación.
    - `limit`: Cantidad máxima de resultados por página.
    - `project`: Lista de proyecciones personalizadas.

    La función devuelve una consulta de MongoDB que puede ser utilizada con
    `aggregate` para obtener resultados paginados.

    Ejemplo de uso:
    ```
    query = {'field': 'value'}
    sort = {'_id': 1}
    page = 1
    limit = 10
    project = [{'$project': {'field1': 1, 'field2': 1}}]

    consulta = paginated_search(query, sort, page, limit, project)
    results = collection.aggregate(consulta)
    ```
    """

    # Comprueba si los parámetros son None y los inicializa si es necesario.
    if project is None:
        project = []
    if sort is None:
        sort = {'_id': 1}
    if query is None:
        query = {}

    # Inicializa las listas para las etapas de la consulta.
    response = []
    data = []
    metadata = []

    # Calcula el número de documentos a saltar para la paginación.
    if page and limit:
        skip = (page - 1) * limit
        data.append({'$skip': skip})
        data.append({'$limit': limit})

    # Agrega etapas para obtener información de paginación.
    metadata.append({'$count': 'total'})
    metadata.append({'$addFields': {'page': page}})
    metadata.append({'$addFields': {'totalPages': {
        '$ceil': {'$divide': ['$total', limit]}}} if limit else 0})

    # Agrega la etapa de búsqueda al inicio de la consulta.
    response.append({'$match': query})

    # Agrega proyecciones personalizadas si se proporcionan.
    if project:
        response = response + project

    # Agrega etapas de ordenamiento y facet (para obtener datos y metadatos).
    response.append({'$sort': sort})
    response.append({'$facet': {'data': data, 'metadata': metadata}})

    # Desenrolla los datos de metadatos para que sean accesibles.
    response.append({'$unwind': {'path': '$metadata'}})

    # Devuelve la consulta de MongoDB completa para ser utilizada en la
    # función `aggregate`.
    return response

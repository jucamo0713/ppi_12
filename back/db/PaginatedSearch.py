def paginated_search(query=None, sort=None, page=0, limit=0, project=None):
    """
    Función que construye una consulta de MongoDB para realizar una búsqueda paginada.

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
    """
    if project is None:
        project = []
    if sort is None:
        sort = {'_id': 1}
    if query is None:
        query = {}
    response = []
    data = []
    metadata = []
    if page and limit:
        skip = (page - 1) * limit
        data.append({'$skip': skip})
        data.append({'$limit': limit})
    metadata.append({'$count': 'total'})
    metadata.append({'$addFields': {'page': page}})
    metadata.append({'$addFields': {'totalPages': {'$ceil': {'$divide': [
        '$total', limit]}}} if limit else 0})
    response.append({'$match': query})
    if project:
        response = response + project
    response.append({'$sort': sort})
    response.append({'$facet': {'data': data, 'metadata': metadata}})
    response.append({'$unwind': {'path': '$metadata'}})
    return response

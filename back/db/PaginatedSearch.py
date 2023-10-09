from typing import List


def paginated_search(query=None, sort=None, page=0, limit=0, project=None):
    if project is None:
        project = []
    if sort is None:
        sort = {'_id': 1}
    if query is None:
        query = {}
    response = []
    data = []
    metadata = []
    print(query)
    if page and limit:
        skip = (page - 1) * limit
        data.append({'$skip': skip})
        data.append({'$limit': limit})
    data.append({'$unset': '_id'})
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

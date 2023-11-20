consolidated_aggregate = [
    {
        '$lookup': {
            'from': 'users',
            'localField': 'user_id',
            'foreignField': '_id',
            'as': 'user'
        }
    }, {
        '$unwind': {
            'path': '$user'
        }
    }, {
        '$lookup': {
            'from': 'books',
            'localField': 'book_id',
            'foreignField': '_id',
            'as': 'book'
        }
    }, {
        '$unwind': {
            'path': '$book'
        }
    }, {
        '$facet': {
            'users': [
                {
                    '$group': {
                        '_id': '$user_id',
                        'user': {
                            '$first': '$user'
                        }
                    }
                }, {
                    '$project': {
                        '_id': '$user._id',
                        'name': '$user.name',
                        'user': '$user.user',
                        'email': '$user.email',
                        'burn_date': '$user.burn_date',
                        'password': '$user.password',
                        'registered_date': '$user.registered_date'
                    }
                }
            ],
            'books': [
                {
                    '$group': {
                        '_id': '$book._id',
                        'book': {
                            '$first': '$book'
                        }
                    }
                }, {
                    '$project': {
                        '_id': '$_id',
                        'isbn_code': '$book.isbn_code',
                        'title': '$book.title',
                        'author': '$book.author',
                        'image': '$book.image',
                        'rating': '$book.rating',
                        'total_ratings': '$book.total_ratings'
                    }
                }
            ],
            'relations': [
                {
                    '$unset': [
                        'book', 'user'
                    ]
                }
            ]
        }
    }
]

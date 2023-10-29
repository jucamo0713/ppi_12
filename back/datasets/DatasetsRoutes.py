# Importaciones de módulos internos de la aplicación
from back.datasets.LoadBooksDatasetToDb import LOAD_BOOKS_DATASET_TO_DB


# Definición de las rutas y controladores
DATASETS_ROUTES = [{'path': '/datasets',
                    'tag': 'Datasets',
                    'instance': LOAD_BOOKS_DATASET_TO_DB}]

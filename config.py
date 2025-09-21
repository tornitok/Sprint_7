class URL:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/'

class Endpoints:
    COURIER = 'api/v1/courier'
    COURIER_LOGIN = 'api/v1/courier/login'
    COURIER_DELETE = 'api/v1/courier'  # use with path param in client: /{id}
    ORDERS = 'api/v1/orders'
    ORDERS_ACCEPT = 'api/v1/orders/accept/'
    ORDERS_TRACK = 'api/v1/orders/track'

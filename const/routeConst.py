from routing.settings.settingsRoute import SettingsRoute
from routing.auth.authRoute import AuthRoute
from routing.customer.customerRoute import CustomerRoute

class RouteConst:
    USER_ROUTES = {
            'auth':             AuthRoute,
            'customer':         CustomerRoute,
            'settings':         SettingsRoute
    }

#     QUESTS_ROUTES = {
#             'auth':             AuthRoute,
#             'settings':         SettingsRoute
#     }
    
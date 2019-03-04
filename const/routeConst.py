from routing.settings.settingsRoute import SettingsRoute
from routing.auth.authRoute import AuthRoute

class RouteConst:
    ROUTES = {
            'auth':             AuthRoute,
            'settings':         SettingsRoute
    }
    
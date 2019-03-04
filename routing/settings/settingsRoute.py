from routing.route import Route
from const.pathConst import PathConst
from routing.response.jsonRequestHandler import JsonRequestHandler

class SettingsRoute(Route): 
    def __settingsBase(self, params):
        result = JsonRequestHandler()
        
        result.setContents(self.user.getBaseEditResponse())

        return result

    def _routing(self):
        return {
                PathConst.SETTING_BASE      :self.__settingsBase
        }

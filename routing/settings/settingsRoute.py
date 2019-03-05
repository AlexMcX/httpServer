from routing.route import Route
from const.pathConst import PathConst
from routing.response.jsonRequestHandler import JsonRequestHandler

class SettingsRoute(Route): 
    def __settingsBase(self, params):
        result = JsonRequestHandler()

        result.setContents(self.user.getBaseEditResponse())

        return result

    def __settingsBaseSave(self, params):
        result = JsonRequestHandler()

        self.user.applyChanges(params)

        result.setContentsBool(True)

        return result

    def _routing(self):
        return {
                PathConst.SETTING_BASE_GET      :self.__settingsBase,
                PathConst.SETTING_BASE_POST     :self.__settingsBaseSave
        }

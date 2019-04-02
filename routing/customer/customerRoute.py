from routing.route import Route
from utils.objectEx import *
from const.restConst import RestConst
from const.pathConst import PathConst
from service.dataBaseService import DataBaseService
from database.vo.profileVO import ProfileVO
from routing.response.jsonRequestHandler import JsonRequestHandler
from routing.customer.response.authRequestHandler import AuthRequestHandler
class CustomerRoute(Route):
    def __init__(self, customer):
        self.__BD = DataBaseService.getInstance().profile

        super().__init__(customer)

    def _onInit(self):
        if self.user:
            self.__setProfileUser(self.user.readBDData)

    def save(self):
        if self.user.profile:
            saveData = self.user.profile.getChangeCompression()

            self.__BD.change(saveData)

    def _routing(self):
        return {
                RestConst.GET: {
                    PathConst.CUSTOMER      :   self.__customerGET,
                    PathConst.CUSTOMER_FORM :   self.__customerFromGET
                },
                RestConst.POST:{
                    PathConst.CUSTOMER     :   self.__customerPOST    
                }
        }      

    def __customerGET(self, params):
        result = JsonRequestHandler()

        result.setContents(self.user.GETResponse())

        return result

    def __customerPOST(self, params):
        result = AuthRequestHandler()

        if not self.user.profile:
            self.__BD.insert(params)

            self.__setProfileUser(params)

            result.setContentsSuccess()

            self.user.type = "register"
        else:
            result.setContentsUserExist()

        return result

    def __customerFromGET(self, params):
        result = JsonRequestHandler()
        
        result.setContents(self.user.profile.GETResponseForm())

        return result

    def __setProfileUser(self, params):
        readParams = getCommonFields(params, ProfileVO)    

        dbResponce = self.__BD.read(readParams)
        
        self.user.profile = createObjectFromBD(ProfileVO, dbResponce)

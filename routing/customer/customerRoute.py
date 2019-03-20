from routing.route import Route
from utils.objectEx import *
from const.restConst import RestConst
from const.pathConst import PathConst
from service.dataBaseService import DataBaseService
from database.vo.profileVO import ProfileVO
from routing.response.jsonRequestHandler import JsonRequestHandler

class CustomerRoute(Route):
    def __init__(self, customer):
        self.__BD = DataBaseService.getInstance().profile

        super().__init__(customer)

    # def _onInit(self):
    #     if self.user:
    #         self.__setProfileUser(self.user.readBDData)

    def save(self):
        pass

    def _routing(self):
        return {
                RestConst.GET: {
                    PathConst.CUSTOMER     :   self.__customerGET
                },
                RestConst.POST:{
                    PathConst.CUSTOMER     :   self.__customerPOST    
                }
        }      

    def __customerGET(self, params):
        result = JsonRequestHandler()
        response = self.user.GETResponse()

        response["profile"] = self.__getProfile(params)

        result.setContents(response)

        return result

    def __customerPOST(self, params):
        print("__customerPOST ", params)

    def __getProfile(self, params):
        readParams = getCommonFields(params, ProfileVO)    
        dbResponce = self.__BD.read(readParams)
        result = getCommonFields(dbResponce, ProfileVO)

        return result


    # def __setProfileUser(self, params):        
    #     readParams = getCommonFields(params, ProfileVO)    

    #     dbResponce = self.__BD.read(readParams)
        
    #     self.user.profile = createObjectFromBD(ProfileVO, dbResponce)
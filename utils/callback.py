# if __name__ == '__main__':
#     from callback import CallBack

#     def test(param1):
#         print('is test ', param1)

#     call = CallBack()
#     idA = call.add(test)
#     idB = call.add(test)
#     print(idA, idB)
#     call.fire("is params from test")
#     call.remove(idA)
#     # call.clear()


class CallBack:
    def __init__(self):
        self.__inc = 0
        self.__items = {}

    def add(self, callBack):
        if not callBack in self.__items.values():
            self.__items[self.__inc] = callBack

            self.__inc += 1
            
            return self.__inc - 1
        return -1


    def remove(self, ids):
        if ids in self.__items.keys():
            self.__items.pop(ids, None)
    
    def fire(self, *params):
        lenParmas = len(params)
        calls = list(self.__items.values())

        for call in calls:
            if lenParmas == 0:
                call()
            elif lenParmas == 1:
                call(params[0])
            elif lenParmas == 2:
                call(params[0], params[1])
        
    def clear(self):
        self.__items.clear()
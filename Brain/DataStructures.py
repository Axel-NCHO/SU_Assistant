class Queue:

    def __init__(self, elementsType: type, args: list = None):
        self.__Elements_Type = elementsType
        if args is None:
            args = []
        if len(args) != 0:
            for element in args:
                if type(element) != self.__Elements_Type:
                    raise TypeError("One element in the given list has a wrong type")
        self.__List = args

    def __len__(self) -> int:
        return self.length()

    def is_empty(self) -> bool:
        return len(self.__List) == 0

    def length(self) -> int:
        return len(self.__List)

    def enqueue(self, element):
        self.__List.append(element)

    def dequeue(self):
        if not self.is_empty():
            return self.__List.pop(0)
        raise IndexError("Accessing queue with invalid index")

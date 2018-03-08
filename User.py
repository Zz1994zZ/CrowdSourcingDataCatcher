#coding:utf8
class User:
    def __init__(self):
        self.id=''
        self.nickname = ''
        self.city = ''
        self.work = ''
        self.price =''
        self.workPlace = ''
        self.workTime = ''
        self.skillList = {}
    def show(self):
        print(self.id, self.nickname, self.city, self.work, self.price, self.workPlace, self.workTime, self.skillList)
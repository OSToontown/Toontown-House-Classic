class HolidayManager:
    def getCurrHoliday(self):
        holidayList = ["Christmas", "Ice Age",
                        "AprilToons", "Halloween",
                        "Empty"]
        self.holiday = holidayList[4]
        return self.holiday
 
    def printHoliday(self):
        if self.holiday == "Empty":
            print('No holiday is currently in progress.')
        else:
            print('The current holiday %s is in progress.') % self.holiday
 
    def getSpecialEvent(self):
        eventList = ["Fireworks", "Easter", "Empty"]
        self.event = eventList[2]
        return self.event
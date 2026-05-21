import datetime

class DailyLogEntry:
    """
    """
    def __init__(self):
        """
        """
        self.entry_id: str = ""
        self.user_id: str = ""
        self.creation_time: datetime.datetime = datetime.datetime.now()
        self.modification_time: datetime.datetime = datetime.datetime.now()
        self.entry_items: list = []

class DailyLogEntryItems:
    """
    """
    def __init__(self):
        self._order: int = 0

    @property
    def order(self):
        """
        """
        return self._order
    
    @order.setter
    def order(self, order: int):
        """
        """
        self._order = order

class DailyLogEntryItem:
    """
    """
    def __init__(self):
        self.order: int = 0
        self.items: list[DailyLogEntryItems] = []

    def addItem(self, item: DailyLogEntryItems):
        """
        """
        if isinstance(item, DailyLogEntryItems):
            item.order = len(self.items)
            self.items.append(item)
        else:
            raise ValueError("DailyLogEntryItem.addItem input is not a DailyLogEntryItems")

class DailyLogEntryActivity(DailyLogEntryItems):
    """
    """
    def __init__(self, activity: str):
        """
        """
        super().__init__()
        self.activity: str = activity

class DailyLogEntryComment(DailyLogEntryItems):
    """
    """
    def __init__(self, comment: str):
        """
        """
        super().__init__()
        self.comment: str = comment

class DailyLogEntryTime(DailyLogEntryItems):
    """
    """
    def __init__(self, date_time: datetime.datetime):
        """
        """
        super().__init__()
        self.start_time: datetime.datetime = date_time


import src.parser.classes as classes

##### 1

# test = classes.DailyLogEntryItems()
# print(test.order)
# test.order = 1
# print(test.order)

##### 2

test_item = classes.DailyLogEntryItem()
test_activity = classes.DailyLogEntryActivity(activity="Testing")

test_item.addItem(test_activity)
print(test_item.items)

for i in test_item.items:
    print(i.order)
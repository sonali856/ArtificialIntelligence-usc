def longest(sentence):
    list1 = sentence.split(" ")
    max = 0
    for item in list1:
        if len(item)>max and len(item)%2==0:
            max=item
            actual_item=item
    print(actual_item)
        
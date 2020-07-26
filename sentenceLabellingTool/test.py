import re

texts = ['Here are some \n\n\n\n\n\n\n\n\n\nwords about\n\n\n\n\n\n\n\n us right\n\n\n\n.']

texts = [text.splitlines() for text in texts]
print(texts)
# [['Here are some ', '', '', '', '', '', '', '', '', '', 'words about', '', '', '', '', '', '', '', ' us right', '', '', '', '.']]

x = []
for txt in texts:
    # x.append([line for line in txt if line.strip() != ""])
    for line in txt:
        if line.strip() != "":
            x.append([line])

print(x)

# [['Here', 'are', 'some'], [], [], [], [], [], [], [], [], [], ['words', 'about'], [], [], [], [], [], [], [], ['us', 'right'], [], [], [], []]

# for x in txt:
#     x=re.sub("\n","ad",x)
#     print(x)

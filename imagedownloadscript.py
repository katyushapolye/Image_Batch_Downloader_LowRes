from typing import Counter
import requests
from requests.api import get

query = input("Query: ")
pages = 10


txt = open("urls.txt",mode = 'w')
file = open("html.html",mode = 'w')

def get_html_code(page):
    ret = requests.get("""https://www.google.com//search?q={}&client=firefox-b-d&biw=1057&bih=648&ie=UTF-8&tbm=isch&ei=K9MSYbXxCKHf1sQPpq-Q6Ag&start={}&sa=N""".format(query,page*20))
                                                                                                                                         ##start=n*20, for n = page number
    return ret


html = get_html_code(2).text
file.write(html)
file.close()



def find_first_index(htmlcode):

    index = htmlcode.find("""https://encrypted-tbn0.gstatic.com/images?q=tbn""")
    return index

def slice_index(htmlcode,index):
    return str(htmlcode[index+126:])


def parse_url(htmlcode,index):
    for i in htmlcode[index:len(htmlcode)]:
        if i == ';':
            break
        txt.write(i)

    txt.write("\n")

for k in range(pages):
    html_temp = get_html_code(k).text
    for l in range(pages*2):
        if find_first_index(html_temp) == -1:
            print("Next Page")
            break
        parse_url(html_temp,find_first_index(html_temp))
        html_temp = slice_index(html_temp,find_first_index(html_temp))


txt.flush()
txt.close()


urls = open("urls.txt",'r')
count = 0
lines = urls.readlines()

c = 0
for l in lines:
    jpg = get(l)
    path = "imgs/{}{}.jpg".format(query,c)
    c +=1
    f = open(path,'bx')
    f.write(jpg.content)
    f.close()
    print(l)



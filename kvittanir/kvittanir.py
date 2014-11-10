# coding: utf-8

import Image
import pytesseract  # also install tesseract-ocr and tesseract-ocr-isl
from itertools import islice, groupby
import locale


filename = 'bonus.jpg'

def is_line_divider(line):
    if line.strip() == "":
        return True
    if line[:2] in ['__', '_.', '_„']:
        return True
    else:
        return False

def generator_get(gen, n):
    return next(islice(gen, n, n+1))

def ocr(filename):
    return pytesseract.image_to_string(Image.open(filename), lang="isl")
    
def bonus_items(ocrtext):
    ocrtext = ocrtext.splitlines()
    grouped = groupby(ocrtext, is_line_divider)
    items = list(generator_get(grouped, 6)[1])
    return list(items)

def price2int(text):
    return int(filter(lambda x: x.isdigit(), text))


def parse_bonus(ocr):
    bonus = bonus_items(ocr)
    items = []
    for i in range(len(bonus)):
        if bonus[i][-1] in ['B', 'A']:
            line = bonus[i].split(' ')
            if line[1] == "stk":
                itemname = bonus[i-1]
                itemprice = line[3]
            else:
                itemname = " ".join(line[:-2])
                itemprice = line[-2]
            items.append({'name': itemname.strip(),
                          'price': price2int(itemprice)})

    return items

if __name__ == '__main__':
    text = 
    kvittun = parse_bonus(text)
    for stuff in kvittun:
        print "{0}\t{1} kr".format(stuff['name'], stuff['price'])


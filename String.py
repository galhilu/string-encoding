class CyclicCharsError(Exception):
    pass


class CyclicCharsDecodeError(Exception):
    pass


class BytePairError(Exception):
    pass


class BytePairDecodeError(Exception):
    pass


class Base64DecodeError(Exception):
    pass


class String:
    index = 0

    def __init__(self, s):
        self.s = s
        self.len = len(str(s))
        self.rules = []

    def __str__(self):
        return self.s

    def __add__(self, other):
        if type(other) == String:
            ns = str(self.s) + str(other.s)
            return String(ns)
        elif type(other) == str:
            ns = str(self.s) + str(other)
            return String(ns)
        else:
            raise SyntaxError

    def __eq__(self, other):
        if type(other) == String:
            return self.s == other.s
        elif type(other) == str:
            return self.s == other
        else:
            raise SyntaxError

    def __mul__(self, other):
        n = ""
        for i in range(0, other):
            n = n + self.s
        return String(n)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index <= len(self.s) - 1:
            i = self.index
            self.index += 1
            return i
        else:
            self.index = 0
            raise StopIteration

    def __getitem__(self, item):
        return String(str(self.s[item]))

    def __len__(self):
        return len(self.s)

    def unitobin(st):
        ns = ""
        for i in str(st):
            byt = bin(ord(i)).replace('0b', '')
            while len(byt) < 8:
                byt = "0" + byt
            ns = ns + byt
        return ns

    def sixfourtobin(lst):
        ns = ""
        for i in lst:
            byt = bin(i).replace('0b', '')
            while len(byt) < 6:
                byt = "0" + byt
            ns = ns + byt
        return ns

    def count(self, sub):
        return self.s.count(sub)

    def isupper(self):
        isup = self.s
        return str(isup).isupper()

    def islower(self):
        islow = self.s
        return str(islow).islower()

    def base64(self) -> 'String':
        s = self.s
        s = self.unitobin()
        while len(s) % 6 != 0:
            s = s + "0"
        nlist = []
        for i in range(0, len(s), 6):
            nlist.append(s[i:i + 6])
        for i in range(0, len(nlist)):
            nlist[i] = int(nlist[i], 2)
        for i in range(0, len(nlist)):
            if nlist[i] <= 25:
                nlist[i] = chr(nlist[i] + 65)
            elif nlist[i] <= 51:
                nlist[i] = chr(nlist[i] - 26 + 97)
            elif nlist[i] <= 61:
                nlist[i] = str(nlist[i] - 52)
            elif nlist[i] == 62:
                nlist[i] = "+"
            elif nlist[i] == 63:
                nlist[i] = "/"
        s = ""
        for i in range(0, len(nlist)):
            s = s + nlist[i]
        return String(s)

    def byte_pair_encoding(self) -> 'String':
        s = self.s
        rules = []
        other = True
        digits = True
        upper = True
        lower = True
        pointer = -1

        for i in s:
            if 33 <= ord(i) <= 47 or 58 <= ord(i) <= 64 or 91 <= ord(i) <= 96 or 123 <= ord(i) <= 126:
                other = False
            if 48 <= ord(i) <= 57:
                digits = False
            if 65 <= ord(i) <= 90:
                upper = False
            if 97 <= ord(i) <= 122:
                lower = False
        valuelist = []

        if other:
            for i in range(33, 48):
                valuelist = valuelist + [int(i)]
            for i in range(58, 65):
                valuelist = valuelist + [int(i)]
            for i in range(91, 97):
                valuelist = valuelist + [int(i)]
            for i in range(124, 127):
                valuelist = valuelist + [int(i)]
        if digits:
            for i in range(48, 58):
                valuelist = valuelist + [int(i)]
        if upper:
            for i in range(65, 91):
                valuelist = valuelist + [int(i)]
        if lower:
            for i in range(97, 122):
                valuelist = valuelist + [int(i)]

        if valuelist == []:
            raise BytePairDecodeError

        while True:
            pointer = pointer + 1
            if pointer == len(valuelist):
                raise BytePairDecodeError
            dic = {}
            for i in range(len(s) - 1):
                if s[i + 1] != s[i - 1] or i == 0:
                    seq = s[i] + s[i + 1]
                    if seq in dic:
                        dic[seq] = dic[seq] + 1
                    else:
                        dic.update({seq: 1})
            mseq = max(dic.items(), key=lambda p: p[1])
            if dic[str(mseq[0])] == 1:
                break
            else:
                s = s.replace(mseq[0], chr(valuelist[pointer]))
                rules = rules + [chr(valuelist[pointer]) + " = " + mseq[0]]

        ns = String(s)
        ns.rules = rules
        return ns

    def cyclic_bits(self, num: int) -> 'String':
        s = self.s
        s = self.unitobin()
        if num > 0:
            slic = s[:num:]
            s = s[num::]
            s = s + slic
        elif num < 0:
            slic = s[num::]
            s = s[:num:]
            s = slic + s
        nstring = ""
        for i in range(0, len(s), 8):
            slic = int(s[i:i + 8], 2)
            nstring = nstring + chr(slic)
        return String(nstring)

    def cyclic_chars(self, num: int) -> 'String':
        s = self.s
        nstr = []
        for i in range(len(s)):
            nstr = nstr + [ord(s[i])]

        for i in range(len(nstr)):
            if not (127 > nstr[i] > 31):
                raise CyclicCharsDecodeError
            else:
                nstr[i] = nstr[i] + num
                if nstr[i] > 126:
                    nstr[i] = nstr[i] - 127 + 32
                if nstr[i] < 32:
                    nstr[i] = nstr[i] + 127 - 32
        s = ""
        for i in range(len(nstr)):
            s = s + chr(nstr[i])
        return String(s)

    def histogram_of_chars(self) -> dict:
        s = self.s
        dic = {"control code": 0, "digits": 0, "upper": 0, "lower": 0, "other printable": 0, "higher than 128": 0}
        while s != "":
            if 0 <= ord(s[0]) <= 32 or ord(s[0]) == 127:
                dic["control code"] = dic["control code"] + 1
            if 128 <= ord(s[0]) <= 256:
                dic["higher than 128"] = dic["higher than 128"] + 1
            if 48 <= ord(s[0]) <= 57:
                dic["digits"] = dic["digits"] + 1
            if 65 <= ord(s[0]) <= 90:
                dic["upper"] = dic["upper"] + 1
            if 97 <= ord(s[0]) <= 122:
                dic["lower"] = dic["lower"] + 1
            if 33 <= ord(s[0]) <= 47 or 58 <= ord(s[0]) <= 64 or 91 <= ord(s[0]) <= 96 or 123 <= ord(s[0]) <= 126:
                dic["other printable"] = dic["other printable"] + 1
            s = s[1::]

        return dic

    def decode_base64(self) -> 'String':
        s = self.s
        nlist = []
        for i in s:
            if i == "/":
                nlist = nlist + [63]
            elif i == "+":
                nlist = nlist + [62]
            elif 90 >= ord(i) >= 65:
                nlist = nlist + [ord(i) - 65]
            elif 122 >= ord(i) >= 97:
                nlist = nlist + [ord(i) - 97 + 26]
            elif 57 >= ord(i) >= 48:
                nlist = nlist + [int(i) + 52]
            else:
                raise Base64DecodeError
        nlist = self.sixfourtobin(nlist)
        if len(nlist) == 6:
            raise Base64DecodeError
        rem = len(nlist) % 8
        if rem != 0:
            nlist = nlist[:-rem:]
        flist = []

        for i in range(0, len(nlist), 8):
            flist = flist + [nlist[i:i + 8]]
        s = ""
        for i in range(0, len(flist)):
            flist[i] = int(flist[i], 2)
            s = s + chr(flist[i])

        return String(s)

    def decode_byte_pair(self) -> 'String':
        rules = self.rules
        s = self.s
        if rules == []:
            raise BytePairDecodeError

        while rules != []:
            s = s.replace(rules[-1][0], rules[-1][4::])
            rules.pop(-1)
        return String(s)

    def decode_cyclic_bits(self, num: int) -> 'String':
        s = self.s
        s = self.unitobin(s)
        num = -num
        if num > 0:
            slic = s[:num:]
            s = s[num::]
            s = s + slic
        elif num < 0:
            slic = s[num::]
            s = s[:num:]
            s = slic + s
        nstring = ""
        for i in range(0, len(s), 8):
            slic = int(s[i:i + 8], 2)
            nstring = nstring + chr(slic)
        return String(nstring)

    def decode_cyclic_chars(self, num: int) -> 'String':
        s = self.s
        nstr = []
        for i in range(len(s)):
            nstr = nstr + [ord(s[i])]

        for i in range(len(nstr)):
            if not (127 > nstr[i] > 31):
                raise CyclicCharsDecodeError
            else:
                nstr[i] = nstr[i] - num
                if nstr[i] >= 127:
                    nstr[i] = nstr[i] - 127 + 32
                if nstr[i] <= 31:
                    nstr[i] = nstr[i] + 127 - 32
        s = ""
        for i in range(len(nstr)):
            s = s + chr(nstr[i])
        return String(s)


m = String("Hello world")
m=m.base64()
print(m)
#m=m.decode_cyclic_bits(8)
#print(m)
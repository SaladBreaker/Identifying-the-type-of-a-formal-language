class Grammar:
    def __init__(self):
        self.__VN = self.__readV("Vn")
        self.__VT = self.__readV("Vt")
        self.__S = self.__readS()
        self.__P = self.__readP()

# GETTERS
    def getP(self):
        return self.__P

    def getS(self):
        return self.__S

    def getVN(self):
        return self.__VN

    def getVT(self):
        return self.__VT

# FUNCTION FOR CORRECTNESS
    def __correctFormatV(self,text):
        if text[0] == '{' and text[-1] == '}':
            return 1
        return 0

    def __correctFormatS(self,text):
        if text[0] == '{' and text[-1] == '}':
            return 1
        return 0

    def __correctFormatP(self,text):
        if text[0] == '{' and text[-1] == '}':
            aux = text[1:-1].split(",")
            for p in aux:
                if ('=' not in p) and ('→' not in p):
                    return 0
            return 1
        return 0


# FUNCTIONS FOR READING
    def __readV(self, option):
        # reading from the keyboard the Vn or Vt (common function)
        print("Please write the " + option + " (respect the format: {A, B, C})")
        text = self.__readWithoutSpaces()
        if not self.__correctFormatV(text):
            raise Exception("Incorrect input at:" + option)
        text = text[1:]
        text = text [:-1]
        text = text.split(",")
        text.append("λ")
        return text

    def __readS(self):
        # reading from keyboard the S
        print("Please write the S (respect the format: {x0})")
        text = self.__readWithoutSpaces()
        if not self.__correctFormatS(text):
            raise Exception("Incorrect input at S!")
        text = text[1:]
        text = text[:-1]
        return text

    def __readP(self):
        print("Please write the S (respect the format: {A → 0A|1B|1, B → 0C|1A} or {A = 0A|1B|1, B = 0C|1A})")
        text = self.__readWithoutSpaces()
        if not self.__correctFormatP(text):
            raise Exception("Incorrect input at P!")
        text = text[1:]
        text = text[:-1]
        text = text.split(",")

        i = 0
        n = len(text)
        while i < n:

            # breaks A → 0A|1B|1 in  A → 0A, A → 1B, A → 1
            if "|" in text[i]:
                aux = text[i].split("|")
                if "=" in aux[0]:
                    head = aux[0].split("=")[0] + "="
                elif "→" in text[i]:
                    head = aux[0].split("→")[0] + "→"

                text[i] = aux[0]

                j = 1
                for j in range(1, len(aux)):
                    text.append(head + aux[j])
                    n += 1
                if j == len(aux):
                    n -= 1

            # splits each production rule regarding the = or →
            if "=" in text[i]:
                text[i] = text[i].split("=")
            elif "→" in text[i]:
                text[i] = text[i].split("→")
            i += 1
        return text


# FUNCTIONS FOR PRINTING
    def __printVn(self):
        result = "{"
        for a in self.__VN:
            result += a + ","
        result = result[:-1] + '}'
        return result

    def __printVT(self):
        result = "{"
        for a in self.__VT:
            result += a + ","
        result = result[:-1] + '}'
        return result

    def __printS(self):
        return "{"+self.__S+"}"

    def __printP(self):
        result = "{"
        for a in self.__P:
            result += a[0] + "→" + a[1] + ","
        result = result[:-1] + '}'
        return result

    def __repr__(self):
        return "Vn=" + self.__printVn() + " Vt=" + self.__printVT() + " S=" + self.__printS() + " P=" + self.__printP()

# ADDITIONAL FUNCTIONS
    def __readWithoutSpaces(self):
        #reads from keyboard and deletes the sapces
        result = ""
        text = input()
        for i in range(len(text)):
            if text[i] != " ":
                result += text[i]
        return result

# FUNCTIONS FOR DETERMINING THE TYPE
    def __compressRule(self,rule):
        # if more consecutive Vt elements are found they are compressed
        if self.__getLenght(rule) < 2:
            return rule

        n = len(rule)
        i = 0
        word = ""
        while i < n:
            if word in self.getVN() and word != "":
                word = rule[i]
                i += 1
            elif word in self.getVT() and word != "":
                aux = len(word)
                rule = rule[:i - len(word)] + "{" + rule[i:]
                i = i - aux + 1
                word = ""
            else:
                word = word + rule[i]
                i += 1
            n = len(rule)
        if word in self.getVT() and word != "":
            rule = rule[:i - len(word)] + "{"

        result = list(rule)
        rule = ""
        i= 0
        n = len(result)
        while i < n:
            if result[i] != "{":
                rule += result[i]
            else:
                while i < n and result[i] == "{":
                    i += 1
                i -= 1
                rule += self.getVT()[0]
            i += 1
            n = len(result)

        return rule

    def __getRuleOrientation(self,rule):
        n = len(rule)
        i = 1
        word = rule[0]
        while i < n:
            if word in self.getVN():
                if len(word) == n:
                    return "none"
                return "left"
            elif word in self.getVT():
                if len(word) == n:
                    return "none"
                return "right"
            word = word + rule[i]
            i += 1

        if word in self.getVN() or word in self.getVT():
            return "none"

        raise Exception("Possible coding error! (found at Grammar::__getRuleOrientation)")

    def __getLenght(self,rule):
        n = len(rule)
        i = 1
        ct = 0
        word = rule[0]
        while i < n:
            if (word in self.getVT()) or (word in self.getVN()):
                ct += 1
                word = rule[i]
            else:
                word = word + rule[i]
            i += 1
        if (word in self.getVT()) or (word in self.getVN()):
            ct += 1
        else:
            raise Exception("Undefined term used or common elements found in Vn and Vt!")
        return ct

    def __checkLeftSide(self):
        # checks length of left side of production rules
        P = self.getP()
        for rule in P:
            if self.__getLenght(rule[0]) != 1:
                return 0
        return 1

    def __checkRightSide(self):
        # checks length of right side of production rules > 2
        P = self.getP()
        for rule in P:
            if self.__getLenght(self.__compressRule(rule[1])) > 2:
                return 0
        return 1

    def __checkOrientation(self):

        check = list()
        P = self.getP()
        for rule in P:
            check.append(self.__getRuleOrientation(self.__compressRule(rule[1])))

        i = 0
        while i < len(check) and check[i] == "none":
            i += 1

        if i == len(check):
            return 1
        for j in range(i, len(check)):
            if check[i] != check[j] and check[j] != "none":
                return 0
        return 1

    def __checkBreaking(self):
        #check length of left and right
        P = self.getP()
        for rule in P:
            if self.__getLenght(rule[0]) > self.__getLenght(rule[1]):
                return 1
        return 0

    def getType(self):
        if self.__checkLeftSide() == 1:
            if self.__checkRightSide() == 1 and self.__checkOrientation() == 1:
                return "Type 3"
            else:
                return "Type 2"
        elif self.__checkBreaking() == 1:
            return "Type 0"
        else:
            return "Type 1"


def main():
    try:
        a = Grammar()
        print(a.getType())
        print(a)
        print("Do you want to restart?(Y/N)")
        a = input()
        if a in {"yes", "y", "Y", "Yes"}:
            main()
            return
        elif a in {"No", "no", "N", "n"}:
            return
        else:
            print("Unknown answer. Exiting!")
            return
    except Exception as error:
        print(error)
        print("Do you want to restart?(Y/N)")
        a = input()
        if a in {"yes","y","Y","Yes"}:
            main()
            return
        elif a in {"No","no","N","n"}:
            return
        else:
            print("Unknown answer. Exiting!")
            return

main()
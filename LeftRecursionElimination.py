gram = { "A":[["B", "a", "d"], ["A", "a"], ["c"]], "B":[["B", "b"], ["A", "b", "b"], ["d"]]}
N = ["A", "B"]

def checkForIndirect(gram, A1, A2):
    if A2 not in gram:
        return False
    if A1 == A2:
        return True

    if A2 in gram.keys():
        for i in gram[A2]:
            if i[0] == A1:
                return True
    return False


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def elminateLR(gram):

    newGram = {}
    verifiedGram = {}
    noILR = True

    for i in gram:
        newVal = None
        j = 0
        while j < len(gram[i]):
            for k in gram[i][j]:
                # print(i, j, k, gram, verifiedGram, newGram)

                if gram[i][j].index(k) == 0:
                    if checkForIndirect(verifiedGram,i, k):
                        tempVal = gram[i].pop(j)
                        tempVal.pop(0)

                        for values in gram[k]:
                            valuesCopy = values.copy()
                            if tempVal:
                                for val in tempVal:
                                    valuesCopy.append(val)


                            gram[i].insert(j, valuesCopy)

                        j -= 1
                        break

                if j + 1 == len(gram[i])  and gram[i][j].index(k) == 0 and noILR == False:
                    noILR = True
                    j = -1
                    break


                if k == i and noILR == True:
                    newVal = k + "1"
                    if newVal not in newGram:
                        newValList = []
                        newValList.append(['\u03BB'])

                    else:
                        newValList = newGram[newVal]

                    newValList.insert(0, gram[i].pop(j))
                    newValList[0].remove(k)
                    if len(newValList[0])> 1:
                        newValList[0].append(newVal)
                    newGram[newVal] = newValList
                    j -= 1
                    break

            if newVal and newVal not in gram[i][j]:
                gram[i][j].append(newVal)

            j += 1

        verifiedGram[i] = gram[i]
        noILR = False

    newGram = merge_two_dicts(gram, newGram)
    return newGram


def show(gram):
    for k in sorted(gram.keys()):
        str = ""
        for l in gram[k]:
            for m in l:
                str += m + " "
            str += " | "
        print(k, "->", str[:-2])


print("Initial gram")
show(gram)

gram = elminateLR(gram)

print("\nFinal gram")
show(gram)

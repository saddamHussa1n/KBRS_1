import re
import sys
from functools import reduce
from math import gcd
from math import sqrt


def readFile(name):
    f = open(name)
    content = f.read()
    f.close()
    return content



def distanceToNormalFrencuencies(aeosFrecuencies):
    normalFrecuencies = [0.1260, 0.0937, 0.0834, 0.0770]
    sum = 0
    for i in range(0, 4):
        sum += (normalFrecuencies[i] - aeosFrecuencies[i]) ** 2
    return sqrt(sum)


def generateKey(baseKey, length):
    baseKeyLength = len(baseKey)
    key = [baseKey[i % baseKeyLength] for i in range(0, length)]
    return key


def decipher(message, key):
    messageLength = len(message)
    decipheredMessage = ""
    keyArray = generateKey(key, messageLength)
    for i in range(0, messageLength):
        decipheredNumber = (ord(message[i]) - ord(keyArray[i]) + 26) % 26
        decipheredMessage += chr(decipheredNumber + 65)
    return decipheredMessage


def addToLetter(letter, n):
    positionInAlphabet = ord(letter) - 65
    newLetter = (positionInAlphabet + n) % 26
    return chr(newLetter + 65)


def getNGrams(text, n):
    regex = f".\x7B{n}\x7D"
    matches = re.findall(regex, text)
    nGrams = dict({})
    for match in matches:
        if match in nGrams:
            nGrams[match] = nGrams[match] + 1
        else:
            nGrams[match] = 1
    return sorted(nGrams.items(), key=lambda x: x[1], reverse=True)


def getNGramPositions(nGram, text):
    matches = re.finditer(nGram, text)
    positions = []
    for match in matches:
        positions.append(match.end(0))
    return positions


def estimateKeyLength(cipheredText):
    def estimateKeyLength(cipheredText, maxSamples):
        tetraGrams = getNGrams(cipheredText, 4)
        triGrams = getNGrams(cipheredText, 3)
        positions = []
        i = 0
        j = 0
        while len(positions) < maxSamples:
            if tetraGrams[i][1] >= 2:
                positions.append(getNGramPositions(tetraGrams[i][0], cipheredText))
                i += 1
            elif triGrams[i][1] >= 2:
                positions.append(getNGramPositions(triGrams[j][0], cipheredText))
                j += 1
            else:
                break
        differences = []
        for pos in positions:
            differences += [y - x for x, y in zip(pos, pos[1:])]
        return reduce(gcd, differences)

    keyLength = 1
    maxSamples = 6
    while (keyLength == 1 and maxSamples > 1):
        maxSamples -= 1
        keyLength = estimateKeyLength(cipheredText, maxSamples)
    return keyLength


def getSubcriptograms(keyLength, text):  # делит строку на подстроки
    textLength = len(text)
    return [text[i:textLength:keyLength] for i in range(0, keyLength)]


def getLettersFrecuency(letters, text):
    criptogramLength = len(text)
    lettersDictionary = dict(getNGrams(text, 1))
    frecuencies = []
    for letter in letters:
        if not (letter in lettersDictionary):
            frecuencies.append(0)
        else:
            frecuencies.append(lettersDictionary[letter] / criptogramLength)
    return frecuencies


def getKey(keyLength, cipheredText):
    criptograms = getSubcriptograms(keyLength, cipheredText)
    print(keyLength)
    possibleKey = []
    for criptogram in criptograms:
        letters = getNGrams(criptogram, 1)
        distances = []
        for i in range(0, 6):
            possibleA = letters[i][0]
            possibleE = addToLetter(possibleA, 4)
            possibleO = addToLetter(possibleE, 10)
            possibleS = addToLetter(possibleO, 5)
            possibleAEOS = [possibleA, possibleE, possibleO, possibleS]
            frecuencies = getLettersFrecuency(possibleAEOS, criptogram)
            distances.append((possibleA, distanceToNormalFrencuencies(frecuencies)))
        sortedDistances = sorted(distances, key=lambda x: x[1])
        possibleKey.append(sortedDistances[0][0])
    return possibleKey


def printResults(keyLength, key, message):
    print(f"Key length: {keyLength}")
    print(f"Most probable key: {key}")
    print("--------------------------")
    print("MESSAGE")
    print("--------------------------")
    print(message)


def main():
    cipheredText = 'HWRJHKCHHAMJTREWUKJDTJCHHAJIHKIYOLXFOGXVBKKPMFGAJDVVTRKUIPSGNZRPIDXYXTOJJEQJWYZHENTVKNKAKWPCRZRVSGETVCYZJKMKNLRLIOEITLYVCEWGTGJDXEPVLMSLIEQGECXHDOSDPYXLCWCCHAQAXAWPLRKTYJENTWCOYYLZLLUATEJWBAASJBSITITVMHIUZCGIBATVKQUUJKVVOCXZUISIXYJCQJGVWKGSMWVVNQKZQPITALOXKAGREJKKSNCGMMBPHWPVQRUYJESEBLCOYYLZMCTJHUTKLRNLLEGKBKYMYHIJFYQPDCXYXKOUQYGVLQOIBAEEWBKTQJHJTPGUIKQGTWSLDPXFWCIYOLXKACSPDWTIHNKYBUMDIJKTUJXVWAXFFPSMBPGSUTXFKROVDWXKTAQYUYSMXPOUWPLVYGRLISMKAMAAJDIUXAXFFPMFGIKFYOEEBLZYQYXRUJKWHKFCXKGUTZMWYGIBBPXFMPGJUZMXBRGSSQVIXLIPUOWLVFGZKGEJAMXIYPGFBLGUTKXYXPIYOLXFVSXYUJGPTPKBIAHWHPZOUNEELMSZCWOZGEZYQYMEZYTKFNSJXAAAYJKKACVLHLIKKYZVHOHZYDOJKHXITLYVCSEIXYZAQYOJTPKAOLMTTJRFSWVIBCJVKPYJBLMHJNSATLZOQPMJWGYNKEWVWYYHBAKZMGSHJAJZECZOQPXYXSYLHEWKKGIRUZMEMMJVMJPFTBOUWKVFICTPDCAYXLOAQNVZOCYHIWRVFYOSQPXRVFSLDPLFPCBLHKRVAGMOFNSWBJKLNWQGECZOUSEEGYIYOSSIFRXHLAPCXBGBJKQRMGIHBHCSXRCLUJGFFNAAUNWNBRNVKPYJXPOUJAVRVROVDOXRKROUWBVFFYXVKJHKACAZUKJITLYVCSEIXQIHCOLRLEXVMJMEMCXUQPMFGYRSOPLVKCCLHAQZEJOVDNEELMSDQNIRMRGJAOMEMFKMYNWKLGDTEJXYLMLAXEWDTPQZQERTKCGZUKZVKRNPIOEDXROTUBVRFCOUYJNLGCBLDZSIFAGMUAVVECGZUZHRMYYOESMEZRNHJEXYTBIVBHITMCJTENIKAYTKEQFCXRNLDQQSXPUMIWQGECYVVNEELMSDQNIKAYZXKWVKXPZOQJMKAYJPDPLVLYSLGQEIMCXVVPLVIPKCYKYJRCGYSNCGMMRVSGIIPYYWQNXZVSRHHHCJNAILIOJLENXVSQVZGEGUUOXZFYZLTQWDBJRPEJFVYMXLYPARLRGRUJHFPLHFQQXYHPOAYAWRGBIYOLXFPYRSMWWVLROTQPIUUWZOUQWWXBKYQHFLKCGBEBMEOCYAYCEKBMTMREXFAYBLQYGINCJVLAVLLKOSBESEUWPBDAOAAEQQXCOAAFMQADOAZFPRWGLADENQACNYZFPRWFLBZFPNXFNBZFMOAFKYCINNZGKYDHMOAFKYDHMOZGKYCIMRXFKYCIMOZGNYOKBPJLYZHWZ'
    keyLength = estimateKeyLength(cipheredText)
    keyLetters = getKey(keyLength, cipheredText)
    if keyLetters == []:
        print("Unable to decrypt message")
        exit(1)
    key = reduce(lambda x, y: x + y, keyLetters)
    printResults(keyLength, key, message)


main()

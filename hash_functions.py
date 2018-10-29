import hashlib
import itertools
import time
import re
    
hashBits = 32
hashChars = hashBits//4 #(1/4 hex)
numVariations = 2**(hashBits//2)

"""
convert base 10 number i to base b with a maximum num digits n
@param i: the number in decimal we wish to convert
@param b: the base to which we wish to convert i
@param n: the maximum number of digits we wish to respect when building the converted value
@returns: a list containing the digits corresponding to the number i when converted to base
"""
def baseConvert(i,b,n):
    result = []
    while i > 0:
            result.insert(0, i % b)
            i //= b
    return [0]*(n-len(result)) + result


"""apply collision attack by adding combinations of space-backspace to the end of input string to generate hash variances
@param om: original message 
@param fm: fraudulent message
@returns: whether an identical fraudulent hash was located (true) or not (false)
"""
def endInsert(originalMessage,fraudMessage):
    start_time = time.time()
    #2. B generates 2^m/2 variations x' of x 
    print("generating x' variations of legitimate message")
    xp = [0]*numVariations
    for i in range(numVariations):
        xp[i] = hashlib.md5((originalMessage + " \b"*i).encode("utf-8")).hexdigest()[:hashChars]
    print("finished generating {0} variations of original message in time = {1} seconds".format(numVariations,int(time.time() - start_time)))
    start_time = time.time()
    
    #4. generate variations y' of y until a match is found
    print("generating and comparing y' variations of fraudulent message")
    for i in itertools.count():
        fraudVar = fraudMessage + " \b"*i
        hashedFraudVar = hashlib.md5(fraudVar.encode("utf-8")).hexdigest()[:hashChars]
        if hashedFraudVar in xp:
            ind = xp.index(hashedFraudVar)
            print("found y' number {0} = '{1} with hash {2} matching \nx' number {3} = '{4} in time = {5} seconds".format(
                i,fraudMessage + "'" + ' + " \\b"*'+str(i),hashedFraudVar,ind,
                originalMessage + "'" + ' + " \\b"*'+str(ind),int(time.time() - start_time)))
            return True
    return False

"""apply collision attack by interweaving combinations of spaces and backspaces in place of spaces in input string to generate hash variances
@param om: original message 
@param fm: fraudulent message
@returns: whether an identical fraudulent hash was located (true) or not (false)
"""
def interweave(om,fm):
    start_time = time.time()
    oms = [m.start() for m in re.finditer(' ', om)]
    fms = [m.start() for m in re.finditer(' ', fm)]
    vs = [" ", " \b ", "  \b", "  \b\b "]
    #2. B generates 2^m/2 variations x' of x 
    print("generating x' variations of legitimate message")
    xp = [0]*numVariations
    xpo = [0]*numVariations
    for i in range(numVariations):
        curVal = baseConvert(i,4,8)
        modifiedMessage = om[:oms[0]] + vs[curVal[0]] + om[oms[0]+1:oms[1]] + vs[curVal[1]] + om[oms[1]+1:oms[2]] + vs[curVal[2]] + om[oms[2]+1:oms[3]] + vs[curVal[3]] \
        + om[oms[3]+1:oms[4]] + vs[curVal[4]] + om[oms[4]+1:oms[5]] + vs[curVal[5]] + om[oms[5]+1:oms[6]] + vs[curVal[6]] + om[oms[6]+1:oms[7]] + vs[curVal[7]] + om[oms[7]+1:]
        xp[i] = hashlib.md5(modifiedMessage.encode("utf-8")).hexdigest()[:hashChars]
        xpo[i] = modifiedMessage
    print("finished generating {0} variations of original message in time = {1} seconds".format(numVariations,int(time.time() - start_time)))
    start_time = time.time()
    
    #4. generate variations y' of y until a match is found
    print("generating and comparing y' variations of fraudulent message")
    for i in range(numVariations):
        curVal = baseConvert(i,4,8)
        fraudVar = fm[:fms[0]] + vs[curVal[0]] + fm[fms[0]+1:fms[1]] + vs[curVal[1]] + fm[fms[1]+1:fms[2]] + vs[curVal[2]] + fm[fms[2]+1:fms[3]] + vs[curVal[3]] \
        + fm[fms[3]+1:fms[4]] + vs[curVal[4]] + fm[fms[4]+1:fms[5]] + vs[curVal[5]] + fm[fms[5]+1:fms[6]] + vs[curVal[6]] + fm[fms[6]+1:fms[7]] + vs[curVal[7]] + fm[fms[7]+1:]
        hashedFraudVar = hashlib.md5(fraudVar.encode("utf-8")).hexdigest()[:hashChars]
        if hashedFraudVar in xp:
            ind = xp.index(hashedFraudVar)
            print("found y' number {0} = {1} with hash {2} matching \nx' number {3} = {4} in time = {5} seconds".format(
                i,repr(fraudVar),hashedFraudVar,ind, repr(xpo[ind]),int(time.time() - start_time)))
            return True
    return False

def main():
    #1,3. establish legitimate and fradulent base messages
    originalMessage = input("please enter legitimate message (leave blank for default): ")
    if (originalMessage == ""):
        originalMessage = "The quick brown fox jumps over the lazy dog."
    print("legitimate message detected as '{0}'".format(originalMessage))
    fraudMessage = input("please enter fraudulent message (leave blank for default): ")
    if (fraudMessage == ""):
        fraudMessage = "The scheming purple fox jumps onto the frightened dog."
    print("fraudulent message detected as '{0}'".format(fraudMessage))
    if (len(fraudMessage.split(" ")) < 9 or len(originalMessage.split(" ")) < 9):
        print("too few spaces to properly interweave insertions; sticking space-backspace characters at the end instead")
        return endInsert(originalMessage,fraudMessage)
    if (not interweave(originalMessage,fraudMessage)):
        print("interweave failed to find a match; fall-back to space-back end insertion")
        return endInsert(originalMessage, fraudMessage)

if __name__ == "__main__":
    main()
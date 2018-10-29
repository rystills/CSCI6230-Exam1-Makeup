import hashlib
import itertools
import time
import itertools
    
hashBits = 32 #more bits = more secure, but takes longer + more memory
hashChars = hashBits//4 #(1/4 hex)
numVariations = 2**(hashBits//2)

def base_convert(i, b,n):
    result = []
    while i > 0:
            result.insert(0, i % b)
            i = i // b
    return [0]*(n-len(result)) + result

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
            break

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

if __name__ == "__main__":
    main()
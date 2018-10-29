import hashlib
import itertools
import time
    
hashBits = 32 #more bits = more secure, but takes longer + more memory
hashChars = hashBits//4 #(1/4 hex)
numVariations = 2**(hashBits//2)

def main():
    start_time = time.time()
    #1. A is prepared to sign legitimate message x
    originalMessage = input("please enter legitimate message (leave blank for default): ")
    if (originalMessage == ""):
        originalMessage = "The quick brown fox jumps over the lazy dog."
    print("legitimate message detected as '{0}'".format(originalMessage))
    fraudMessage = input("please enter fraudulent message (leave blank for default): ")
    if (fraudMessage == ""):
        fraudMessage = "The scheming purple fox jumps onto the frightened dog"
    print("fraudulent message detected as '{0}'".format(fraudMessage))
    
    #2. B generates 2^m/2 (for md5, 2^64) variations x' of x 
    xp = [0]*numVariations
    for i in range(numVariations):
        xp[i] = hashlib.md5((originalMessage + " \b"*i).encode("utf-8")).hexdigest()[:hashChars]
    print("finished generating {0} variations of original message in time = {1} seconds".format(numVariations,time.time() - start_time))
    start_time = time.time()
    
    #3. B prepares fraudulent message y (already performed this during step 1)
    
    #4. generate variations y' of y until a match is found
    for i in itertools.count():
        fraudVar = fraudMessage + " \b"*i
        hashedFraudVar = hashlib.md5(fraudVar.encode("utf-8")).hexdigest()[:hashChars]
        if hashedFraudVar in xp:
            ind = xp.index(hashedFraudVar)
            print("found y' number {0} with hash {1} matching x' number {2} in time = {3} seconds".format(i,hashedFraudVar,ind,time.time() - start_time))
            print("x' = {0}".format(repr(originalMessage + " \b"*ind)))
            print("y' = {0}".format(repr(fraudVar)))
            break
        
    #5. now we can send off our fraudulent message with the accepted hash

if __name__ == "__main__":
    main()
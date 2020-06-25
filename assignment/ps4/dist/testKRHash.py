from dnaseq import krHashDNA
from dnaseq import nearPrime
from dnaseq import subsequenceHashes

seq = 'TACGTCC'
k = 3
for sub, hsh in subsequenceHashes(seq, k):
    print(sub, hsh)

# find the adjecent prime given n

n = 10000
print(nearPrime(n))


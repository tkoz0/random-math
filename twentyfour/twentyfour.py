import sys
from fractions import Fraction

# binary operators that can always be used
# division uses / because Fraction is being used for more flexibility
ops = \
{
    '+': lambda x,y : x+y,
    '-': lambda x,y : x-y,
    '*': lambda x,y : x*y,
    '/': lambda x,y : x/y
}

precedence = \
{
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}

# returns a dictionary mapping possible value to a parse tree for computing it
# the parse tree is represented as a Fraction or recursive list:
# [operation, left, right], left/right are recursive or Fraction
# operation is a string key from ops
def search(nums):
    assert len(nums) > 0
    for num in nums:
        assert type(num) == Fraction
    if len(nums) == 1:
        return {nums[0]:nums[0]}
    # use the bits to determine set inclusion for the partitioning
    S = dict()
    for subsetnum in range(1,2**len(nums)-1):
        A = [] # 0
        B = [] # 1
        for i in range(len(nums)):
            if subsetnum % 2 == 0:
                A.append(nums[i])
            else:
                B.append(nums[i])
            subsetnum = subsetnum // 2
        A_vals = search(A)
        B_vals = search(B)
        for a in A_vals:
            for b in B_vals:
                for op in ops:
                    # try/except because zero division is possible
                    try:
                        r = ops[op](a,b)
                        if r in S: continue # already found a way to compute it
                        S[r] = [op,A_vals[a],B_vals[b]]
                    except:
                        continue
    return S

def tree2str(t): # tree to string
    if type(t) != list:
        return str(t)
    # do some operator precedence stuff to remove unnecessary parethesis
    top = precedence[t[0]]
    lop = 99 if type(t[1]) != list else precedence[t[1][0]]
    rop = 99 if type(t[2]) != list else precedence[t[2][0]]
    lstr = tree2str(t[1])
    rstr = tree2str(t[2])
    if lop < top: lstr = '('+lstr+')'
    if rop < top: rstr = '('+rstr+')'
    return lstr+t[0]+rstr

if __name__ == '__main__':
    target = Fraction(sys.argv[1])
    inputs = list(map(Fraction,sys.argv[2:]))
    assert len(inputs) > 0
    result = search(inputs)
    if target in result:
        print('found solution')
        print(target,'=',tree2str(result[target]))
    else:
        print('no solution')


**Problem: [single-number](https://www.interviewbit.com/problems/single-number)**

XOR operation of two same bits results in zero.


Since the problem description says that all the integers are repeated exactly twice except one, we can use XOR operation on all the elements of the array to filter out the integer appearing exactly once.

>Example : A = [ 1, 4, 1, 5, 4, 5, 8 ]

For the above example the following are the cummulative XOR (`k^=A[i]`) values 

    k after i=0 : 1
    k after i=1 : 5
    k after i=2 : 4
    k after i=3 : 1
    k after i=4 : 5
    k after i=5 : 0
    k after i=6 : 8
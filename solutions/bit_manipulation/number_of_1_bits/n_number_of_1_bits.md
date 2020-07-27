**Problem: [number-of-1-bits](https://www.interviewbit.com/problems/number-of-1-bits)**

This problem requires us to check and set kth bit in an integer.

**Check kth bit**

- To check **kth** bit in an integer **n** use `x = n&1<<k`
    - `x=1` if set
    - `x=0` if unset
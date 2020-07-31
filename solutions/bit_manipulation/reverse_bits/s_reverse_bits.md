**Problem: [reverse-bits](https://www.interviewbit.com/problems/reverse-bits)**



    unsigned int Solution::reverse(unsigned int A) {
        unsigned int res=0;
        for(int i=31;i>=0;i--){
            if(A&1<<i){
                res= res|(1<<(32-i-1));
            }
        }
        return res;
    }
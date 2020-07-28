

    int Solution::numSetBits(unsigned int A) {
        int count=0;
        for(int i=0;i<32;i++){
            if(A& (1<<i)){
                count+=1;
            }
        }
        return count;
    }


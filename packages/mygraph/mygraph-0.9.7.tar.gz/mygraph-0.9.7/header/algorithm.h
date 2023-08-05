// ========================================================
//  algorithm.h
//  MyGraph
//
//  Created by tonny.achilles on 5/24/14.
//  Copyright (c) 2014 Jiangshan Ma. All rights reserved.
// ========================================================

#ifndef ALGORITHM_H
#define ALGORITHM_H
#include <sys/timeb.h>

class Algorithm {
private:
    
    int start_ms;
    
    int get_now_ms() const;
    
public:
    
    Algorithm();
    
    ~Algorithm();
    
    int get_elapesd_ms() const;
};

#endif /* ALGORITHM_H_ */

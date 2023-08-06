// ========================================================
//  dijkstra.h
//  MyGraph
//
//  Created by tonny.achilles on 5/25/14.
//  Copyright (c) 2014 Jiangshan Ma. All rights reserved.
// ========================================================

#ifndef DIJKSTRA_H
#define DIJKSTRA_H

#include <limits>
#include <string>
#include "algorithm.h"
#include "graph.h"
#include "radixheap.h"
#include <boost/python/numeric.hpp>
namespace bp = boost::python;
class Dijkstra :
public Algorithm
{
private:
    
    Graph* g;
    
    float* u;
    
    int* pre_idx;
    
    bool* open;
    
    bool* close;
    
    Heap* heap;
    
public:
    
    // or const & here: passing by reference or passing a pointer
    Dijkstra(Graph* const _g);
    
    ~Dijkstra();
    
    // to make it thread-safe, run shouldn't change anything of Graph (no write)
    void run(string _oid, const float* _weights);
    
    // get final node labels as node potentials
    const float* get_vlabels();
    
    vector<string> get_path(string _oid, string _did);
    
    bp::list wrapper_get_path(string _oid, string _did);
    
    string get_path_string(const vector<string> &_path, const string _delimeter);
    
};
#endif /* DIJKSTRA_H_ */

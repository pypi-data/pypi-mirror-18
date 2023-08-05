// ========================================================
//  PREDEFINE.h
//  MyGraph
//
//  Created by tonny.achilles on 5/29/14.
//  Copyright (c) 2014 Jiangshan Ma. All rights reserved.
// ========================================================

#ifndef PREDEFINE_H
#define PREDEFINE_H

//#define DRM_NUM_NODES 195669
//#define DRM_NUM_LINKS 460098


#define CONNECTION "host=localhost port=5432 dbname=testdb user=postgres password=password"
const std::string WORKING_DIRECTORY = "/Volumes/SSD/Projects/Xcode/hypernav";



// test graph path settings
constexpr auto GRAPH_BELL_ONEWAY_CSV_PATH = "./data/BellOneway.csv";
constexpr auto GRAPH_BELL_CSV_PATH = "./data/Bell_biway.csv";
constexpr auto GRAPH_TOKYO_DRM_BIDIRECTIONAL_CSV_PATH = "./data/Tokyo_DRM_bidirectional.csv";

// hypernav path settings
const auto HDF5 = WORKING_DIRECTORY + "/data/5-95.h5";
const auto TURN_RESTRICTIONS_CSV_PATH = WORKING_DIRECTORY + "/data/turn_restrictions.csv";

// matsim module path settings
const auto GRAPH_TOKYO_MATSIM_CSV_PATH = WORKING_DIRECTORY + "/data/input_Tokyo/network.csv";
const auto PROFILE_TOKYO_MATSIM_CSV_PATH = WORKING_DIRECTORY + "/data/input_Tokyo/maxdelay.csv";

#endif

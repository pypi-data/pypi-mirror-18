//
//  main.cpp
//  main
//
//  Created by tonny.achilles on 12/25/14.
//  Copyright (c) 2014 tonny.achilles. All rights reserved.
//

#include "matsimhelper.hpp"
#include <iostream>
using namespace std;

int main(int argc, char** argv){
    
    // set default thread number 4
    if(argc == 1)
    {
        pplan_handler_omp("/Users/tonny/Documents/github/hypernav/input_Tokyo/test/in_all.xml", "/Users/tonny/Documents/github/hypernav/input_Tokyo/test/out.xml", 4);
    }
    else
    {
    // ---------------- print out arguments -------------------
    printf("arguments: \n");
    for (int i = 0; i < argc; ++i)
    {
        printf("%s\n", argv[i]);
    }

    string network_path = "input/network.xml";
    string plans_path = "input/plans.xml";
    string maxdelay_path = "input/maxdelay.csv";
    string plans_out_path = "output/plans_out.xml";
    string events_out_path = "output/events_out.xml";
    
    // ---------------- analyze events.xml.gz -----------------
    
    // ---------------- modify profile.csv --------------------
    
    // ---------------- analyze ext1_config.xml ---------------
    
    int number_of_threads = argc == 3 ? std::stoi(argv[1]) : 20;
    const string config_path = argc == 3 ? argv[2] : "/Users/tonny/Documents/github/hypernav/input_Tokyo/tmp/ext1_config.xml";
    cout << "analyzing " << config_path << endl;
    
    boost::property_tree::ptree *pt_config = new boost::property_tree::ptree();
    boost::property_tree::xml_parser::read_xml(config_path, *pt_config);
    
    auto params = pt_config->get_child("config.module");
    
    for (const auto& param : params) {
        if (param.first == "param") {
            if (param.second.get<string>("<xmlattr>.name")
                == "inputPlansFilename")
                plans_path = param.second.get<string>("<xmlattr>.value");
            if (param.second.get<string>("<xmlattr>.name") == "networkFilename")
                network_path = param.second.get<string>("<xmlattr>.value");
            if (param.second.get<string>("<xmlattr>.name")
                == "workingEventsTxtFilename")
                events_out_path = param.second.get<string>("<xmlattr>.value");
            if (param.second.get<string>("<xmlattr>.name")
                == "workingPlansFilename")
                plans_out_path = param.second.get<string>("<xmlattr>.value");
            
            cout << param.second.get<string>("<xmlattr>.name") << ": "
            << param.second.get<string>("<xmlattr>.value") << endl;
        }
    }
    
    delete pt_config;
    
    pplan_handler_omp(plans_path, plans_out_path, number_of_threads);
    
#pragma omp barrier // wait for all
    
    cout << "the end" << endl;
    cout << "end time: " << get_current_time() << endl;
}
    cout << "completed!" << endl;
    
    return 0;
}
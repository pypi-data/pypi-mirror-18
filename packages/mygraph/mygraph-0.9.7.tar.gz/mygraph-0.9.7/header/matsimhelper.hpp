//
//  matsimhelper.h
//  hyperpath_td
//
//  Created by tonny.achilles on 1/5/15.
//  Copyright (c) 2015 tonny.achilles. All rights reserved.
//

#ifndef hyperpath_td_matsimhelper_h
#define hyperpath_td_matsimhelper_h
#include <iostream>
#include <fstream>
#include <unordered_map>
#include <random>
#include <iomanip>
#include <string>

#include "graph.hpp"
#include "dijkstra.h"
#include "hyperpath.h"
#include "csvhelper.hpp"
#include "graphbuilder.hpp"
#include "graphhelper.hpp"
#include "datetimehelper.hpp"
#include <boost/lexical_cast.hpp>

#ifdef OPENMP
#include <omp.h>
#endif
using namespace std;
using namespace boost::property_tree::xml_parser;

void omp_process_one_element(pair<const string, boost::property_tree::basic_ptree<string, string,less<string> > > &element,
                             Graph* const g, ostream* output, int m, vector<int> &time_second_keys,
                             float* const weights_min, float* const weights_dist,
                             const std::unordered_map<string, std::unordered_map<int, float> >& profile)
{
    float* const weights_max = new float[m];
    auto first = element.first;
    auto pid = element.second.get<string>("<xmlattr>.id");
    //    auto p_age = element.second.get<string>("<xmlattr>.age");
    auto p_employed = element.second.get<string>("<xmlattr>.employed");
    // process one person plan
    
    //    println_safe("person " + pid);
    string o_id = "";
    string d_id = "";
    string start_edge = "";
    string end_edge = "";
    
    // only process trip plans with "selected" = yes
    auto &actlegs = element.second.get_child("plan");
    
    bool skip = false;
    for (const auto &actleg : actlegs)
    {
        if(actleg.first == "<xmlattr>")
        {
            string selected = "";
            // skip plans not selected
            if (actleg.second.get<string>("selected") == "no")
            {
                skip = true;
            }
        }
        if (actleg.first == "act")
        {
            if (actleg.second.get<string>("<xmlattr>.type") == "h9")
            {
                auto first_e_id = actleg.second.get<string>("<xmlattr>.link");
                start_edge = first_e_id;
                o_id = g->get_edge(first_e_id)->to_vertex->id;
            }
            
            else if (actleg.second.get<string>("<xmlattr>.type") == "w5")
            {
                auto end_e_id = actleg.second.get<string>("<xmlattr>.link");
                end_edge = end_e_id;
                d_id = g->get_edge(end_e_id)->from_vertex->id;
            }
        }
    }
    
    auto &legs = element.second.get_child("plan.leg");
    if (skip) {
        auto settings = boost::property_tree::xml_writer_make_settings<std::string> ('\t', 1);
#pragma omp critical
        write_xml_element(*output, std::basic_string<boost::property_tree::ptree::key_type::value_type>(),
                          element.second, -1, settings);
        
        return;
        
    }
    string dep_time = legs.get<string>("<xmlattr>.dep_time");
    
    // calculate arrival time by using departure time and travel time of hyeprpath route
    boost::posix_time::ptime ptime_dep = time_parse_exact(dep_time,"%H:%M:%S");
    
    int dep_time_seconds = ptime_dep.time_of_day().hours() * 3600
    + ptime_dep.time_of_day().minutes() * 60
    + ptime_dep.time_of_day().seconds();
    
    //    cout << "from " << o_id << " to " << d_id << " @ " << dep_time_seconds << endl;
    
    // change the maxdelay in the network according to departure time
    /*refer to http://www.sgi.com/tech/stl/Map.html*/
    /*******************memeory leak if t_seconds is not a key******************/
    
    int converted_time_key = 0;
    for (const auto& time_second_key : time_second_keys)
    {
        if (dep_time_seconds > time_second_key)
        {
            converted_time_key = time_second_key;
            continue;
        }
        else
        {
            //            cout << "time key converted: " << dep_time_seconds << " to "<< converted_time_key<<endl;
            break;
        }
    }
    
    for (int i=0;i< m; ++i)
    {
        auto e_id = g->get_edge(i)->id;
        if (profile.find(e_id)!= profile.end())
        {
            weights_max[i] = profile.at(e_id).at(converted_time_key) + weights_min[i];
        }
        else {weights_max[i] = weights_min[i];}
    }
    //############################################################
    //TODO: call hyperpath to calculate dist, trav_time and route
    
    auto alg = Hyperpath(g);
    Dijkstra dij(g);
    dij.run(o_id, weights_min);
    auto h = dij.get_vlabels();
    alg.run(o_id, d_id, weights_min, weights_max, h);
    
    auto path = alg.get_path_rec(o_id, d_id);
    // not necessary
    //    float path_time = alg.get_path_weights_sum(path, weights_min);
    float path_dist = alg.get_path_weights_sum(path, weights_dist);
    string path_links = start_edge + " " + alg.get_path_rec_estring(path, " ") + " " + end_edge;
    
    //############################################################
    // not necessary
    //    string trav_time = format_time(path_time);
    string distance = to_string(path_dist);
    
    // not necessary
    //    boost::posix_time::ptime ptime_trav = time_parse_exact(trav_time, "%H:%M:%S");
    //    boost::posix_time::ptime ptime_arr = ptime_dep
    //    + boost::posix_time::hours(ptime_trav.time_of_day().hours())
    //    + boost::posix_time::minutes(ptime_trav.time_of_day().minutes())
    //    + boost::posix_time::seconds(ptime_trav.time_of_day().seconds());
    
    // convert ptime to string
    //    std::stringstream stream;
    //    boost::posix_time::time_facet* facet = new boost::posix_time::time_facet();
    //    facet->format("%H:%M:%S");
    //    stream.imbue(std::locale(std::locale::classic(), facet));
    //    stream << ptime_arr;
    //    string arr_time = stream.str();
    
    //#ifdef DEBUG
    //    cout << "departure time: " << dep_time << endl;
    //        cout << "path links to write: " << path_links << endl;
    //    cout << "hyperpath travel time: " << trav_time << endl;
    //    cout << "hyperpath distance: " << distance << endl;
    //    cout << "hyperpath arrival time: " << arr_time << endl;
    //#endif
    
    auto settings = boost::property_tree::xml_writer_make_settings<std::string> ('\t', 1);
    
#pragma omp critical
    {
        // no deparute time choice, also trav_time and arr_time will be recalulated anyway
        //        legs.put("<xmlattr>.trav_time", trav_time);
        //        legs.put("<xmlattr>.arr_time", arr_time);
        legs.put("route", path_links);
        legs.put("route.<xmlattr>.type", "links");
        legs.put("route.<xmlattr>.distance", distance);
        //        legs.put("route.<xmlattr>.trav_time", trav_time);
        *output << "<person id=\"" << pid << "\""<<" ";
        //        *output << "age=\"" << p_age << "\"" << " ";
        *output << "employed=\"" << p_employed << "\">" << endl;
        write_xml_element(*output, std::basic_string<boost::property_tree::ptree::key_type::value_type>(),
                          element.second, -1, settings);
        *output << "</person>\n";
    }
    delete [] weights_max;
    
}

// parallel with openmp, tested for all agents, OK
void pplan_handler_omp(string _input_plan, string _output_plan, int num_threads){
    //int num_threads = omp_get_max_threads();
#ifdef OPENMP
    omp_set_num_threads(num_threads);
#endif
    cout << "starting time: " << get_current_time() << endl;
    // --------------------------- anaylze network.csv ------------------------------
    cout << "analyzing network.csv" << endl;
    const int m = 444228;
    float* const weights_min = new float[m];
    float* const weights_dist = new float[m];
    Graph g = get_tokyo_drm_graph(weights_min, weights_dist);
    
    // -------------------------- anaylze maxdelay.csv ------------------------------
    cout << "analyzing maxdelay.csv" <<endl;
    vector<int> time_second_keys;
    
    const std::unordered_map<std::string, std::unordered_map<int, float> > profile = get_profile(time_second_keys);
    
    // ------------------------- anaylze ext1_plans.xml -----------------------------
    
    cout << "analyzing " << _input_plan << endl;
    boost::property_tree::ptree *pt_plans = new boost::property_tree::ptree();
    boost::property_tree::xml_parser::read_xml(_input_plan, *pt_plans, boost::property_tree::xml_parser::trim_whitespace);
    
    auto &root = pt_plans->get_child("population"); // plans in v4
    
    auto elements = vector<pair <const string, boost::property_tree::basic_ptree<string, string,less<string> > > >();
    for (const auto& element : root) {
        if (element.first == "person") {
            elements.push_back(element);
        }
    }
    delete pt_plans;
    std::filebuf fb;
    cout << "plans_out_path" << _output_plan << endl;
    fb.open(_output_plan, std::ios::out);
    std::ostream output(&fb);
    
    auto settings = boost::property_tree::xml_writer_make_settings<std::string> ('\t', 1);
    
    output << "<?xml version=\"1.0\" encoding=\"";
    output << settings.encoding;
    output << "\"?>\n";
    output<< "<!DOCTYPE population SYSTEM \"http://www.matsim.org/files/dtd/population_v5.dtd\">" << '\n';
    output << "<population>\n";
    
    int p_cnt = 0;
    auto size = elements.size();
#pragma omp parallel for
    for (int i = 0; i < size; ++i  )
    {
#pragma omp atomic
        p_cnt++;
        if(p_cnt % 100 == 0) {
            cout << p_cnt  << '\n';
        }
        
        
        pair<const string, boost::property_tree::basic_ptree<string, string,less<string> > > element = elements[i];
        omp_process_one_element(element, &g, &output, m, time_second_keys, weights_min, weights_dist, profile);
    }
    output << "</population>";
    fb.close();
    delete [] weights_min;
    delete [] weights_dist;
}



#endif


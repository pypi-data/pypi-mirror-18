// ========================================================
//  PREDEFINE.h
//  MyGraph
//
//  Created by tonny.achilles on 9/25/14.
//  Copyright (c) 2014 Jiangshan Ma. All rights reserved.
// ========================================================

#ifndef DRMHELPER_H
#define DRMHELPER_H
#include <hdf5.h>
#include <hdf5_hl.h>
#include <stdlib.h>
#include <iostream>
#include <sys/timeb.h>
#include <time.h>
#include <string>
#include <pqxx/pqxx>
#include <boost/unordered_map.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/python/tuple.hpp>
#include <boost/python.hpp>
#include "PREDEFINE.h"
#include "graph.hpp"

using namespace std;
class Drmhelper {
    
private:
    
    hid_t file_id, dataset_id;
    unordered_map<string, hsize_t> h5key_map;
    unordered_map<string, float> length_map;
    unordered_map<string, float> ffspeed_map;
    unordered_map<string, string> geojson_map;
    
    boost::shared_ptr<Graph> drm_graph;
    pqxx::result r;
    pqxx::connection *conn;
    pqxx::work *x;
    
public:
    
    Drmhelper() {
        drm_graph = nullptr;
        conn = new pqxx::connection(CONNECTION);
    }
    
    ~Drmhelper() {
        delete conn;
    }
    
    void open_hdf(const string &hdf5_path, const string &dataset_name)
    {
        file_id = H5Fopen(hdf5_path.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
        dataset_id = H5Dopen2(file_id, dataset_name.c_str(), H5P_DEFAULT);
    }
    
    void close_hdf()
    {
        H5Fclose(file_id);
        H5Dclose(dataset_id);
    }
    
    struct Coordinate {float lon; float lat;};
    
    string get_nearest_nodecode(const Coordinate& lonlat, const string& nodestable)
    {
        auto lon = lonlat.lon;
        auto lat = lonlat.lat;
        if(! conn->is_open()) conn->activate();
        string nodecode = "";
        float lon_new, lat_new;
        // be care of CRS
    
        try {
            pqxx::work x(*conn);
            
            string query (" SELECT  St_AsText(geom), St_X(St_Transform(geom, 4326)), St_Y(St_Transform(geom, 4326)) FROM"
            " (SELECT geom FROM " + nodestable + " ORDER BY ST_Distance(ST_Transform(ST_GeomFromText('POINT("+
            to_string(lon) + " " + to_string(lat) + ")',4326), 4301) , geom) LIMIT 1 ) AS t;");
            
            r = x.exec(query);
            nodecode = r[0][0].c_str();

//            try {
            lon_new = boost::lexical_cast<float>(r[0][1].c_str());
//            } catch(bad_lexical_cast&) {
//                //Do your errormagic
//            }
            lat_new = boost::lexical_cast<float>(r[0][2].c_str());

        }
        catch (std::exception &e){
            std::cerr << e.what() << endl;
        }
        
        if (nodecode == "") throw std::runtime_error("ERROR: Couldn't find the nearest node");
        return nodecode;
    }
    
    // tests
    // -- 533974-0235: 139.5476, 35.9762
    // -- 533974-0308: 139.6067, 35.9907
    boost::python::tuple wrapper_get_nearest_nodecode(boost::python::object lonlat, const string& nodestable)
    {
        float lon = boost::python::extract<float>(lonlat[0]);
        float lat = boost::python::extract<float>(lonlat[1]);
        if(! conn->is_open()) conn->activate();
        string nodecode = "";
        float lon_new, lat_new;
        // be care of CRS
        try {
            pqxx::work x(*conn);
            
// slightly slower query but may faster when very large nodes set
/*            SELECT geom, nodecode, ST_x(geom) AS lon, ST_y(geom) AS lat FROM
              ST_Transform(ST_GeomFromText('POINT(139.5476 35.9762)', 4326), 4301) AS g1,
              (SELECT * FROM Nodes WHERE ST_Contains(ST_Buffer(ST_Transform(ST_GeomFromText('POINT(139.5476 35.9762)', 4326), 3857), 3000), ST_Transform(geom, 3857))) AS Subgraph_nodes
              ORDER BY ST_Distance(geom, g1) LIMIT 1;
 */
            auto query(" SELECT  St_AsText(geom), St_X(St_Transform(geom, 4326)), St_Y(St_Transform(geom, 4326)) FROM (SELECT geom FROM " + nodestable + " ORDER BY ST_Distance(ST_Transform(ST_GeomFromText('POINT("+
            to_string(lon) + " " + to_string(lat) + ")',4326), 4301) , geom) LIMIT 1 ) AS t;");
            
            r = x.exec(query);
            nodecode = r[0][0].c_str();
//            lon_new = atof(r[0][1].c_str());
            lon_new = boost::lexical_cast<float>(r[0][1].c_str());
//            lat_new = atof(r[0][2].c_str());
            lat_new = boost::lexical_cast<float>(r[0][2].c_str());
            
        }
        catch (std::exception &e){
            cout << e.what() <<endl;
        }
        return boost::python::make_tuple(nodecode, boost::python::make_tuple(lon_new, lat_new));
    }
    
    const boost::shared_ptr<Graph> make_graph(const string& links_view, int n, int m)
    {
        if(! conn->is_open()) conn->activate();
        
        pqxx::work x(*conn);
        
        boost::shared_ptr<Graph> g (boost::make_shared<Graph>(n, m));
        
        string query (" SELECT linkcode, h5key, basic_length AS length, ffspeed,"
        " ST_AsText(ST_StartPoint(geom)) AS fnode,"
        " ST_AsText(ST_EndPoint(geom))  AS tnode,"
        " ST_AsGeojson(ST_Transform(geom, 4326)) AS geojson"
        " FROM " + links_view + ";");
        
        try{
            // TODO: this can be changed to the links inside the rectangle only
            r = x.exec(query);
            for (const auto &row : r)
            {
                string linkcode = row[0].c_str();
                h5key_map[linkcode] = atoi(row[1].c_str());
                length_map[linkcode] =  atof(row[2].c_str());
                ffspeed_map[linkcode] = atof(row[3].c_str());
                g->add_edge(linkcode, row[4].c_str(), row[5].c_str());
                geojson_map[linkcode] = row[6].c_str();
            }
            
        } catch (std::exception &e) {
            cout << e.what() << endl;
        }
        
        drm_graph = g;
        if (drm_graph == nullptr)
            throw GraphException::GraphNotSet();
        
        return drm_graph;
    }
    
    const boost::shared_ptr<Graph> make_graph2(const string& links_view, int n, int m,
                                               int length_lowerlimit = numeric_limits<int>::infinity(), int count_upperlimit = 0)
    {
        if(! conn->is_open()) conn->activate();
        
        pqxx::work x(*conn);
        
        boost::shared_ptr<Graph> g (boost::make_shared<Graph>(n, m));
        
        string query (" SELECT linkcode, h5key, basic_length AS length, ffspeed,"
        " ST_AsText(ST_StartPoint(geom)) AS fnode,"
        " ST_AsText(ST_EndPoint(geom))  AS tnode,"
        " ST_AsGeojson(ST_Transform(geom, 4326)) AS geojson,"
        " count "
        " FROM " + links_view + ";");
        
        
        try{
            // TODO: this can be changed to the links inside the rectangle only
            r = x.exec(query);
            for (const auto &row : r)
            {
                string linkcode = row[0].c_str();
                h5key_map[linkcode] = atoi(row[1].c_str());
                bool condition = atoi(row[7].c_str()) < count_upperlimit && atoi(row[2].c_str()) > length_lowerlimit;
                length_map[linkcode] =  (condition) ? numeric_limits<float>::infinity(): atof(row[2].c_str());
                ffspeed_map[linkcode] = atof(row[3].c_str());
                g->add_edge(linkcode, row[4].c_str(), row[5].c_str());
                geojson_map[linkcode] = row[6].c_str();
            }
            
        } catch (std::exception &e) {
            cout << e.what() << endl;
        }
        
        drm_graph = g;
        if (drm_graph == nullptr)
            throw GraphException::GraphNotSet();
        
        return drm_graph;
    }
    
    
    //TODO: where roadtype = ??
    const boost::shared_ptr<Graph> make_subgraph(const Coordinate& origin, const Coordinate& destination, const string& condition, int buf_dist)
    {
        if(! conn->is_open()) conn->activate();
        
        const float lon_o = origin.lon;
        const float lat_o = origin.lat;
        const float lon_d = destination.lon;
        const float lat_d = destination.lat;
        
        pqxx::work x(*conn);
        string query(
        " DROP VIEW IF EXISTS subgraph_links;"
        " DROP VIEW IF EXISTS subgraph_links;"
        " DROP VIEW IF EXISTS subgraph_nodes;"
        " DROP VIEW IF EXISTS box;"
        " DROP VIEW IF EXISTS buffer_o;"
        " DROP VIEW IF EXISTS buffer_d;"
        " CREATE TEMP VIEW Buffer_O AS SELECT ST_Buffer("
        " ST_Transform"
        " ( "
        "       ST_SetSRID(ST_MakePoint("+ to_string(lon_o)  + "," + to_string(lat_o) + "), 4326), 3857"
        " )," + to_string(buf_dist) + " ) AS geom;"
        
        " CREATE TEMP VIEW Buffer_D AS SELECT ST_Buffer("
        " ST_Transform"
        " ("
        "       ST_SetSRID(ST_MakePoint("+ to_string(lon_d) + "," + to_string(lat_d) + "), 4326), 3857"
        " )," + to_string(buf_dist) + " ) AS geom;"
        " CREATE TEMP VIEW box as select ST_Envelope( "
        " ST_UNION(Buffer_O.geom, Buffer_D.geom) "
        " ) AS geom FROM buffer_o, buffer_d;"
        " CREATE TEMP VIEW subgraph_links AS SELECT links.* FROM links, box WHERE ST_Contains( ST_Transform(box.geom,4301), links.geom) AND "
        + condition + " ;");
        //      e.g.: condition = "basic_roadtype < 6"
        
        //TODO: use WHERE ST_Intersects(nodes.geom, links.geom) to get the subgraph_nodes
        
        cout << query << endl;
        try
        {
            r = x.exec(query);
        }
        catch(std::exception &e)
        {
            cout << e.what() << endl;
        }
        
        int n = 0;
        int m = 0;
        query = "SELECT COUNT(*) AS n FROM (SELECT meshcode || "
        "fnodecode FROM subgraph_links UNION SELECT meshcode || "
        "tnodecode FROM subgraph_links) AS t;";
        try {
            //***********************************************************
            // auto calculate m and n may be slow when the linksview is large
            // (when O and D are far from each other), consider hierarchy based methods
            r = x.exec(query);
            n = r[0]["n"].as<int>();
        }
        catch(std::exception &e)
        {
            cout << e.what() << endl;
        }
        
        query = "SELECT count(*) as m FROM subgraph_links;";
        try {
            r = x.exec(query);
            m = r[0]["m"].as<int>();
        }
        catch (std::exception &e) {
            cout << e.what() << endl;
        }
        
        query = " SELECT linkcode, h5key, basic_length AS length, ffspeed,"
        " ST_AsText(ST_StartPoint(geom)) AS fnode,"
        " ST_AsText(ST_EndPoint(geom))  AS tnode"
        " FROM subgraph_links;";
        try{
            // TODO: this can be changed to the links inside the rectangle only
            r = x.exec(query);
            x.commit();
            boost::shared_ptr<Graph> g (boost::make_shared<Graph>(n, m));
            for (const auto &row : r)
            {
                string linkcode = row["linkcode"].as<string>();
                g->add_edge(linkcode, row["fnode"].as<string>(), row["tnode"].as<string>());
                h5key_map[linkcode] = row["h5key"].as<int>();
                length_map[linkcode] = row["length"].as<float>();
                ffspeed_map[linkcode] = row["ffspeed"].as<float>();
            }
            drm_graph = g;
            
        } catch (std::exception &e) {
            cout << e.what() << endl;
        }
        if (drm_graph == nullptr)
            throw GraphException::GraphNotSet();
        
        return drm_graph;
    }
    
    //　TODO: where roadtype = ??
    //　http://www.cplusplus.com/doc/tutorial/exceptions/
    const boost::shared_ptr<Graph> wrapper_make_subgraph(const boost::python::object &origin, const boost::python::object &destination, const string& condition, int buf_dist) throw()
    {
        if(! conn->is_open()) conn->activate();
        const float lon_o = boost::python::extract<float>(origin[0]);
        const float lat_o = boost::python::extract<float>(origin[1]);
        const float lon_d = boost::python::extract<float>(destination[0]);
        const float lat_d = boost::python::extract<float>(destination[1]);
        
        
        // 3 kilometer rectangle buffer
        
        pqxx::work x(*conn);
        string query =
        " DROP VIEW IF EXISTS subgraph_links;"
        " DROP VIEW IF EXISTS subgraph_links;"
        " DROP VIEW IF EXISTS subgraph_nodes;"
        " DROP VIEW IF EXISTS box;"
        " DROP VIEW IF EXISTS buffer_o;"
        " DROP VIEW IF EXISTS buffer_d;"
        " CREATE TEMP VIEW Buffer_O AS SELECT ST_Buffer("
        " ST_Transform"
        " ( "
        "       ST_SetSRID(ST_MakePoint("+ to_string(lon_o)  + "," + to_string(lat_o) + "), 4326), 3857"
        " )," + to_string(buf_dist) + " ) AS geom;"
        
        " CREATE TEMP VIEW Buffer_D AS SELECT ST_Buffer("
        " ST_Transform"
        " ("
        "       ST_SetSRID(ST_MakePoint("+ to_string(lon_d) + "," + to_string(lat_d) + "), 4326), 3857"
        " )," + to_string(buf_dist) + " ) AS geom;"
        " CREATE TEMP VIEW box as SELECT ST_Envelope( "
        " ST_UNION(Buffer_O.geom, Buffer_D.geom) "
        " ) AS geom FROM buffer_o, buffer_d;"
        " CREATE TEMP VIEW subgraph_links AS SELECT links.* FROM links, box WHERE ST_Contains( box.geom, ST_Transform(links.geom, 3857)) AND "
        + condition + " ;";
        //      e.g.: condition = "basic_roadtype < 6"
        
        //TODO: use WHERE ST_Intersects(nodes.geom, links.geom) to get the subgraph_nodes
        try
        {
            r = x.exec(query);
        }
        catch(std::exception &e)
        {
            cout << e.what() << endl;
        }
        
        int n = 0;
        int m = 0;
        query = "SELECT COUNT(*) AS n FROM (SELECT meshcode || "
        "fnodecode FROM subgraph_links UNION SELECT meshcode || "
        "tnodecode FROM subgraph_links) AS t;";
        try {
            //***********************************************************
            // auto calculate m and n may be slow when the linksview is large
            // (when O and D are far from each other), consider hierarchy based methods
            r = x.exec(query);
            n = r[0]["n"].as<int>();
        }
        catch(std::exception &e)
        {
            cout << e.what() << endl;
        }
        
        query = "SELECT count(*) AS m FROM subgraph_links;";
        try {
            r = x.exec(query);
            m = r[0]["m"].as<int>();
        }
        catch (std::exception &e) {
            cout << e.what() << endl;
        }
            
        query = " SELECT linkcode, h5key, basic_length AS length, ffspeed,"
        " ST_AsText(ST_StartPoint(geom)) AS fnode,"
        " ST_AsText(ST_EndPoint(geom))  AS tnode"
        " FROM subgraph_links;";
        
        try{
            // TODO: this can be changed to the links inside the rectangle only
            r = x.exec(query);
            x.commit();
            boost::shared_ptr<Graph> g (boost::make_shared<Graph>(n, m));
            for (const auto &row : r)
            {
                string linkcode = row["linkcode"].as<string>();
                g->add_edge(linkcode, row["fnode"].as<string>(), row["tnode"].as<string>());
                h5key_map[linkcode] = row["h5key"].as<int>();
                length_map[linkcode] = row["length"].as<float>();
                ffspeed_map[linkcode] = row["ffspeed"].as<float>();
            }
            drm_graph = g;
            
        } catch (std::exception &e) {
            std::cerr << e.what() << std::endl;
        }
        if (drm_graph == nullptr)
            throw GraphException::GraphNotSet();
        
        return drm_graph;
    }
    
    const boost::shared_ptr<Graph> get_drm_graph() const {
        return drm_graph;
    }
    
    hsize_t get_h5key(const string &linkcode) const {
        return h5key_map.at(linkcode);
    }
    float get_ffspeed(const string &linkcode) const{
        return ffspeed_map.at(linkcode);
    }
    float get_length (const string &linkcode) const{
        return length_map.at(linkcode);
    }
    string get_geojson(const string &linkcode) const{
        return geojson_map.at(linkcode);
    }
    
    void fill_speeds(hsize_t idx, float (&buffer)[96][2]) const{
        hid_t dataspace = H5Dget_space(dataset_id);
        hsize_t start[2] = { idx, 0 };
        hsize_t count[2] = { 96, 2 };
        H5Sselect_hyperslab(dataspace, H5S_SELECT_SET, start, NULL, count,
                            NULL);
        
        hsize_t mem_dims[2] = { 96, 2 };
        
        // the dimension of mem is 2
        hid_t memspace = H5Screate_simple(2, mem_dims, NULL);
        
        H5Dread(dataset_id, H5T_NATIVE_FLOAT, memspace, dataspace,
                                H5P_DEFAULT, buffer);
        H5Sclose(memspace);
        H5Sclose(dataspace);
    }
};

#endif  //_DRMHELPER_H

// ========================================================
//  datetimehelper.h
//  hyperpath_td
//
//  Created by tonny.achilles on 12/26/14.
//  Copyright (c) 2014 Jiangshan Ma. All rights reserved.
// ========================================================

#ifndef hyperpath_td_datetimehelper_h
#define hyperpath_td_datetimehelper_h

#include <chrono>
#include <boost/date_time.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <sys/timeb.h>

int get_now_ms()
{
    timeb tb;
    ftime(&tb);
    int nCount = tb.millitm + (tb.time & 0xfffff) * 1000;
    return nCount;
}

int get_elapesd_ms(int start_ms){
    int nSpan = get_now_ms() - start_ms;
    if (nSpan < 0)
        nSpan += 0x100000 * 1000;
    return nSpan;
}

std::string get_current_time() {
    std::ostringstream msg;
    const boost::posix_time::ptime now =
    boost::posix_time::second_clock::local_time();
    boost::posix_time::time_facet* const f = new boost::posix_time::time_facet("%Y-%m-%d %H:%M:%S");
    msg.imbue(std::locale(msg.getloc(), f));
    msg << now;
    return msg.str();
}

template<class T>
std::string format_time(T _tt) {
    int t = int(_tt);
    int hour = t / 3600;
    int min = (t % 3600) / 60;
    int sec = (t % 3600) % 60;
    char buff[10];
    struct tm mytime;
    mytime.tm_hour = hour;
    mytime.tm_min = min;
    mytime.tm_sec = sec;
    strftime(buff, 10, "%H:%M:%S", &mytime);
    std::string mybuff(buff);
    return mybuff;
}

boost::posix_time::ptime time_parse_exact(const std::string& time_str,
                                          const std::string& format) {
    boost::posix_time::ptime output;
    boost::posix_time::time_input_facet facet1(format, 1);
    
    std::stringstream ss1(time_str);
    ss1.imbue(std::locale(ss1.getloc(), &facet1));
    ss1 >> output;
    return output;
}

#endif

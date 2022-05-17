//main.h
#ifndef MAIN_H_INCLUDED
#define MIAN_H_INCLUDED

//#ifdef __cplusplus
//#define EXPORT extern "C" __declspec (dllexport)
//#else
//#define EXPORT __declspec (dllexport)
//#endif // __cplusplus

#include <windows.h>
//#include <iostream>
//using namespace std;

//EXPORT  void test();
//EXPORT  void c_water_flow(int terrain_row, int terrain_col, double** water_map);



extern "C" {
    void test();
    double* c_water_flow(int terrain_row, int terrain_col, double* in_water_map, double* in_landform_map, char* in_legal_direction);
    double* show2(double* num_list,int len);
}

#endif // MAIN_H_INCLUDED

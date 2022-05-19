#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <vector>
#include <map>
#include<algorithm>
#include "main.hpp"

using namespace std;

class point {
public:
    int x;
    int y;
    double absolute_water_high;
    double drop_high;

    point(int x, int y) {
        this->x = x;
        this->y = y;
    }

};

bool operator < (point a, point b) {
    if (a.x!=b.x)
        return a.x<b.x;
    return a.y<b.y;
}

bool operator > (point a, point b) {
    return !(a<b);
}

bool point_water_drop (point a, point b) {
    return a.drop_high<b.drop_high;
}

// ��ȫ�ֱ�����һ������!!!
vector<vector<double>> water_map;
vector<vector<double>> landform_map;
vector<string> legal_direction;

void trans_block(int row, int col, double* in_map, vector<vector<double>> &my_map) {
    my_map.resize(row);
    for(int i = 0;i<row;i++)
        my_map[i].resize(col);
    for(int i = 0;i<row;i++)
        for(int j = 0;j<col;j++) {
            my_map[i][j]=in_map[i*col+j];
        }
}

void trans_data(int terrain_row, int terrain_col, double* in_water_map, double* in_landform_map, char* in_legal_direction) {
    //  ����water_map
    trans_block(terrain_row, terrain_col, in_water_map, water_map);
    //  ����landform_map
    trans_block(terrain_row, terrain_col, in_landform_map, landform_map);
    //  ����legal_direction
    legal_direction.clear();
    for(int i = 0; in_legal_direction[i] != '\0'; i++) {
        if(i == 0 || in_legal_direction[i-1]=='\n') {
            string str(1,in_legal_direction[i]);
            legal_direction.push_back(str);
            continue;
        }
        if(in_legal_direction[i] == '\n')
            continue;
        legal_direction[legal_direction.size()-1].push_back(in_legal_direction[i]);
    }

}

point position_and_direction_get_adjacent(int row_index, int col_index, string direction, int terrain_row, int terrain_col) {
    if (direction == "stay")
        return point(row_index, col_index);
    if (direction == "right" && col_index + 1 < terrain_col)
        return point(row_index, col_index + 1);
    else if (direction == "left" && col_index > 0)
        return point(row_index, col_index - 1);
    else if (direction == "down" && row_index + 1 < terrain_row)
        return point(row_index + 1, col_index);
    else if (direction == "up" && row_index > 0)
        return point(row_index - 1, col_index);

    // �趨x=-1Ϊδ�ҵ�
    return point(-1, col_index);
}

double* water_flow(int terrain_row, int terrain_col, double* in_water_map, double* in_landform_map, char* in_legal_direction) {

    trans_data(terrain_row, terrain_col, in_water_map, in_landform_map, in_legal_direction);

    int row_index, col_index;
    for(row_index = 0; row_index < terrain_row; row_index++) {
        for(col_index = 0; col_index < terrain_col; col_index++) {

            // ���������ˮ�ߵ���0.1 ����������
            if(water_map[row_index][col_index] < 0.1) {
                water_map[row_index][col_index] = 0;
                continue;
            }
            // �õ��Լ��ľ���ˮ��
            double absolute_water_high = water_map[row_index][col_index] + landform_map[row_index][col_index];
            double land_high=landform_map[row_index][col_index];

            vector<point> adjacent_positions;
//            adjacent_positions.clear();

            for(size_t i =0;i<legal_direction.size();i++) {
                point adjacent_position= position_and_direction_get_adjacent(row_index, col_index, legal_direction[i], terrain_row, terrain_col);
                if(adjacent_position.x!=-1)
                    adjacent_positions.push_back(adjacent_position);
            }

            // �ж����кϷ�����ľ���ˮ�� ��ֻ����������λ��

            vector<point> adjacent_points;
            double sum_absolute_water_high = absolute_water_high;

            for(size_t i =0;i<adjacent_positions.size();i++) {
                int x = adjacent_positions[i].x;
                int y = adjacent_positions[i].y;
                double adjacent_absolute_water_high = water_map[x][y] + landform_map[x][y];

                // ���ҵ�ʱ�ͼ���������߶�
                adjacent_positions[i].drop_high = land_high - adjacent_absolute_water_high;
                // ��������<Ҫ��Ҫ�ĳ�<=
                if(adjacent_absolute_water_high < absolute_water_high) {
                    adjacent_positions[i].absolute_water_high = adjacent_absolute_water_high;
//                    cout<<"adjacent_x_y: "<<adjacent_positions[i].x<<" "<<adjacent_positions[i].y<<endl;
                    adjacent_points.push_back(adjacent_positions[i]);
                    sum_absolute_water_high += adjacent_absolute_water_high;
                }
            }

            // ������涼������ˮ����
            if (adjacent_points.size() == 0)
                continue;
            // ����һ����ֵ����
            double avg_absolute_water_high = sum_absolute_water_high / (adjacent_points.size() + 1);

            // ��������ƽ
            if(avg_absolute_water_high < landform_map[row_index][col_index]) {
                // ��ǰʣ��ˮ��������Ϊֹ
                double water_amount = water_map[row_index][col_index];
                water_map[row_index][col_index] = 0;

                vector<point>temp;
                // �����ѭ����ȥ��drop_high<=0��
                for(size_t i =0;i<adjacent_points.size();i++) {
                    if(adjacent_points[i].drop_high<=0)
                        continue;
                    temp.push_back(adjacent_points[i]);
                }
                adjacent_points = temp;
                temp.clear();

                std::sort(adjacent_points.begin(), adjacent_points.end(), point_water_drop);

                double sum_drop_high=0;
                double big_drop_high=0;
                int idx=0;

                // �����ѭ���м����㹻����ö���drop_high��������ʣ����water_amount
                for(size_t i =0;i<adjacent_points.size();i++) {
                    sum_drop_high+=adjacent_points[i].drop_high*(adjacent_points.size() - idx);
                    if(sum_drop_high>=water_amount) {
                        sum_drop_high -= adjacent_points[i].drop_high*(adjacent_points.size() - idx);
                        if(i > 0)
                            big_drop_high = adjacent_points[i-1].drop_high;
                        idx = i;
                    }
                }
                water_amount = water_amount - sum_drop_high;

                // �ȴ����ܱ�������
                for(int i=0;i<idx;i++) {
                    // ����Ĵ�����ܻ�������!!!
                    if(adjacent_points[i].absolute_water_high < land_high)
                        adjacent_points[i].absolute_water_high=land_high;
                }
                //Ȼ������������
                for(size_t i =idx;i<adjacent_points.size();i++) {
                    adjacent_points[i].absolute_water_high+=big_drop_high+water_amount/(adjacent_points.size() - idx);
                }
            }
            // ������ƽ
            else {
                // �޸�ԭ���ˮ��ͼ
                water_map[row_index][col_index] = avg_absolute_water_high - landform_map[row_index][col_index];
                // �޸����ڵ�ľ���ˮ��
                for(size_t i =0;i<adjacent_points.size();i++) {
                    adjacent_points[i].absolute_water_high = avg_absolute_water_high;
                }
            }

            // ��������ڵ�ľ���ˮ�ߵļ��㣬���ڿ�ʼ�޸�ˮ��ͼ
            for(size_t i =0;i<adjacent_points.size();i++) {
                water_map[adjacent_points[i].x][adjacent_points[i].y] = adjacent_points[i].absolute_water_high - landform_map[adjacent_points[i].x][adjacent_points[i].y];
            }
        }
    }

    double* res = new double[terrain_row*terrain_col];
    for(int i = 0; i < terrain_row; i++)
        for(int j = 0; j < terrain_col; j++)
            res[i*terrain_col+j]=water_map[i][j];

    return res;
}

double* c_water_flow(int terrain_row, int terrain_col, double* in_water_map, double* in_landform_map, char* in_legal_direction) {
    return water_flow(terrain_row, terrain_col, in_water_map, in_landform_map, in_legal_direction);
}

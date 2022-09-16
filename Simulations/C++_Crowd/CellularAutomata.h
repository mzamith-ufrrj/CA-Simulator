#ifndef CELLULAR_AUTOMATA_H
#define CELLULAR_AUTOMATA_H
#define DELTA_T 100.0f
#include <random>
#define NEIGHTBORS 9 
using namespace std;
struct stPerson{
    int x, y, vx0, vy0, vx1, vy1, type;
    bool state,
         winner;
    int whoIam;

};

struct stLayers{
    bool beg;
    double dispute[NEIGHTBORS];
    int    whoIam[NEIGHTBORS];
};

class CellularAutomata{
public:
    static const int DOOR = 1;
    static const int PERSON = 2;
    //---------------------------------
     static const int NW = 0x00;
     static const int N  = 0x01;
     static const int NE = 0x02;
     static const int W  = 0x03;
     static const int C  = 0x04;
     static const int E  = 0x05;
     static const int SW = 0x06;
     static const int S  = 0x07;
     static const int SE = 0x08;
     
    CellularAutomata(int, int);
    ~CellularAutomata();
    void render(void);
    int getCellX(void)      { return mCellX; };
    int getCellY(void)      { return mCellY; };
    float getScaleX(void)   { return mScaleX; };
    float getScaleY(void)   { return mScaleY; };


    void clear(void);
    void update(double);

    void initCond(void);
protected:
    void moveRule(void);
    void outflowRule(void);
    void disputeRule(void);
    void updateRule(void);


    int mCellX,
        mCellY;
    float mScaleX,
          mScaleY;

    int *mGrid;
    stLayers *mLayers;
    stPerson *mPeople;

    int mStep;

   static random_device m_RD;
   static mt19937_64  m_Gen64;
   static uniform_int_distribution<int> m_Uniform;
};
#endif
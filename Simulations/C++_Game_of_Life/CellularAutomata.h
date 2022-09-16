#ifndef CELLULAR_AUTOMATA_H
#define CELLULAR_AUTOMATA_H
#define DELTA_T 100.0f
class CellularAutomata{
public:
    CellularAutomata(int, int);
    ~CellularAutomata();
    void render(void);
    int getCellX(void){ return mCellX; };
    int getCellY(void){ return mCellY; };
    float getScaleX(void){ return mScaleX; };
    float getScaleY(void){ return mScaleY; };
    float getAlive(void){ return mAlive/mCells; };
    float getDead(void){ return mDead/mCells;};
    void changeState(int, int);
    void clear(void);
    void random(void);
    void update(double);
    void increaseTime(void);
    void decreaseTime(void);
    void increaseDistance(void);
    void decreaseDistance(void);
    
protected:
    int mCellX,
        mCellY;
    float mScaleX,
          mScaleY;
    int *mOldState, *mCurrentState;
    int mDistance;
    float mDead,
          mAlive,
          mCells;
    double mTimeInstant,
           mDeltaT;
    
};
#endif
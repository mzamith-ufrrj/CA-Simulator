#include <CellularAutomata.h>
#ifdef __APPLE__
#include <GLUT/glut.h>
#include <OpenGL/glu.h>
#include <OpenGL/gl.h>
#else
#include <GL/glut.h>
#include <GL/glu.h>
#include <GL/gl.h>
#endif
#include <iostream>
#include <ctime>
#include <cstring>
using namespace std;

CellularAutomata::CellularAutomata(int x, int y):
mCellX(x),
mCellY(y),
mTimeInstant(0.0f),
mDeltaT(10.0f),
mDistance(1){
    srand (time(NULL));
    cout << "Cell X = " << mCellX << endl;
    cout << "Cell Y = " << mCellY << endl;
    
    mCells = static_cast<float>(mCellX * mCellY);
    mScaleX = 1.0f/static_cast<float>(x);
    mScaleY = 1.0f/static_cast<float>(y);
    
    mOldState = new int[mCellX * mCellY];
    mCurrentState = new int[mCellX * mCellY];
    clear();

};
CellularAutomata::~CellularAutomata(){
    delete[] mOldState;
    delete[] mCurrentState;
};


void CellularAutomata::render(void){
    
    float dX = 0.0f,
          dY = 0.0f;
    int type = GL_LINE_LOOP;
    
    //glScalef(, mScaleY, 1.0f);
    
    mAlive = 0.0f;
    mDead = 0.0f;
    for (int j = 0; j < mCellY; j++){
        for (int i = 0; i < mCellX; i++){
            glPushMatrix();
            glColor3f(1.0f, 0.0f, 0.0f);
            glTranslatef(dX, dY, 0.0f);
            int p = (mCellX * j) + i;
            if (mCurrentState[p] == 1){
                type = GL_QUADS;
                mAlive++;
            }
            else{
                type = GL_LINE_LOOP;
                mDead++;
            }
            glBegin(type); //GL_QUADS);GL_LINE_LOOP
            
            glVertex3f(0.0f, 0.0f, 0.0f);
            glVertex3f(0.0f, -mScaleY, 0.0f);
            glVertex3f(mScaleX, -mScaleY, 0.0f);
            glVertex3f(mScaleX, 0.0f, 0.0f);
            
            
            glEnd();
            glPopMatrix();
            dX += mScaleX;
            
        }
        dY -= mScaleY;
        dX = 0.0f;
        
    }
    

     
};


void CellularAutomata::changeState(int i, int j){
    int p = (j * mCellX) + i;
    mCurrentState[p] = !mCurrentState[p];
};


void CellularAutomata::clear(void){
    bzero(mOldState, sizeof(int)*mCellX*mCellY);
    bzero(mCurrentState, sizeof(int)*mCellX*mCellY);


};
void CellularAutomata::random(void){
    for (int i = 0 ; i < mCellY; i++){
        for (int j = 0; j < mCellX; j++){
            int r = rand() % 10000 + 1;
            int p = (mCellX * j) + i;
            if (r < 3500)
                mCurrentState[p] = 1;
            else
                mCurrentState[p] = 0;
        }
    }


};

/*
    Moore neighborhood with r = 1
 
            |nw|n|ne|
            |w | |e |
            |sw|s|se|
 
 */

void CellularAutomata::update(double time){
    mTimeInstant+=time;
    if (mTimeInstant < mDeltaT)
        return;
    
        mTimeInstant = 0.0f;

    int *swap = mCurrentState;
    mCurrentState = mOldState;
    mOldState = swap;

    
    int r = mDistance;
    int sum = 0;
    int x, y, p;

    for (int j = 0; j < mCellY; j++)
        for (int i = 0; i < mCellX; i++){
            sum = 0;
            p = (j * mCellX) + i;
            

            for (int rj = -r; rj <= r; rj++){
                
                int pj = j - rj;

                for (int ri = -r; ri <= r; ri++){
                    
                
                    int pi = i + ri;
                    
                    if ((pi >= 0) && (pi < mCellX) && (pj >= 0) && (pj < mCellY)){
                        p = (pj * mCellX) + pi;
                        if (!((rj == 0) && (ri == 0)))
                            sum += mOldState[p];
                    }//else
                       // sum++;
                    
                }
                    
                
                
                
            }
            
            
            p = (j * mCellX) + i;
            if ((sum == 3) && (mOldState[p] == 0))
                mCurrentState[p] = 1;
            else if  ( ((sum >= 2) && (sum <= 3)) && (mOldState[p] == 1))
                mCurrentState[p] = 1;
            else
                mCurrentState[p] = 0;
            
        }

    
    
};

/*
void CellularAutomata::update(double time){
    mTimeInstant+=time;
    if (mTimeInstant < mDeltaT)
        return;
    
    mTimeInstant = 0.0f;
    
    int *swap = mCurrentState;
    mCurrentState = mOldState;
    mOldState = swap;
    
    
    int r = mDistance;
    int sum = 0;
    int x, y, p;
    for (int j = 0; j < mCellY; j++)
        for (int i = 0; i < mCellX; i++){
            sum = 0;
            p = (j * mCellX) + i;
            
            for (int rj = -r; rj <= r; rj++){
                
                int pj = j - rj;
                if (pj < 0)
                    pj = mCellY + pj;
                else if (pj >= mCellY)
                    pj %= mCellY;
                
                for (int ri = -r; ri <= r; ri++){
                    
                    
                    int pi = i + ri;
                    if (pi < 0)
                        pi = mCellX + ri;
                    else if (pi >= mCellX)
                        pi %= mCellX;
                    
                    
                    
                    p = (pj * mCellX) + pi;
                    if (!((rj == 0) && (ri == 0)))
                        sum += mOldState[p];
                }
                
                
                
            }
            
            
            p = (j * mCellX) + i;
            if ((sum == 3) && (mOldState[p] == 0))
                mCurrentState[p] = 1;
            else if  ( ((sum == 2) || (sum == 3)) && (mOldState[p] == 1))
                mCurrentState[p] = 1;
            else
                mCurrentState[p] = 0;
            
        }
    
    
    
};

*/
void CellularAutomata::increaseTime(void){
    mDeltaT+100.0f;
    if (mDeltaT > 1000.0f);
        mDeltaT = 1000.0f;
};

void CellularAutomata::decreaseTime(void){
        mDeltaT-100.0f;
        if (mDeltaT < 100.0f);
            mDeltaT = 100.0f;
};

void CellularAutomata::increaseDistance(void){
    mDistance++;
    if (mDistance > 10)
        mDistance = 10;
};

            

void CellularAutomata::decreaseDistance(void){
    mDistance--;
    if (mDistance < 1)
        mDistance = 1;

};

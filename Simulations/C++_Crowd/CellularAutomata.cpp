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
#include <cmath>
using namespace std;


/*
 * Static attibutes: 
 * These C++ components does not work dynamically
 */
uniform_int_distribution<int> CellularAutomata::m_Uniform(1, 100);
random_device CellularAutomata::m_RD{};
mt19937_64  CellularAutomata::m_Gen64{m_RD()};


CellularAutomata::CellularAutomata(int x, int y):
mCellX(x),
mCellY(y),
mPeople(NULL),
mLayers(NULL),
mStep(0){
    srand (time(NULL));
    cout << "Cell X = " << mCellX << endl;
    cout << "Cell Y = " << mCellY << endl;
    
   
    mScaleX = 1.0f/static_cast<float>(x);
    mScaleY = 1.0f/static_cast<float>(y);
    mGrid = new int[mCellX * mCellY];
    mLayers =  new stLayers[mCellX * mCellY];
    clear();
    

};
CellularAutomata::~CellularAutomata(){
    if (mPeople != NULL)
        delete[] mPeople;

    delete[] mGrid;
    delete[] mLayers;

};


void CellularAutomata::render(void){
    
    float dX = 0.0f,
          dY = 0.0f;
    int type = GL_LINE_LOOP;
    

    for (int j = 0; j < mCellY; j++){
        for (int i = 0; i < mCellX; i++){
            glPushMatrix();
            glColor3f(1.0f, 0.0f, 0.0f);
            glTranslatef(dX, dY, 0.0f);
            int p = (mCellX * j) + i;
            if (mGrid[p] > -1){
                type = GL_QUADS;
                
            }
            else{
                type = GL_LINE_LOOP;
                
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


 

void CellularAutomata::clear(void){
  

    for (int i = 0; i < mCellX*mCellY; i++)
        mGrid[i] = -1;

    bzero(mLayers, sizeof(stLayers) * mCellX * mCellY);
};


/*
    Moore neighborhood with r = 1
 
            |nw|n|ne|
            |w | |e |
            |sw|s|se|
 
 */

int min(int a, int b){
    if (a < b) return a;
    return b;
}
void CellularAutomata::moveRule(void){
    stPerson door = mPeople[0];
   
    for (int i = 1; i < 9; i++){
        if (mPeople[i].state){
            int x = (door.x - mPeople[i].x), 
                y = (door.y - mPeople[i].y),
                vx = 0, vy = 0;

                if (y > 0)      {vy =  1;}
                else if (y < 0) {vy = -1;}

                if (x > 0)      {vx =  1;}
                else if (x < 0) {vx = -1;}

                if (m_Uniform(m_Gen64) < 35){
                    vx = vy = 0;
                }

                mPeople[i].vx0 = vx;
                mPeople[i].vy0 = vy;
        }//if (mPeople[i].state){
    }//for (int i = 1; i < 9; i++){
}//void CellularAutomata::move(void){

void CellularAutomata::outflowRule(void){
    stPerson door = mPeople[0];
    for (int i = 1; i < 9; i++){
        if ((mPeople[i].x == door.x) && (mPeople[i].y == door.y))
            mPeople[i].state = false;
    }//for (int i = 1; i < 9; i++){

}//void CellularAutomata::outflowRule(void){

void CellularAutomata::disputeRule(void){   
    for (int i = 1; i < 9; i++){
        if (mPeople[i].state){
            int x = mPeople[i].x +  mPeople[i].vx0, 
                y = mPeople[i].y +  mPeople[i].vy0;
               
            int cell = mGrid[y * mCellX + x];
            if (cell > 1){
                 mPeople[i].vx0 = mPeople[i].vy0 = 0;
            }else{

                int lx = (mPeople[i].vx0 * -1) + 1;
                int ly = (mPeople[i].vy0 * -1) + 1;

                int whoIam = ly * 3 + lx;
                int chicken = m_Uniform(m_Gen64);
                cout << "I(" <<  i << ") Bet(" << chicken << ") ->";
                cout << whoIam << "  (" << x << "," << y <<  ")";
                cout << " -> (" << lx << "," << ly <<  ")" << endl;

                mLayers[y * mCellX + x].dispute[whoIam] = chicken;
                mLayers[y * mCellX + x].whoIam[whoIam] = i;
                mLayers[y * mCellX + x].beg = true;
            }//if (cell > 1){
        }//if (mPeople[i].state){
    }//for (int i = 1; i < 9; i++){


}//void CellularAutomata::disputeRule(void){


void CellularAutomata::updateRule(void){   
    for (int i = 0; i < mCellX*mCellY; i++){
        stLayers layer = mLayers[i];

        if (layer.beg){
            bool disputed = false;
            int win = -1, 
                max = 0;
            for (int j = 0; j < NEIGHTBORS; j++){
                if (layer.dispute[j] > 0){
                    if (layer.dispute[j] > max){
                        max = layer.dispute[j];
                        win = layer.whoIam[j];
                    }
                }
            }//for (int j = 0; j < 8; j++){

            if (win > 0)
                mPeople[win].winner = true;

        }//if (layer.beg){
    }//for (int i = 0; i < mCellX*mCellY; i++){
        

    for (int i = 1; i < 9; i++){
        if (mPeople[i].state){
            if (mPeople[i].winner){
                mPeople[i].x +=  mPeople[i].vx0, 
                mPeople[i].y +=  mPeople[i].vy0;
                mPeople[i].vx0 = mPeople[i].vy0 = 0;
            }
            mPeople[i].winner = false;
        }//if (mPeople[i].state){
    }//for (int i = 1; i < 9; i++){

    clear();

}//void CellularAutomata::disputeRule(void){


void CellularAutomata::update(double time){
    cout << "Updating..." << endl;
    cout.flush();
     
    if (mStep > 0){
        moveRule();
        disputeRule();
        updateRule();
        outflowRule();
    }//if (step > 0){


    for (int i = 0; i < 9; i++){
        if (mPeople[i].state == true){
            mGrid[mPeople[i].y * mCellX +  mPeople[i].x] = i;
        }
    }

    mStep++;
};



void CellularAutomata::initCond(void){
    int mi = mCellX / 2;
    int mj = mCellY / 2;

/*
    mGrid[mj * mCellX + mi] = 1;

    mGrid[(mj-2) * mCellX + (mi-2)] = 1;
    mGrid[(mj-2) * mCellX + mi] = 1;
    mGrid[(mj-2) * mCellX + (mi+2)] = 1;

    mGrid[(mj+2) * mCellX + (mi-2)] = 1;
    mGrid[(mj+2) * mCellX + mi] = 1;
    mGrid[(mj+2) * mCellX + (mi+2)] = 1;




    mGrid[mj * mCellX + (mi-2)] = 1;
    mGrid[mj * mCellX + (mi+2)] = 1;
*/
    mPeople = new stPerson[9];
    
    int i = 0;
    mPeople[i].x = 60; //mi;
    mPeople[i].y = 8; //mj;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::DOOR;
    mPeople[i].state = true; 
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 
    i++;


    mPeople[i].x = mi - 2;
    mPeople[i].y = mj - 2;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::PERSON;
    mPeople[i].state = true;
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 
    i++;
    
    mPeople[i].x = mi ;
    mPeople[i].y = mj - 2;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::PERSON;
    mPeople[i].state = true;
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 
    i++;
    
    mPeople[i].x = mi + 2;
    mPeople[i].y = mj - 2;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::PERSON;
    mPeople[i].state = true;
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 
    i++;
    
    mPeople[i].x = mi - 2;
    mPeople[i].y = mj + 2;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::PERSON;
    mPeople[i].state = true;
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 
    i++;
    
    mPeople[i].x = mi;
    mPeople[i].y = mj + 2;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::PERSON;
    mPeople[i].state = true;
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 
    i++;
    
    cout << "I(" << i << ")" << endl;
    mPeople[i].x = mi + 2;
    mPeople[i].y = mj + 2;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::PERSON;
    mPeople[i].state = true;
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 
    i++;
    
    mPeople[i].x = mi - 2;
    mPeople[i].y = mj;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::PERSON;
    mPeople[i].state = true;
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 
    i++;
    
    mPeople[i].x = mi + 2;
    mPeople[i].y = mj;
    mPeople[i].vx0 = mPeople[i].vx1 = mPeople[i].vy0 = mPeople[i].vx1 = 0;
    mPeople[i].type = CellularAutomata::PERSON;
    mPeople[i].state = true;
    mPeople[i].winner = false; 
    mPeople[i].whoIam = -1; 



    update(0);



};
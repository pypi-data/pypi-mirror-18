/*========================================
 *    sl.c: SL version 5.02
 *        Copyright 1993,1998,2014
 *                  Toyoda Masashi
 *                  (mtoyoda@acm.org)
 *        Last Modified: 2014/06/03
 *========================================
 */

#include <curses.h>
#include <unistd.h>

#include <stdlib.h>
#include <string.h>

#include "sl.h"

void add_smoke(int y, int x);
void add_man(int y, int x);
int add_C51(int x);
int add_D51(int x);
int add_sl(int x);
void option(char *str);
int ACCIDENT  = 0;
int LOGO      = 0;
int FLY       = 0;
int C51       = 0;

typedef struct {
    int y,x;
    char c;
}store;
int COLS,LINES,N;

int  my_mvaddstr(int y, int x, char *str);
void my_output(void);
void windowInit(int c, int l, char *arg);
void windowDestroy(void);
int  count(void);
int  addchModify(int y, int x, char c);
void mapModify(int n);

store** store_all ;
int*    store_nums;
int     store_now ;
char*   output_map;

int count()
{
    int min = 0;
    if (LOGO == 1)
        min = -LOGOLENGTH-1;
    else if (C51 == 1)
        min = -C51LENGTH-1;
    else 
        min = -D51LENGTH-1;
    return min;
}

int addchModify(int y, int x, char c)
{
//    printf("%d %d %c\n",y,x,c);
    if(y<0)
        return ERR;
    if( x >= COLS)//too large
        return ERR;

    store *s = &store_all[store_now][store_nums[store_now]++];
    s->y = y;
    s->x = x;
    s->c = c;
    return OK;
}

int my_mvaddstr(int y, int x, char *str)
{
    for ( ; x < 0; ++x, ++str)
        if (*str == '\0')  return ERR;
    for ( ; *str != '\0'; ++str, ++x)
        if (addchModify(y, x, *str) == ERR)  return ERR;
    return OK;
}

void option(char *str)
{
    extern int ACCIDENT, FLY;//, LONG; //what is LONG 

    while (*str != '\0' && *str != '-') {
        switch (*str++) {
            case 'a': ACCIDENT = 1; break;
            case 'F': FLY      = 1; break;
            case 'l': LOGO     = 1; break;
            case 'c': C51      = 1; break;
            default:                break;
        }
    }
}

void windowInit(int c, int l, char *arg)
{
    // set var
    extern int COLS,LINES,N;
    COLS = c;//83;
    LINES= l;//47;
    for (;*arg;++arg){
        if (*arg == '-') {
            option(arg+1);
        }
    }
    N = -count()+COLS-1;

    // store data
    store_all  = (store **)malloc(sizeof(store*)*N);
    store_nums = (int *)   malloc(sizeof(int)   *N);

    int x;
    for (x = COLS - 1; ; --x) {
        int mod = -x+COLS-1;
        if(mod >= N) 
            break;
        store_now = mod;
        store_nums [mod] = 0;
        store_all  [mod] = (store *)malloc(sizeof(store)*COLS*LINES);
        if (LOGO == 1)
            add_sl(x);
        else if (C51 == 1) 
            add_C51(x);
        else
            add_D51(x);
    }


    // output string
    output_map = (char *)malloc(sizeof(char)*LINES*(COLS+1));
    memset(output_map,' ',     (sizeof(char)*LINES*(COLS+1)));
    for(x=0; x<LINES; ++x)
        output_map[x*(COLS+1)+COLS]='\n';
    output_map[LINES*(COLS+1)-1]='\0';
}

void windowDestroy()
{
    int x;
    for (x = 0; x<N; ++x) 
        free(store_all[x]);
    free(store_all );
    free(store_nums);
    free(output_map);
}

/* main
int main(int argc, char *argv[])
{
    windowInit(83,47,"-F");
    my_output();
    windowDestroy();
    printf("OK\n");
    return 0;
}
*/ 

void my_output()
{
    int x;
    for(x=0; x<N; ++x)
    {
        mapModify(x);
        printf("%s\n",output_map);
        usleep(10000);
    }
}

void mapModify(int n)
{
    int i;
    store *s = store_all[n];
    for(i=0;i<store_nums[n];++i)
        if( s[i].x < COLS)
            output_map[s[i].y*(COLS+1)+s[i].x] = s[i].c;
}

int add_sl(int x)
{
    static char *sl[LOGOPATTERNS][LOGOHIGHT + 1]
        = {{LOGO1, LOGO2, LOGO3, LOGO4, LWHL11, LWHL12, DELLN},
           {LOGO1, LOGO2, LOGO3, LOGO4, LWHL21, LWHL22, DELLN},
           {LOGO1, LOGO2, LOGO3, LOGO4, LWHL31, LWHL32, DELLN},
           {LOGO1, LOGO2, LOGO3, LOGO4, LWHL41, LWHL42, DELLN},
           {LOGO1, LOGO2, LOGO3, LOGO4, LWHL51, LWHL52, DELLN},
           {LOGO1, LOGO2, LOGO3, LOGO4, LWHL61, LWHL62, DELLN}};

    static char *coal[LOGOHIGHT + 1]
        = {LCOAL1, LCOAL2, LCOAL3, LCOAL4, LCOAL5, LCOAL6, DELLN};

    static char *car[LOGOHIGHT + 1]
        = {LCAR1, LCAR2, LCAR3, LCAR4, LCAR5, LCAR6, DELLN};

    int i, y, py1 = 0, py2 = 0, py3 = 0;

    y = LINES / 2 - 3;

    if (FLY == 1) {
        y = (x / 6) + LINES - (COLS / 6) - LOGOHIGHT;
        py1 = 2;  py2 = 4;  py3 = 6;
    }
    for (i = 0; i <= LOGOHIGHT; ++i) {
        my_mvaddstr(y + i, x, sl[(LOGOLENGTH + x) / 3 % LOGOPATTERNS][i]);
        my_mvaddstr(y + i + py1, x + 21, coal[i]);
        my_mvaddstr(y + i + py2, x + 42, car[i]);
        my_mvaddstr(y + i + py3, x + 63, car[i]);
    }
    if (ACCIDENT == 1) {
        add_man(y + 1, x + 14);
        add_man(y + 1 + py2, x + 45);  add_man(y + 1 + py2, x + 53);
        add_man(y + 1 + py3, x + 66);  add_man(y + 1 + py3, x + 74);
    }
    add_smoke(y - 1, x + LOGOFUNNEL);
    return OK;
}


int add_D51(int x)
{
    static char *d51[D51PATTERNS][D51HIGHT + 1]
        = {{D51STR1, D51STR2, D51STR3, D51STR4, D51STR5, D51STR6, D51STR7,
            D51WHL11, D51WHL12, D51WHL13, D51DEL},
           {D51STR1, D51STR2, D51STR3, D51STR4, D51STR5, D51STR6, D51STR7,
            D51WHL21, D51WHL22, D51WHL23, D51DEL},
           {D51STR1, D51STR2, D51STR3, D51STR4, D51STR5, D51STR6, D51STR7,
            D51WHL31, D51WHL32, D51WHL33, D51DEL},
           {D51STR1, D51STR2, D51STR3, D51STR4, D51STR5, D51STR6, D51STR7,
            D51WHL41, D51WHL42, D51WHL43, D51DEL},
           {D51STR1, D51STR2, D51STR3, D51STR4, D51STR5, D51STR6, D51STR7,
            D51WHL51, D51WHL52, D51WHL53, D51DEL},
           {D51STR1, D51STR2, D51STR3, D51STR4, D51STR5, D51STR6, D51STR7,
            D51WHL61, D51WHL62, D51WHL63, D51DEL}};
    static char *coal[D51HIGHT + 1]
        = {COAL01, COAL02, COAL03, COAL04, COAL05,
           COAL06, COAL07, COAL08, COAL09, COAL10, COALDEL};

    int y, i, dy = 0;

    y = LINES / 2 - 5;

    if (FLY == 1) {
        y = (x / 7) + LINES - (COLS / 7) - D51HIGHT;
        dy = 1;
    }
    for (i = 0; i <= D51HIGHT; ++i) {
        my_mvaddstr(y + i, x, d51[(D51LENGTH + x) % D51PATTERNS][i]);
        my_mvaddstr(y + i + dy, x + 53, coal[i]);
    }
    if (ACCIDENT == 1) {
        add_man(y + 2, x + 43);
        add_man(y + 2, x + 47);
    }
    add_smoke(y - 1, x + D51FUNNEL);
    return OK;
}

int add_C51(int x)
{
    static char *c51[C51PATTERNS][C51HIGHT + 1]
        = {{C51STR1, C51STR2, C51STR3, C51STR4, C51STR5, C51STR6, C51STR7,
            C51WH11, C51WH12, C51WH13, C51WH14, C51DEL},
           {C51STR1, C51STR2, C51STR3, C51STR4, C51STR5, C51STR6, C51STR7,
            C51WH21, C51WH22, C51WH23, C51WH24, C51DEL},
           {C51STR1, C51STR2, C51STR3, C51STR4, C51STR5, C51STR6, C51STR7,
            C51WH31, C51WH32, C51WH33, C51WH34, C51DEL},
           {C51STR1, C51STR2, C51STR3, C51STR4, C51STR5, C51STR6, C51STR7,
            C51WH41, C51WH42, C51WH43, C51WH44, C51DEL},
           {C51STR1, C51STR2, C51STR3, C51STR4, C51STR5, C51STR6, C51STR7,
            C51WH51, C51WH52, C51WH53, C51WH54, C51DEL},
           {C51STR1, C51STR2, C51STR3, C51STR4, C51STR5, C51STR6, C51STR7,
            C51WH61, C51WH62, C51WH63, C51WH64, C51DEL}};
    static char *coal[C51HIGHT + 1]
        = {COALDEL, COAL01, COAL02, COAL03, COAL04, COAL05,
           COAL06, COAL07, COAL08, COAL09, COAL10, COALDEL};

    int y, i, dy = 0;

    y = LINES / 2 - 5;

    if (FLY == 1) {
        y = (x / 7) + LINES - (COLS / 7) - C51HIGHT;
        dy = 1;
    }
    for (i = 0; i <= C51HIGHT; ++i) {
        my_mvaddstr(y + i, x, c51[(C51LENGTH + x) % C51PATTERNS][i]);
        my_mvaddstr(y + i + dy, x + 55, coal[i]);
    }
    if (ACCIDENT == 1) {
        add_man(y + 3, x + 45);
        add_man(y + 3, x + 49);
    }
    add_smoke(y - 1, x + C51FUNNEL);
    return OK;
}


void add_man(int y, int x)
{
    static char *man[2][2] = {{"", "(O)"}, {"Help!", "\\O/"}};
    int i;

    for (i = 0; i < 2; ++i) {
        my_mvaddstr(y + i, x, man[(LOGOLENGTH + x) / 12 % 2][i]);
    }
}


void add_smoke(int y, int x)
#define SMOKEPTNS        16
{
    static struct smokes {
        int y, x;
        int ptrn, kind;
    } S[1000];
    static int sum = 0;
    static char *Smoke[2][SMOKEPTNS]
        = {{"(   )", "(    )", "(    )", "(   )", "(  )",
            "(  )" , "( )"   , "( )"   , "()"   , "()"  ,
            "O"    , "O"     , "O"     , "O"    , "O"   ,
            " "                                          },
           {"(@@@)", "(@@@@)", "(@@@@)", "(@@@)", "(@@)",
            "(@@)" , "(@)"   , "(@)"   , "@@"   , "@@"  ,
            "@"    , "@"     , "@"     , "@"    , "@"   ,
            " "                                          }};
    static char *Eraser[SMOKEPTNS]
        =  {"     ", "      ", "      ", "     ", "    ",
            "    " , "   "   , "   "   , "  "   , "  "  ,
            " "    , " "     , " "     , " "    , " "   ,
            " "                                          };
    static int dy[SMOKEPTNS] = { 2,  1, 1, 1, 0, 0, 0, 0, 0, 0,
                                 0,  0, 0, 0, 0, 0             };
    static int dx[SMOKEPTNS] = {-2, -1, 0, 1, 1, 1, 1, 1, 2, 2,
                                 2,  2, 2, 3, 3, 3             };
    int i;

    if (x % 4 == 0) {
        for (i = 0; i < sum; ++i) {
            my_mvaddstr(S[i].y, S[i].x, Eraser[S[i].ptrn]);
            S[i].y    -= dy[S[i].ptrn];
            S[i].x    += dx[S[i].ptrn];
            S[i].ptrn += (S[i].ptrn < SMOKEPTNS - 1) ? 1 : 0;
            my_mvaddstr(S[i].y, S[i].x, Smoke[S[i].kind][S[i].ptrn]);
        }
        my_mvaddstr(y, x, Smoke[sum % 2][0]);
        S[sum].y = y;    S[sum].x = x;
        S[sum].ptrn = 0; S[sum].kind = sum % 2;
        sum ++;
    }
}

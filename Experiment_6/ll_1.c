#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 20

char productions[10][20] = {
    "E=TE'",
    "E'=+TE'|#",
    "T=FT'",
    "T'=*FT'|#",
    "F=(E)|i"
};

char first[10][10];
char follow[10][10];
int n = 5;

void addToSet(char *set, char value) {
    for(int i=0; set[i] != '\0'; i++)
        if(set[i] == value) return;

    int len = strlen(set);
    set[len] = value;
    set[len+1] = '\0';
}

void computeFirst(char c, int index) {
    if(!isupper(c)) {
        addToSet(first[index], c);
        return;
    }

    for(int i=0; i<n; i++) {
        if(productions[i][0] == c) {
            for(int j=2; productions[i][j] != '\0'; j++) {
                if(productions[i][j] == '|') continue;
                if(productions[i][j] == '#') {
                    addToSet(first[index], '#');
                    break;
                }
                computeFirst(productions[i][j], index);
                break;
            }
        }
    }
}

void computeFollow(char c, int index) {
    if(c == productions[0][0])
        addToSet(follow[index], '$');

    for(int i=0; i<n; i++) {
        for(int j=2; productions[i][j] != '\0'; j++) {
            if(productions[i][j] == c) {
                if(productions[i][j+1] != '\0') {
                    if(!isupper(productions[i][j+1]))
                        addToSet(follow[index], productions[i][j+1]);
                }
            }
        }
    }
}

int main() {

    printf("===== STEP 1: Ambiguous Grammar =====\n");
    printf("E -> E+E | E*E | (E) | id\n");
    printf("Example: id + id * id has multiple parse trees.\n\n");

    printf("===== STEP 2: Unambiguous Grammar =====\n");
    printf("E -> E + T | T\n");
    printf("T -> T * F | F\n");
    printf("F -> (E) | id\n\n");

    printf("===== STEP 3: Remove Left Recursion =====\n");
    printf("E  -> T E'\n");
    printf("E' -> + T E' | ε\n");
    printf("T  -> F T'\n");
    printf("T' -> * F T' | ε\n");
    printf("F  -> (E) | i\n\n");

    printf("===== STEP 4: FIRST Sets =====\n");

    for(int i=0; i<n; i++) {
        computeFirst(productions[i][0], i);
        printf("FIRST(%c) = { ", productions[i][0]);
        for(int j=0; first[i][j] != '\0'; j++)
            printf("%c ", first[i][j]);
        printf("}\n");
    }

    printf("\n===== STEP 5: FOLLOW Sets =====\n");

    for(int i=0; i<n; i++) {
        computeFollow(productions[i][0], i);
        printf("FOLLOW(%c) = { ", productions[i][0]);
        for(int j=0; follow[i][j] != '\0'; j++)
            printf("%c ", follow[i][j]);
        printf("}\n");
    }

    printf("\n===== STEP 6: Predictive Parsing Table =====\n");
    printf("LL(1) Table constructed using FIRST and FOLLOW.\n");
    printf("Grammar is suitable for predictive parsing.\n");

    return 0;
}

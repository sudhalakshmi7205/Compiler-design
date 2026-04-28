#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX 100

typedef struct {
    int start;
    char label;
    int end;
} Transition;

Transition transitions[MAX];
int trans_count = 0;
int state_count = 0;

void add_transition(int s, char l, int e) {
    transitions[trans_count].start = s;
    transitions[trans_count].label = l;
    transitions[trans_count].end = e;
    trans_count++;
}

void re_to_nfa(char *postfix) {
    int stack[MAX], top = -1;
    int s1, s2, e1, e2, new_s, new_e;

    for (int i = 0; postfix[i] != '\0'; i++) {
        char c = postfix[i];

        if (c >= 'a' && c <= 'z') {
            s1 = state_count++;
            e1 = state_count++;
            add_transition(s1, c, e1);
            stack[++top] = s1; stack[++top] = e1;
        } 
        else if (c == '.') {
            e2 = stack[top--]; s2 = stack[top--];
            e1 = stack[top--]; s1 = stack[top--];
            add_transition(e1, 'e', s2);
            stack[++top] = s1; stack[++top] = e2;
        } 
        else if (c == '|') {
            e2 = stack[top--]; s2 = stack[top--];
            e1 = stack[top--]; s1 = stack[top--];
            new_s = state_count++; new_e = state_count++;
            add_transition(new_s, 'e', s1);
            add_transition(new_s, 'e', s2);
            add_transition(e1, 'e', new_e);
            add_transition(e2, 'e', new_e);
            stack[++top] = new_s; stack[++top] = new_e;
        } 
        else if (c == '*') {
            e1 = stack[top--]; s1 = stack[top--];
            new_s = state_count++; new_e = state_count++;
            add_transition(new_s, 'e', s1);
            add_transition(new_s, 'e', new_e);
            add_transition(e1, 'e', s1);
            add_transition(e1, 'e', new_e);
            stack[++top] = new_s; stack[++top] = new_e;
        }
    }
}

int main() {
    char postfix[MAX];
    scanf("%s", postfix);
    re_to_nfa(postfix);
    
    for (int i = 0; i < trans_count; i++) {
        printf("q%d --%c--> q%d\n", transitions[i].start, transitions[i].label, transitions[i].end);
    }
    return 0;
}

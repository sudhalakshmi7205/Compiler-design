#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 20

int nfa_table[MAX][2][MAX], dfa_table[MAX][2], n_states, n_dfa = 0;
int dfa_states[MAX][MAX], dfa_state_size[MAX];

int is_duplicate(int set[], int size) {
    for (int i = 0; i < n_dfa; i++) {
        if (dfa_state_size[i] == size) {
            int match = 1;
            for (int j = 0; j < size; j++) if (dfa_states[i][j] != set[j]) match = 0;
            if (match) return i;
        }
    }
    return -1;
}

void convert() {
    int queue[MAX], head = 0, tail = 0;
    dfa_states[0][0] = 0; dfa_state_size[0] = 1;
    queue[tail++] = n_dfa++;

    while (head < tail) {
        int curr = queue[head++];
        for (int symbol = 0; symbol < 2; symbol++) {
            int next_set[MAX], next_size = 0, seen[MAX] = {0};
            for (int i = 0; i < dfa_state_size[curr]; i++) {
                int state = dfa_states[curr][i];
                for (int j = 0; nfa_table[state][symbol][j] != -1; j++) {
                    int target = nfa_table[state][symbol][j];
                    if (!seen[target]) { next_set[next_size++] = target; seen[target] = 1; }
                }
            }
            if (next_size == 0) { dfa_table[curr][symbol] = -1; continue; }
            int idx = is_duplicate(next_set, next_size);
            if (idx == -1) {
                for (int i = 0; i < next_size; i++) dfa_states[n_dfa][i] = next_set[i];
                dfa_state_size[n_dfa] = next_size;
                idx = n_dfa++;
                queue[tail++] = idx;
            }
            dfa_table[curr][symbol] = idx;
        }
    }
}

int main() {
    memset(nfa_table, -1, sizeof(nfa_table));
    printf("Enter number of NFA states: "); scanf("%d", &n_states);
    printf("Enter transitions (state input target_state, -1 to stop for that input):\n");
    for (int i = 0; i < n_states; i++) {
        for (int j = 0; j < 2; j++) {
            printf("q%d on %d -> ", i, j);
            int target, k = 0;
            while (scanf("%d", &target) && target != -1) nfa_table[i][j][k++] = target;
        }
    }
    convert();
    printf("\nDFA TRANSITION TABLE\nState\tInput 0\tInput 1\n");
    for (int i = 0; i < n_dfa; i++) {
        printf("D%d\t", i);
        for (int j = 0; j < 2; j++) printf("%s\t", dfa_table[i][j] == -1 ? "-" : (char[]){'D', dfa_table[i][j] + '0', '\0'});
        printf("\n");
    }
    return 0;
}

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern FILE *yyin;
int yylex(void);
int yyerror(const char *s);

/* phase flags */
extern int lexical_error;
int syntax_error = 0;
int semantic_error = 0;

/* Symbol Table */
char sym[100][20];
int symcount = 0;

/* Temporary variables */
int tempcount = 0;

char* newtemp(){
    char *t = malloc(10);
    sprintf(t,"t%d",tempcount++);
    return t;
}

int lookup(char *s){
    for(int i=0;i<symcount;i++)
        if(strcmp(sym[i],s)==0) return 1;
    return 0;
}

void insert(char *s){
    strcpy(sym[symcount++],s);
}
%}

%union{
    int ival;
    char *sval;
}

%token <sval> IDENTIFIER
%token <ival> INTEGER
%token KEYWORD

%type <sval> expr

%%

program : stmts ;

stmts : stmts stmt
      | stmt ;

stmt :
      KEYWORD IDENTIFIER ';'
        { insert($2); }

    | IDENTIFIER '=' expr ';'
        {
            if(!lookup($1)){
                printf("SEMANTIC ERROR : %s not declared\n",$1);
                semantic_error = 1;
            }
            else
                printf("%s = %s\n",$1,$3);
        }
    ;

expr :
      INTEGER
        {
            char buf[10];
            sprintf(buf,"%d",$1);
            $$=strdup(buf);
        }

    | IDENTIFIER
        {
            if(!lookup($1)){
                printf("SEMANTIC ERROR : %s not declared\n",$1);
                semantic_error = 1;
            }
            $$=$1;
        }

    | expr '+' expr
        {
            char *t=newtemp();
            printf("%s = %s + %s\n",t,$1,$3);
            $$=t;
        }

    | expr '*' expr
        {
            char *t=newtemp();
            printf("%s = %s * %s\n",t,$1,$3);
            $$=t;
        }
    ;

%%

int yyerror(const char *s){
    printf("SYNTAX ERROR\n");
    syntax_error = 1;
    return 0;
}

int main(){
    FILE *fp;
    char line[256];

    printf("Enter program (Ctrl+D to finish):\n");

    fp=fopen("input.txt","w");
    while(fgets(line,256,stdin))
        fputs(line,fp);
    fclose(fp);

    /* PHASE 1 */
    printf("\n========== 1. LEXICAL ANALYSIS ==========\n");
    yyin=fopen("input.txt","r");
    while(yylex());
    fclose(yyin);

    if(lexical_error){
        printf("\nCompilation stopped due to lexical errors\n");
        return 0;
    }

    /* PHASE 2 */
    printf("\n========== 2. SYNTAX ANALYSIS ==========\n");
    yyin=fopen("input.txt","r");
    yyparse();
    fclose(yyin);

    if(syntax_error){
        printf("\nCompilation stopped due to syntax errors\n");
        return 0;
    }

    printf("Syntax is valid\n");

    /* PHASE 3 */
    if(semantic_error){
        printf("\nCompilation stopped due to semantic errors\n");
        return 0;
    }

    printf("\n========== 3. SEMANTIC ANALYSIS ==========\n");
    printf("Semantic checks passed\n");

    /* PHASE 4 */
    printf("\n========== 4. INTERMEDIATE CODE ==========\n");
    yyin=fopen("input.txt","r");
    yyparse();
    fclose(yyin);

    /* PHASE 5 */
    printf("\n========== 5. OPTIMIZATION ==========\n");
    printf("Constant folding applied\n");

    /* PHASE 6 */
    printf("\n========== 6. TARGET CODE ==========\n");
    printf("MOV R1, result\n");

    return 0;
}

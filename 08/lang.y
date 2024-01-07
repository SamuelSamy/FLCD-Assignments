%{
	#include <ctype.h> 
  #include <stdio.h> 

  #define YYDEBUG 1

  int productions[1024];
  int production_index = 0;

  void addProduction(int production) 
  {
    productions[production_index++] = production;
  }

  void printProductions() 
  {
    int i;
    for (i = 0; i < production_index; i++) 
    {
      printf("%d ", productions[i]);
    }
    printf("\n");
  }
%}


%token READ
%token WRITE
%token NUMBER
%token DECIMAL
%token STR
%token CAR
%token LET
%token IN
%token SEQ
%token WHILE
%token VECTOR
%token IF
%token ELSE
%token VAR

%token IDENTIFIER
%token NUMBER_CONST
%token STRING_CONST
%token CHAR_CONST

%token ADD
%token SUB
%token MUL
%token DIV
%token MOD

%token EQ
%token NE
%token LT
%token LE
%token GT
%token GE

%token ASSIGN

%token OR
%token AND
%token NOT

%token OPEN_CURLY
%token CLOSE_CURLY
%token OPEN_BRACKET
%token CLOSE_BRACKET
%token OPEN_SQUARE
%token CLOSE_SQUARE

%token COMMA
%token COLON
%token SEMICOLON

%start program

%%
program : statement_list
        ;

statement_list : statement {addProduction(1);}
               | statement_list statement {addProduction(2);}
               ;

statement : declaration {addProduction(3);}
          | assignement {addProduction(4);}
          | io {addProduction(5);}
          | if {addProduction(6);}
          | while {addProduction(7);}
          | for {addProduction(8);}
          ;

io : read {addProduction(9);}
   | write {addProduction(10);}
   ;

complex_identifier : IDENTIFIER OPEN_SQUARE expression CLOSE_SQUARE {addProduction(11);}
                   | IDENTIFIER {addProduction(12);}
                   ;

read : READ complex_identifier SEMICOLON {addProduction(13);}
     ;

write : WRITE expression SEMICOLON {addProduction(14);}
      ;


declaration : simple_declaration {addProduction(15);}
            | assignment_declaration {addProduction(16);}
            ;

simple_declaration : VAR IDENTIFIER COLON type SEMICOLON {addProduction(17);}
                    ;

assignment_declaration : VAR IDENTIFIER COLON type ASSIGN expression SEMICOLON {addProduction(18);}
                        ;

type : simple_type {addProduction(19);}
      | VECTOR LT simple_type GT {addProduction(20);}
      ;

simple_type : NUMBER {addProduction(21);}
            | DECIMAL {addProduction(22);}
            | STR {addProduction(23);}
            | CAR {addProduction(24);}
            ;

// assignment
assignement : complex_identifier ASSIGN expression SEMICOLON {addProduction(25);}
            ;

// if
if : IF OPEN_BRACKET condition CLOSE_BRACKET OPEN_CURLY statement_list CLOSE_CURLY {addProduction(26);}
   | IF OPEN_BRACKET condition CLOSE_BRACKET OPEN_CURLY statement_list CLOSE_CURLY ELSE OPEN_CURLY statement_list CLOSE_CURLY {addProduction(27);}
   ;
    

// while
while : WHILE OPEN_BRACKET condition CLOSE_BRACKET OPEN_CURLY statement_list CLOSE_CURLY {addProduction(28);}
      ;


// for
for : LET IDENTIFIER IN SEQ OPEN_BRACKET sequence CLOSE_BRACKET OPEN_CURLY statement_list CLOSE_CURLY {addProduction(29);}
    ;

sequence : expression {addProduction(30);}
         | expression COMMA expression {addProduction(31);}
         | expression COMMA expression COMMA expression {addProduction(32);}
         ;

// condition
condition : expression relation condition {addProduction(33);}
          | expression {addProduction(34);}
          ;

relation : EQ {addProduction(35);}
         | NE {addProduction(36);}
         | LT {addProduction(37);}
         | LE {addProduction(38);}
         | GT {addProduction(39);}
         | GE {addProduction(40);}
         ;

// expression
expression : expression ADD term {addProduction(41);}
           | expression SUB term {addProduction(42);}
           | term {addProduction(43);}
           ;

term : term MUL factor {addProduction(44);}
     | term DIV factor {addProduction(45);}
     | term MOD factor {addProduction(46);}
     | factor {addProduction(47);}
     ;

factor : OPEN_BRACKET expression CLOSE_BRACKET {addProduction(48);}
       | NUMBER_CONST {addProduction(49);}
       | STRING_CONST {addProduction(50);}
       | CHAR_CONST {addProduction(51);}
       | complex_identifier {addProduction(52);}
       ;

%%

yyerror(char *s)
{
    printf("%s\n", s);
}

extern FILE *yyin;

int main(int argc, char** argv) 
{
  if (argc > 1) 
  {
    yyin = fopen(argv[1], "r");
    if (!yyin) 
    {
      printf("'%s': Could not open specified file\n", argv[1]);
      return 1;
    }
  }

  if (argc > 2 && strcmp(argv[2], "-d") == 0) 
  {
    printf("Debug mode on\n");
    yydebug = 1;
  }

  printf("Starting parsing...\n");

  if (yyparse() == 0) 
  {
    printf("Parsing successful!\n");
    printProductions();
    return 0;
  }

  printf("Parsing failed!\n");
  return 0;
}  
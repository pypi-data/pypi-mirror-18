/**
 * sdpl - schema-driven processing language - grammar
 * @author Bohdan Mushkevych
 */
grammar sdpl;

@lexer::members {
CHANNEL_WHITESPACE = 1
CHANNEL_COMMENTS = 2
}

startrule:  (libDecl | relationDecl | projectionDecl | quotedCode | expandSchema |
             storeDecl | storeSchemaDecl | joinDecl | filterDecl | orderByDecl | groupByDecl)+ ;

// REGISTERING A LIBRARY
libDecl
    :  'REGISTER' quotedString ('AS' ID )? ';'
    ;


// DECLARING AND DEFNING A RELATION OR A SCHEMA
relationDecl
    :  ID '=' 'LOAD' 'SCHEMA' quotedString 'VERSION' INTEGER ';'
    |  ID '=' 'LOAD' 'TABLE' quotedString 'FROM' quotedString 'WITH' 'SCHEMA' quotedString 'VERSION' INTEGER ';'
    ;

// SCHEMA PROJECTION
projectionDecl
    :  ID '=' 'SCHEMA' 'PROJECTION' '(' schemaFields ')' ';'
    ;

schemaFields    :  schemaField (',' schemaField)* ;
schemaField
    :  ('-')? ID '.' ( ID | '*') ('AS' ID)?
    ;

// EXPANDING
expandSchema    :  'EXPAND' 'SCHEMA' ID ';' ;


// STORING
storeDecl       :  'STORE' ID 'INTO' 'TABLE' quotedString 'FROM' quotedString ';' ;
storeSchemaDecl :  'STORE' 'SCHEMA' ID 'INTO' quotedString ';' ;


// JOINING
joinDecl
    :  ID '=' 'JOIN' joinElement (',' joinElement)+ 'WITH' 'SCHEMA' 'PROJECTION' '(' schemaFields ')' ';'
    ;
joinElement     :  ID 'BY' relationColumns ;

relationColumns :  '(' relationColumn (',' relationColumn)* ')' ;
relationColumn  :  ID '.' ID ;

// FILTERING
filterDecl      :  ID '=' 'FILTER' ID 'BY' filterExpression ';' ;

filterExpression
    : filterExpression AND filterExpression
    | filterExpression OR filterExpression
    | filterOperation
    | '(' filterExpression ')'
    ;

filterOperation
    :  filterOperand compOperator filterOperand
    | '(' filterOperation ')'
    ;

filterOperand
    :  quotedString
    |  relationColumn
    |  ('-')? DECIMAL
    |  ('-')? INTEGER
    ;

// ORDER BY
orderByDecl     :  ID '=' 'ORDER' ID 'BY' relationColumn (',' relationColumn)* ';' ;


// GROUP BY
groupByDecl     :  ID '=' 'GROUP' ID 'BY' relationColumn (',' relationColumn)* ';' ;


quotedString
    : '\'' (ID | '.' | ':' | '/' | '$' | '{' | '}' | '@' | '%' | '?' )* '\''
    ;

quotedCode  :  QUOTE_DELIM .*? QUOTE_DELIM ;

compOperator
    : CO_NE
    | CO_EQ
    | CO_LE
    | CO_LT
    | CO_GE
    | CO_GT
    ;

// CO stands for *comparison operator*
CO_NE   : '!=' ;
CO_EQ   : '==' ;
CO_LE   : '<=' ;
CO_LT   : '<'  ;
CO_GE   : '>=' ;
CO_GT   : '>'  ;

AND  : 'AND' ;
OR   : 'OR'  ;
QUOTE_DELIM : '```' ;

ID          :  LETTER (LETTER | NUMBER | UNDERSCORE)* ;
DECIMAL     :  NUMBER+ '.' NUMBER+ ;
INTEGER     :  NUMBER+ ;

WS  :  ( '\t' | ' ' | '\r' | '\n' )+ -> channel(1) ;  // channel(1)

// single line comment
SL_COMMENT
    :   ('--' | '#') .*? '\n'   -> channel(2)   // channel(2)
    ;

fragment
UNDERSCORE :  '_' ;

fragment
NUMBER :  [0-9] ;

fragment
LETTER  :  [a-zA-Z] ;

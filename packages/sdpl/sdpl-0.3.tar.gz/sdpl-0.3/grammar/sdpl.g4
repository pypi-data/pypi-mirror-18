/**
 * sdpl - schema-driven processing language - grammar
 * @author Bohdan Mushkevych
 */
grammar sdpl;

@lexer::members {
CHANNEL_WHITESPACE = 1
CHANNEL_COMMENTS = 2
}

start_rule
    : (libDecl | relationDecl | projectionDecl | quotedCode | expandSchema | storeDecl
       | storeSchemaDecl | joinDecl | filterDecl | orderByDecl | groupByDecl)+  EOF
    ;

// REGISTERING A LIBRARY
libDecl
    : 'REGISTER' quotedString ('AS' ID )? ';'
    ;


// DECLARING AND DEFINING A RELATION OR A SCHEMA
relationDecl
    : ID '=' 'LOAD' 'SCHEMA' quotedString 'VERSION' INTEGER ';'
    | ID '=' 'LOAD' 'TABLE' quotedString 'FROM' quotedString 'WITH' 'SCHEMA' quotedString 'VERSION' INTEGER ';'
    ;


// SCHEMA PROJECTION
projectionDecl
    : ID '=' 'PROJECTION' '(' projectionFields ')' ('NOEMIT')? ';'
    ;

projectionFields    : projectionField (',' projectionField)* ;

projectionField
    : computeDecl
    | schemaField
    ;

schemaField
    : ('-')? ID '.' ( ID | '*') ('AS' ID)?
    ;

// COMPUTE FUNCTION / ARITHMETIC
computeDecl
    : computeExpression 'AS' typedField
    ;

computeExpression
    : computeExpression arithmOperator computeExpression
    | arithmOperation
    | '(' computeExpression ')'
    ;

arithmOperation
    : functionExpression
    | operand arithmOperator operand
    | '(' arithmOperation ')'
    ;

typedField      : ID ':' ID ;


// EXPANDING
expandSchema    : 'EXPAND' 'SCHEMA' ID ';' ;


// STORING
storeDecl       : 'STORE' ID 'INTO' 'TABLE' quotedString 'FROM' quotedString ';' ;
storeSchemaDecl : 'STORE' 'SCHEMA' ID 'INTO' quotedString ';' ;


// JOINING
joinDecl
    : ID '=' 'JOIN' joinElement (',' joinElement)+ 'WITH' 'PROJECTION' '(' projectionFields ')' ';'
    ;
joinElement     : ID 'BY' relationColumns ;

relationColumns : '(' relationColumn (',' relationColumn)* ')' ;
relationColumn  : ID '.' ID ;


// FILTERING
filterDecl      : ID '=' 'FILTER' ID 'BY' filterExpression ';' ;

filterExpression
    : filterExpression AND filterExpression
    | filterExpression OR filterExpression
    | filterOperation
    | '(' filterExpression ')'
    ;

filterOperation
    : operand compOperator operand
    | '(' filterOperation ')'
    ;


// ORDER BY
orderByDecl     : ID '=' 'ORDER' ID 'BY' relationColumn (',' relationColumn)* ';' ;


// GROUP BY
groupByDecl     : ID '=' 'GROUP' ID 'BY' relationColumn (',' relationColumn)* ';' ;


// QUOTED CODE
quotedCode      : QUOTE_DELIM .*? QUOTE_DELIM ;


// OPERAND definition
operand
    : quotedString
    | relationColumn
    | ('-')? DECIMAL
    | ('-')? INTEGER
    | functionExpression
    ;

functionExpression
    : functionName '(' ')'
    | functionName '(' operand (',' operand)* ')'
    ;

// function name could be either:
// package-based, such as `xyz.package_name.function_name`
// build-in, such as SUM or EXP
functionName    : ID ('.' ID)* ;

quotedString
    : '\'' (ID | '.' | ':' | '/' | '$' | '{' | '}' | '@' | '%' | '?' )* '\''
    ;

compOperator
    : CO_NE
    | CO_EQ
    | CO_LE
    | CO_LT
    | CO_GE
    | CO_GT
    ;

arithmOperator
    : AO_MULTIPLY
    | AO_DIVIDE
    | AO_PLUS
    | AO_MINUS
    | AO_POWER
    ;

// AO stands for *arithmetic operator*
AO_MULTIPLY : '*' ;
AO_DIVIDE   : '/' ;
AO_PLUS     : '+' ;
AO_MINUS    : '-' ;
AO_POWER    : '^' ;

// CO stands for *comparison operator*
CO_NE   : '!=' ;
CO_EQ   : '==' ;
CO_LE   : '<=' ;
CO_LT   : '<'  ;
CO_GE   : '>=' ;
CO_GT   : '>'  ;

AND     : 'AND' ;
OR      : 'OR'  ;

QUOTE_DELIM : '```' ;

ID          : LETTER (LETTER | NUMBER | UNDERSCORE)* ;
DECIMAL     : NUMBER+ '.' NUMBER+ ;
INTEGER     : NUMBER+ ;

WS  : ( '\t' | ' ' | '\r' | '\n' )+ -> channel(1) ;  // channel(1)

// single line comment
SL_COMMENT
    : ('--' | '#') .*? '\n'         -> channel(2)   // channel(2)
    ;

fragment
UNDERSCORE  : '_' ;

fragment
NUMBER      : [0-9] ;

fragment
LETTER      : [a-zA-Z] ;

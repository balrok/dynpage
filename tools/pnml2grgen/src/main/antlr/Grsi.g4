grammar Grsi;

root
	: (expr)* EOF
	;

expr
	: COMMENT
	| 'new' new_stmt
	;

new_stmt
	: 'graph' graph
	| node
	| arc
	;

// new graph "Rules" "DefaultGraph"
graph
	: name (name)?
	;

// new :PetriNet($ = "$4_3_2_0", id = "Petri Net")
node
	: elementdecl
	;


// new @("$4_3_1_30") - :inArc($ = "$4_3_1_5F") -> @("$4_3_1_46")
arc
	: reference directedarcright reference
	| reference directedarcleft reference
	| reference undirectedarc reference
	;

reference
	: '@(' StringLiteral ')'
	| name
	;

elementdecl
	: id? ':' name constructor?
	;
constructor
	: '(' parameter (',' parameter)* ')'
	| '(' ')'
	;

directedarcright
	: '-' elementdecl '->'
	;
directedarcleft
	: '<-' elementdecl '-'
	;
undirectedarc
	: '-' elementdecl '-'
	;


parameter
	: key '=' value
	;

id  : name
	;

key : name
	| '$'
	;

name
	: FREESTRING
	| StringLiteral
	;

FREESTRING
	: [a-zA-Z] [a-zA-Z0-9_]*
	;

value
	: INT
	| BOOLEAN
	| StringLiteral
	;

INT
	: [0-9]+
	;

BOOLEAN
	: [tT][rR][uU][eE]
	| [fF][aA][lL][sS][eE]
	;

StringLiteral
	: '"' (~["\r\n] | '\\"')* '"'
	| '\'' (~['\r\n] | '\\\'')* '\''
	;

COMMENT
	: '#' ~[\r\n]*
	;

WS
	: [ \t\u000B\u000C\u0020\u00A0]+ -> skip
	;
NL
	: [\r\n]+ -> skip
	;

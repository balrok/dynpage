grammar Net;
// .net                    ::= (<trdesc>|<pldesc>|<lbdesc>|<prdesc>|<ntdesc>|<netdesc>)*
root
	: (trdesc | pldesc | lbdesc | prdesc | ntdesc | netdesc)* EOF
	;
// netdesc                 ::= ’net’ <net>
netdesc
	: 'net' net
	;
// trdesc                  ::= ’tr’ <transition> {":" <label>} {<interval>} {<tinput> -> <toutput>}
trdesc
	: 'tr' transition (':' label)? (interval)? (tinput* '->' toutput*)?
	;
// pldesc                  ::= ’pl’ <place> {':' <label>} {(<marking>)} {<pinput> -> <poutput>}
pldesc
	: 'pl' place (':' label)? ('(' marking ')')? (pinput* '->' poutput*)?
	;
// ntdesc                  ::= ’nt’ <note> (’0’|’1’) <annotation>
ntdesc
	: 'nt' note (BOOLINT) annotation
	;
// lbdesc                  ::= ’lb’ [<place>|<transition>] <label>
lbdesc
	: 'lb' (place | transition) label
	;
// prdesc                  ::= ’pr’ (<transition>)+ ('<'|'>') (<transition>)+
prdesc
	: 'pr' (transition)+ ('<' | '>') (transition)+
	;
// interval                        ::= (’[’|’]’)INT’,’INT(’[’|’]’) | (’[’|’]’)INT’,’w[’
interval
	: ('[' | ']') INT ',' INT ('['|']')
	| ('[' | ']') INT ',' 'w['
	;
// tinput                  ::= <place>{<arc>}
tinput
	: place arc?
	;
// toutput                 ::= <place>{<normal_arc>}
toutput
	: place normal_arc?
	;
// pinput                  ::= <transition>{<normal_arc>}
pinput
	: transition normal_arc?
	;
// poutput                 ::= <transition>{arc}
poutput
	: transition arc?
	;
// arc                     ::= <normal_arc> | <test_arc> | <inhibitor_arc> |
//                             <stopwatch_arc> | <stopwatch-inhibitor_arc>
arc
	: normal_arc | test_arc | inhibitor_arc | stopwatch_arc | stopwatch_inhibitor_arc
	;
// normal_arc              ::= ’*’<weight>
normal_arc
	: '*' weight
	;
// test_arc                ::= ’?’<weight>
test_arc
	: '?' weight
	;
// inhibitor_arc           ::= ’?-’<weight>
inhibitor_arc
	: '?-' weight
	;
// stopwatch_arc           ::= ’!’<weight>
stopwatch_arc
	: '!' weight
	;
// stopwatch-inhibitor_arc ::= ’!-’<weight>
stopwatch_inhibitor_arc
	: '!-' weight
	;
// weight, marking         ::= INT{’K’|’M’}
weight
	: INT ('K' | 'M')?
	;
marking
	: INT ('K' | 'M')?
	;
// net, place, transition, label, note, annotation ::= ANAME | ’{’QNAME’}’
net
	: NAME
	;
place
	: NAME
	;
transition
	: NAME
	;
label
	: NAME
	;
note
	: NAME
	;
annotation
	: NAME
	;
// INT                     ::= unsigned integer
INT
	: [1-9][0-9]*
	;
BOOLINT
	: [01]
	;
NAME
	: ANAME
	| QNAME
	;
// ANAME                   ::= alphanumeric name, see Notes below
ANAME
	: [A-Za-z_'][A-Za-z_'0-9]*
	;

// QNAME                   ::= arbitrary name, see Notes below
QNAME
	: '{' ~[\{\}]* '}'
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

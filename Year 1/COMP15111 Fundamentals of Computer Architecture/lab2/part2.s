; Hello Someone program - version 2

	B main

hello	DEFB	"Hello \0"
goodbye	DEFB	" and good-bye!\n\0"
	ALIGN

main	ADR	R0, hello	; print("Hello ")
	SVC 	3
next				; while (true) { //The { is just to ease readability, python does not use them
	SVC	1		; input a character to R0

	CMP R0, #10; if R0 == 10 do: // translate to ARM code
    BNE skip

	ADR	R0, goodbye 	;   printf(" and good-bye!")
	SVC	3
	SVC  	2		;   stop the program

	; done // translate to ARM code

skip 	SVC	0		; output the character in R0
	B	next		; } //while


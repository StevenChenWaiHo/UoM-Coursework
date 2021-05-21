; COMP15111 lab 4 - Template file

print_char	equ	0		; Define names to aid readability
stop		equ	2
print_str	equ	3
print_no	equ	4

cLF		equ	10		; Line-feed character


		ADR	SP, _stack	; set SP pointing to the end of our stack
		B	main

		DEFS	100		; this chunk of memory is for the stack
_stack					; This label is 'just after' the stack space


wasborn		DEFB	"This person was born on ",0
was		DEFB	"This person was ",0
on		DEFB	" on ",0
is		DEFB	"This person is ",0
today		DEFB	" today!",0
willbe		DEFB	"This person will be ",0
		ALIGN

pDay		  DEFW	23		;  pDay = 23    //or whatever is today's date
pMonth		DEFW	11		;  pMonth = 11  //or whatever is this month
pYear		  DEFW	2005	;  pYear = 2005 //or whatever is this year

printdate
		MOV	R0, R6
		SVC	print_no
		MOV	R0, #'/'
		SVC	print_char
		MOV	R0, R1
		SVC	print_no
		MOV	R0, #'/'
		SVC	print_char
		MOV	R0, R4
		SVC	print_no
		MOV	R0, #cLF
		SVC	print_char
        MOV	PC, LR


; def printAgeHistory (bDay, bMonth, bYear)

; parameters
;  R0 = bDay (on entry, moved to R6 to allow SVC to output via R0)
;  R1 = bMonth
;  R2 = bYear
; local variables (callee-saved registers)
;  R4 = year
;  R5 = age
;  R6 = bDay - originally R0


printAgeHistory	STMFD SP!, {R4-R6}			; callee saves three registers

		MOV	R6, R0	; Get parameters

;   year = bYear + 1
		ADD	R4, R2, #1
;   age = 1;
		MOV	R5, #1

; print("This person was born on " + str(bDay) + "/" + str(bMonth) + "/" + str(bYear))
		ADRL	R0, wasborn
        SVC	print_str
        SUB R4, R4, #1
		
        STMFD SP!, {LR}
		BL	printdate
		LDMFD SP!, {LR}

        ADD	R4, R4, #1

; this code does: while year < pYear //{
loop1	LDR	R0, pYear
		CMP	R4, R0
		BHS	end1		; Years are unsigned
; for part 4, should be changed to:
; while year < pYear or
;				(year == pYear and bMonth < pMonth) or
;				(year == pYear and bMonth == pMonth and bDay < pDay):

;  print("This person was " + str(age) + " on " + str(bDay) + "/" + str(bMonth) + "/" + str(year))
		ADRL	R0, was
		SVC	print_str
		MOV	R0, R5
		SVC	print_no
		ADRL	R0, on
		SVC	print_str

        STMFD SP!, {LR}
		BL	printdate
		LDMFD SP!, {LR}

		; year = year + 1
		ADD	R4, R4, #1
		; age = age + 1
		ADD	R5, R5, #1
		; //}
		B	loop1

end1
; this code does: if (bMonth == pMonth):
; for part 4, should be changed to:
; if (bMonth == pMonth and bDay == pDay):
		LDR	R0, pMonth
		CMP	R1, R0
		BNE	else1

; print("This person is " + str(age) + " today!")
		ADRL	R0, is
		SVC	print_str
		MOV	R0, R5
		SVC	print_no
		ADRL	R0, today
		SVC	print_str
		MOV	R0, #cLF
		SVC	print_char

; else
		B	end2
else1
; print("This person will be " + str(age) + " on " + str(bDay) + "/" + str(bMonth) + "/" + str(year))
		ADRL	R0, willbe
		SVC	print_str
		MOV	R0, R5
		SVC	print_no
		ADRL	R0, on
		SVC	print_str

		STMFD SP!, {LR}
		BL	printdate
		LDMFD SP!, {LR}

; }// end of printAgeHistory
end2		LDMFD SP!, {R4-R6}		; callee saved registers
		MOV	PC, LR

another		DEFB	"Another person",10,0
		ALIGN

; def main():
main
	LDR	R4, =&12345678		; Test value - not part of Java compilation
	MOV	R5, R4			; See later if these registers corrupted
	MOV	R6, R4

; printAgeHistory(pDay, pMonth, 2000)
		LDR	R0, pDay        ; Stack first parameter
		LDR	R1, pMonth      ; Stack second parameter
		MOV	R2, #2000       ; Stack third parameter
        STMFD SP!, {R0-R2}
		BL	printAgeHistory
		LDMFD SP!, {R0-R2}  ; Deallocate three 32-bit variables

; print("Another person");
		ADRL	R0, another
		SVC	print_str

; printAgeHistory(13, 11, 2000)
		MOV	R0, #13			
		MOV	R1, #11
		MOV	R2, #2000
		STMFD	SP!, {R0-R2}		; The STore Multiple parameter
		BL	printAgeHistory
		LDMFD SP!, {R0-R2}			; Deallocate three 32-bit variables

	; Now check to see if register values intact (Not part of Java)
	LDR	R0, =&12345678		; Test value
	CMP	R4, R0			; Did you preserve these registers?
	CMPEQ	R5, R0			;
	CMPEQ	R6, R0			;

	ADRLNE	R0, whoops1		; Oh dear!
	SVCNE	print_str		;

	ADRL	R0, _stack		; Have you balanced pushes & pops?
	CMP	SP, R0			;

	ADRLNE	R0, whoops2		; Oh no!!
	SVCNE	print_str		; End of test code

; }// end of main
		SVC	stop


whoops1		DEFB	"\n** BUT YOU CORRUPTED REGISTERS!  **\n", 0
whoops2		DEFB	"\n** BUT YOUR STACK DIDN'T BALANCE!  **\n", 0

// MU0 FSM design - behavioural style
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps

// for simulation purposes, do not delete
`default_nettype none

// module header

module mu0_fsm(input  wire         Clk, 
	           input  wire         Reset, 
			   input  wire         Halted, 
			   output reg          state);

// internal variables
reg next_state;

// Behavioural description
always @ (*)
    case (state)
        1'b0:       next_state = 1'b1;
        default:    next_state = 1'b0;
    endcase



always @ (posedge Clk, posedge Reset) // Asynchronous Reset
    if (Reset)
        state <= 1'b0;
    else if(~Halted)
        state <= next_state;

endmodule 

// for simulation purposes, do not delete
`default_nettype wire

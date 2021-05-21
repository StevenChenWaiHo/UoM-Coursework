// MU0 16 bit register design - behavioural style
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps

// for simulation purposes, do not delete
`default_nettype none

// module header

module mu0_reg16(input  wire        Clk, 
	             input  wire        Reset,     
			     input  wire        En, 
			     input  wire [15:0] D, 
			     output reg  [15:0] Q);

// behavioural code - clock driven
always @(posedge Clk, posedge Reset)
    if (Reset)
        Q <= 0;
    else if (En)
        Q <= D;

endmodule 

// for simulation purposes, do not delete
`default_nettype wire

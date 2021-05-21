// 16-bit adder design using verilog primitive gates
// P W Nutter (based on a design by Jeff Pepper)
// Date 1/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps

// for simulation purposes, do not delete
`default_nettype none

module adder_16bit(input  wire [15:0]  a, 
	               input  wire [15:0]  b, 
				   input  wire         cin, 
				   output wire [15:0]  s, 
				   output wire         cout);

//Internal carry connections

wire c0;
wire c1;
wire c2;

// Instantiate 4 x adder_4bit
adder_4bit adder0(a[3:0],b[3:0],cin,s[3:0],c0);
adder_4bit adder1(a[7:4],b[7:4],c0,s[7:4],c1);  
adder_4bit adder2(a[11:8],b[11:8],c1,s[11:8],c2);
adder_4bit adder3(a[15:12],b[15:12],c2,s[15:12],cout);



endmodule 

// for simulation purposes, do not delete
`default_nettype wire

// 4-bit adder design using verilog primitive gates
// P W Nutter (based on a design by Jeff Pepper)
// Date 1/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps

// for simulation purposes, do not delete
`default_nettype none

//Module definition

module adder_4bit(input  wire [3:0]  a, 
                  input  wire [3:0]  b, 
                  input  wire        cin, 
                  output wire [3:0]  s, 
                  output wire        cout);

//Internal carry connections

wire c0;
wire c1;
wire c2;

// Instantiate 4 x full_adder

full_adder adder0(a[0],b[0],cin,s[0],c0);
full_adder adder1(a[1],b[1],c0,s[1],c1);  
full_adder adder2(a[2],b[2],c1,s[2],c2);
full_adder adder3(a[3],b[3],c2,s[3],cout);


endmodule 

// for simulation purposes, do not delete
`default_nettype wire

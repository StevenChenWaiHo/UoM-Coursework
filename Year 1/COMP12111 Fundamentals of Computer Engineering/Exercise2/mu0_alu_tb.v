// MU0 ALU testbench 
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// #1 = 1ns
`timescale 1ns/100ps 

module mu0_alu_tb();

// Internal connections
reg [15:0]  X; 
reg [15:0]  Y;
reg [1:0]   M;
wire  [15:0]  Q;

// Instantiate mu0_alu as dut (device under test)

mu0_alu dut(X, Y, M, Q);

// Test vectors
initial
begin
//Test
#100 X=16'h0000; Y=16'h0000; M=2'b00;

//M==00 Y
#100 X=16'h0000; Y=16'h000F; M=2'b00;//Test for Connection Y Y>0
#100 X=16'h0000; Y=16'hFFFF; M=2'b00;//Test for Y<0

//M==01 X + Y
#100 X=16'h000F; Y=16'h000F; M=2'b01;//Test for Y>0 X>0
#100 X=16'h000F; Y=16'hFFFF; M=2'b01;//Test for Y<0 X>0
#100 X=16'hFFFF; Y=16'h000F; M=2'b01;//Test for Y>0 X<0
#100 X=16'hFFFF; Y=16'hFFFF; M=2'b01;//Test for Y<0 X<0

//M==10 X + 1
#100 X=16'h000F; Y=16'h0000; M=2'b10;//Test for Connection X X>0
#100 X=16'hFFFF; Y=16'h0000; M=2'b10;//Test for X<0

//M==11 X - Y
#100 X=16'h000F; Y=16'h000F; M=2'b11;//Test for Y>0 X>0
#100 X=16'h000F; Y=16'hFFFF; M=2'b11;//Test for Y<0 X>0
#100 X=16'hFFFF; Y=16'h000F; M=2'b11;//Test for Y>0 X<0
#100 X=16'hFFFF; Y=16'hFFFF; M=2'b11;//Test for Y<0 X<0

#100 $finish;;   // end the simulation
end
 
// Save results as VCD file 
// Do not change
initial
 begin
  $dumpfile("mu0_alu_tb_results.vcd");  // Save simulation waveforms in this file
  $dumpvars; // Capture all simulation waveforms
 end

endmodule 

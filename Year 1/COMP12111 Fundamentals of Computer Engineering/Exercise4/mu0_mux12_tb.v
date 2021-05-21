// MU0 12 bit, 2 to 1 MUX testbench
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps 

// module header

module mu0_mux12_tb();

// Internal connections
reg [11:0]A;
reg [11:0]B;
reg S;
wire [11:0]Q;

// Instantiate mu0_mux16 as dut (device under test)
// Uses explicit dot pins - safer than position substitution
mu0_mux12 dut(
.A (A),
.B (B),
.S (S),
.Q (Q));

// Test vectors
initial
  begin
    A=16'h000; B=16'hFFF; S=0;
    #100
    S=1;
    #100
  $finish; // exit the simulation
  end
 
// Save results as VCD file 
// Do not change
initial
 begin
  $dumpfile("mu0_mux12_tb_results.vcd");  // Save simulation waveforms in this file
  $dumpvars; // Capture all simulation waveforms
 end

endmodule 

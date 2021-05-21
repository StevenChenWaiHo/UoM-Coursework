// Full adder testbench
// P W Nutter (based on a design by Jeff Pepper)
// Date 1/9/2020

// Do not touch the following line it is required for simulation 
// #1 = 1ns
`timescale 1ns/100ps 

module full_adder_tb();

// Internal connections
reg a;
reg b;
reg cin;
wire s;
wire cout;

// Instantiate full adder as dut (device under test)

full_adder dut(a, b, cin, s, cout);

// Test vectors
// All combinations required 
initial
 begin
  a = 0; b = 0; cin = 0;
  #100 a = 1;
  #100 a = 0; b = 1;
  #100 a = 1;
  #100 a = 0; b = 0; cin = 1;
  #100 a = 1;
  #100 a = 0; b = 1;
  #100 a = 1;
  #100 $finish; // exit the simulation
 end
 
// Save results as VCD file 
// Do not change
initial
 begin
  $dumpfile("full_adder_tb_results.vcd");  // Save simulation waveforms in this file
  $dumpvars; // Capture all simulation waveforms
 end

endmodule 

// MU0 16 bit register testbench
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps 

// module header

module mu0_reg16_tb();

// Internal connections
reg Clk;
reg Reset;
reg En;
reg [15:0]D;
wire [15:0]Q;


// Instantiate mu0_reg16 as dut (device under test)
// Uses explicit dot pins - safer than position substitution
mu0_reg16 dut(
.Clk (Clk),
.Reset (Reset),
.En (En),
.D (D),
.Q (Q));


// Set up the clock
initial Clk = 0;
always
    begin
    #50
    Clk = ~Clk;
    end


// Test vectors
initial
 begin
  Reset=0;  // Initialize
  #100  // Test Clk Working
  En=1;   D=16'hFFFF;     // Test When En is high
  #100
  En = 0;   D=16'h0000;     // Test When En is low
  #100
  $finish;      // exit the simulation
 end
 
// Save results as VCD file 
// Do not change
initial
 begin
  $dumpfile("mu0_reg16_tb_results.vcd");  // Save simulation waveforms in this file
  $dumpvars; // Capture all simulation waveforms
 end

endmodule 

// MU0 FSM testbench
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps 

// module header

module mu0_fsm_tb();

// Internal connections
reg Clk;
reg Reset;
reg Halted;
wire state;

// Instantiate mu0 fsm as dut (device under test)
// Uses explicit dot pins - safer than position substitution

mu0_fsm dut(
.Clk (Clk),
.Reset (Reset),
.Halted (Halted),
.state (state));

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
    #100                // Test for Clk Signal
    Reset = 1; Halted = 0;    
    #50 Reset = 0;       
    #150                // Test if state change from 0 to 1 to 0
    #100 Reset = 1;     // Test Asynchronous Reset
    #50
    Reset = 0;  
    Halted = 1;         // Halted at Fetch
    #100
    Halted = 0;
    #50
    Halted = 1;         //Halted at Execute
    #100
    $finish;        // end the simulation
end
 
// Save results as VCD file 
// Do not change
initial
 begin
  $dumpfile("mu0_fsm_tb_results.vcd");  // Save simulation waveforms in this file
  $dumpvars; // Capture all simulation waveforms
 end

endmodule 

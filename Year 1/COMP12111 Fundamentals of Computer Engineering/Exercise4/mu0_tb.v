// MU0 testbench
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps 

module mu0_tb();

// Internal connections
reg Reset;
reg Clk;

wire Rd;
wire Wr;
wire [15:0] Data_in;
wire [15:0] Data_out;
wire [11:0] Address;

wire Halted;

// Instantiate mu0 as dut (device under test)
// Instantiate mu0_memory as memory

mu0 dut(Clk, Reset, Data_in, Rd, Wr, Address, Data_out, Halted);
mu0_memory memory(Clk, Wr, Rd, Address, Data_out, Data_in);


// Set up the clock
initial Clk = 0;
always
    begin
    #50
    Clk = ~Clk;
    end

// Perform a reset action of MU0
initial
begin
    Reset=1;
    #100 Reset=0; 
    #4000


   $finish; // exit the simulation - could tie this to the Halted signal going high
end
 
// Save results as VCD file 
// Do not change
initial
 begin
  $dumpfile("mu0_tb_results.vcd");  // Save simulation waveforms in this file
  $dumpvars; // Capture all simulation waveforms
 end

endmodule 

// MU0 Decode testbench
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps 

module mu0_decode_tb();

// Internal connections
reg state;
reg [3:0]F;
reg N;
reg Z;
wire fetch;
wire PC_En;
wire IR_En;
wire Acc_En;
wire X_sel;
wire Y_sel;
wire Addr_sel;
wire [1:0]M;
wire Rd;
wire Wr;
wire Halted;

// Instantiate mu0 control as dut (device under test)
// Uses explicit dot pins - safer than position substitution
mu0_decode dut(
.state (state),
.F (F),
.N (N),
.Z (Z),
.fetch (fetch),
.PC_En (PC_En),
.IR_En (IR_En),
.Acc_En (Acc_En),
.X_sel (X_sel),
.Y_sel (Y_sel),
.Addr_sel (Addr_sel),
.M (M),
.Rd (Rd),
.Wr (Wr),
.Halted (Halted));

// Test vectors
// Make sure that we go through both fetch and execute
initial
begin
  state = 0;
  #100 state = 1; F=3'b000;       // Test for LDA
  #100 state = 1; F=3'b001;       // Test for STA
  #100 state = 1; F=3'b010;       // Test for ADD
  #100 state = 1; F=3'b011;       // Test for SUB
  #100 state = 1; F=3'b100;       // Test for JMP
  #100 state = 1; F=3'b101; N=0;  // Test for JGE when N = 0
  #100 state = 1; F=3'b101; N=1;  // Test for JGE when N = 1  
  #100 state = 1; F=3'b110; Z=0;  // Test for JNE when Z = 0
  #100 state = 1; F=3'b110; Z=1;  // Test for JNE when Z = 1
  #100 state = 1; F=3'b111;       // Test for STP
  #100
  $finish;   // end the simulation
end

 
// Save results as VCD file 
// Do not change
initial
 begin
  $dumpfile("mu0_decode_tb_results.vcd");  // Save simulation waveforms in this file
  $dumpvars; // Capture all simulation waveforms
 end

endmodule 

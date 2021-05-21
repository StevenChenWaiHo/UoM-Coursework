// MU0 Control testbench
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps 

module mu0_control_tb();

// Internal connections
reg Clk;
reg Reset;
reg [3:0]F;
reg N;
reg Z;
wire fetch;
wire PC_En;
wire IR_En;
wire Acc_En;
wire X_sel;
wire Y_sel;
wire addr_sel;
wire [1:0]M;
wire Rd;
wire Wr;
wire Halted;

// Instantiate mu0 control as dut (device under test)

mu0_control dut(
.Clk (Clk),
.Reset (Reset),
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


// Set up the clock

initial Clk = 0;
always
    begin
    #50
    Clk = ~Clk;
    end

// Test vectors
// Using #200 to make sure that we go through both fetch and execute
initial
begin
    #150    // Test for Clk
    Reset = 1; N = 0; Z = 0;
    #50 Reset = 0;
    #150    // Test for fetch execute cycle
    #100 F = 3'b000;            // Test LDA
    #100                   
    #100 F = 3'b001;            // Test STA
    #100
    #100 F = 3'b010;            // Test ADD
    #100
    #100 F = 3'b011;            // Test SUB
    #100
    #100 F = 3'b100;            // Test JMP
    #100
    #100 F = 3'b101; N = 0;     // Test JGE when N = 0
    #100
    #100 F = 3'b101; N = 1;     // Test JGE when N = 1
    #100
    #100 F = 3'b110; Z = 0;     // Test JNE when Z = 0
    #100
    #100 F = 3'b110; Z = 1;     // Test JNE when Z = 1
    #100
    #100 F = 3'b111;            // Test STP
    #100
    #100 Reset = 1;             // Test Reset in Execute state
    #100
  $finish;   // end the simulation
end

 
// Save results as VCD file 
// Do not change
initial
 begin
  $dumpfile("mu0_control_tb_results.vcd");  // Save simulation waveforms in this file
  $dumpvars; // Capture all simulation waveforms
 end

endmodule 

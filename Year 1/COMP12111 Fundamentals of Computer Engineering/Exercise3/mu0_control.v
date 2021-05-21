// MU0 control design - behavioural style
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps

// for simulation purposes, do not delete
`default_nettype none

// module definition

module mu0_control(input  wire         Clk,      // System clock
                   input  wire         Reset,    // System reset
                   input  wire  [3:0]  F,        // Bits [15:12] of the IR
                   input  wire         N,        // Negative flag
                   input  wire         Z,        // Zero flag
                   output wire          fetch,    // Used for debug
                   output wire          PC_En,    // Update PC
                   output wire          IR_En,    // Update IR
                   output wire          Acc_En,   // Update Acc
                   output wire          X_sel,    // Data Out mux(X port on ALU) 0 for Acc, 1 for PC
                   output wire          Y_sel,    // mux, Y port on ALU, 0 for Data In, 1 for Instr 
                   output wire          Addr_sel, // mux, 0 for PC, 1 for IR
                   output wire   [1:0]  M,        // ALU op, 0) Y, 1) X+Y, 2) X+1, 3) X-Y
                   output wire          Rd,       // Memory read
                   output wire          Wr,       // Memory write
                   output wire          Halted);  // MU0 stopped


//Internal signals
wire state;

// Instantiate MU0 FSM
// Uses explicit dot pins - safer than position substitution
mu0_fsm fsm(Clk, Reset, Halted, state);

// Instantiate Control decode
mu0_decode decode(state, F, N, Z, fetch, PC_En, IR_En, Acc_En, X_sel, Y_sel, Addr_sel, M, Rd, Wr, Halted);


endmodule 

// for simulation purposes, do not delete
`default_nettype wire

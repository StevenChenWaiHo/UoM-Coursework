// MU0 decode design - behavioural style
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps

// for simulation purposes, do not delete
`default_nettype none

// module definition

module mu0_decode(input  wire        state,      // System clock
                  input  wire [3:0]  F,          // Bits [15:12] of the IR
                  input  wire        N,          // Negative flag
                  input  wire        Z,          // Zero flag
                  output reg         fetch,      // Used for debug
                  output reg         PC_En,      // Update PC
                  output reg         IR_En,      // Update IR
                  output reg         Acc_En,     // Update Acc
                  output reg         X_sel,      // Data Out mux(X port on ALU) 0 for Acc, 1 for PC
                  output reg         Y_sel,      // mux, Y port on ALU, 0 for Data In, 1 for Instr 
                  output reg         Addr_sel,   // mux, 0 for PC, 1 for IR
                  output reg  [1:0]  M,          // ALU op, 0) Y, 1) X+Y, 2) X+1, 3) X-Y
                  output reg         Rd,         // Memory read
                  output reg         Wr,         // Memory write
                  output reg         Halted);    // MU0 stopped


// Control decode
always @ (*) begin
    if (~state) begin // Fetch Stage
        fetch = 1'b1;
        PC_En = 1'b1;
        IR_En = 1'b1;
        Acc_En = 1'b0;
        M = 2'b10;
        X_sel = 1'b1;
        Y_sel = 1'hx;
        Addr_sel = 1'b0;
        Rd = 1'b1;
        Wr = 1'b0;
        Halted = 1'b0;
        end
    else if (state) begin// LDA
        fetch = 1'b0;
        case (F)
            3'b000: begin 
                        PC_En = 1'b0;
                        IR_En = 1'b0;
                        Acc_En = 1'b1;
                        M = 2'b00;
                        X_sel = 1'hx;
                        Y_sel = 1'b0;
                        Addr_sel = 1'b1;
                        Rd = 1'b1;
                        Wr = 1'b0;
                        Halted = 1'b0;
                        end
            3'b001: begin // STA
                        PC_En = 1'b0;
                        IR_En = 1'b0;
                        Acc_En = 1'b0;
                        M = 2'hx;
                        X_sel = 1'b0;
                        Y_sel = 1'hx;
                        Addr_sel = 1'b1;
                        Rd = 1'b0;
                        Wr = 1'b1;
                        Halted = 1'b0;
                        end
            3'b010: begin // ADD
                        PC_En = 1'b0;
                        IR_En = 1'b0;
                        Acc_En = 1'b1;
                        M = 2'b01;
                        X_sel = 1'b0;
                        Y_sel = 1'b0;
                        Addr_sel = 1'b1;
                        Rd = 1'b1;
                        Wr = 1'b0;
                        Halted = 1'b0;
                        end
            3'b011: begin // SUB
                        PC_En = 1'b0;
                        IR_En = 1'b0;
                        Acc_En = 1'b1;
                        M = 2'b11;
                        X_sel = 1'b0;
                        Y_sel = 1'b0;
                        Addr_sel = 1'b1;
                        Rd = 1'b1;
                        Wr = 1'b0;
                        Halted = 1'b0;
                        end
            3'b100: begin // JMP
                        PC_En = 1'b1;
                        IR_En = 1'b0;
                        Acc_En = 1'b0;
                        M = 2'b00;
                        X_sel = 1'hx;
                        Y_sel = 1'b1;
                        Addr_sel = 1'hx;
                        Rd = 1'b0;
                        Wr = 1'b0;
                        Halted = 1'b0;
                        end
            3'b101: begin // JGE
                        if (~N) begin // JMP if not negative
                            PC_En = 1'b1;
                            IR_En = 1'b0;
                            Acc_En = 1'b0;
                            M = 2'b00;
                            X_sel = 1'hx;
                            Y_sel = 1'b1;
                            Addr_sel = 1'hx;
                            Rd = 1'b0;
                            Wr = 1'b0;
                            Halted = 1'b0;
                            end
                        else begin
                            PC_En = 1'b0;
                            IR_En = 1'b0;
                            Acc_En = 1'b0;
                            M = 2'hx;
                            X_sel = 1'hx;
                            Y_sel = 1'hx;
                            Addr_sel = 1'hx;
                            Rd = 1'b0;
                            Wr = 1'b0;
                            Halted = 1'b0;
                            end
                            end
            3'b110: begin // JNE
                        if (~Z) begin // JMP if not zero
                            PC_En = 1'b1;
                            IR_En = 1'b0;
                            Acc_En = 1'b0;
                            M = 2'b00;
                            X_sel = 1'hx;
                            Y_sel = 1'b1;
                            Addr_sel = 1'hx;
                            Rd = 1'b0;
                            Wr = 1'b0;
                            Halted = 1'b0;
                            end
                        else begin
                            PC_En = 1'b0;
                            IR_En = 1'b0;
                            Acc_En = 1'b0;
                            M = 2'hx;
                            X_sel = 1'hx;
                            Y_sel = 1'hx;
                            Addr_sel = 1'hx;
                            Rd = 1'b0;
                            Wr = 1'b0;
                            Halted = 1'b0;
                            end
                            end
            3'b111: begin // STP
                        PC_En = 1'b0;
                        IR_En = 1'b0;
                        Acc_En = 1'b0;
                        M = 2'hx;
                        X_sel = 1'hx;
                        Y_sel = 1'hx;
                        Addr_sel = 1'hx;
                        Rd = 1'b0;
                        Wr = 1'b0;
                        Halted = 1'b1;
                        end
            default: begin // Invalid Instruction
                        PC_En = 1'b0;
                        IR_En = 1'b0;
                        Acc_En = 1'b0;
                        M = 2'hx;
                        X_sel = 1'hx;
                        Y_sel = 1'hx;
                        Addr_sel = 1'hx;
                        Rd = 1'b0;
                        Wr = 1'b0;
                        Halted = 1'b0;
                        end
            endcase
        end
        else // Invalid State
            begin
                PC_En = 1'b0;
                IR_En = 1'b0;
                Acc_En = 1'b0;
                M = 2'hx;
                X_sel = 1'hx;
                Y_sel = 1'hx;
                Addr_sel = 1'hx;
                Rd = 1'b0;
                Wr = 1'b0;
                Halted = 1'b0;
                end
end
endmodule 

// for simulation purposes, do not delete
`default_nettype wire

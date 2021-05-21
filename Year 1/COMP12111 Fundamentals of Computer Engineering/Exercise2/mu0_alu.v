// MU0 ALU design 
// P W Nutter (based on a design by Jeff Pepper)
// Date 2/9/2020
// 

// Do not touch the following line it is required for simulation 
`timescale 1ns/100ps

// for simulation purposes, do not delete
`default_nettype none

// module header

module mu0_alu(input  wire [15:0]  X, 
               input  wire [15:0]  Y, 
               input  wire [1:0]   M, 
               output reg  [15:0]  Q);

// behavioural description
always @(*) begin
    case (M[1:0])
        2'b00:    Q[15:0] = Y[15:0];
        2'b01:    Q[15:0] = X[15:0] + Y[15:0];
        2'b10:    Q[15:0] = X[15:0] + 1;
        2'b11:    Q[15:0] = X[15:0] - Y[15:0];
    endcase
  end
endmodule 

// for simulation purposes, do not delete
`default_nettype wire

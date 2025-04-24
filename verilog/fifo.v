//--------------------------------------------------------------------
//  _____    __  __    _____          ____     ____     _  __
// |\____\  |\_\|\_\  |\_____\       /\___\   /\___\   /\____\
// \|_   _| ||  \/  | ||  ___|  _   |\/ _ _\ |\/ _  \  \/ ____|
//   || |   ||      | || |_\   |\_\ || |     || /_\  | \| |__
//  _|| |_  || |\/| | ||  _|_  \|_| || |___  || |__| |  _\__ \
// |\_| |_\ || |  | | || |___\      \| |___\ || | || | |\__\| |
// \|_____| \|_|  |_| \|_____|       \\____/ \|_| \|_| \|____/
//
// COPYRIGHT 2023, ALL RIGHTS RESERVED
// Institute of Microelectronics, Chinese Academy of Sciences
//
// Filename:    tinyriscv_soc_top.v
// Author:      CIM Team of YuanYiyang
// Date:        2024-03-16
// 
// Project:     Verilog
// Description: fifo module
//--------------------------------------------------------------------


module fifo (
    input wire clk,
    input wire srst,
    input wire wr_en,
    input wire rd_en,
	 
    input wire [31:0] din,
    output reg [31:0] dout,
	 
    output wire empty,
    output wire full
);
	 reg [4:0] wr_ptr;
	 reg [4:0] rd_ptr;
	 
    parameter DEPTH = 32;

    // FIFO memory
    reg [31:0] fifo_mem [0:DEPTH-1];

    // Write to FIFO
    always @(posedge clk or negedge srst) begin
        if (!srst)
            wr_ptr <= 0;
        else if (wr_en && !full)
            wr_ptr <= wr_ptr + 5'b1;
    end

    always @(posedge clk) begin
        if (wr_en && !full)
            fifo_mem[wr_ptr] <= din;
    end

    // Read from FIFO
    always @(posedge clk or negedge srst) begin
        if (!srst)
            rd_ptr <= 0;
        else if (rd_en && !empty)
            rd_ptr <= rd_ptr + 5'b1;
    end


    always @(posedge clk) begin
        if (rd_en && !empty)
            dout <= fifo_mem[rd_ptr];
    end

    // Empty and full flags
    assign empty = (wr_ptr == rd_ptr);
    assign full = (wr_ptr == rd_ptr - 1) || ((wr_ptr == DEPTH - 1) && (rd_ptr == 0));

endmodule
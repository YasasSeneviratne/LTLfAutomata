module new1TruthTable (
	output reg new1,
	input wire clk, run, rst, A,B,new2,new0
);
	reg old1;
	initial
	old1 = 1'b0;

	always @(posedge clk)
	case ({A, B, new2, new0})
		// A B new2 new0 old1 : new1
		5'b01000 : new1 = 1'b1;
		5'b00100 : new1 = 1'b0;
		5'b01100 : new1 = 1'b0;
		5'b11100 : new1 = 1'b0;
		5'b11001 : new1 = 1'b0;
		5'b00011 : new1 = 1'b1;
		5'b10011 : new1 = 1'b1;
		5'b00010 : new1 = 1'b1;
		5'b01010 : new1 = 1'b1;
		5'b10010 : new1 = 1'b1;
		5'b11010 : new1 = 1'b1;
		5'b00001 : new1 = 1'b0;
		5'b10100 : new1 = 1'b1;
		5'b00000 : new1 = 1'b0;
		5'b10001 : new1 = 1'b1;
		5'b01011 : new1 = 1'b0;
		5'b11011 : new1 = 1'b0;
		5'b11000 : new1 = 1'b0;
		5'b10000 : new1 = 1'b1;
		5'b01001 : new1 = 1'b1;
	endcase

	always @(posedge clk, posedge rst)
	begin
		if(rst == 1'b1)
			old1 = 1'b0;
		else if (run == 1'b1)
			old1 = new1;
	end
endmodule



module new0TruthTable (
	output reg new0,
	input wire clk, run, rst, A,B,new2,new1
);
	reg old0;
	initial
	old0 = 1'b0;

	always @(posedge clk)
	case ({A, B, new2, new1})
		// A B new2 new1 old0 : new0
		5'b01000 : new0 = 1'b0;
		5'b00100 : new0 = 1'b0;
		5'b01100 : new0 = 1'b0;
		5'b11100 : new0 = 1'b0;
		5'b11001 : new0 = 1'b0;
		5'b00011 : new0 = 1'b1;
		5'b10011 : new0 = 1'b1;
		5'b00010 : new0 = 1'b0;
		5'b01010 : new0 = 1'b0;
		5'b10010 : new0 = 1'b0;
		5'b11010 : new0 = 1'b0;
		5'b00001 : new0 = 1'b1;
		5'b10100 : new0 = 1'b1;
		5'b00000 : new0 = 1'b1;
		5'b10001 : new0 = 1'b1;
		5'b01011 : new0 = 1'b0;
		5'b11011 : new0 = 1'b0;
		5'b11000 : new0 = 1'b0;
		5'b10000 : new0 = 1'b1;
		5'b01001 : new0 = 1'b0;
	endcase

	always @(posedge clk, posedge rst)
	begin
		if(rst == 1'b1)
			old0 = 1'b0;
		else if (run == 1'b1)
			old0 = new0;
	end
endmodule



module new2TruthTable (
	output reg new2,
	input wire clk, run, rst, A,B,new1,new0
);
	reg old2;
	initial
	old2 = 1'b0;

	always @(posedge clk)
	case ({A, B, new1, new0})
		// A B new1 new0 old2 : new2
		5'b01000 : new2 = 1'b0;
		5'b00100 : new2 = 1'b1;
		5'b01100 : new2 = 1'b1;
		5'b11100 : new2 = 1'b1;
		5'b11001 : new2 = 1'b1;
		5'b00011 : new2 = 1'b0;
		5'b10011 : new2 = 1'b0;
		5'b00010 : new2 = 1'b0;
		5'b01010 : new2 = 1'b0;
		5'b10010 : new2 = 1'b0;
		5'b11010 : new2 = 1'b0;
		5'b00001 : new2 = 1'b0;
		5'b10100 : new2 = 1'b0;
		5'b00000 : new2 = 1'b0;
		5'b10001 : new2 = 1'b0;
		5'b01011 : new2 = 1'b1;
		5'b11011 : new2 = 1'b1;
		5'b11000 : new2 = 1'b1;
		5'b10000 : new2 = 1'b0;
		5'b01001 : new2 = 1'b0;
	endcase

	always @(posedge clk, posedge rst)
	begin
		if(rst == 1'b1)
			old2 = 1'b0;
		else if (run == 1'b1)
			old2 = new2;
	end
endmodule



module reportTruthTable 
(
	output reg report,
	input wire new2,new1,new0
);

	always @*
	case ({new2,new1,new0})
		// new2 new1 new0 : report
		3'b001 : report = 1'b1;
		3'b100 : report = 1'b1;
		3'b010 : report = 1'b0;
		3'b000 : report = 1'b0;
		3'b011 : report = 1'b0;
		default : report = 1'b0;

	endcase
endmodule


module TransitionTable(B, A, clk, run, rst, report);

	input B, A, clk, run, rst;
	output wire report;
	wire new0, new1, new2;

	// Instantiate truth tables
	new1TruthTable new1tt(
		.new1(new1),
		.A(A),
		.B(B),
		.new2(new2),
		.new0(new0),
		.clk(clk),
		.run(run),
		.rst(rst)
	);

	new0TruthTable new0tt(
		.new0(new0),
		.A(A),
		.B(B),
		.new2(new2),
		.new1(new1),
		.clk(clk),
		.run(run),
		.rst(rst)
	);

	new2TruthTable new2tt(
		.new2(new2),
		.A(A),
		.B(B),
		.new1(new1),
		.new0(new0),
		.clk(clk),
		.run(run),
		.rst(rst)
	);

	reportTruthTable reporttt(
		.report(report),
		.new2(new2),
		.new1(new1),
		.new0(new0)
	);

endmodule

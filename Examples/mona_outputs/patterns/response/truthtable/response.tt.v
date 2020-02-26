module new1TruthTable (
	output reg new1,
	input wire clk, run, rst, A,B,new0
);
	reg old1;
	initial
	old1 = 1'b0;

	always @(posedge clk)
	case ({A, B, new0})
		// A B new0 old1 : new1
		4'b0000 : new1 = 1'b0;
		4'b0100 : new1 = 1'b0;
		4'b1100 : new1 = 1'b0;
		4'b1000 : new1 = 1'b1;
		4'b1001 : new1 = 1'b1;
		4'b0010 : new1 = 1'b1;
		4'b1010 : new1 = 1'b1;
		4'b0001 : new1 = 1'b0;
		4'b0101 : new1 = 1'b0;
		4'b1101 : new1 = 1'b0;
		4'b0110 : new1 = 1'b0;
		4'b1110 : new1 = 1'b0;
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
	input wire clk, run, rst, A,B,new1
);
	reg old0;
	initial
	old0 = 1'b0;

	always @(posedge clk)
	case ({A, B, new1})
		// A B new1 old0 : new0
		4'b0000 : new0 = 1'b1;
		4'b0100 : new0 = 1'b1;
		4'b1100 : new0 = 1'b1;
		4'b1000 : new0 = 1'b0;
		4'b1001 : new0 = 1'b0;
		4'b0010 : new0 = 1'b0;
		4'b1010 : new0 = 1'b0;
		4'b0001 : new0 = 1'b1;
		4'b0101 : new0 = 1'b1;
		4'b1101 : new0 = 1'b1;
		4'b0110 : new0 = 1'b1;
		4'b1110 : new0 = 1'b1;
	endcase

	always @(posedge clk, posedge rst)
	begin
		if(rst == 1'b1)
			old0 = 1'b0;
		else if (run == 1'b1)
			old0 = new0;
	end
endmodule



module reportTruthTable 
(
	output reg report,
	input wire new1,new0
);

	always @*
	case ({new1,new0})
		// new1 new0 : report
		2'b01 : report = 1'b1;
		2'b10 : report = 1'b0;
		2'b00 : report = 1'b0;
		default : report = 1'b0;

	endcase
endmodule


module TransitionTable(B, A, clk, run, rst, report);

	input B, A, clk, run, rst;
	output wire report;
	wire new1, new0;

	// Instantiate truth tables
	new1TruthTable new1tt(
		.new1(new1),
		.A(A),
		.B(B),
		.new0(new0),
		.clk(clk),
		.run(run),
		.rst(rst)
	);

	new0TruthTable new0tt(
		.new0(new0),
		.A(A),
		.B(B),
		.new1(new1),
		.clk(clk),
		.run(run),
		.rst(rst)
	);

	reportTruthTable reporttt(
		.report(report),
		.new1(new1),
		.new0(new0)
	);

endmodule

module simple_counter_top (
    clk,
    reset,
    enable,
    counter
);

input clk;
input reset;
input enable;
output reg [7:0] counter;
initial counter = 0;

always @(posedge clk) begin
    if (reset) begin
        counter <= 0;
    end
    else if (enable) begin
        counter <= counter + 1;
    end
    else begin
        counter <= counter;
    end
end
endmodule
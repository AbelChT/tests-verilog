#include <stdlib.h>
#include <iostream>
#include <memory>
#include <verilated.h>
#include <verilated_vcd_c.h>
#include "Vsimple_counter_top.h"

int main(int argc, char** argv, char** env) {
    // 40 ps simuation
    static constexpr vluint64_t max_simulation_time = 40;

    // DUT
    auto dut = std::make_unique<Vsimple_counter_top>();

    // Enable wave trace
    Verilated::traceEverOn(true);
    auto wave_trace = std::make_unique<VerilatedVcdC>();
    dut->trace(wave_trace.get(), 2);
    static constexpr auto wavetrace_path = "waveform.vcd";
    wave_trace->open(wavetrace_path);

    // Initial state
    dut->reset = 0;
    dut->enable = 1;

    for (vluint64_t simulation_time = 0; simulation_time < max_simulation_time; simulation_time++) {
        // Clock cycle of 2ps
        dut->clk = !dut->clk;

        // Simulation specification
        switch (simulation_time)
        {
        case 16:
            // 16 ps reset
            dut->reset = 1;
            break;

        case 20:
            // 20 ps stop reset 
            dut->reset = 0;
            break;
        
        case 26:
            // 26 ps disable count
            dut->enable = 0;
            break;

        case 34:
            // 34 ps enable count
            dut->enable = 1;
            break;
        }


        // Evaluate model
        dut->eval();

        // Dump trace
        wave_trace->dump(simulation_time);
    }

    wave_trace->close();
    return 0;
}
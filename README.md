# Set of simple designs in Verilog
## Requisites
Have installed verilator, gtkwave and python3 (>3.7):

```bash
sudo apt install verilator
sudo apt install gtkwave
sudo apt install python3
```

## Build tool
For building the different designs we will use the script "script/build.py".  
This script have the following options:
- "--design": Specify the design to use (e.g. simple_counter)
- "--configure": Compile the design using verilog into the out/obj_dir directory. It will generate the headers of the design.
- "--build": Compile the design and the testbench using verilog into the out/obj_dir directory
- "--execute": Run the design to generate the waveform

## Designs

### 8 bits simple counter
Sources located in designs/simple_counter.

To execute and generate the waveform run:
```bash
./scripts/build.py --design simple_counter --build --execute
```

To visualize the waveform execute:
```bash
gtkwave out/simple_counter/waveform.vcd
```

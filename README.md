## APBRST: A Pyverilog Based RTL to Specification Translation Tool

### Author: sasasatori, Contact: 2861704773@qq.com

### Preview

APBRST is designed for helping Verilog RTL developers to generate raw specifications from Verilog codes automatically & easily, to accelerate the process of understanding and documentation codes, maybe can also translate SystemVerilog / generate raw RTL codes from specifications in the future. This tool is written in Python, based on the open-source project [**Pyverilog**](https://github.com/PyHDI/Pyverilog).

### License

Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

### Installation

*Requirements same with **Pyverilog***.

- Python3: 3.7 or later
- Icarus Verilog: 10.1 or later

```
sudo apt install iverilog
```

- Jinja2: 2.10 or later
- PLY: 3.4 or later

```
pip3 install jinja2 ply
```

*APBRST can be directly used once **Pyverilog** is installed.*

Now you can install Pyverilog using setup.py script:

```
python3 setup.py install
```

### Usage

You can now directly run APBRST with:

```
python3 verilog2spec.py ./verilog/<filename>.v
```

two example Verilog files are stored in `/verilog`, `cmsdk_ahb_gpio.v` & `fifo.v`

running results examples:

```
User@System:~/<path>/APBRST$ python3 verilog2spec.py ./verilog/cmsdk_ahb_gpio.v 
Generating LALR tables
WARNING: 183 shift/reduce conflicts

-------------------------generate module tree-------------------------

cmsdk_ahb_gpio (top)
├── u_ahb_to_gpio: cmsdk_ahb_to_iop
└── u_iop_gpio: cmsdk_iop_gpio

-------------------------generate param table-------------------------

| Parameter | Default Value | Function |
| :-------: | :-----------: | :------: |
| ALTERNATE_FUNC_MASK |    16'h0000   |          |
| ALTERNATE_FUNC_DEFAULT |    16'h0000   |          |
| BE        |       0       |          |

-------------------------generate port table-------------------------

|     Port     | Width | Direction | Function |
| :----------: | :---: | :-------: | :------: |
|     HCLK    |   1   |   Input   |          |
|   HRESETn   |   1   |   Input   |          |
|     FCLK    |   1   |   Input   |          |
|     HSEL    |   1   |   Input   |          |
|    HREADY   |   1   |   Input   |          |
|    HTRANS   |   2   |   Input   |          |
|    HSIZE    |   3   |   Input   |          |
|    HWRITE   |   1   |   Input   |          |
|    HADDR    |   12  |   Input   |          |
|    HWDATA   |   32  |   Input   |          |
|  ECOREVNUM  |   4   |   Input   |          |
|    PORTIN   |   16  |   Input   |          |
|  HREADYOUT  |   1   |   Output  |          |
|    HRESP    |   1   |   Output  |          |
|    HRDATA   |   32  |   Output  |          |
|   PORTOUT   |   16  |   Output  |          |
|    PORTEN   |   16  |   Output  |          |
|   PORTFUNC  |   16  |   Output  |          |
|   GPIOINT   |   16  |   Output  |          |
|   COMBINT   |   1   |   Output  |          |
```

```
User@System:~/<path>/APBRST$ python3 verilog2spec.py python3 verilog2spec.py ./verilog/fifo.v 
Generating LALR tables
WARNING: 183 shift/reduce conflicts

-------------------------generate module tree-------------------------

fifo (top)

-------------------------generate param table-------------------------

| Parameter | Default Value | Function |
| :-------: | :-----------: | :------: |


-------------------------generate port table-------------------------

|     Port     | Width | Direction | Function |
| :----------: | :---: | :-------: | :------: |
|     clk     |   1   |   Input   |          |
|     srst    |   1   |   Input   |          |
|    wr_en    |   1   |   Input   |          |
|    rd_en    |   1   |   Input   |          |
|     din     |   32  |   Input   |          |
|     dout    |   32  |   Output  |          |
|    empty    |   1   |   Output  |          |
|     full    |   1   |   Output  |          |
```

### Todo-list

- [x] Module tree extraction
- [x] Parameter table extraction
- [x] Port table extraction
- [ ] Detect duplicated instances declared by `generate for(;;) endgenerate` 
- [ ] Annotation detection & extraction
- [ ] Multiple files processing
- [ ] Supporting for SystemVerilog
- [ ] Generating raw RTL from spec
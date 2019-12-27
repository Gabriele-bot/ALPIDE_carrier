onbreak {quit -force}
onerror {quit -force}

asim -t 1ps +access +r +m+phase_shifter -L xil_defaultlib -L xpm -L unisims_ver -L unimacro_ver -L secureip -O5 xil_defaultlib.phase_shifter xil_defaultlib.glbl

do {wave.do}

view wave
view structure

do {phase_shifter.udo}

run -all

endsim

quit -force

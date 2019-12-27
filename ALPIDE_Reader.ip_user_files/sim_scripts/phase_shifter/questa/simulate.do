onbreak {quit -f}
onerror {quit -f}

vsim -t 1ps -lib xil_defaultlib phase_shifter_opt

do {wave.do}

view wave
view structure
view signals

do {phase_shifter.udo}

run -all

quit -force

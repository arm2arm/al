export device="/dev/sg15"
export slot="48"
export st="/dev/nst1"
mtx -f $device status
mtx -f $device unload
mtx -f $device load $slot
mt -f $st rewind

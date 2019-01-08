#!/bin/bash

COUNTER=0
while [  $COUNTER -lt 199 ]; do
t="input"
s=""
#if [ $COUNTER -lt 10 ] && [ $COUNTER -gt 0 ]
#then
#s="000"
#elif [ $COUNTER -lt 100 ] && [ $COUNTER -gt 9 ]
#then
#s="00"
#elif [ $COUNTER -lt 1000 ] && [ $COUNTER -gt 99 ]
#then
#s="0"
#else
#s=""
#fi
x=".txt"
filename=$t$COUNTER$x


rm -rf input.txt
cp ./resources/$filename .
mv $filename input.txt

mytime="$(time ( python HW3_NO_PRINT.py; ) 2>&1 1>/dev/null )"

ans=$filename" - "$mytime

mkdir outputTest

outputfile = outputTest/output$COUNTER$x
echo $ans >> outputfile

#echo $ans >> output/test_output.txt

let COUNTER=COUNTER+1
done

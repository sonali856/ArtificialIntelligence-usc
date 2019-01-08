#!/bin/bash

COUNTER=1
while [  $COUNTER -lt 500 ]; do
t="input"
s=""
if [ $COUNTER -lt 10 ] && [ $COUNTER -gt 0 ]
then
s="000"
elif [ $COUNTER -lt 100 ] && [ $COUNTER -gt 9 ]
then
s="00"
elif [ $COUNTER -lt 1000 ] && [ $COUNTER -gt 99 ]
then
s="0"
else
s=""
fi
x=".txt"
filename=$t$s$COUNTER$x

if [ $COUNTER -eq 183 ]
then
ans="Skipping - "$filename
else
rm -rf input.txt
cp ./resources/$filename .
mv $filename input.txt

mytime="$(time ( python HW2.py; ) 2>&1 1>/dev/null )"

ans=$filename" - "$mytime
fi

echo $ans >> test_outputOriginal.txt

let COUNTER=COUNTER+1
done

#!/bin/bash
for((i=2;i<255;i++));do
	ping -n 1 -w 1 10.10.1.$i > /dev/null 2>&1 && echo "10.10.1.$i is success!"
done






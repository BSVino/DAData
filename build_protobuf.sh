#!/bin/bash

protoc -I=../DoubleAction/mp/src/datanetworking/ --python_out=. ../DoubleAction/mp/src/datanetworking/data.proto
protoc -I=../DoubleAction/mp/src/datanetworking/ --python_out=. ../DoubleAction/mp/src/datanetworking/math.proto
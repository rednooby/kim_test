#!/bin/bash


for i in $(ls ../../malware); do
  python ngram.py ../../malware/$i
done

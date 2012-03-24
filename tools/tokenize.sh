#!/bin/bash

tr 'A-Z' 'a-z' < $1 | tr -cs 'a-z0-9' '\n' | sort | uniq | wc -l


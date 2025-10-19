#!/bin/bash

. "$(dirname "$0")/utils.sh"

tllme "0" "What is in this image?" "$@" < image.jpg &&
	result "LIVED"
tllme "1" image.jpg "What is in this image?" "$@" &&
	result "LIVED"
tllme "2" "What is in this image?" image.jpg "$@" &&
	result "LIVED"
tllme "3" "What is in this image? image.jpg" "$@" &&
	result "LIVED"

tllme "4" "What is in this image?" image.jpg "Is this image similar to the previous one?" image.jpg "$@" &&
	result "LIVED"

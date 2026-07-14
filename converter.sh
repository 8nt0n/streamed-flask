#!/bin/bash

shopt -s globstar nullglob

# number of CPU cores
max_jobs=4 

for input in **/*.mkv; do
    output="${input%.mkv}.mp4"
    
    # only convert the audio (-c:a aac)
    ffmpeg -y -i "$input" -c:v copy -c:a aac "$output" -nostdin -loglevel error &
    while [ $(jobs -r | wc -l) -ge "$max_jobs" ]; do
        sleep 1
    done
done

wait
echo "booom were through 🗿"

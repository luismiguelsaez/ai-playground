#!/usr/bin/env bash

MODEL="DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking"
CONTENT="What implications would have a virus like the one from The Last of Us in the real world?"
CONTENT='Hi there'

for i in {1..1}; do
  curl -s http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
          "model":"'$MODEL'",
          "messages":[
            {
              "role":"user",
              "content":"'$CONTENT'"
            }
          ],
          "max_tokens":2048
        }' &
done
wait

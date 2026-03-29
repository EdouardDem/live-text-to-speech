FROM vllm/vllm-openai:v0.18.0

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir git+https://github.com/vllm-project/vllm-omni.git

ENV MODEL_NAME=mistralai/Voxtral-4B-TTS-2603

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "vllm serve $MODEL_NAME --omni --host 0.0.0.0 --port 8000 $EXTRA_ARGS"]

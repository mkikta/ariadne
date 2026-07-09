FROM ollama/ollama:0.31.0

ARG MODEL=qwen3-embedding:0.6b
ENV MODEL=$MODEL

RUN /bin/ollama serve & \
    sleep 5 && \
    ollama pull "$MODEL" && \
    kill %1

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]

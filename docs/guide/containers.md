# Other systems with Distrobox

**Status: written for Beta 1 (Plow).**

The image includes Distrobox and Podman. Use them when a program is packaged for Ubuntu or Arch.

    distrobox create --name ubuntu --image ubuntu:24.04
    distrobox enter ubuntu

Ollama has no apt repository. Project Nomad runs the `ollama/ollama` container on `127.0.0.1:11434`. The first-boot installer pulls `llama3.2:3b`. Tags containing `-text-` are base models and produce gibberish. Do not select them. DeepSeek R1 remains available if you pull it yourself.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).

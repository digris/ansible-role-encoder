set("server.telnet",true)
set("log.syslog", true)
set("log.file.path","{{ encoder_log_dir }}/<script>.log")

s = input.alsa(device="default")



output.harbor(
    %wav(stereo=true, channels=2, samplerate=48000, samplesize=16),
    id="source_wav",
    mount="source.wav",
    port=8000,
    fallible=true,
    start=true,
    s
)

output.harbor(
    %aac(channels=2, samplerate=48000, bitrate=320),
    id="source_aac",
    mount="source.aac",
    port=8000,
    fallible=true,
    start=false,
    s
)

# clap-detection
Detects claps using Pyaudio.

Install pyaudio using:
```pip install pyaudio```
Make sure you have portaudio.

Example usage:This will print clap when a clap is heard
```python

  cp = ClapDetector()
  print('Ready')
  while True:
      try:
          cp.listen()
      except KeyboardInterrupt:
          cp.stop()
          sys.exit()
```

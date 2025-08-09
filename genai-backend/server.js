const express = require('express');
const { spawn } = require('child_process');

const app = express();
const port = 5000;

app.use(express.json());

app.post('/generate', (req, res) => {
  const prompt = req.body.prompt;

  if (typeof prompt !== 'string' || prompt.trim() === '') {
    return res.status(400).json({ error: 'Prompt must be a non-empty string' });
  }

  // 🔍 Confirm this file is being used
  console.log('🛠️ Running correct version of server.js');
  console.log(`[Prompt received] ${prompt}`);

  // ✅ Correct spawn without --prompt flag
  const ollama = spawn('ollama', ['run', 'llama2'], {
    stdio: ['pipe', 'pipe', 'pipe'],
    shell: true // 👈 Important for Windows
  });

  let result = '';
  let errorOutput = '';

  // 🔁 Timeout after 30s
  const timeout = setTimeout(() => {
    ollama.kill('SIGTERM');
    console.error('[Timeout] Ollama process killed after 30s');
    return res.status(504).json({ error: 'Ollama timed out after 30 seconds' });
  }, 30000);

  // 📥 Output from Ollama
  ollama.stdout.on('data', (data) => {
    result += data.toString();
  });

  // 📤 Error output
  ollama.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  // ✅ Done
  ollama.on('close', (code) => {
    clearTimeout(timeout);

    if (code !== 0) {
      console.error(`[Error] Code ${code}: ${errorOutput}`);
      return res.status(500).json({ error: errorOutput.trim() });
    }

    res.json({ response: result.trim() });
  });

  // ✅ Send prompt via stdin
  ollama.stdin.write(`${prompt}\n`);
  ollama.stdin.end();
});

app.listen(port, () => {
  console.log(`🚀 Server running at http://localhost:${port}`);
});

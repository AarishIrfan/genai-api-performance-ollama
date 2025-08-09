const express = require('express');
const router = express.Router();

router.post('/generate', (req, res) => {
  const { spawn } = require('child_process');
  const prompt = req.body.prompt;

  if (typeof prompt !== 'string' || prompt.trim() === '') {
    return res.status(400).json({ error: 'Prompt must be a non-empty string' });
  }

  console.log(`[Prompt received] ${prompt}`);

  const ollama = spawn('ollama', ['run', 'llama2'], {
    stdio: ['pipe', 'pipe', 'pipe'],
    shell: true
  });

  let result = '';
  let errorOutput = '';

  const timeout = setTimeout(() => {
    ollama.kill('SIGTERM');
    console.error('[Timeout] Ollama process killed after 30s');
    return res.status(504).json({ error: 'Ollama timed out after 30 seconds' });
  }, 30000);

  ollama.stdout.on('data', (data) => {
    result += data.toString();
  });

  ollama.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  ollama.on('close', (code) => {
    clearTimeout(timeout);

    if (code !== 0) {
      console.error(`[Error] Code ${code}: ${errorOutput}`);
      return res.status(500).json({ error: errorOutput.trim() });
    }

    res.json({ response: result.trim() });
  });

  ollama.stdin.write(`${prompt}\n`);
  ollama.stdin.end();
});

module.exports = router;

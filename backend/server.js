const express = require('express');
const cors = require('cors');
const ollamaRoutes = require('./routes/ollama');
const healthRoutes = require('./routes/health');
const requestLogger = require('./middleware/logging');

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(requestLogger);

// Routes
app.use('/api/ollama', ollamaRoutes);
app.use('/health', healthRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

app.listen(port, () => {
  console.log(`🚀 Server running at http://localhost:${port}`);
});

const { createServer } = require('@smithery/jina-ai-mcp-server');

// Get the API key from environment variables or use the one from .env
const apiKey = process.env.JINA_MCP_API_KEY || 'jina_065c1b3fd3d340c7a8cbaa610fc36a0aF4sgZ7Ar1TeBkyoPQGnHuEZNainP';

// Create and start the server
const server = createServer({
  apiKey,
  port: 8080,
  host: '0.0.0.0'
});

server.start().then(() => {
  console.log('MCP Server is running on port 8080');
}).catch(err => {
  console.error('Failed to start MCP Server:', err);
}); 
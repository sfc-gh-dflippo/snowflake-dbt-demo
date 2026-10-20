import { createServer } from 'node:http';

// Serve only named in-memory fixtures. Never expose a directory or accept writes.
export async function startLocalServer(resources) {
  const routes = new Map();
  for (const [route, resource] of Object.entries(resources)) {
    if (!/^\/[A-Za-z0-9._/-]*$/.test(route) || route.split('/').includes('..')) {
      throw new Error(`Invalid fixture route: ${route}`);
    }
    routes.set(route, {
      body: Buffer.from(resource.body),
      contentType: resource.contentType ?? 'text/html; charset=utf-8',
    });
  }

  let origin;
  let host;
  const server = createServer((request, response) => {
    response.setHeader('Cache-Control', 'no-store');
    response.setHeader('X-Content-Type-Options', 'nosniff');
    response.setHeader('Referrer-Policy', 'no-referrer');
    if (request.headers.host !== host
        || (request.headers.origin && request.headers.origin !== origin)) {
      response.writeHead(403).end();
      return;
    }
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      response.writeHead(405, { Allow: 'GET, HEAD' }).end();
      return;
    }
    const resource = routes.get(request.url);
    if (!resource) {
      response.writeHead(404).end();
      return;
    }
    response.writeHead(200, {
      'Content-Type': resource.contentType,
      'Content-Length': resource.body.length,
    });
    response.end(request.method === 'HEAD' ? undefined : resource.body);
  });
  server.requestTimeout = 5_000;
  server.headersTimeout = 5_000;
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      server.removeListener('error', reject);
      resolve();
    });
  });
  host = `127.0.0.1:${server.address().port}`;
  origin = `http://${host}`;

  return {
    origin,
    async close() {
      await new Promise((resolve, reject) => {
        server.close((error) => error ? reject(error) : resolve());
        server.closeAllConnections();
      });
    },
  };
}

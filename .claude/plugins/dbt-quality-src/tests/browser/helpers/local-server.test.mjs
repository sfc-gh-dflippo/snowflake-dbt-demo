import assert from 'node:assert/strict';
import { request } from 'node:http';
import test from 'node:test';
import { startLocalServer } from './local-server.mjs';

async function send(origin, path, options = {}) {
  return new Promise((resolve, reject) => {
    const call = request(origin, { path, ...options }, (response) => {
      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => resolve({
        status: response.statusCode,
        headers: response.headers,
        body: Buffer.concat(chunks).toString('utf8'),
      }));
    });
    call.on('error', reject);
    call.end();
  });
}

test('serves only exact fixture routes on loopback', async (context) => {
  const server = await startLocalServer({ '/report.html': { body: 'synthetic report' } });
  context.after(() => server.close());
  assert.equal(new URL(server.origin).hostname, '127.0.0.1');

  const response = await send(server.origin, '/report.html');
  assert.equal(response.status, 200);
  assert.equal(response.body, 'synthetic report');
  assert.equal(response.headers['content-type'], 'text/html; charset=utf-8');
  assert.equal(response.headers['cache-control'], 'no-store');
  assert.equal(response.headers['x-content-type-options'], 'nosniff');
  assert.equal(response.headers['referrer-policy'], 'no-referrer');

  const head = await send(server.origin, '/report.html', { method: 'HEAD' });
  assert.equal(head.status, 200);
  assert.equal(head.body, '');
  assert.equal(head.headers['content-length'], String(Buffer.byteLength(response.body)));

  for (const path of ['/', '/report.html?file=private', '/../package.json', '/%2e%2e/package.json']) {
    assert.equal((await send(server.origin, path)).status, 404, path);
  }
});

test('rejects writes and foreign hosts or origins', async (context) => {
  const server = await startLocalServer({ '/report.html': { body: 'synthetic report' } });
  context.after(() => server.close());
  for (const method of ['POST', 'PUT', 'DELETE', 'OPTIONS']) {
    assert.equal((await send(server.origin, '/report.html', { method })).status, 405, method);
  }
  assert.equal((await send(server.origin, '/report.html', {
    headers: { Host: 'foreign.invalid' },
  })).status, 403);
  assert.equal((await send(server.origin, '/report.html', {
    headers: { Origin: 'https://foreign.invalid' },
  })).status, 403);
});

test('copies fixture bytes before serving them', async (context) => {
  const body = Buffer.from('original');
  const server = await startLocalServer({ '/report.html': { body } });
  context.after(() => server.close());
  body.fill(0);
  assert.equal((await send(server.origin, '/report.html')).body, 'original');
});

test('rejects unsafe route names before opening a socket', async () => {
  for (const route of ['../private', '/../../private', '/report.html?data=value', '//foreign?']) {
    await assert.rejects(startLocalServer({ [route]: { body: 'unused' } }), /Invalid fixture route/);
  }
});

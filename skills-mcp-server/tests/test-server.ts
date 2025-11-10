#!/usr/bin/env tsx
/**
 * TypeScript Tests for Skills MCP Server
 * 
 * Tests the TypeScript MCP server implementation:
 * - Resource listing and metadata
 * - Resource content retrieval
 * - Prompts
 * - Tool execution
 */

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let testsRun = 0;
let testsPassed = 0;
let testsFailed = 0;

function assert(condition: boolean, message: string) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

async function test(name: string, fn: () => Promise<void>) {
  testsRun++;
  try {
    await fn();
    testsPassed++;
    console.log(`  ✅ ${name}`);
  } catch (error: any) {
    testsFailed++;
    console.log(`  ❌ ${name}`);
    console.log(`     Error: ${error.message}`);
  }
}

async function runTests() {
  console.log('\n🧪 Testing Skills MCP Server (TypeScript)\n');
  console.log('='.repeat(70));

  const transport = new StdioClientTransport({
    command: 'node',
    args: [path.join(__dirname, '..', 'dist', 'index.js')],
  });

  const client = new Client({
    name: 'test-client',
    version: '1.0.0',
  }, {
    capabilities: {},
  });

  await client.connect(transport);
  console.log('✅ Connected to MCP server\n');

  // Test 1: Resource Listing
  console.log('📋 Test Suite 1: Resource Listing');
  console.log('-'.repeat(70));

  await test('Server exposes exactly 3 resources', async () => {
    const resources = await client.listResources();
    assert(resources.resources.length === 3, `Expected 3 resources, got ${resources.resources.length}`);
  });

  await test('All expected resource URIs are present', async () => {
    const resources = await client.listResources();
    const uris = resources.resources.map(r => r.uri);
    assert(uris.includes('script://sync-skills.py'), 'Missing Python script URI');
    assert(uris.includes('script://sync-skills.ts'), 'Missing TypeScript script URI');
    assert(uris.includes('doc://manage-repositories'), 'Missing manage-repositories doc URI');
  });

  await test('Python script has correct metadata', async () => {
    const resources = await client.listResources();
    const pyResource = resources.resources.find(r => r.uri === 'script://sync-skills.py');
    assert(!!pyResource, 'Python resource not found');
    assert(pyResource!.name === 'Skills Sync Script (Python)', 'Wrong name');
    assert(pyResource!.mimeType === 'text/x-python', 'Wrong MIME type');
    assert(pyResource!.description.includes('python3 sync-skills.py'), 'Missing execution command');
  });

  await test('TypeScript script has correct metadata', async () => {
    const resources = await client.listResources();
    const tsResource = resources.resources.find(r => r.uri === 'script://sync-skills.ts');
    assert(!!tsResource, 'TypeScript resource not found');
    assert(tsResource!.name === 'Skills Sync Script (TypeScript)', 'Wrong name');
    assert(tsResource!.mimeType === 'application/typescript', 'Wrong MIME type');
    assert(tsResource!.description.includes('tsx sync-skills.ts'), 'Missing execution command');
  });

  // Test 2: Resource Reading
  console.log('\n📥 Test Suite 2: Resource Reading');
  console.log('-'.repeat(70));

  await test('Python script content is retrievable', async () => {
    const result = await client.readResource({ uri: 'script://sync-skills.py' });
    assert(result.contents.length === 1, 'Expected 1 content item');
    const content = result.contents[0];
    assert('text' in content, 'Content should have text property');
    assert(content.text!.startsWith('#!/usr/bin/env python3'), 'Missing Python shebang');
    assert(content.text!.includes('def main():'), 'Missing main function');
  });

  await test('TypeScript script content is retrievable', async () => {
    const result = await client.readResource({ uri: 'script://sync-skills.ts' });
    assert(result.contents.length === 1, 'Expected 1 content item');
    const content = result.contents[0];
    assert('text' in content, 'Content should have text property');
    assert(content.text!.startsWith('#!/usr/bin/env node'), 'Missing Node shebang');
    assert(content.text!.includes('function main()'), 'Missing main function');
  });

  await test('Documentation content is retrievable', async () => {
    const result = await client.readResource({ uri: 'doc://manage-repositories' });
    assert(result.contents.length === 1, 'Expected 1 content item');
    const content = result.contents[0];
    assert('text' in content, 'Content should have text property');
    assert(content.text!.includes('Add a Repository'), 'Missing add instructions');
    assert(content.text!.includes('Remove a Repository'), 'Missing remove instructions');
  });

  // Test 3: Prompts
  console.log('\n💬 Test Suite 3: Prompts');
  console.log('-'.repeat(70));

  await test('Server exposes exactly 2 prompts', async () => {
    const prompts = await client.listPrompts();
    assert(prompts.prompts.length === 2, `Expected 2 prompts, got ${prompts.prompts.length}`);
  });

  await test('sync-skills prompt is available', async () => {
    const prompts = await client.listPrompts();
    const syncPrompt = prompts.prompts.find(p => p.name === 'sync-skills');
    assert(!!syncPrompt, 'sync-skills prompt not found');
    assert(syncPrompt!.description.includes('sync'), 'Wrong description');
  });

  await test('manage-repositories prompt is available', async () => {
    const prompts = await client.listPrompts();
    const managePrompt = prompts.prompts.find(p => p.name === 'manage-repositories');
    assert(!!managePrompt, 'manage-repositories prompt not found');
    assert(managePrompt!.description.includes('repositories'), 'Wrong description');
  });

  await test('sync-skills prompt returns instructions', async () => {
    const result = await client.getPrompt({ name: 'sync-skills' });
    assert(result.messages.length > 0, 'Expected at least 1 message');
    const message = result.messages[0];
    assert('content' in message, 'Message should have content');
    const content = message.content;
    assert('text' in content, 'Content should have text');
    assert(content.text.includes('Step 1'), 'Missing step-by-step instructions');
  });

  // Test 4: Tools
  console.log('\n🔧 Test Suite 4: Tools');
  console.log('-'.repeat(70));

  await test('Server exposes exactly 1 tool', async () => {
    const tools = await client.listTools();
    assert(tools.tools.length === 1, `Expected 1 tool, got ${tools.tools.length}`);
  });

  await test('get_sync_instructions tool is available', async () => {
    const tools = await client.listTools();
    const tool = tools.tools.find(t => t.name === 'get_sync_instructions');
    assert(!!tool, 'get_sync_instructions tool not found');
    assert(tool!.description.includes('sync'), 'Wrong description');
  });

  await test('get_sync_instructions tool returns instructions', async () => {
    const result = await client.callTool({
      name: 'get_sync_instructions',
      arguments: {},
    });
    assert(result.content.length > 0, 'Expected content');
    const content = result.content[0];
    assert('text' in content, 'Content should have text');
    assert(content.text.includes('Step 1'), 'Missing step-by-step instructions');
  });

  // Test 5: Server Info
  console.log('\n📊 Test Suite 5: Server Info');
  console.log('-'.repeat(70));

  await test('Server initializes successfully', async () => {
    // Just verify we can connect and the server responds
    const resources = await client.listResources();
    assert(resources.resources.length > 0, 'Server should expose resources');
  });

  await test('Server capabilities include resources, prompts, and tools', async () => {
    const serverInfo = (client as any)._serverCapabilities;
    assert('resources' in serverInfo, 'Missing resources capability');
    assert('prompts' in serverInfo, 'Missing prompts capability');
    assert('tools' in serverInfo, 'Missing tools capability');
  });

  await client.close();

  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('📊 Test Summary\n');
  console.log(`  Total:  ${testsRun}`);
  console.log(`  ✅ Passed: ${testsPassed}`);
  console.log(`  ❌ Failed: ${testsFailed}`);
  console.log();

  if (testsFailed > 0) {
    console.log('❌ Some tests failed!\n');
    process.exit(1);
  } else {
    console.log('✅ All tests passed!\n');
    process.exit(0);
  }
}

runTests().catch((error) => {
  console.error('\n💥 Test runner failed:', error);
  process.exit(1);
});


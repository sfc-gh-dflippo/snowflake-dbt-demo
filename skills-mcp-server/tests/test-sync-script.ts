#!/usr/bin/env tsx
/**
 * Tests for TypeScript sync-skills.ts script
 * 
 * Tests the TypeScript implementation directly:
 * - Script syntax and structure
 * - Required functions exist
 * - Script can be compiled
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

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

async function test(name: string, fn: () => void | Promise<void>) {
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
  console.log('\n🧪 Testing TypeScript sync-skills.ts Script\n');
  console.log('='.repeat(70));

  const syncScriptPath = path.join(__dirname, '..', 'src', 'resources', 'sync-skills.ts');
  
  // Verify script exists
  if (!fs.existsSync(syncScriptPath)) {
    console.error(`❌ Script not found: ${syncScriptPath}`);
    process.exit(1);
  }

  const scriptContent = fs.readFileSync(syncScriptPath, 'utf-8');

  // Test Suite 1: Script Structure
  console.log('📋 Test Suite 1: Script Structure');
  console.log('-'.repeat(70));

  await test('Script has valid TypeScript syntax', () => {
    try {
      execSync(`npx tsc --noEmit --skipLibCheck "${syncScriptPath}"`, {
        cwd: path.join(__dirname, '..'),
        stdio: 'pipe',
      });
    } catch (error: any) {
      throw new Error(`TypeScript compilation failed: ${error.stderr?.toString() || error.message}`);
    }
  });

  await test('Script has proper shebang line', () => {
    const firstLine = scriptContent.split('\n')[0];
    assert(firstLine.startsWith('#!/usr/bin/env node'), 'Script should start with node shebang');
  });

  await test('Script has required functions', () => {
    const requiredFunctions = [
      'readRepoList',
      'scanAllSkills',
      'updateAgentsMd',
      'main',
    ];

    for (const func of requiredFunctions) {
      assert(
        scriptContent.includes(`function ${func}(`),
        `Missing required function: ${func}`
      );
    }
  });

  await test('Script has proper imports', () => {
    const requiredImports = [
      "import * as fs from 'fs'",
      "import * as path from 'path'",
      "import * as child_process from 'child_process'",
    ];

    for (const imp of requiredImports) {
      assert(scriptContent.includes(imp), `Missing import: ${imp}`);
    }
  });

  await test('Script size is reasonable', () => {
    const size = scriptContent.length;
    assert(size > 9000 && size < 13000, `Script size ${size} bytes seems unusual (expected ~10-11KB)`);
  });

  // Test Suite 2: Script Content
  console.log('\n📄 Test Suite 2: Script Content');
  console.log('-'.repeat(70));

  await test('Script has configuration constants', () => {
    assert(scriptContent.includes('SCRIPT_DIR'), 'Missing SCRIPT_DIR constant');
    assert(scriptContent.includes('SKILLS_DIR'), 'Missing SKILLS_DIR constant');
    assert(scriptContent.includes('CONFIG_FILE'), 'Missing CONFIG_FILE constant');
    assert(scriptContent.includes('AGENTS_MD'), 'Missing AGENTS_MD constant');
  });

  await test('Script has proper error handling', () => {
    assert(scriptContent.includes('try'), 'Script should have try-catch blocks');
    assert(scriptContent.includes('catch'), 'Script should have try-catch blocks');
  });

  await test('Script has main execution block', () => {
    assert(scriptContent.includes('main()'), 'Script should call main()');
  });

  await test('Script handles frontmatter parsing', () => {
    assert(
      scriptContent.includes('frontmatter') || scriptContent.includes('parseFrontmatter'),
      'Script should handle frontmatter parsing'
    );
  });

  // Test Suite 3: Script Compilation
  console.log('\n🔨 Test Suite 3: Script Compilation');
  console.log('-'.repeat(70));

  await test('Script compiles to JavaScript', () => {
    try {
      const tempDir = path.join(__dirname, '.test-compile');
      if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir);
      }

      execSync(
        `npx tsc "${syncScriptPath}" --outDir "${tempDir}" --skipLibCheck`,
        {
          cwd: path.join(__dirname, '..'),
          stdio: 'pipe',
        }
      );

      const compiledFile = path.join(tempDir, 'sync-skills.js');
      assert(fs.existsSync(compiledFile), 'Compiled file should exist');

      // Cleanup
      fs.rmSync(tempDir, { recursive: true });
    } catch (error: any) {
      throw new Error(`Compilation failed: ${error.stderr?.toString() || error.message}`);
    }
  });

  await test('Compiled script has valid JavaScript', () => {
    try {
      const tempDir = path.join(__dirname, '.test-compile');
      if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir);
      }

      execSync(
        `npx tsc "${syncScriptPath}" --outDir "${tempDir}" --skipLibCheck`,
        {
          cwd: path.join(__dirname, '..'),
          stdio: 'pipe',
        }
      );

      const compiledFile = path.join(tempDir, 'sync-skills.js');
      const compiledContent = fs.readFileSync(compiledFile, 'utf-8');
      
      // Check for valid JavaScript patterns
      assert(compiledContent.includes('function'), 'Compiled code should have functions');
      assert(compiledContent.includes('exports') || compiledContent.includes('export'), 'Compiled code should have exports');

      // Cleanup
      fs.rmSync(tempDir, { recursive: true });
    } catch (error: any) {
      throw new Error(`JavaScript validation failed: ${error.message}`);
    }
  });

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


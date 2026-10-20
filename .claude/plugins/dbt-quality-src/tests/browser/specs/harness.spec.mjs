import { readFile } from 'node:fs/promises';
import { test, expect } from '@playwright/test';
import { startLocalServer } from '../helpers/local-server.mjs';

const fixtureUrl = new URL('../fixtures/sanity.html', import.meta.url);
const fixture = await readFile(fixtureUrl);

// These tests prove the browser harness works. Product report tests belong in a separate spec.
for (const scheme of ['file', 'http']) {
  for (const colorScheme of ['light', 'dark']) {
    test(`synthetic page works over ${scheme} in ${colorScheme} mode`, async ({ page }) => {
      const server = scheme === 'http'
        ? await startLocalServer({ '/sanity.html': { body: fixture } })
        : undefined;
      const url = server ? `${server.origin}/sanity.html` : fixtureUrl.href;
      const unexpectedRequests = [];
      const pageErrors = [];
      page.on('pageerror', (error) => pageErrors.push(error.message));
      await page.route('**/*', async (route) => {
        const target = route.request().url();
        if (target === url) {
          await route.continue();
        } else {
          unexpectedRequests.push(target);
          await route.abort();
        }
      });
      try {
        await page.setViewportSize({ width: 360, height: 800 });
        await page.emulateMedia({ colorScheme, reducedMotion: 'reduce' });
        await page.goto(url);
        await expect(page.getByRole('heading', { name: 'Browser harness sanity check' })).toBeVisible();
        await expect(page.getByRole('status')).toHaveText('Ready');
        await page.keyboard.press('Tab');
        await expect(page.getByRole('button', { name: 'Run check' })).toBeFocused();
        await page.keyboard.press('Enter');
        await expect(page.getByRole('status')).toHaveText('Check complete');
        await expect(page.locator('body')).toHaveCSS(
          'background-color', colorScheme === 'dark' ? 'rgb(20, 27, 38)' : 'rgb(255, 255, 255)',
        );
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
        expect(unexpectedRequests).toEqual([]);
        expect(pageErrors).toEqual([]);
      } finally {
        await server?.close();
      }
    });
  }
}

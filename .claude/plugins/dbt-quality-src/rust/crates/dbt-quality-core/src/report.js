(() => {
  'use strict';
  const byId = id => document.getElementById(id);
  const report = JSON.parse(byId('report-data').textContent);
  const findings = report.suggestions || [];
  const contract = report.html || {};
  const models = contract.models || {};
  const rules = report.rules || {};
  // Show category names, not three-letter codes.
  const categoryNames = Object.fromEntries(((report.summary || {}).categories || []).map(category => [category.category, category.label]));
  const categoryName = code => categoryNames[code] || code;
  const limit = 262144;
  const pageSize = 50;
  const dialog = byId('finding-dialog');
  const sourceView = byId('source-view');
  const editor = byId('source-editor');
  let page = 0;
  let focusReturn = null;
  let selectedFinding = null;
  let selectedModel = null;
  let selectedLine = 0;
  let loaded = null;
  let dirty = false;
  let requestVersion = 0;
  let sourceStart = 0;
  let chart = null;
  const make = (tag, text, className) => {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = String(text);
    if (className) element.className = className;
    return element;
  };
  const badge = (kind, value) => make('span', value || 'unknown', `badge ${kind}-${String(value).replace(/[^a-z]/g, '')}`);
  const setText = (id, value) => { byId(id).textContent = value || ''; };
  const safeLink = value => {
    try {
      if (/[\s\u0000-\u001f\u007f\\]/u.test(value) || /%(?![\da-f]{2})/iu.test(value)) return null;
      const parsed = new URL(value);
      return parsed.protocol === 'https:' && parsed.hostname && !parsed.username && !parsed.password ? parsed.href : null;
    } catch (_) { return null; }
  };
  const status = message => setText('action-status', message);
  const confirmDiscard = () => !dirty || window.confirm('Discard this edited copy? The original project file has not changed.');
  const encodeSource = (text, bom) => new TextEncoder().encode((bom ? '\ufeff' : '') + text);
  // Textareas normalize all newline forms; keep original bytes separately.
  const normalized = text => text.replace(/\r\n|\r/g, '\n');
  const currentText = () => {
    if (!loaded) return '';
    if (!dirty) return loaded.text;
    return loaded.newline === 'crlf' ? editor.value.replace(/\r?\n/g, '\r\n') : editor.value;
  };
  const bytesForDownload = () => encodeSource(currentText(), loaded.bom);
  const newlineInfo = text => {
    const crlf = (text.match(/\r\n/g) || []).length;
    const lf = (text.match(/\n/g) || []).length - crlf;
    const cr = (text.match(/\r/g) || []).length - crlf;
    const kinds = [crlf, lf, cr].filter(value => value > 0).length;
    return kinds > 1 ? 'mixed' : crlf ? 'crlf' : lf ? 'lf' : cr ? 'cr' : 'none';
  };
  // `current` files were read for the report, not kept by the audit; their
  // finding lines still match because nothing ran in between.
  const verifiedLine = () => loaded && ['verified', 'current'].includes(loaded.alignment) && !['mixed', 'cr'].includes(loaded.newline) && !dirty
    ? selectedLine : 0;
  function renderSource() {
    sourceView.replaceChildren();
    if (!loaded) return;
    const lines = normalized(loaded.text).split('\n');
    const line = verifiedLine();
    // Keep the DOM bounded while allowing navigation through the full model.
    const start = Math.max(0, Math.min(Math.max(0, lines.length - 1), sourceStart));
    const end = Math.min(lines.length, start + 400);
    byId('previous-lines').disabled = start === 0;
    byId('next-lines').disabled = end >= lines.length;
    byId('focus-line').disabled = !line;
    for (let index = start; index < end; index += 1) {
      const row = make('div', undefined, `code-row${line === index + 1 ? ' selected' : ''}`);
      row.append(make('span', index + 1, 'line-number'), make('span', lines[index] || ' ', 'line-text'));
      sourceView.append(row);
    }
    setText('source-window', `${lines.length} lines. Showing ${start + 1}-${end}. ${line ? 'Highlighted line matches the audit snapshot.' : 'Finding locations are unverified; no line is highlighted.'}`);
    const selected = sourceView.querySelector('.selected');
    if (selected) sourceView.scrollTop = Math.max(0, selected.offsetTop - sourceView.offsetTop - 80);
  }
  function updateEditState() {
    dirty = Boolean(loaded && editor.value !== normalized(loaded.text));
    setText('edit-state', dirty ? 'Unsaved edited copy. Findings are stale until you apply the file and run the audit again.' : 'Unchanged copy. No project file was modified.');
    byId('edit-state').classList.toggle('danger', dirty);
    byId('reset-copy').disabled = !dirty;
    const tooLarge = loaded && bytesForDownload().length > limit;
    byId('download-copy').disabled = !loaded || tooLarge;
    byId('copy-source').disabled = !loaded || tooLarge;
    if (tooLarge) status('This edited copy exceeds 256 KiB. Shorten it before copying or downloading.');
    renderSource();
  }
  function installSource(source) {
    loaded = source;
    dirty = false;
    sourceStart = Math.max(0, verifiedLine() - 100);
    editor.value = normalized(source.text);
    editor.hidden = true;
    sourceView.hidden = false;
    byId('edit-copy').disabled = !source.editable;
    byId('edit-copy').textContent = 'Edit a copy';
    byId('download-copy').disabled = false;
    byId('copy-source').disabled = false;
    byId('source-controls').hidden = false;
    byId('change-preview').hidden = true;
    setText('source-status', `${source.message} UTF-8${source.bom ? ' with BOM' : ''}; ${source.newline} line endings.`);
    updateEditState();
  }
  function selectModel(modelId, line) {
    selectedModel = modelId ? models[modelId] : null;
    selectedLine = Number(line || 0);
    for (const tab of byId('source-files').children) tab.setAttribute('aria-pressed', String(tab.dataset.file === modelId && Number(tab.dataset.line || 0) === selectedLine));
    loaded = null;
    dirty = false;
    requestVersion += 1;
    byId('model-file').value = '';
    byId('source-controls').hidden = true;
    byId('change-preview').hidden = true;
    byId('copy-fallback-box').hidden = true;
    sourceView.replaceChildren();
    editor.value = '';
    editor.hidden = true;
    sourceView.hidden = false;
    setText('source-window', '');
    setText('edit-state', '');
    setText('source-title', selectedModel ? selectedModel.path || selectedModel.file : 'Finding evidence');
    byId('choose-file').hidden = !selectedModel;
    byId('model-file-label').hidden = !selectedModel;
    status('');
    if (!selectedModel) {
      setText('source-status', 'This finding is not linked to an exact model file. Only its evidence is available.');
      return;
    }
    const source = selectedModel.source || {};
    if (typeof source.text === 'string') {
      installSource({ ...source });
    } else {
      setText('source-status', source.message || 'Model text is unavailable. Select a local file to view a copy.');
    }
  }
  function openDialog(index, trigger) {
    if (!confirmDiscard()) return;
    focusReturn = trigger || document.activeElement;
    selectedFinding = Number.isInteger(index) ? findings[index] : null;
    const finding = selectedFinding;
    const rule = finding ? rules[finding.rule_id] : null;
    setText('detail-title', finding ? `${finding.rule_id}: ${finding.title}` : 'Model source');
    setText('detail-location', finding ? `${finding.project || ''} / ${finding.file || 'Project-level finding'}${finding.line ? `:${finding.line}` : ''}` : 'Model snapshot');
    setText('detail-message', finding ? finding.message : 'View the source or edit a downloaded copy.');
    setText('detail-evidence', finding ? finding.evidence || 'No source excerpt is available.' : 'No finding selected.');
    setText('detail-rationale', rule ? rule.rationale : '');
    setText('detail-remediation', finding ? finding.remediation : 'Apply any downloaded edit yourself, then run dbt-quality again.');
    byId('detail-examples').replaceChildren();
    for (const example of rule ? rule.examples || [] : []) {
      const box = make('details');
      box.append(make('summary', example.title), make('p', 'Review the rule guidance and conditions before using this alternative.'), make('p', 'Example'), make('pre', example.bad), make('p', 'Alternative to consider'), make('pre', example.good));
      byId('detail-examples').append(box);
    }
    byId('detail-references').replaceChildren();
    for (const reference of rule ? rule.references || [] : []) {
      const item = make('li');
      const href = safeLink(reference.url);
      if (href) {
        const link = make('a', reference.title); link.href = href; link.target = '_blank'; link.rel = 'noopener noreferrer'; item.append(link);
      } else item.textContent = reference.title;
      byId('detail-references').append(item);
    }
    // A finding can refer to several files: its own file, related models, or
    // dbt_project.yml. Show one at a time with a file switcher.
    const legacy = (contract.finding_models || [])[index];
    const links = Number.isInteger(index)
      ? (contract.finding_files ? contract.finding_files[index] : legacy ? [{ id: legacy, line: finding.line }] : [])
      : [];
    const tabs = byId('source-files');
    tabs.replaceChildren();
    for (const link of links.length > 1 ? links : []) {
      const file = models[link.id];
      const tab = make('button', `${file.file.split('/').pop()}${link.line ? `:${link.line}` : ''}`, 'file-tab');
      tab.dataset.file = link.id; tab.dataset.line = link.line || '';
      tab.title = file.path || file.file;
      tab.addEventListener('click', () => { if (confirmDiscard()) selectModel(link.id, link.line); });
      tabs.append(tab);
    }
    tabs.hidden = links.length < 2;
    selectModel(links.length ? links[0].id : null, links.length ? links[0].line : 0);
    if (!dialog.open) dialog.showModal();
    byId('close-detail').focus();
  }
  function closeDialog() {
    if (!confirmDiscard()) return;
    requestVersion += 1;
    dirty = false;
    dialog.close();
    if (focusReturn && focusReturn.isConnected) focusReturn.focus();
  }
  function filterFindings() {
    const search = byId('finding-search').value.toLocaleLowerCase().trim();
    const project = byId('filter-project').value;
    const pack = byId('filter-pack').value;
    const level = byId('filter-level').value;
    const severity = byId('filter-severity').value;
    const scope = byId('filter-scope').value;
    const matched = findings.map((finding, index) => ({ finding, index })).filter(({ finding }) => {
      if (scope === 'active' && finding.suppressed || scope === 'suppressed' && !finding.suppressed) return false;
      if (project && finding.project !== project || pack && finding.category !== pack || level && finding.level !== level || severity && finding.severity !== severity) return false;
      return !search || [finding.rule_id, finding.title, finding.message, finding.file, finding.evidence, finding.project].join(' ').toLocaleLowerCase().includes(search);
    });
    const sort = byId('filter-sort').value;
    const rank = { error: 0, warning: 1, information: 2, critical: 0, high: 1, medium: 2, low: 3 };
    matched.sort((left, right) => {
      const first = left.finding[sort], second = right.finding[sort];
      const order = sort === 'level' || sort === 'severity' ? (rank[first] ?? 9) - (rank[second] ?? 9) : String(first || '').localeCompare(String(second || ''));
      return order || left.index - right.index;
    });
    return matched;
  }
  function renderFindings() {
    const matched = filterFindings();
    const pages = Math.max(1, Math.ceil(matched.length / pageSize));
    page = Math.min(page, pages - 1);
    const body = byId('finding-rows');
    body.replaceChildren();
    for (const { finding, index } of matched.slice(page * pageSize, (page + 1) * pageSize)) {
      const row = make('tr');
      const severity = make('td'); severity.append(badge('level', finding.level), badge('severity', finding.severity));
      const location = make('td', undefined, 'location'); location.append(make('strong', finding.project || 'Portfolio'), make('br'), make('code', `${finding.file || '(no file)'}${finding.line ? `:${finding.line}` : ''}`));
      const message = make('td', undefined, 'message'); message.append(make('strong', finding.rule_id), make('br'), make('span', finding.message));
      const action = make('td', undefined, 'action'); const button = make('button', 'View', 'primary view'); button.dataset.finding = index; button.setAttribute('aria-label', `View ${finding.rule_id} in ${finding.file || 'project'}`); action.append(button);
      row.append(action, severity, location, message); body.append(row);
    }
    setText('result-count', `${matched.length} matched of ${findings.length} returned findings. Active and suppressed views are separate.`);
    setText('page-count', `Page ${page + 1} of ${pages}`);
    byId('previous-page').disabled = page === 0;
    byId('next-page').disabled = page + 1 >= pages;
    byId('empty-findings').hidden = matched.length !== 0;
    byId('finding-table').hidden = matched.length === 0;
  }
  function fillFilter(id, field, label = value => value) {
    for (const value of [...new Set(findings.map(finding => finding[field]).filter(Boolean))].sort((a, b) => label(a).localeCompare(label(b)))) {
      const option = make('option', label(value)); option.value = value; byId(id).append(option);
    }
  }
  async function loadLocal(file) {
    if (!file || !selectedModel) return;
    if (!confirmDiscard()) return;
    const version = ++requestVersion;
    const model = selectedModel;
    if (!/\.(sql|py)$/i.test(file.name)) { status('Select a SQL or Python model file.'); return; }
    if (file.size > limit) { status('This file exceeds 256 KiB. It was not loaded or truncated.'); return; }
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      if (version !== requestVersion) return;
      if (bytes.length > limit) throw new Error('This file exceeds 256 KiB.');
      const text = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
      if ([...bytes].some(byte => byte < 32 && ![9, 10, 13].includes(byte) || byte === 127)) throw new Error('The file contains unsupported control bytes.');
      const bom = text.startsWith('\ufeff');
      const sourceText = bom ? text.slice(1) : text;
      let alignment = 'unverified';
      let message = 'Local file association is unverified. A browser cannot confirm the project path.';
      const expected = model.source && model.source.sha256;
      if (expected && window.crypto && crypto.subtle) {
        const digest = await crypto.subtle.digest('SHA-256', bytes);
        if (version !== requestVersion) return;
        const hash = [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
        if (hash === expected) {
          alignment = model.source.alignment === 'verified' ? 'verified' : 'stale';
          message = alignment === 'verified' ? 'Local bytes match the verified snapshot. The browser does not confirm the path.' : 'Local bytes match the snapshot, but that snapshot changed after the audit.';
        } else {
          if (!window.confirm(`These bytes differ from ${model.file}. Associate this file as an edited copy? Finding locations will be stale.`)) { status('File association cancelled.'); return; }
          alignment = 'stale'; message = 'Selected bytes differ from the audit snapshot. Finding locations are stale.';
        }
      } else if (!window.confirm(`Associate ${file.name} with ${model.file}? The browser cannot verify its path or audit bytes. Finding locations will remain unverified.`)) {
        status('File association cancelled.'); return;
      }
      const newline = newlineInfo(sourceText);
      installSource({ text: sourceText, bom, newline, alignment, message, editable: !['mixed', 'cr'].includes(newline) });
      status(newline === 'mixed' || newline === 'cr' ? 'This newline format is view-only. You can download the original bytes.' : 'Local source loaded. No project file was changed.');
    } catch (error) { status(`Could not load this source: ${error.message}. Select a valid UTF-8 model.`); }
  }
  async function copy(text) {
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('unavailable');
      await navigator.clipboard.writeText(text); status('Copied.');
    } catch (_) {
      byId('copy-fallback-box').hidden = false;
      byId('copy-fallback').value = text;
      byId('copy-fallback').focus(); byId('copy-fallback').select();
      status('Clipboard access is unavailable. Copy the selected text with your keyboard.');
    }
  }
  function changePreview() {
    if (!loaded) return;
    const original = normalized(loaded.text).split('\n');
    const edited = editor.value.split('\n');
    const result = [];
    let changed = 0;
    const compared = Math.min(Math.max(original.length, edited.length), 2000);
    for (let index = 0; index < compared; index += 1) {
      if (original[index] !== edited[index]) {
        changed += 1;
        if (result.length < 120) result.push(`Line ${index + 1}\n- ${(original[index] || '').slice(0, 500)}\n+ ${(edited[index] || '').slice(0, 500)}`);
      }
    }
    setText('change-preview', result.length ? `${changed} changed line positions in the first ${compared} lines. This is a bounded line comparison, not a patch.\n\n${result.join('\n\n')}` : 'No differences in the compared lines.');
    byId('change-preview').hidden = false;
  }
  function drawChart() {
    if (!window.Chart) return;
    try {
      const colorProbe = make('span');
      colorProbe.hidden = true;
      document.body.append(colorProbe);
      const color = name => { colorProbe.style.color = `var(${name})`; return getComputedStyle(colorProbe).color; };
      const colors = { blue: color('--blue'), fg: color('--fg'), muted: color('--muted'), line: color('--line') };
      colorProbe.remove();
      const categories = (report.summary || {}).categories || [];
      if (chart) chart.destroy();
      byId('chart-box').hidden = false;
      chart = new Chart(byId('category-chart'), {
        type: 'bar',
        data: { labels: categories.map(category => category.label || category.category), datasets: [{ label: 'Active findings (all audit)', data: categories.map(category => category.total), backgroundColor: colors.blue }] },
        options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: colors.fg }, grid: { display: false } }, y: { beginAtZero: true, ticks: { color: colors.muted, precision: 0 }, grid: { color: colors.line } } } }
      });
      setText('chart-status', 'Chart shows all-audit active findings. The table below contains the same values.');
    } catch (_) { byId('chart-box').hidden = true; setText('chart-status', 'Chart unavailable. Use the category table below.'); }
  }
  fillFilter('filter-project', 'project'); fillFilter('filter-pack', 'category', categoryName);
  for (const id of ['finding-search', 'filter-project', 'filter-pack', 'filter-level', 'filter-severity', 'filter-scope', 'filter-sort']) {
    byId(id).addEventListener(id === 'finding-search' ? 'input' : 'change', () => { page = 0; renderFindings(); });
  }
  byId('reset-filters').addEventListener('click', () => {
    for (const id of ['finding-search', 'filter-project', 'filter-pack', 'filter-level', 'filter-severity']) byId(id).value = '';
    byId('filter-scope').value = 'active'; byId('filter-sort').value = 'level'; page = 0; renderFindings();
  });
  byId('previous-page').addEventListener('click', () => { page -= 1; renderFindings(); });
  byId('next-page').addEventListener('click', () => { page += 1; renderFindings(); });
  document.addEventListener('click', event => {
    const findingButton = event.target.closest('[data-finding]');
    if (findingButton) openDialog(Number(findingButton.dataset.finding), findingButton);
  });
  byId('previous-lines').addEventListener('click', () => { sourceStart = Math.max(0, sourceStart - 400); renderSource(); });
  byId('next-lines').addEventListener('click', () => { sourceStart += 400; renderSource(); });
  byId('focus-line').addEventListener('click', () => { sourceStart = Math.max(0, verifiedLine() - 100); renderSource(); sourceView.focus(); });
  byId('close-detail').addEventListener('click', closeDialog);
  dialog.addEventListener('cancel', event => { event.preventDefault(); closeDialog(); });
  byId('copy-path').addEventListener('click', () => copy(selectedModel ? selectedModel.path || selectedModel.file : selectedFinding ? selectedFinding.file : ''));
  byId('copy-source').addEventListener('click', () => { if (loaded && bytesForDownload().length <= limit) copy(currentText()); });
  byId('edit-copy').addEventListener('click', () => {
    if (!loaded || !loaded.editable) return;
    editor.hidden = !editor.hidden; sourceView.hidden = !editor.hidden;
    byId('edit-copy').textContent = editor.hidden ? 'Edit a copy' : 'View original';
    if (!editor.hidden) editor.focus();
  });
  editor.addEventListener('input', updateEditState);
  byId('reset-copy').addEventListener('click', () => { if (loaded && confirmDiscard()) { editor.value = normalized(loaded.text); updateEditState(); byId('change-preview').hidden = true; } });
  byId('preview-changes').addEventListener('click', changePreview);
  byId('download-copy').addEventListener('click', () => {
    if (!loaded) return;
    const bytes = bytesForDownload();
    if (bytes.length > limit) { status('This edited copy exceeds 256 KiB.'); return; }
    const url = URL.createObjectURL(new Blob([bytes], { type: 'application/octet-stream' }));
    const link = make('a'); link.href = url;
    link.download = selectedModel.file.split('/').pop().replace(/[\u0000-\u001f\u007f\\:]/g, '_');
    document.body.append(link); link.click(); link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    status('Downloaded a copy. Apply it yourself, then run dbt-quality again. Findings remain unchanged.');
  });
  byId('model-file').addEventListener('change', event => loadLocal(event.target.files[0]));
  byId('choose-file').hidden = typeof window.showOpenFilePicker !== 'function';
  byId('choose-file').addEventListener('click', async () => {
    try {
      if (!window.showOpenFilePicker) { byId('model-file').click(); return; }
      const [handle] = await window.showOpenFilePicker({ multiple: false, types: [{ description: 'dbt model', accept: { 'text/plain': ['.sql', '.py'] } }] });
      await loadLocal(await handle.getFile());
    } catch (error) { status(error.name === 'AbortError' ? 'File selection cancelled.' : 'File access was denied or unavailable. Use the file input.'); }
  });
  const scheme = window.matchMedia('(prefers-color-scheme: dark)');
  byId('theme').addEventListener('change', () => { document.documentElement.dataset.theme = byId('theme').value; drawChart(); });
  scheme.addEventListener('change', () => { if (byId('theme').value === 'auto') drawChart(); });
  document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => {
    const target = byId(link.getAttribute('href').slice(1)); if (target && target.tagName === 'DETAILS') target.open = true;
  }));
  const externalChart = byId('chart-library');
  externalChart.addEventListener('load', drawChart);
  externalChart.addEventListener('error', () => setText('chart-status', 'Chart library unavailable or blocked. The table and source tools still work.'));
  renderFindings();
  document.documentElement.classList.add('js-ready');
  byId('script-status').hidden = true;
  drawChart();
})();

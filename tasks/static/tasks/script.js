
(() => {
  const addBtn = document.getElementById('add-task-btn');
  const clearBtn = document.getElementById('clear-form-btn');
  const loadJsonBtn = document.getElementById('load-json-btn');
  const sampleBtn = document.getElementById('sample-btn');
  const analyzeBtn = document.getElementById('analyze-btn');
  const suggestBtn = document.getElementById('suggest-btn');
  const bulkJson = document.getElementById('bulk-json');
  const resultsEl = document.getElementById('results');
  const suggestionsEl = document.getElementById('suggestions');
  const statusEl = document.getElementById('status');
  const loader = document.getElementById('loader');
  const strategyEl = document.getElementById('strategy');

  let stagedTasks = [];

  function showStatus(text, isError=false){
    statusEl.textContent = text || '';
    statusEl.style.color = isError ? '#ffb4b4' : '';
  }
  function setLoading(on){
    if(on){
      loader.classList.remove('hidden');
      analyzeBtn.disabled = true;
      suggestBtn.disabled = true;
    } else {
      loader.classList.add('hidden');
      analyzeBtn.disabled = false;
      suggestBtn.disabled = false;
    }
  }

  function priorityLabel(score){
    if(score >= 70) return {text:'High', cls:'high'};
    if(score >= 40) return {text:'Medium', cls:'medium'};
    return {text:'Low', cls:'low'};
  }

  function renderResults(tasks){
    resultsEl.innerHTML = '';
    if(!tasks || tasks.length === 0){
      resultsEl.innerHTML = '<p class="hint">No results to show. Click Analyze.</p>';
      return;
    }
    tasks.forEach(t => {
      const container = document.createElement('div');
      container.className = 'task';

      const left = document.createElement('div');
      left.className = 'left';
      const title = document.createElement('div');
      title.className = 'title';
      title.textContent = t.title || '(no title)';
      const meta = document.createElement('div');
      meta.className = 'meta';
      const due = t.due_date ? `Due: ${t.due_date}` : 'No due date';
      meta.textContent = `${due} • Effort: ${t.estimated_hours || 0}h • Importance: ${t.importance || 5}`;

      left.appendChild(title);
      left.appendChild(meta);

      const right = document.createElement('div');
      right.className = 'right';
      const scoreDiv = document.createElement('div');
      scoreDiv.className = 'score';
      scoreDiv.textContent = (typeof t.score === 'number') ? `${t.score}` : '-';

      const badgeInfo = priorityLabel(t.score || 0);
      const badge = document.createElement('div');
      badge.className = `badge ${badgeInfo.cls}`;
      badge.textContent = `${badgeInfo.text}`;

      right.appendChild(scoreDiv);
      right.appendChild(badge);

      container.appendChild(left);
      container.appendChild(right);

      // explanation
      const exp = document.createElement('div');
      exp.className = 'explanation';
      exp.textContent = t.explanation || '';

      const wrapper = document.createElement('div');
      wrapper.appendChild(container);
      wrapper.appendChild(exp);

      resultsEl.appendChild(wrapper);
    });
  }

  function renderSuggestions(suggestions){
    suggestionsEl.innerHTML = '';
    if(!suggestions || suggestions.length === 0){
      suggestionsEl.innerHTML = '<p class="hint">No suggestions available. Run Analyze first.</p>';
      return;
    }
    suggestions.forEach(s => {
      const div = document.createElement('div');
      div.className = 'suggestion';
      div.innerHTML = `<strong>${s.title}</strong> — Score: ${s.score}<div class="meta">${s.why}</div>`;
      suggestionsEl.appendChild(div);
    });
  }

  addBtn.addEventListener('click', () => {
    const title = document.getElementById('title').value.trim();
    if(!title){
      showStatus('Title is required to add a task', true);
      return;
    }
    const due_date = document.getElementById('due_date').value || null;
    const estimated_hours = parseFloat(document.getElementById('estimated_hours').value) || 1;
    let importance = parseInt(document.getElementById('importance').value, 10);
    if(!importance || importance < 1) importance = 5;
    const depsRaw = document.getElementById('dependencies').value.trim();
    const dependencies = depsRaw ? depsRaw.split(',').map(s => parseInt(s.trim(),10)).filter(n => !Number.isNaN(n)) : [];
    const tmpId = stagedTasks.length ? Math.max(...stagedTasks.map(t=>t.id||0))+1 : 1;
    const task = { id: tmpId, title, due_date, estimated_hours, importance, dependencies };
    stagedTasks.push(task);
    showStatus(`Added task: "${title}"`);
    clearForm();
    renderResults(stagedTasks.map(t => ({...t, score: 0, explanation: 'Staged (not analyzed)'})));
  });

  clearBtn.addEventListener('click', () => {
    clearForm();
    showStatus('');
  });

  function clearForm(){
    document.getElementById('title').value = '';
    document.getElementById('due_date').value = '';
    document.getElementById('estimated_hours').value = '1';
    document.getElementById('importance').value = '5';
    document.getElementById('dependencies').value = '';
  }

  // Load JSON
  loadJsonBtn.addEventListener('click', () => {
    const txt = bulkJson.value.trim();
    if(!txt){
      showStatus('Paste JSON array first', true);
      return;
    }
    let arr;
    try {
      arr = JSON.parse(txt);
      if(!Array.isArray(arr)) throw new Error('Not an array');
    } catch (err) {
      showStatus('Invalid JSON: ' + err.message, true);
      return;
    }
    stagedTasks = arr.map((t,idx) => {
      const id = (t.id !== undefined) ? t.id : (idx+1);
      return {
        id,
        title: t.title || `Task ${id}`,
        due_date: t.due_date || null,
        estimated_hours: (t.estimated_hours !== undefined) ? t.estimated_hours : 1,
        importance: (t.importance !== undefined) ? t.importance : 5,
        dependencies: Array.isArray(t.dependencies) ? t.dependencies : []
      };
    });
    showStatus(`Loaded ${stagedTasks.length} tasks from JSON`);
    renderResults(stagedTasks.map(t => ({...t, score:0, explanation: 'Loaded (not analyzed)'})));
  });

  sampleBtn.addEventListener('click', () => {
    const sample = [
      {"id":1,"title":"Fix login bug","due_date":null,"estimated_hours":3,"importance":8,"dependencies":[]},
      {"id":2,"title":"Write README","due_date":null,"estimated_hours":1,"importance":6,"dependencies":[1]},
      {"id":3,"title":"Prepare deploy","due_date":null,"estimated_hours":5,"importance":9,"dependencies":[]}
    ];
    bulkJson.value = JSON.stringify(sample, null, 2);
    showStatus('Sample JSON loaded into paste area — click "Load JSON" to use it');
  });

  async function analyze(){
    if(!stagedTasks || stagedTasks.length === 0){
      showStatus('No tasks to analyze. Add tasks or paste JSON.', true);
      return;
    }
    const strategy = strategyEl.value || 'smart_balance';
    setLoading(true);
    showStatus('Analyzing tasks...');
    try {
      const res = await fetch(`/api/tasks/analyze/?strategy=${encodeURIComponent(strategy)}`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(stagedTasks)
      });
      if(!res.ok){
        const err = await res.json().catch(()=>({detail:'Server error'}));
        showStatus('Analysis failed: ' + (err.detail || JSON.stringify(err)), true);
        setLoading(false);
        return;
      }
      const payload = await res.json();
      const tasks = payload.tasks || [];
      renderResults(tasks);
      showStatus(`Analysis complete — ${tasks.length} tasks scored.`);
    } catch (err){
      showStatus('Network or unexpected error: ' + err.message, true);
    } finally {
      setLoading(false);
    }
  }

  analyzeBtn.addEventListener('click', analyze);

  async function getSuggestions(){
    setLoading(true);
    showStatus('Fetching suggestions...');
    try {
      const res = await fetch('/api/tasks/suggest/');
      if(!res.ok){
        const err = await res.json().catch(()=>({detail:'Server error'}));
        showStatus('Failed to get suggestions: ' + (err.detail || JSON.stringify(err)), true);
        setLoading(false);
        return;
      }
      const payload = await res.json();
      const suggestions = payload.suggestions || [];
      renderSuggestions(suggestions);
      showStatus('Top suggestions loaded.');
    } catch (err){
      showStatus('Network or unexpected error: ' + err.message, true);
    } finally {
      setLoading(false);
    }
  }

  suggestBtn.addEventListener('click', getSuggestions);

  renderResults([]);
  renderSuggestions([]);
  showStatus('Ready — add tasks or paste JSON, then Analyze.');
})();

/* ============================================================
   suspects.js — C.I.D. SYSTEM v2.0
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    let allSuspects = [];
    let repeatMap = {};
    let caseCountMap = {};
    let currentFilter = 'all';
    let currentSearch = '';
    let isCardView = false;

    // ── Load Data ──
    Promise.all([
        fetch('/api/suspects').then(res => res.json()),
        fetch('/api/suspects/repeat-offenders').then(res => res.json())
    ])
    .then(([suspects, repeatOffenders]) => {
        if (suspects.error) throw new Error(suspects.error);

        allSuspects = suspects || [];

        // Build repeat offender map
        if (repeatOffenders && !repeatOffenders.error) {
            repeatOffenders.forEach(ro => {
                repeatMap[ro.suspect_id] = true;
                caseCountMap[ro.suspect_id] = ro.case_count;
            });
        }

        // Update stats
        const total = allSuspects.length;
        const repeatCount = Object.keys(repeatMap).length;
        const avgCases = total > 0 ? (repeatCount > 0
            ? (Object.values(caseCountMap).reduce((a, b) => a + b, 0) / repeatCount).toFixed(1)
            : '1.0') : '—';

        const totalEl = document.getElementById('susp-total');
        const repeatEl = document.getElementById('susp-repeat');
        const avgEl = document.getElementById('susp-avg');

        if (totalEl && window.animateCount) animateCount(totalEl, total, 700);
        if (repeatEl && window.animateCount) animateCount(repeatEl, repeatCount, 700);
        if (avgEl) avgEl.textContent = avgCases;

        renderView();
    })
    .catch(err => {
        console.error('Error loading suspects:', err);
        document.getElementById('suspects-tbody').innerHTML = `<tr><td colspan="7" class="table-empty">
            <span class="table-empty-icon">⚠️</span>
            Error loading suspects: ${err.message}
        </td></tr>`;
    });

    // ── Filter Data ──
    function getFiltered() {
        let data = [...allSuspects];

        if (currentFilter === 'repeat') {
            data = data.filter(s => repeatMap[s.suspect_id]);
        } else if (currentFilter === 'record') {
            data = data.filter(s => s.criminal_record && s.criminal_record.trim() !== '');
        }

        if (currentSearch) {
            const q = currentSearch.toLowerCase();
            data = data.filter(s =>
                s.name.toLowerCase().includes(q) ||
                (s.gender || '').toLowerCase().includes(q) ||
                String(s.suspect_id).includes(q)
            );
        }

        return data;
    }

    // ── Render Appropriate View ──
    function renderView() {
        if (isCardView) renderCardView();
        else renderTableView();
    }

    // ── Table View ──
    function renderTableView() {
        const tbody = document.getElementById('suspects-tbody');
        const data = getFiltered();
        const countEl = document.getElementById('suspects-count');
        if (countEl) countEl.textContent = data.length;

        tbody.innerHTML = '';

        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" class="table-empty">
                <span class="table-empty-icon">🔍</span>
                No suspects match your search.
            </td></tr>`;
            return;
        }

        data.forEach(s => {
            const isRepeat = repeatMap[s.suspect_id];
            const caseCount = caseCountMap[s.suspect_id] || 1;
            const dob = s.dob ? new Date(s.dob).toLocaleDateString('en-IN') : '—';
            const record = s.criminal_record
                ? `<span title="${s.criminal_record}">${s.criminal_record.substring(0, 45)}${s.criminal_record.length > 45 ? '…' : ''}</span>`
                : '<span style="color:var(--text-muted);">None on record</span>';

            const flags = isRepeat
                ? `<span class="badge badge-red">🚨 Repeat (${caseCount} cases)</span>`
                : '<span style="color:var(--text-muted); font-size:0.78rem;">—</span>';

            const row = document.createElement('tr');
            if (isRepeat) row.style.background = 'rgba(239,68,68,0.03)';
            row.innerHTML = `
                <td class="font-mono" style="color:var(--accent-blue);">#${s.suspect_id}</td>
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:30px; height:30px; border-radius:50%; background:${isRepeat ? 'rgba(239,68,68,0.15)' : 'var(--bg-hover)'}; 
                             border:1px solid ${isRepeat ? 'rgba(239,68,68,0.3)' : 'var(--border)'}; 
                             display:flex; align-items:center; justify-content:center; font-size:0.8rem; flex-shrink:0;">
                            ${s.name.charAt(0).toUpperCase()}
                        </div>
                        <strong style="color:var(--text-light);">${s.name}</strong>
                    </div>
                </td>
                <td style="font-size:0.85rem;">${dob}</td>
                <td style="font-size:0.85rem;">${s.gender || '—'}</td>
                <td class="truncate" style="max-width:200px;">${record}</td>
                <td style="font-family:var(--font-mono); font-size:0.82rem; color:var(--text-muted);">${caseCount}</td>
                <td>${flags}</td>
            `;
            tbody.appendChild(row);
        });
    }

    // ── Card View ──
    function renderCardView() {
        const grid = document.getElementById('suspects-grid');
        const data = getFiltered();
        const countEl = document.getElementById('suspects-count');
        if (countEl) countEl.textContent = data.length;

        grid.innerHTML = '';

        if (data.length === 0) {
            grid.innerHTML = `<div style="grid-column:1/-1; text-align:center; color:var(--text-muted); padding:40px;">
                <div style="font-size:2rem; opacity:0.3; margin-bottom:12px;">🔍</div>
                No suspects match your search.
            </div>`;
            return;
        }

        data.forEach(s => {
            const isRepeat = repeatMap[s.suspect_id];
            const caseCount = caseCountMap[s.suspect_id] || 1;
            const dob = s.dob ? new Date(s.dob).toLocaleDateString('en-IN') : '—';

            const card = document.createElement('div');
            card.className = `suspect-card${isRepeat ? ' repeat-offender' : ''}`;
            card.innerHTML = `
                <div class="suspect-card-header">
                    <div class="suspect-avatar">${s.name.charAt(0).toUpperCase()}</div>
                    <div>
                        <div class="suspect-name">${s.name}</div>
                        <div class="suspect-id">ID #${s.suspect_id}</div>
                    </div>
                    ${isRepeat ? `<span class="badge badge-red" style="margin-left:auto;">🚨 Repeat</span>` : ''}
                </div>
                <div class="suspect-details">
                    <div class="suspect-detail-item">
                        <span class="label">Date of Birth</span>
                        <span class="value">${dob}</span>
                    </div>
                    <div class="suspect-detail-item">
                        <span class="label">Gender</span>
                        <span class="value">${s.gender || '—'}</span>
                    </div>
                    <div class="suspect-detail-item">
                        <span class="label">Cases Involved</span>
                        <span class="value" style="color:${isRepeat ? 'var(--accent-red)' : 'var(--text-main)'}; font-weight:${isRepeat ? '700' : '500'};">
                            ${caseCount}
                        </span>
                    </div>
                    <div class="suspect-detail-item">
                        <span class="label">Status</span>
                        <span class="value">${isRepeat ? '⚠️ High Risk' : '📋 Registered'}</span>
                    </div>
                </div>
                ${s.criminal_record ? `<div class="suspect-record">${s.criminal_record}</div>` : ''}
            `;
            grid.appendChild(card);
        });
    }

    // ── Search ──
    const searchInput = document.getElementById('suspect-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            currentSearch = this.value.trim().toLowerCase();
            renderView();
        });
    }

    // ── Filter Buttons ──
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            renderView();
        });
    });

    // ── Toggle View ──
    const toggleBtn = document.getElementById('btn-toggle-view');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            isCardView = !isCardView;
            const tableView = document.getElementById('table-view');
            const cardView = document.getElementById('card-view');
            if (isCardView) {
                tableView.style.display = 'none';
                cardView.style.display = 'block';
                toggleBtn.textContent = '≡ Table View';
            } else {
                tableView.style.display = 'block';
                cardView.style.display = 'none';
                toggleBtn.textContent = '⊞ Grid View';
            }
            renderView();
        });
    }
});

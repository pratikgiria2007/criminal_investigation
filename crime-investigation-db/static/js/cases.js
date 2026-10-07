/* ============================================================
   cases.js — C.I.D. SYSTEM v2.0
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    let allCases = [];
    let currentFilter = 'all';
    let currentSearch = '';
    let sortCol = 'case_id';
    let sortDir = 'desc';

    // ── Fetch Cases ──
    function loadCases() {
        fetch('/api/cases')
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    renderError(data.error);
                    return;
                }
                allCases = data || [];
                renderTable();
            })
            .catch(err => {
                console.error('Failed to load cases:', err);
                renderError('Failed to connect to server.');
            });
    }

    // ── Status Helpers ──
    function getStatusBadge(status) {
        const map = {
            'Open': 'badge-open',
            'Under Investigation': 'badge-investigation',
            'Solved': 'badge-solved',
            'Closed': 'badge-green',
            'Cold Case': 'badge-default'
        };
        const cls = map[status] || 'badge-default';
        const pulse = (status === 'Open' || status === 'Under Investigation') ? ' badge-pulse' : '';
        return `<span class="badge ${cls}${pulse}">${status}</span>`;
    }

    // ── Filter & Sort ──
    function getFiltered() {
        let data = [...allCases];

        // Filter by status
        if (currentFilter !== 'all') {
            data = data.filter(c => c.status === currentFilter);
        }

        // Filter by search query
        if (currentSearch) {
            const q = currentSearch.toLowerCase();
            data = data.filter(c =>
                c.case_title.toLowerCase().includes(q) ||
                (c.lead_officer || '').toLowerCase().includes(q) ||
                String(c.case_id).includes(q)
            );
        }

        // Sort
        data.sort((a, b) => {
            let va = a[sortCol], vb = b[sortCol];
            if (sortCol === 'case_id' || sortCol === 'suspect_count' || sortCol === 'evidence_count') {
                va = parseInt(va) || 0;
                vb = parseInt(vb) || 0;
            } else {
                va = (va || '').toString().toLowerCase();
                vb = (vb || '').toString().toLowerCase();
            }
            if (va < vb) return sortDir === 'asc' ? -1 : 1;
            if (va > vb) return sortDir === 'asc' ? 1 : -1;
            return 0;
        });

        return data;
    }

    // ── Render Table ──
    function renderTable() {
        const tbody = document.getElementById('cases-tbody');
        const data = getFiltered();
        const countEl = document.getElementById('cases-count');
        if (countEl) countEl.textContent = data.length;

        tbody.innerHTML = '';

        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" class="table-empty">
                <span class="table-empty-icon">🗂️</span>
                No cases match your search.
            </td></tr>`;
            return;
        }

        data.forEach(c => {
            const officerText = c.lead_officer || '<span style="color:var(--text-muted);">Unassigned</span>';
            const suspectCount = c.suspect_count || 0;
            const evidenceCount = c.evidence_count || 0;

            const actions = USER_ROLE === 'Official'
                ? `<div style="display:flex; gap:6px;">
                       <a href="/cases/${c.case_id}" class="btn btn-sm btn-primary">View</a>
                       <button class="btn btn-sm btn-ghost" onclick="event.stopPropagation(); openEditModal(${c.case_id}, '${(c.case_title || '').replace(/'/g, "\\'")}', '${c.status}')">✏️</button>
                   </div>`
                : `<a href="/cases/${c.case_id}" class="btn btn-sm btn-ghost">View</a>`;

            const row = document.createElement('tr');
            row.className = 'clickable-row';
            row.innerHTML = `
                <td class="font-mono" style="color:var(--accent-blue);">#${c.case_id}</td>
                <td><strong style="color:var(--text-light);">${c.case_title}</strong></td>
                <td>${getStatusBadge(c.status)}</td>
                <td style="font-size:0.85rem;">${officerText}</td>
                <td>
                    ${suspectCount > 0 
                        ? `<span style="color:var(--text-light); font-weight:600;">${suspectCount}</span>` 
                        : `<span style="color:var(--text-muted);">0</span>`}
                </td>
                <td>
                    ${evidenceCount > 0
                        ? `<span style="color:var(--accent-cyan); font-weight:600;">${evidenceCount}</span>` 
                        : `<span style="color:var(--text-muted);">0</span>`}
                </td>
                <td onclick="event.stopPropagation();">${actions}</td>
            `;
            row.addEventListener('click', () => window.location.href = `/cases/${c.case_id}`);
            tbody.appendChild(row);
        });
    }

    function renderError(msg) {
        const tbody = document.getElementById('cases-tbody');
        tbody.innerHTML = `<tr><td colspan="7" class="table-empty">
            <span class="table-empty-icon">⚠️</span>
            Error: ${msg}
        </td></tr>`;
    }

    // ── Search ──
    const searchInput = document.getElementById('case-search');
    if (searchInput) {
        // Pre-fill from URL query
        const urlParams = new URLSearchParams(window.location.search);
        const qParam = urlParams.get('q');
        if (qParam) {
            searchInput.value = qParam;
            currentSearch = qParam;
        }

        searchInput.addEventListener('input', function() {
            currentSearch = this.value.trim().toLowerCase();
            renderTable();
        });
    }

    // ── Filter Buttons ──
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            renderTable();
        });
    });

    // ── Sortable Headers ──
    document.querySelectorAll('.data-table th[data-sort]').forEach(th => {
        th.addEventListener('click', function() {
            const col = this.dataset.sort;
            if (sortCol === col) {
                sortDir = sortDir === 'asc' ? 'desc' : 'asc';
            } else {
                sortCol = col;
                sortDir = 'asc';
            }
            document.querySelectorAll('.data-table th').forEach(t => {
                t.classList.remove('sort-asc', 'sort-desc');
            });
            this.classList.add(sortDir === 'asc' ? 'sort-asc' : 'sort-desc');
            renderTable();
        });
    });

    // ── Refresh Button ──
    const refreshBtn = document.getElementById('btn-refresh-cases');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            allCases = [];
            document.getElementById('cases-tbody').innerHTML = `<tr><td colspan="7" class="table-empty">Refreshing...</td></tr>`;
            loadCases();
        });
    }

    // ── New Case Modal ──
    const newCaseBtn = document.getElementById('btn-new-case');
    const modal = document.getElementById('new-case-modal');
    const closeBtn = document.getElementById('close-case-modal');
    const cancelBtn = document.getElementById('cancel-case-btn');
    const form = document.getElementById('new-case-form');

    function openNewModal() {
        modal.classList.add('active');
        document.getElementById('date_opened').valueAsDate = new Date();
        document.getElementById('case_title').focus();
    }

    function closeNewModal() {
        modal.classList.remove('active');
        form.reset();
        const errEl = document.getElementById('case-form-error');
        if (errEl) errEl.style.display = 'none';
    }

    if (newCaseBtn) newCaseBtn.addEventListener('click', openNewModal);
    if (closeBtn) closeBtn.addEventListener('click', closeNewModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeNewModal);
    if (modal) modal.addEventListener('click', e => { if (e.target === modal) closeNewModal(); });

    if (form) {
        form.addEventListener('submit', e => {
            e.preventDefault();
            const saveBtn = document.getElementById('save-case-btn');
            const errEl = document.getElementById('case-form-error');
            if (errEl) errEl.style.display = 'none';
            if (saveBtn) { saveBtn.disabled = true; saveBtn.textContent = '⏳ Saving...'; }

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            if (!data.lead_officer_id) data.lead_officer_id = null;
            else data.lead_officer_id = parseInt(data.lead_officer_id);

            fetch('/api/cases', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(resData => {
                if (saveBtn) { saveBtn.disabled = false; saveBtn.textContent = '💾 Save Case'; }
                if (resData.error) {
                    if (errEl) { errEl.textContent = 'Error: ' + resData.error; errEl.style.display = 'block'; }
                    return;
                }
                closeNewModal();
                showToast('Case created successfully! #' + resData.case_id, 'success');
                loadCases();
            })
            .catch(err => {
                if (saveBtn) { saveBtn.disabled = false; saveBtn.textContent = '💾 Save Case'; }
                if (errEl) { errEl.textContent = 'Network error. Please try again.'; errEl.style.display = 'block'; }
            });
        });
    }

    // ── Edit Case Modal ──
    window.openEditModal = function(caseId, title, status) {
        const editModal = document.getElementById('edit-case-modal');
        if (!editModal) return;
        document.getElementById('edit_case_id').value = caseId;
        document.getElementById('edit_case_title').value = title;
        document.getElementById('edit_status').value = status;
        editModal.classList.add('active');
    };

    const editModal = document.getElementById('edit-case-modal');
    const closeEditBtn = document.getElementById('close-edit-modal');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const editForm = document.getElementById('edit-case-form');

    function closeEditModal() { if (editModal) editModal.classList.remove('active'); }
    if (closeEditBtn) closeEditBtn.addEventListener('click', closeEditModal);
    if (cancelEditBtn) cancelEditBtn.addEventListener('click', closeEditModal);
    if (editModal) editModal.addEventListener('click', e => { if (e.target === editModal) closeEditModal(); });

    if (editForm) {
        editForm.addEventListener('submit', e => {
            e.preventDefault();
            const caseId = parseInt(document.getElementById('edit_case_id').value);
            const payload = {
                case_title: document.getElementById('edit_case_title').value,
                description: document.getElementById('edit_description').value,
                status: document.getElementById('edit_status').value,
                lead_officer_id: parseInt(document.getElementById('edit_lead_officer_id').value) || null
            };
            fetch(`/api/cases/${caseId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(rd => {
                if (rd.error) { showToast('Error: ' + rd.error, 'error'); return; }
                showToast('Case updated successfully', 'success');
                closeEditModal();
                loadCases();
            });
        });
    }

    // ── Initial Load ──
    loadCases();
});

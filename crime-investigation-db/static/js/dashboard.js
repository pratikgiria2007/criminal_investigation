/* ============================================================
   dashboard.js — C.I.D. SYSTEM v2.0
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ── 1. Overview Stats with Count-Up Animation ──
    fetch('/api/stats/overview')
        .then(res => res.json())
        .then(data => {
            if (data.error) return;
            const fields = {
                'stat-total-cases': data.total_cases,
                'stat-open-cases': data.open_cases,
                'stat-solved-cases': data.solved_cases,
                'stat-total-suspects': data.total_suspects,
                'stat-total-evidence': data.total_evidence
            };
            Object.entries(fields).forEach(([id, value]) => {
                const el = document.getElementById(id);
                if (el && window.animateCount) {
                    animateCount(el, parseInt(value) || 0, 900);
                } else if (el) {
                    el.textContent = value;
                }
            });

            // Solve rate for casual users
            const srEl = document.getElementById('solve-rate-pct');
            const srBar = document.getElementById('solve-rate-bar');
            if (srEl && data.total_cases > 0) {
                const pct = Math.round((data.solved_cases / data.total_cases) * 100);
                setTimeout(() => {
                    if (window.animateCount) animateCount(srEl, pct, 1000);
                    srEl.textContent = pct + '%';
                }, 300);
                if (srBar) {
                    setTimeout(() => { srBar.style.width = pct + '%'; }, 400);
                }
            }
        })
        .catch(err => console.error('Stats error:', err));

    // ── 2. No-Evidence Alerts ──
    const noEvList = document.getElementById('no-evidence-list');
    if (noEvList) {
        fetch('/api/cases/no-evidence')
            .then(res => res.json())
            .then(data => {
                noEvList.innerHTML = '';
                if (!data || data.length === 0) {
                    noEvList.innerHTML = `<li style="background:var(--accent-green-dim); border-color:var(--accent-green-border); color:var(--accent-green);">
                        <span style="margin-right:4px;">✅</span> All cases have at least one evidence item.
                    </li>`;
                } else {
                    data.forEach(item => {
                        noEvList.innerHTML += `<li>
                            <a href="/cases/${item.case_id}" style="color:inherit; text-decoration:none; flex:1;">
                                <span style="color:var(--text-muted); margin-right:4px;">#${item.case_id}</span>
                                ${item.case_title}
                            </a>
                        </li>`;
                    });
                }
            })
            .catch(err => console.error('Alerts error:', err));
    }

    // ── 3. Officer Leaderboard (list view) ──
    const leaderboardEl = document.getElementById('leaderboard-list');
    if (leaderboardEl) {
        fetch('/api/stats/officer-leaderboard')
            .then(res => res.json())
            .then(data => {
                if (!data || data.error) return;
                const maxVal = Math.max(...data.map(d => d.solved_cases), 1);
                const ranks = ['gold', 'silver', 'bronze'];
                const rankEmoji = ['🥇', '🥈', '🥉'];

                leaderboardEl.innerHTML = '';
                data.forEach((d, i) => {
                    const pct = Math.round((d.solved_cases / maxVal) * 100);
                    leaderboardEl.innerHTML += `
                        <div class="leaderboard-item">
                            <div class="leaderboard-rank ${ranks[i] || ''}">${rankEmoji[i] || (i + 1)}</div>
                            <div class="leaderboard-name">${d.name}</div>
                            <div class="leaderboard-bar-container">
                                <div class="leaderboard-bar">
                                    <div class="leaderboard-fill" style="width:${pct}%;"></div>
                                </div>
                            </div>
                            <div class="leaderboard-score">${d.solved_cases}</div>
                        </div>`;
                });
            });
    }

    // ── 4. Officer Bar Chart ──
    const officerChartEl = document.getElementById('officerChart');
    if (officerChartEl) {
        fetch('/api/stats/officer-leaderboard')
            .then(res => res.json())
            .then(data => {
                if (!data || data.error) return;
                const labels = data.map(d => d.name.split(' ')[0]); // First name only for brevity
                const values = data.map(d => d.solved_cases);

                new Chart(officerChartEl.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels,
                        datasets: [{
                            label: 'Cases Solved',
                            data: values,
                            backgroundColor: values.map((_, i) =>
                                i === 0 ? 'rgba(59,130,246,0.8)' :
                                i === 1 ? 'rgba(6,182,212,0.6)' :
                                'rgba(139,92,246,0.5)'
                            ),
                            borderColor: 'transparent',
                            borderRadius: 6,
                            borderSkipped: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: { duration: 1000, easing: 'easeOutQuart' },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: { color: '#6e7d91', font: { size: 11 } },
                                grid: { color: 'rgba(30,38,50,0.8)' }
                            },
                            x: {
                                ticks: { color: '#b8c4d0', font: { size: 11 } },
                                grid: { display: false }
                            }
                        },
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                backgroundColor: '#161b22',
                                borderColor: '#1e2632',
                                borderWidth: 1,
                                titleColor: '#e8edf2',
                                bodyColor: '#b8c4d0',
                                callbacks: {
                                    label: ctx => ` ${ctx.raw} cases solved`
                                }
                            }
                        }
                    }
                });
            });
    }

    // ── 5. Case Status Doughnut Chart ──
    const statusChartEl = document.getElementById('statusChart');
    if (statusChartEl) {
        fetch('/api/stats/case-status')
            .then(res => res.json())
            .then(data => {
                if (!data || data.error) return;
                const labels = data.map(d => d.status);
                const values = data.map(d => d.count);

                const colorMap = {
                    'Open': '#ef4444',
                    'Under Investigation': '#f59e0b',
                    'Solved': '#10b981',
                    'Closed': '#3b82f6',
                    'Cold Case': '#6e7d91'
                };
                const colors = labels.map(l => colorMap[l] || '#6e7d91');

                new Chart(statusChartEl.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels,
                        datasets: [{
                            data: values,
                            backgroundColor: colors.map(c => c + 'CC'),
                            borderColor: colors,
                            borderWidth: 2,
                            hoverOffset: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: { duration: 1000, easing: 'easeOutQuart' },
                        cutout: '68%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    color: '#b8c4d0',
                                    font: { size: 11 },
                                    padding: 12,
                                    usePointStyle: true,
                                    pointStyleWidth: 8
                                }
                            },
                            tooltip: {
                                backgroundColor: '#161b22',
                                borderColor: '#1e2632',
                                borderWidth: 1,
                                titleColor: '#e8edf2',
                                bodyColor: '#b8c4d0',
                                callbacks: {
                                    label: ctx => ` ${ctx.raw} cases`
                                }
                            }
                        }
                    }
                });
            });
    }

    // ── 6. Recent Activity Feed ──
    const activityEl = document.getElementById('recent-activity');
    if (activityEl) {
        fetch('/api/stats/recent-cases')
            .then(res => res.json())
            .then(cases => {
                if (!cases || cases.error) return;
                activityEl.innerHTML = '';
                if (cases.length === 0) {
                    activityEl.innerHTML = '<div style="text-align:center; color:var(--text-muted); padding:20px;">No recent cases</div>';
                    return;
                }
                const dotColors = {
                    'Open': 'red',
                    'Under Investigation': 'amber',
                    'Solved': 'green',
                    'Closed': 'blue',
                    'Cold Case': ''
                };
                cases.forEach(c => {
                    const color = dotColors[c.status] || 'blue';
                    const dateStr = c.date_opened ? new Date(c.date_opened).toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric' }) : '';
                    activityEl.innerHTML += `
                        <div class="activity-item">
                            <div class="activity-dot ${color}"></div>
                            <div class="activity-content">
                                <div class="activity-text">
                                    <strong><a href="/cases/${c.case_id}" style="color:var(--text-light); text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-light)'">#${c.case_id}: ${c.case_title}</a></strong>
                                </div>
                                <div class="activity-time">${c.status} · ${c.lead_officer || 'Unassigned'} · ${dateStr}</div>
                            </div>
                        </div>`;
                });
            })
            .catch(() => {});
    }

    // ── 7. Cross-Scene Fingerprint Matches ──
    const fpEl = document.getElementById('fingerprint-matches');
    if (fpEl) {
        fetch('/api/fingerprints/cross-scene')
            .then(res => res.json())
            .then(data => {
                if (!data || data.error) {
                    fpEl.innerHTML = `<div style="color:var(--text-muted); text-align:center; padding:16px;">Unable to load data</div>`;
                    return;
                }
                if (data.length === 0) {
                    fpEl.innerHTML = `<div style="color:var(--accent-green); text-align:center; padding:16px; font-size:0.85rem;">
                        ✅ No cross-scene fingerprint matches found. No serial pattern detected.
                    </div>`;
                    return;
                }
                fpEl.innerHTML = '';
                data.forEach(fp => {
                    fpEl.innerHTML += `
                        <div class="fingerprint-card">
                            🔬 Match Reference: <strong>${fp.match_reference}</strong>
                            &nbsp;—&nbsp; Found at <strong>${fp.scene_count}</strong> crime scene${fp.scene_count > 1 ? 's' : ''}
                            <span class="badge badge-${fp.scene_count > 2 ? 'red' : 'amber'}" style="margin-left:auto;">${fp.scene_count > 2 ? '⚠️ HIGH ALERT' : 'LINK FOUND'}</span>
                        </div>`;
                });
            })
            .catch(() => {
                fpEl.innerHTML = `<div style="color:var(--text-muted); text-align:center; padding:16px;">Error loading forensic data</div>`;
            });
    }

});

document.addEventListener('DOMContentLoaded', () => {
    // Initialize icons
    lucide.createIcons();

    let currentTrackingId = "AMC-2026-000123";

    // Navigation Tab Switching
    const tabs = document.querySelectorAll('.nav-tab');
    const panes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            tabs.forEach(t => {
                t.classList.remove('active');
                t.classList.add('text-slate-400');
            });
            tab.classList.add('active');
            tab.classList.remove('text-slate-400');

            panes.forEach(p => {
                if (p.id === targetTab) {
                    p.classList.remove('hidden');
                } else {
                    p.classList.add('hidden');
                }
            });

            if (targetTab === 'tab-ledger') {
                loadLedger();
            } else if (targetTab === 'tab-status' && currentTrackingId) {
                fetchStatusForId(currentTrackingId);
            }
            lucide.createIcons();
        });
    });

    // 1-Tap Sample Pickers
    const sampleBtns = document.querySelectorAll('.sample-btn');
    const previewImg = document.getElementById('preview-img');
    const previewFilename = document.getElementById('preview-filename');
    const selectedSampleInput = document.getElementById('selected-sample');
    const areaInput = document.getElementById('input-area');
    const fileInput = document.getElementById('file-input');

    sampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const sample = btn.getAttribute('data-sample');
            const area = btn.getAttribute('data-area');
            previewImg.src = `/static/samples/${sample}`;
            previewFilename.innerText = sample;
            selectedSampleInput.value = sample;
            fileInput.value = ''; // clear uploaded file
            if (area) {
                areaInput.value = area;
            }
        });
    });

    // Area Suggestion Chips
    document.querySelectorAll('.area-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            areaInput.value = chip.getAttribute('data-val');
        });
    });

    // Dropzone Click and File Upload
    const dropzone = document.getElementById('dropzone');
    dropzone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            previewFilename.innerText = file.name;
            selectedSampleInput.value = ''; // clear sample
            const reader = new FileReader();
            reader.onload = (re) => {
                previewImg.src = re.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    // Core Form: Execute Autonomous AI Filing
    const formFileComplaint = document.getElementById('form-file-complaint');
    const thinkingStream = document.getElementById('thinking-stream');
    const agentStatusPill = document.getElementById('agent-status-pill');
    const resultCard = document.getElementById('result-card');
    const btnSubmit = document.getElementById('btn-submit-complaint');

    formFileComplaint.addEventListener('submit', async (e) => {
        e.preventDefault();
        btnSubmit.disabled = true;
        btnSubmit.classList.add('opacity-70');
        agentStatusPill.innerText = 'REASONING & TOOL CALLS...';
        agentStatusPill.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 thinking-pulse';

        thinkingStream.innerHTML = `
            <div class="text-emerald-400 font-bold flex items-center gap-2">
                <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-emerald-400 border-t-transparent rounded-full"></span>
                [Agent Runtime] Initializing ReAct cognitive loop...
            </div>
        `;
        resultCard.classList.add('hidden');

        const formData = new FormData(formFileComplaint);

        try {
            const res = await fetch('/api/complaints/file', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                throw new Error(`Server responded with ${res.status}`);
            }

            const data = await res.json();
            renderReasoningTrace(data.reasoningTrace, () => {
                renderResultCard(data);
                btnSubmit.disabled = false;
                btnSubmit.classList.remove('opacity-70');
                agentStatusPill.innerText = 'COMPLETED (SUCCESS)';
                agentStatusPill.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-emerald-400';
            });

        } catch (err) {
            thinkingStream.innerHTML += `
                <div class="text-rose-400 bg-rose-500/10 p-3 rounded-xl border border-rose-500/20">
                    ❌ Execution Error: ${err.message}. Check local mock engine.
                </div>
            `;
            btnSubmit.disabled = false;
            btnSubmit.classList.remove('opacity-70');
            agentStatusPill.innerText = 'FAILED';
            agentStatusPill.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300';
        }
    });

    function renderReasoningTrace(trace, onDone) {
        thinkingStream.innerHTML = '';
        let i = 0;

        function nextStep() {
            if (i >= trace.length) {
                if (onDone) onDone();
                return;
            }

            const step = trace[i];
            const div = document.createElement('div');
            div.className = 'space-y-1 py-1 border-b border-slate-800/60 pb-2 transition-all duration-300';

            let phaseColor = 'text-slate-400';
            let iconName = 'cpu';

            if (step.phase === 'OBSERVATION') {
                phaseColor = 'text-sky-400';
                iconName = 'eye';
            } else if (step.phase === 'THINKING') {
                phaseColor = 'text-amber-400';
                iconName = 'brain';
            } else if (step.phase === 'TOOL_EXECUTION') {
                phaseColor = 'text-emerald-400 font-bold';
                iconName = 'wrench';
            } else if (step.phase === 'SYNTHESIS') {
                phaseColor = 'text-purple-400 font-bold';
                iconName = 'sparkles';
            }

            let toolDetails = '';
            if (step.toolCall) {
                toolDetails = `
                    <div class="mt-1 bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-[11px] font-mono text-slate-300 space-y-1">
                        <div class="flex items-center justify-between text-emerald-400">
                            <span class="font-bold flex items-center gap-1">
                                🔧 Tool: ${step.toolCall.name}
                            </span>
                            <span class="text-[10px] text-slate-500">${step.toolCall.latencyMs}ms</span>
                        </div>
                        <div class="text-slate-400 text-[10px]">${step.toolCall.description}</div>
                    </div>
                `;
            }

            div.innerHTML = `
                <div class="flex items-center justify-between text-[11px]">
                    <span class="${phaseColor} flex items-center gap-1.5 uppercase font-semibold">
                        <i data-lucide="${iconName}" class="w-3.5 h-3.5"></i>
                        Step ${step.stepIndex} · ${step.phase}
                    </span>
                </div>
                <p class="text-slate-200 text-xs pl-5 leading-relaxed">${step.thought}</p>
                ${toolDetails}
            `;

            thinkingStream.appendChild(div);
            thinkingStream.scrollTop = thinkingStream.scrollHeight;
            lucide.createIcons();
            i++;
            setTimeout(nextStep, 250);
        }

        nextStep();
    }

    function renderResultCard(data) {
        if (!data.complaint) return;
        const c = data.complaint;
        currentTrackingId = c.trackingId;

        document.getElementById('res-tracking-id').innerHTML = `
            ${c.trackingId}
            <button id="btn-copy-id" class="text-slate-400 hover:text-white transition p-1" title="Copy ID">
                <i data-lucide="copy" class="w-4 h-4"></i>
            </button>
        `;
        document.getElementById('res-issue').innerText = c.issue;
        document.getElementById('res-ward').innerText = `${c.ward} (${c.wardName})`;
        document.getElementById('res-dept').innerText = c.department;
        document.getElementById('res-sla').innerText = `Target: ${c.expectedSlaAt ? c.expectedSlaAt.substring(0, 16).replace('T', ' ') : 'Within 24h'}`;
        document.getElementById('res-engineer').innerText = c.assignedTo || 'Assigned to Ward Engineer';
        document.getElementById('res-desc').innerText = `"${c.description}"`;

        if (data.socialDraft) {
            document.getElementById('social-preview-body').innerText = data.socialDraft.text;
            document.getElementById('btn-tweet-intent').href = data.socialDraft.intentUrl;
        }

        resultCard.classList.remove('hidden');
        lucide.createIcons();

        document.getElementById('btn-copy-id').addEventListener('click', () => {
            navigator.clipboard.writeText(c.trackingId);
            alert(`Copied ${c.trackingId} to clipboard!`);
        });

        document.getElementById('btn-track-now').addEventListener('click', () => {
            document.querySelector('[data-tab="tab-status"]').click();
            document.getElementById('input-status-query').value = `what's the status of ${c.trackingId}?`;
            fetchStatusForId(c.trackingId);
        });
    }

    // Status Tab Handlers
    const formQueryStatus = document.getElementById('form-query-status');
    const inputStatusQuery = document.getElementById('input-status-query');

    formQueryStatus.addEventListener('submit', async (e) => {
        e.preventDefault();
        const q = inputStatusQuery.value.trim();
        if (!q) return;
        await executeStatusQuery(q);
    });

    document.querySelectorAll('.query-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const query = chip.getAttribute('data-q');
            inputStatusQuery.value = query;
            executeStatusQuery(query);
        });
    });

    async function executeStatusQuery(query) {
        try {
            document.getElementById('status-agent-message').innerText = 'Querying AMC Municipal Ledger...';
            const res = await fetch('/api/agent/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            const data = await res.json();
            if (data.complaint) {
                renderStatusCard(data.complaint, data.message);
            } else {
                document.getElementById('status-agent-message').innerText = data.message;
            }
        } catch (err) {
            document.getElementById('status-agent-message').innerText = `Error: ${err.message}`;
        }
    }

    async function fetchStatusForId(trackingId) {
        try {
            const res = await fetch(`/api/complaints/${trackingId}`);
            if (res.ok) {
                const c = await res.json();
                renderStatusCard(c, `Live status report for ticket ${c.trackingId}`);
            }
        } catch (err) {}
    }

    function renderStatusCard(complaint, agentMessage) {
        currentTrackingId = complaint.trackingId;
        document.getElementById('status-card-id').innerText = complaint.trackingId;
        document.getElementById('status-badge').innerText = complaint.status;

        const progressMap = {
            'Submitted': '20%',
            'Assigned': '40%',
            'In Progress': '65%',
            'Work Verified': '85%',
            'Resolved': '100%'
        };
        document.getElementById('status-progress-bar').style.width = progressMap[complaint.status] || '40%';

        document.getElementById('status-agent-message').innerText = agentMessage;

        const timelineList = document.getElementById('status-timeline-list');
        timelineList.innerHTML = '';

        if (complaint.timeline && complaint.timeline.length > 0) {
            complaint.timeline.forEach(event => {
                const item = document.createElement('div');
                item.className = 'relative pl-4 space-y-0.5';
                item.innerHTML = `
                    <div class="absolute -left-[9px] top-1.5 w-3 h-3 rounded-full bg-emerald-500 border-2 border-slate-900"></div>
                    <div class="flex items-center justify-between text-[11px] font-mono">
                        <span class="font-bold text-white uppercase">${event.status}</span>
                        <span class="text-slate-500">${event.timestamp.substring(0, 16).replace('T', ' ')}</span>
                    </div>
                    <div class="text-xs text-slate-300 font-sans">${event.note}</div>
                `;
                timelineList.appendChild(item);
            });
        }
        lucide.createIcons();
    }

    // Advance Status Stage Demo
    const btnAdvance = document.getElementById('btn-advance-status');
    btnAdvance.addEventListener('click', async () => {
        if (!currentTrackingId) return;
        try {
            const res = await fetch(`/api/complaints/${currentTrackingId}/advance`, {
                method: 'POST'
            });
            if (res.ok) {
                const updated = await res.json();
                renderStatusCard(updated, `Advanced complaint ${updated.trackingId} to next lifecycle phase: ${updated.status}!`);
            }
        } catch (err) {
            alert(`Error advancing status: ${err.message}`);
        }
    });

    // Video Scanner Stretch Goal
    const btnStartScan = document.getElementById('btn-start-video-scan');
    const videoFramesGrid = document.getElementById('video-frames-grid');
    const videoSummary = document.getElementById('video-scan-summary');
    const videoSummaryText = document.getElementById('video-summary-text');

    btnStartScan.addEventListener('click', async () => {
        btnStartScan.disabled = true;
        btnStartScan.innerText = 'Scanning Corridor Frames (3s interval)...';
        videoFramesGrid.innerHTML = `
            <div class="p-6 text-center text-xs text-amber-400 font-mono col-span-2 flex items-center justify-center gap-2">
                <span class="animate-spin inline-block w-4 h-4 border-2 border-amber-400 border-t-transparent rounded-full"></span>
                Processing road surveillance stream along CG Road corridor...
            </div>
        `;

        try {
            const res = await fetch('/api/video/scan', { method: 'POST' });
            const data = await res.json();

            videoFramesGrid.innerHTML = '';
            data.detections.forEach((det, idx) => {
                const card = document.createElement('div');
                card.className = `p-3.5 rounded-xl border ${det.hazardDetected ? 'border-rose-500/50 bg-rose-950/20' : 'border-slate-800 bg-slate-950/40'} space-y-2`;

                card.innerHTML = `
                    <div class="flex items-center justify-between text-xs font-mono">
                        <span class="font-bold ${det.hazardDetected ? 'text-rose-400' : 'text-slate-400'}">
                            Frame #${det.frameNumber} (t = ${det.timestampSeconds}s)
                        </span>
                        <span class="text-[10px] px-2 py-0.5 rounded ${det.hazardDetected ? 'bg-rose-500/20 text-rose-300' : 'bg-slate-800 text-slate-400'}">
                            ${det.hazardDetected ? 'CRATER DETECTED' : 'CLEAR'}
                        </span>
                    </div>
                    <div class="text-[11px] text-slate-300">
                        GPS: ${det.coordinates.lat}, ${det.coordinates.lng} (CG Road)
                    </div>
                    ${det.hazardDetected ? `
                        <div class="text-[11px] font-mono text-emerald-400 bg-slate-950 p-2 rounded border border-emerald-500/30 flex items-center justify-between">
                            <span>Auto-Filed: ${det.autoFiledTrackingId}</span>
                            <span class="text-[10px] text-slate-400">Confidence: ${(det.confidence*100).toFixed(1)}%</span>
                        </div>
                    ` : ''}
                `;
                videoFramesGrid.appendChild(card);
            });

            videoSummary.classList.remove('hidden');
            videoSummaryText.innerText = `Corridor scan complete! Processed ${data.totalFramesSampled} video frames. Identified ${data.totalHazardsDetected} hazardous road craters and auto-filed official AMC tickets.`;

            btnStartScan.disabled = false;
            btnStartScan.innerText = 'Re-Run Road Video Inspection';
            lucide.createIcons();
        } catch (err) {
            videoFramesGrid.innerHTML = `<div class="p-4 text-rose-400 text-xs">Error: ${err.message}</div>`;
            btnStartScan.disabled = false;
            btnStartScan.innerText = 'Execute Road Video Inspection';
        }
    });

    // AMC Ledger Loader
    const ledgerTableBody = document.getElementById('ledger-table-body');
    const btnRefreshLedger = document.getElementById('btn-refresh-ledger');

    async function loadLedger() {
        ledgerTableBody.innerHTML = '<tr><td colspan="7" class="p-4 text-center text-slate-500">Loading AMC database...</td></tr>';
        try {
            const res = await fetch('/api/complaints');
            const complaints = await res.json();
            ledgerTableBody.innerHTML = '';

            complaints.forEach(c => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-950/60 transition';

                const statusColor = {
                    'Submitted': 'text-slate-400',
                    'Assigned': 'text-amber-400',
                    'In Progress': 'text-sky-400',
                    'Work Verified': 'text-indigo-400',
                    'Resolved': 'text-emerald-400'
                }[c.status] || 'text-white';

                tr.innerHTML = `
                    <td class="p-3 font-bold text-white">${c.trackingId}</td>
                    <td class="p-3 capitalize text-slate-300">${c.issue}</td>
                    <td class="p-3 text-slate-300">${c.ward} · ${c.wardName} (${c.zone})</td>
                    <td class="p-3 text-slate-300">${c.department}</td>
                    <td class="p-3 font-semibold ${statusColor}">${c.status}</td>
                    <td class="p-3 text-slate-500 text-[11px]">${c.filedAt.substring(0, 16).replace('T', ' ')}</td>
                    <td class="p-3">
                        <button class="view-ticket-btn px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs text-sky-300 transition" data-id="${c.trackingId}">
                            Track
                        </button>
                    </td>
                `;
                ledgerTableBody.appendChild(tr);
            });

            document.querySelectorAll('.view-ticket-btn').forEach(b => {
                b.addEventListener('click', () => {
                    const id = b.getAttribute('data-id');
                    document.querySelector('[data-tab="tab-status"]').click();
                    fetchStatusForId(id);
                });
            });
        } catch (err) {
            ledgerTableBody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-rose-400">Failed to load: ${err.message}</td></tr>`;
        }
    }

    if (btnRefreshLedger) {
        btnRefreshLedger.addEventListener('click', loadLedger);
    }

    // Reset Seed Data Button
    document.getElementById('btn-reset-seed').addEventListener('click', async () => {
        if (confirm('Reset AMC database back to initial seed data for a fresh demo?')) {
            try {
                const res = await fetch('/api/admin/reset', { method: 'POST' });
                const json = await res.json();
                alert(json.message);
                loadLedger();
            } catch (err) {
                alert(`Error resetting: ${err.message}`);
            }
        }
    });
});

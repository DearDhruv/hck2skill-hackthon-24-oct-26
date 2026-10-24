document.addEventListener('DOMContentLoaded', () => {
    // Initialize icons
    lucide.createIcons();

    let currentTrackingId = "AMC-2026-000123";

    // ==========================================
    // Soothing Theme Controller (Light by default)
    // ==========================================
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlEl = document.documentElement;

    function applyTheme(isDark) {
        if (isDark) {
            htmlEl.classList.add('dark');
            localStorage.setItem('nagrik-theme', 'dark');
            if (themeToggleBtn) {
                themeToggleBtn.innerHTML = `
                    <i data-lucide="sun" class="w-3 h-3 text-amber-300"></i>
                    <span>Day Comfort</span>
                `;
            }
        } else {
            htmlEl.classList.remove('dark');
            localStorage.setItem('nagrik-theme', 'light');
            if (themeToggleBtn) {
                themeToggleBtn.innerHTML = `
                    <i data-lucide="moon" class="w-3 h-3 text-teal-300"></i>
                    <span>Night Comfort</span>
                `;
            }
        }
        lucide.createIcons();
    }

    const savedTheme = localStorage.getItem('nagrik-theme');
    if (savedTheme === 'dark') {
        applyTheme(true);
    } else {
        applyTheme(false);
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const isDark = htmlEl.classList.contains('dark');
            applyTheme(!isDark);
        });
    }

    // ==========================================
    // Toast Notification System
    // ==========================================
    function showNotificationToast(message) {
        const toast = document.getElementById('notification-toast');
        const toastMsg = document.getElementById('toast-message');
        if (!toast) return;
        if (toastMsg) toastMsg.innerText = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3200);
    }

    // ==========================================
    // Navigation Tab Switching
    // ==========================================
    const tabs = document.querySelectorAll('.nav-tab');
    const panes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            tabs.forEach(t => {
                t.classList.remove('active');
                t.classList.add('text-slate-600', 'dark:text-slate-400');
            });
            tab.classList.add('active');
            tab.classList.remove('text-slate-600', 'dark:text-slate-400');

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

    // ==========================================
    // 1-Tap Sample Pickers
    // ==========================================
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
            fileInput.value = '';
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
    if (dropzone) {
        dropzone.addEventListener('click', () => fileInput.click());
    }

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                const file = e.target.files[0];
                previewFilename.innerText = file.name;
                selectedSampleInput.value = '';
                const reader = new FileReader();
                reader.onload = (re) => {
                    previewImg.src = re.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ==========================================
    // Authority Card Helper (Reusable)
    // ==========================================
    function populateAuthorityDetails(prefix, c) {
        if (!c) return;
        const officerName = c.wardOfficer || 'Shri Arvind Trivedi';
        const wardTitle = `Ward ${c.ward || 'W12'} · ${c.wardName || 'Navrangpura'} (${c.zone || 'West'} Zone)`;
        const officerPhone = c.wardContactPhone || '+91-79-2755-1201';
        const cleanPhone = officerPhone.replace(/[^0-9+]/g, '');
        const officeAddress = c.wardOfficeAddress || `AMC ${c.wardName || ''} Ward Office, ${c.zone || ''} Zone, Ahmedabad`;
        const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(officeAddress)}`;
        const helpline = c.amcHelpline || '155303';
        const tollFree = c.tollFreeHelpline || '1800-233-2330';
        const whatsappNum = c.whatsappGrievance || '+91-99783-22880';
        const cleanWhatsapp = whatsappNum.replace(/[^0-9]/g, '');
        const whatsappText = `Hello AMC Grievance Cell, regarding Ticket #${c.trackingId} (${(c.issue || 'civic issue')} at ${c.area}, Ward ${c.ward}): please update on resolution status.`;
        const whatsappUrl = `https://wa.me/${cleanWhatsapp}?text=${encodeURIComponent(whatsappText)}`;
        const deptName = c.department || 'Roads & Buildings';
        const leadEngineer = c.leadEngineer || 'AMC Executive Engineer';
        const deptHotline = c.departmentHotline || '+91-79-2755-1234';
        const deptEmail = c.departmentEmail || 'grievance@ahmedabadcity.gov.in';

        const nameEl = document.getElementById(`${prefix}-officer-name`);
        if (nameEl) nameEl.innerText = officerName;

        const wardEl = document.getElementById(`${prefix}-ward-title`);
        if (wardEl) wardEl.innerText = wardTitle;

        const phoneEl = document.getElementById(`${prefix}-officer-phone`);
        if (phoneEl) phoneEl.innerText = officerPhone;

        const phoneLink = document.getElementById(`${prefix}-officer-phone-link`);
        if (phoneLink) phoneLink.href = `tel:${cleanPhone}`;

        const addrEl = document.getElementById(`${prefix}-office-address`);
        if (addrEl) addrEl.innerText = officeAddress;

        const mapsEl = document.getElementById(`${prefix}-maps-link`);
        if (mapsEl) mapsEl.href = mapsUrl;

        const deptEl = document.getElementById(`${prefix}-dept-name`);
        if (deptEl) deptEl.innerText = deptName;

        const engEl = document.getElementById(`${prefix}-lead-engineer`);
        if (engEl) engEl.innerText = `${leadEngineer} (Executive Engineer)`;

        const hotlineEl = document.getElementById(`${prefix}-dept-hotline`);
        if (hotlineEl) hotlineEl.innerText = deptHotline;

        const hotlineLink = document.getElementById(`${prefix}-dept-hotline-link`);
        if (hotlineLink) hotlineLink.href = `tel:${deptHotline.replace(/[^0-9+]/g, '')}`;

        const emailEl = document.getElementById(`${prefix}-dept-email`);
        if (emailEl) emailEl.innerText = deptEmail;

        const emailLink = document.getElementById(`${prefix}-dept-email-link`);
        if (emailLink) emailLink.href = `mailto:${deptEmail}`;

        // 4 Action Buttons
        const btnCall = document.getElementById(`${prefix}-btn-call-officer`);
        if (btnCall) btnCall.href = `tel:${cleanPhone}`;

        const btnHelp = document.getElementById(`${prefix}-btn-call-helpline`);
        if (btnHelp) btnHelp.href = `tel:${helpline}`;

        const btnWa = document.getElementById(`${prefix}-btn-whatsapp`);
        if (btnWa) btnWa.href = whatsappUrl;

        const btnCopy = document.getElementById(`${prefix}-btn-copy-details`);
        if (btnCopy) {
            btnCopy.onclick = () => {
                const text = [
                    `Ahmedabad Municipal Corporation (AMC) · Authority Contact Details`,
                    `==================================================================`,
                    `Ticket Tracking ID: ${c.trackingId}`,
                    `Civic Issue: ${(c.issue || '').toUpperCase()} at ${c.area}`,
                    `Assigned Ward: Ward ${c.ward} · ${c.wardName} (${c.zone} Zone)`,
                    `Assigned Ward Officer: ${officerName}`,
                    `Direct Officer Phone: ${officerPhone}`,
                    `Ward Office Address: ${officeAddress}`,
                    `Google Maps Link: ${mapsUrl}`,
                    `Department: ${deptName}`,
                    `Executive Engineer: ${leadEngineer}`,
                    `Department Hotline: ${deptHotline}`,
                    `Department Escalation Email: ${deptEmail}`,
                    `AMC 24x7 Civic Helpline: ${helpline} (Toll-Free: ${tollFree})`,
                    `AMC WhatsApp Grievance Desk: ${whatsappNum}`
                ].join('\n');
                navigator.clipboard.writeText(text);
                showNotificationToast('Municipal Authority details copied to clipboard!');
            };
        }
    }

    // ==========================================
    // Complaint Form Submission
    // ==========================================
    const formFileComplaint = document.getElementById('form-file-complaint');
    const thinkingStream = document.getElementById('thinking-stream');
    const agentStatusPill = document.getElementById('agent-status-pill');
    const resultCard = document.getElementById('result-card');
    const errorStateCard = document.getElementById('error-state-card');
    const btnSubmit = document.getElementById('btn-submit-complaint');

    if (formFileComplaint) {
        formFileComplaint.addEventListener('submit', async (e) => {
            e.preventDefault();
            btnSubmit.disabled = true;
            btnSubmit.classList.add('opacity-70');
            agentStatusPill.innerText = 'PROCESSING...';
            agentStatusPill.className = 'text-[10px] font-mono px-3 py-1 rounded-full bg-teal-100 dark:bg-teal-950 text-teal-800 dark:text-teal-300 font-semibold thinking-pulse';

            thinkingStream.innerHTML = `
                <div class="text-teal-700 dark:text-teal-400 font-semibold flex items-center gap-2">
                    <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-teal-700 dark:border-teal-400 border-t-transparent rounded-full"></span>
                    Initializing autonomous civic diagnosis &amp; jurisdiction triage...
                </div>
            `;
            if (resultCard) resultCard.classList.add('hidden');
            if (errorStateCard) errorStateCard.classList.add('hidden');

            const formData = new FormData(formFileComplaint);

            try {
                const res = await fetch('/api/complaints/file', {
                    method: 'POST',
                    body: formData
                });

                const rawText = await res.text();
                let data = null;
                try {
                    data = JSON.parse(rawText);
                } catch (jsonErr) {
                    throw {
                        chaosFault: 'CORRUPTED_PAYLOAD',
                        httpCode: res.status || 200,
                        title: 'Corrupted Municipal Response Payload',
                        subsystem: 'amc_legacy_serializer',
                        detail: `Municipal wire protocol emitted malformed non-JSON data stream: "${rawText.substring(0, 64)}...". JSON parser rejected syntax.`,
                        suggestedRecovery: 'Reject corrupted packet and re-request clean response from municipal gateway.'
                    };
                }

                if (!res.ok) {
                    const faultNameMap = {
                        '500_INTERNAL_ERROR': 'Municipal Database Crash',
                        'NETWORK_TIMEOUT': 'Network Timeout (>5.0s)',
                        'RATE_LIMIT_429': 'AMC API Rate Limit Exceeded',
                        'JURISDICTION_UNRESOLVED': 'Jurisdiction Unresolved (Ward Dispute)',
                        'CORRUPTED_IMAGE_UPLOAD': 'Corrupted Image Buffer Header'
                    };
                    const faultKey = (data && data.chaosFault) || '';
                    throw {
                        chaosFault: faultKey || `HTTP_${res.status}`,
                        httpCode: res.status,
                        title: faultNameMap[faultKey] || `Server Error (HTTP ${res.status})`,
                        subsystem: (data && data.subsystem) || 'amc_municipal_core',
                        detail: (data && data.detail) || `Municipal service returned HTTP ${res.status}`,
                        suggestedRecovery: (data && data.details && data.details.suggested_recovery) || 'Click Self-Heal to automatically recover.'
                    };
                }

                renderReasoningTrace(data.reasoningTrace, () => {
                    renderResultCard(data);
                    btnSubmit.disabled = false;
                    btnSubmit.classList.remove('opacity-70');
                    agentStatusPill.innerText = 'RESOLVED (SUCCESS)';
                    agentStatusPill.className = 'text-[10px] font-mono px-3 py-1 rounded-full bg-teal-100 dark:bg-teal-950 text-teal-800 dark:text-teal-300 font-semibold';
                });

            } catch (err) {
                const faultCode = err.chaosFault || 'RUNTIME_ERROR';
                thinkingStream.innerHTML += `
                    <div class="mt-2 text-rose-800 dark:text-rose-200 bg-rose-50 dark:bg-rose-950/40 p-3.5 rounded-xl border border-rose-300 dark:border-rose-800 space-y-1">
                        <div class="font-bold flex items-center gap-1.5 uppercase text-xs text-rose-700 dark:text-rose-300">
                            <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-600"></i>
                            <span>Fault Intercepted: [${faultCode}]</span>
                        </div>
                        <div class="text-xs font-sans">${err.detail || err.message}</div>
                    </div>
                `;
                btnSubmit.disabled = false;
                btnSubmit.classList.remove('opacity-70');
                agentStatusPill.innerText = `FAILED (${faultCode})`;
                agentStatusPill.className = 'text-[10px] font-mono px-3 py-1 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-200 font-semibold';

                renderErrorStateCard(err);
                lucide.createIcons();
            }
        });
    }

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
            div.className = 'space-y-1 py-1.5 border-b border-slate-100 dark:border-slate-800/80 pb-2.5 transition-all duration-200';

            let phaseColor = 'text-slate-600 dark:text-slate-400';
            let iconName = 'cpu';

            if (step.phase === 'OBSERVATION') {
                phaseColor = 'text-teal-700 dark:text-teal-300 font-semibold';
                iconName = 'eye';
            } else if (step.phase === 'THINKING') {
                phaseColor = 'text-amber-700 dark:text-amber-300 font-semibold';
                iconName = 'brain';
            } else if (step.phase === 'TOOL_EXECUTION') {
                phaseColor = 'text-teal-800 dark:text-teal-200 font-bold';
                iconName = 'wrench';
            } else if (step.phase === 'SYNTHESIS') {
                phaseColor = 'text-indigo-700 dark:text-indigo-300 font-bold';
                iconName = 'sparkles';
            }

            let toolDetails = '';
            if (step.toolCall) {
                toolDetails = `
                    <div class="mt-1 bg-slate-50 dark:bg-slate-900 p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 text-[11px] font-mono text-slate-700 dark:text-slate-300 space-y-0.5">
                        <div class="flex items-center justify-between text-teal-800 dark:text-teal-300">
                            <span class="font-bold flex items-center gap-1">
                                🔧 Tool: ${step.toolCall.name}
                            </span>
                            <span class="text-[10px] text-slate-400">${step.toolCall.latencyMs}ms</span>
                        </div>
                        <div class="text-slate-500 text-[10px]">${step.toolCall.description}</div>
                    </div>
                `;
            }

            div.innerHTML = `
                <div class="flex items-center justify-between text-[11px]">
                    <span class="${phaseColor} flex items-center gap-1.5 uppercase tracking-wide">
                        <i data-lucide="${iconName}" class="w-3.5 h-3.5"></i>
                        Step ${step.stepIndex} · ${step.phase}
                    </span>
                </div>
                <p class="text-slate-800 dark:text-slate-200 text-xs pl-5 leading-relaxed font-sans">${step.thought}</p>
                ${toolDetails}
            `;

            thinkingStream.appendChild(div);
            thinkingStream.scrollTop = thinkingStream.scrollHeight;
            lucide.createIcons();
            i++;
            setTimeout(nextStep, 220);
        }

        nextStep();
    }

    function renderResultCard(data) {
        if (!data.complaint) return;
        const c = data.complaint;
        currentTrackingId = c.trackingId;

        document.getElementById('res-tracking-id').innerHTML = `
            ${c.trackingId}
            <button id="btn-copy-id" class="text-slate-400 hover:text-teal-700 dark:hover:text-teal-300 transition p-1" title="Copy Tracking ID">
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

        // Populate Filed Result Authority Card
        populateAuthorityDetails('filed', c);

        resultCard.classList.remove('hidden');
        lucide.createIcons();

        document.getElementById('btn-copy-id').addEventListener('click', () => {
            navigator.clipboard.writeText(c.trackingId);
            showNotificationToast(`Copied ${c.trackingId} to clipboard!`);
        });

        document.getElementById('btn-track-now').addEventListener('click', () => {
            document.querySelector('[data-tab="tab-status"]').click();
            document.getElementById('input-status-query').value = `what's the status of ${c.trackingId}?`;
            fetchStatusForId(c.trackingId);
        });
    }

    function renderErrorStateCard(errInfo) {
        if (!errorStateCard) return;

        if (resultCard) resultCard.classList.add('hidden');
        errorStateCard.classList.remove('hidden');

        const errHttpBadge = document.getElementById('err-http-badge');
        const errTitle = document.getElementById('err-title');
        const errSubsystem = document.getElementById('err-subsystem');
        const errTimestamp = document.getElementById('err-timestamp');
        const errDetail = document.getElementById('err-detail');
        const errRecoveryText = document.getElementById('err-recovery-text');
        const btnErrDismiss = document.getElementById('btn-err-dismiss');
        const btnErrRetry = document.getElementById('btn-err-retry');
        const btnErrSelfHeal = document.getElementById('btn-err-self-heal');

        if (errHttpBadge) errHttpBadge.innerText = errInfo.httpCode ? `HTTP ${errInfo.httpCode}` : 'ERROR';
        if (errTitle) errTitle.innerText = errInfo.title || 'Simulated Municipal Fault Detected';
        if (errSubsystem) errSubsystem.innerText = errInfo.subsystem || 'amc_municipal_core';
        if (errTimestamp) errTimestamp.innerText = new Date().toLocaleTimeString();
        if (errDetail) errDetail.innerText = errInfo.detail || 'An unexpected municipal error occurred during autonomous triage.';
        if (errRecoveryText) errRecoveryText.innerText = errInfo.suggestedRecovery || 'Click "Disable Chaos & Self-Heal" to automatically recover and re-run complaint filing.';

        if (btnErrDismiss) {
            btnErrDismiss.onclick = () => {
                errorStateCard.classList.add('hidden');
            };
        }

        if (btnErrRetry) {
            btnErrRetry.onclick = () => {
                errorStateCard.classList.add('hidden');
                formFileComplaint.requestSubmit();
            };
        }

        if (btnErrSelfHeal) {
            btnErrSelfHeal.onclick = async () => {
                btnErrSelfHeal.disabled = true;
                btnErrSelfHeal.innerHTML = `
                    <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full"></span>
                    <span>Self-Healing &amp; Retrying...</span>
                `;
                try {
                    const res = await fetch('/api/chaos/toggle', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ enabled: false })
                    });
                    const updated = await res.json();
                    updateChaosUI(updated);
                } catch (e) {
                    console.error('Failed to disable chaos:', e);
                }

                errorStateCard.classList.add('hidden');
                btnErrSelfHeal.disabled = false;
                btnErrSelfHeal.innerHTML = `
                    <i data-lucide="shield-check" class="w-4 h-4"></i>
                    <span>Disable Chaos &amp; Self-Heal</span>
                `;
                lucide.createIcons();

                setTimeout(() => {
                    formFileComplaint.requestSubmit();
                }, 300);
            };
        }

        lucide.createIcons();
    }

    // ==========================================
    // Status Tab Handlers
    // ==========================================
    const formQueryStatus = document.getElementById('form-query-status');
    const inputStatusQuery = document.getElementById('input-status-query');

    if (formQueryStatus) {
        formQueryStatus.addEventListener('submit', async (e) => {
            e.preventDefault();
            const q = inputStatusQuery.value.trim();
            if (!q) return;
            await executeStatusQuery(q);
        });
    }

    document.querySelectorAll('.query-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const query = chip.getAttribute('data-q');
            inputStatusQuery.value = query;
            executeStatusQuery(query);
        });
    });

    async function executeStatusQuery(query) {
        try {
            document.getElementById('status-agent-message').innerText = 'Querying AMC Municipal Records...';
            const res = await fetch('/api/agent/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            const raw = await res.text();
            let data;
            try {
                data = JSON.parse(raw);
            } catch (jsonErr) {
                document.getElementById('status-agent-message').innerHTML = `
                    <div class="text-rose-700 dark:text-rose-300 bg-rose-50 dark:bg-rose-950/40 p-3 rounded-xl border border-rose-300 dark:border-rose-800 space-y-1">
                        <div class="font-bold flex items-center gap-1.5 text-xs">
                            <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-600"></i>
                            ⚠️ [CHAOS FAULT: CORRUPTED_PAYLOAD]
                        </div>
                        <div class="text-xs">Municipal query returned corrupted payload. JSON parse failed.</div>
                    </div>
                `;
                lucide.createIcons();
                return;
            }

            if (!res.ok) {
                document.getElementById('status-agent-message').innerHTML = `
                    <div class="text-rose-700 dark:text-rose-300 bg-rose-50 dark:bg-rose-950/40 p-3 rounded-xl border border-rose-300 dark:border-rose-800 space-y-1">
                        <div class="font-bold flex items-center gap-1.5 text-xs">
                            <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-600"></i>
                            ⚠️ [CHAOS FAULT: ${data.chaosFault || res.status}]
                        </div>
                        <div class="text-xs">${data.detail || 'Municipal service error.'}</div>
                    </div>
                `;
                lucide.createIcons();
                return;
            }

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
                renderStatusCard(c, `Live official status report for ticket ${c.trackingId}`);
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

        // Populate Status Result Authority Card
        populateAuthorityDetails('status', complaint);

        const timelineList = document.getElementById('status-timeline-list');
        timelineList.innerHTML = '';

        if (complaint.timeline && complaint.timeline.length > 0) {
            complaint.timeline.forEach(event => {
                const item = document.createElement('div');
                item.className = 'relative pl-4 space-y-0.5';
                item.innerHTML = `
                    <div class="absolute -left-[9px] top-1.5 w-3 h-3 rounded-full bg-teal-600 border-2 border-white dark:border-slate-900"></div>
                    <div class="flex items-center justify-between text-[11px] font-mono">
                        <span class="font-bold text-slate-800 dark:text-slate-100 uppercase">${event.status}</span>
                        <span class="text-slate-400">${event.timestamp.substring(0, 16).replace('T', ' ')}</span>
                    </div>
                    <div class="text-xs text-slate-600 dark:text-slate-300 font-sans leading-relaxed">${event.note}</div>
                `;
                timelineList.appendChild(item);
            });
        }
        lucide.createIcons();
    }

    // Advance Status Stage Demo
    const btnAdvance = document.getElementById('btn-advance-status');
    if (btnAdvance) {
        btnAdvance.addEventListener('click', async () => {
            if (!currentTrackingId) return;
            try {
                const res = await fetch(`/api/complaints/${currentTrackingId}/advance`, {
                    method: 'POST'
                });
                if (res.ok) {
                    const updated = await res.json();
                    renderStatusCard(updated, `Advanced complaint ${updated.trackingId} to next lifecycle phase: ${updated.status}!`);
                    showNotificationToast(`Advanced ${updated.trackingId} to "${updated.status}"`);
                }
            } catch (err) {
                alert(`Error advancing status: ${err.message}`);
            }
        });
    }

    // ==========================================
    // Road Video Scanner
    // ==========================================
    const btnStartScan = document.getElementById('btn-start-video-scan');
    const videoFramesGrid = document.getElementById('video-frames-grid');
    const videoSummary = document.getElementById('video-scan-summary');
    const videoSummaryText = document.getElementById('video-summary-text');

    if (btnStartScan) {
        btnStartScan.addEventListener('click', async () => {
            btnStartScan.disabled = true;
            btnStartScan.innerHTML = `
                <span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
                <span>Scanning Corridor Frames (3s interval)...</span>
            `;
            videoFramesGrid.innerHTML = `
                <div class="p-6 text-center text-xs text-amber-800 dark:text-amber-200 col-span-2 flex items-center justify-center gap-2">
                    <span class="animate-spin inline-block w-4 h-4 border-2 border-amber-600 border-t-transparent rounded-full"></span>
                    Processing road surveillance stream along CG Road corridor...
                </div>
            `;

            try {
                const res = await fetch('/api/video/scan', { method: 'POST' });
                const data = await res.json();

                videoFramesGrid.innerHTML = '';
                data.detections.forEach((det) => {
                    const card = document.createElement('div');
                    card.className = `p-3.5 rounded-xl border ${det.hazardDetected ? 'border-amber-300 dark:border-amber-800/80 bg-amber-50/60 dark:bg-amber-950/20' : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/40'} space-y-2`;

                    const frameImgTag = det.frameImageUrl ? `
                        <div class="relative overflow-hidden rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-950">
                            <img src="${det.frameImageUrl}" alt="Frame #${det.frameNumber}" class="w-full h-36 object-cover rounded-md" loading="lazy">
                            <div class="absolute bottom-1 right-2 bg-slate-900/80 px-2 py-0.5 rounded text-[10px] font-mono text-white">
                                t = ${det.timestampSeconds}s
                            </div>
                        </div>
                    ` : '';

                    card.innerHTML = `
                        <div class="flex items-center justify-between text-xs">
                            <span class="font-bold ${det.hazardDetected ? 'text-amber-800 dark:text-amber-300' : 'text-slate-600 dark:text-slate-400'}">
                                Frame #${det.frameNumber} (t = ${det.timestampSeconds}s)
                            </span>
                            <span class="text-[10px] px-2 py-0.5 rounded-full ${det.hazardDetected ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-200 font-bold border border-amber-300 dark:border-amber-800' : 'bg-slate-100 dark:bg-slate-800 text-slate-500'}">
                                ${det.hazardDetected ? 'ROAD CRATER DETECTED' : 'CLEAR'}
                            </span>
                        </div>
                        ${frameImgTag}
                        <div class="text-[11px] text-slate-600 dark:text-slate-400">
                            GPS: ${det.coordinates.lat}, ${det.coordinates.lng} (CG Road Corridor)
                        </div>
                        ${det.hazardDetected ? `
                            <div class="text-[11px] font-mono text-teal-800 dark:text-teal-300 bg-white dark:bg-slate-950 p-2 rounded-lg border border-teal-200 dark:border-teal-800 flex items-center justify-between">
                                <span class="font-bold">Auto-Filed: ${det.autoFiledTrackingId}</span>
                                <span class="text-[10px] text-slate-500">Confidence: ${(det.confidence*100).toFixed(1)}%</span>
                            </div>
                        ` : ''}
                    `;
                    videoFramesGrid.appendChild(card);
                });

                videoSummary.classList.remove('hidden');
                videoSummaryText.innerText = `Corridor scan complete! Processed ${data.totalFramesSampled} video frames. Identified ${data.totalHazardsDetected} road craters and auto-filed official AMC tickets with the West Zone cell.`;

                btnStartScan.disabled = false;
                btnStartScan.innerHTML = `
                    <i data-lucide="play-circle" class="w-4 h-4"></i>
                    <span>Re-Run Road Video Inspection</span>
                `;
                lucide.createIcons();
            } catch (err) {
                videoFramesGrid.innerHTML = `<div class="p-4 text-rose-600 text-xs">Error: ${err.message}</div>`;
                btnStartScan.disabled = false;
                btnStartScan.innerHTML = `
                    <i data-lucide="play-circle" class="w-4 h-4"></i>
                    <span>Execute Road Video Inspection</span>
                `;
                lucide.createIcons();
            }
        });
    }

    // ==========================================
    // AMC Ledger Loader & Authority Connect
    // ==========================================
    const ledgerTableBody = document.getElementById('ledger-table-body');
    const btnRefreshLedger = document.getElementById('btn-refresh-ledger');

    async function loadLedger() {
        if (!ledgerTableBody) return;
        ledgerTableBody.innerHTML = '<tr><td colspan="8" class="p-4 text-center text-slate-400">Loading AMC municipal database...</td></tr>';
        try {
            const res = await fetch('/api/complaints');
            const complaints = await res.json();
            ledgerTableBody.innerHTML = '';

            complaints.forEach(c => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 dark:hover:bg-slate-900/60 transition';

                const statusBadge = {
                    'Submitted': '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">Submitted</span>',
                    'Assigned': '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-200">Assigned</span>',
                    'In Progress': '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-200">In Progress</span>',
                    'Work Verified': '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-200">Work Verified</span>',
                    'Resolved': '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-100 text-teal-800 dark:bg-teal-950 dark:text-teal-200">Resolved</span>'
                }[c.status] || `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-800">${c.status}</span>`;

                const officerDisplay = c.wardOfficer ? `<span class="font-medium text-slate-800 dark:text-slate-200">${c.wardOfficer}</span>` : '<span class="text-slate-400">Ward Officer</span>';

                tr.innerHTML = `
                    <td class="p-3.5 font-bold font-mono text-slate-900 dark:text-white">${c.trackingId}</td>
                    <td class="p-3.5 capitalize text-slate-700 dark:text-slate-300">${c.issue}</td>
                    <td class="p-3.5 text-slate-700 dark:text-slate-300">${c.ward} · ${c.wardName} (${c.zone})</td>
                    <td class="p-3.5 text-slate-700 dark:text-slate-300">${officerDisplay}</td>
                    <td class="p-3.5 text-slate-700 dark:text-slate-300">${c.department}</td>
                    <td class="p-3.5">${statusBadge}</td>
                    <td class="p-3.5 text-slate-400 text-[11px]">${c.filedAt.substring(0, 16).replace('T', ' ')}</td>
                    <td class="p-3.5">
                        <div class="flex items-center gap-1.5">
                            <button class="view-ticket-btn btn-capsule min-h-[30px] px-3 py-1 rounded-full bg-teal-700 hover:bg-teal-800 text-[11px] text-white font-semibold transition" data-id="${c.trackingId}">
                                Track
                            </button>
                            <a href="tel:${(c.wardContactPhone || '+917927551201').replace(/[^0-9+]/g, '')}" class="btn-capsule min-h-[30px] px-2.5 py-1 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-[11px] text-teal-700 dark:text-teal-300 font-semibold border border-slate-300 dark:border-slate-700 transition flex items-center gap-1" title="Call Ward Officer directly">
                                <i data-lucide="phone" class="w-3 h-3"></i>
                                <span class="hidden xl:inline">Call</span>
                            </a>
                        </div>
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
            lucide.createIcons();
        } catch (err) {
            ledgerTableBody.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-rose-600">Failed to load: ${err.message}</td></tr>`;
        }
    }

    if (btnRefreshLedger) {
        btnRefreshLedger.addEventListener('click', loadLedger);
    }

    // Reset Seed Data Button
    const btnResetSeed = document.getElementById('btn-reset-seed');
    if (btnResetSeed) {
        btnResetSeed.addEventListener('click', async () => {
            if (confirm('Reset AMC database back to initial seed data for a fresh judge demo?')) {
                try {
                    const res = await fetch('/api/admin/reset', { method: 'POST' });
                    const json = await res.json();
                    showNotificationToast(json.message);
                    loadLedger();
                } catch (err) {
                    alert(`Error resetting: ${err.message}`);
                }
            }
        });
    }

    // ==========================================
    // Ward Directory Modal & Population
    // ==========================================
    const btnOpenDir = document.getElementById('btn-open-directory');
    const modalDir = document.getElementById('modal-ward-directory');
    const btnCloseDir = document.getElementById('btn-close-directory-modal');
    const dirWardList = document.getElementById('directory-ward-list');

    async function loadWardDirectory() {
        if (!dirWardList) return;
        try {
            const res = await fetch('/api/wards');
            const wards = await res.json();
            dirWardList.innerHTML = '';

            wards.forEach(w => {
                const card = document.createElement('div');
                card.className = 'p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 space-y-2';

                const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(w.officeAddress || `${w.name} Ward Office AMC Ahmedabad`)}`;
                const cleanPhone = (w.contactPhone || '+91-79-2539-1811').replace(/[^0-9+]/g, '');

                card.innerHTML = `
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div>
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-slate-900 dark:text-white text-sm">Ward ${w.id} · ${w.name}</span>
                                <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-teal-50 dark:bg-teal-950 text-teal-800 dark:text-teal-300 border border-teal-200 dark:border-teal-800">${w.zone} Zone</span>
                            </div>
                            <div class="text-xs text-slate-600 dark:text-slate-300 mt-0.5">
                                <span class="font-semibold text-slate-800 dark:text-slate-100">${w.wardOfficer || 'AMC Ward Officer'}</span>
                                <span class="text-slate-400">·</span>
                                <span>${w.areas.slice(0, 4).join(', ')}</span>
                            </div>
                        </div>
                        <div class="flex items-center gap-2">
                            <a href="tel:${cleanPhone}" class="btn-capsule min-h-[34px] px-3.5 py-1 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-full flex items-center gap-1.5 transition">
                                <i data-lucide="phone" class="w-3.5 h-3.5"></i>
                                <span>Call: ${w.contactPhone}</span>
                            </a>
                            <a href="${mapsUrl}" target="_blank" rel="noopener noreferrer" class="btn-capsule min-h-[34px] px-3 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-200 text-xs font-semibold rounded-full border border-slate-300 dark:border-slate-700 flex items-center gap-1 transition">
                                <i data-lucide="map-pin" class="w-3.5 h-3.5 text-teal-700 dark:text-teal-400"></i>
                                <span>Office Map</span>
                            </a>
                        </div>
                    </div>
                    <div class="text-[11px] text-slate-500 flex items-center gap-1">
                        <i data-lucide="building" class="w-3 h-3 text-slate-400 flex-shrink-0"></i>
                        <span>${w.officeAddress || 'AMC Ward Office, Ahmedabad'}</span>
                    </div>
                `;
                dirWardList.appendChild(card);
            });
            lucide.createIcons();
        } catch (e) {
            if (dirWardList) dirWardList.innerHTML = `<div class="text-xs text-rose-600">Failed to load directory: ${e.message}</div>`;
        }
    }

    if (btnOpenDir) {
        btnOpenDir.addEventListener('click', () => {
            modalDir.classList.remove('hidden');
            loadWardDirectory();
        });
    }

    if (btnCloseDir) {
        btnCloseDir.addEventListener('click', () => {
            modalDir.classList.add('hidden');
        });
    }

    if (modalDir) {
        modalDir.addEventListener('click', (e) => {
            if (e.target === modalDir) {
                modalDir.classList.add('hidden');
            }
        });
    }

    // ==========================================
    // Chaos & Fault Injection Controller
    // ==========================================
    const btnToggleChaos = document.getElementById('btn-toggle-chaos');
    const chaosStatusText = document.getElementById('chaos-status-text');
    const chaosBoltIcon = document.getElementById('chaos-bolt-icon');
    const chaosFaultSelect = document.getElementById('chaos-fault-select');
    const chaosAlertBanner = document.getElementById('chaos-alert-banner');
    const chaosBannerTitle = document.getElementById('chaos-banner-title');
    const chaosBannerDesc = document.getElementById('chaos-banner-desc');
    const btnChaosInstantHeal = document.getElementById('btn-chaos-instant-heal');

    async function syncChaosUI() {
        try {
            const res = await fetch('/api/chaos');
            if (!res.ok) return;
            const status = await res.json();
            updateChaosUI(status);
        } catch (e) {
            console.warn('Chaos engine sync failed:', e);
        }
    }

    function updateChaosUI(status) {
        if (!status) return;

        if (status.enabled) {
            if (chaosStatusText) {
                chaosStatusText.innerText = 'ACTIVE';
                chaosStatusText.className = 'text-amber-300 uppercase font-mono font-bold text-[10px] animate-pulse';
            }
            if (btnToggleChaos) {
                btnToggleChaos.className = 'px-2 py-0.5 rounded-full font-bold transition flex items-center gap-1.5 bg-amber-900/90 text-amber-200 border border-amber-500/60 active:scale-95 text-[11px]';
            }
            if (chaosBoltIcon) {
                chaosBoltIcon.className = 'w-3 h-3 text-amber-300 animate-bounce';
            }

            if (chaosAlertBanner) {
                chaosAlertBanner.classList.remove('hidden');
            }
            if (chaosBannerTitle) {
                chaosBannerTitle.innerText = `${status.faultName} (${status.activeFault})`;
            }
            if (chaosBannerDesc) {
                chaosBannerDesc.innerText = `· ${status.description}`;
            }
        } else {
            if (chaosStatusText) {
                chaosStatusText.innerText = 'OFF';
                chaosStatusText.className = 'text-teal-300 uppercase font-mono font-bold text-[10px]';
            }
            if (btnToggleChaos) {
                btnToggleChaos.className = 'px-2 py-0.5 rounded-full font-semibold transition flex items-center gap-1.5 bg-teal-800/80 text-teal-100 hover:text-white active:scale-95 text-[11px]';
            }
            if (chaosBoltIcon) {
                chaosBoltIcon.className = 'w-3 h-3 text-amber-300';
            }

            if (chaosAlertBanner) {
                chaosAlertBanner.classList.add('hidden');
            }
        }

        if (chaosFaultSelect && status.activeFault) {
            chaosFaultSelect.value = status.activeFault;
        }
        lucide.createIcons();
    }

    if (btnToggleChaos) {
        btnToggleChaos.addEventListener('click', async () => {
            try {
                const res = await fetch('/api/chaos/toggle', { method: 'POST' });
                const updated = await res.json();
                updateChaosUI(updated);
            } catch (err) {
                alert(`Failed to toggle chaos: ${err.message}`);
            }
        });
    }

    if (chaosFaultSelect) {
        chaosFaultSelect.addEventListener('change', async () => {
            const chosenFault = chaosFaultSelect.value;
            try {
                const res = await fetch('/api/chaos/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ faultType: chosenFault })
                });
                const updated = await res.json();
                updateChaosUI(updated);
            } catch (err) {
                alert(`Failed to update fault type: ${err.message}`);
            }
        });
    }

    if (btnChaosInstantHeal) {
        btnChaosInstantHeal.addEventListener('click', async () => {
            try {
                const res = await fetch('/api/chaos/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ enabled: false })
                });
                const updated = await res.json();
                updateChaosUI(updated);
                showNotificationToast('Chaos Mode disabled. System returned to normal.');
            } catch (err) {
                alert(`Recovery failed: ${err.message}`);
            }
        });
    }

    // Call sync on startup
    syncChaosUI();
});

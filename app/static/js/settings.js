async function saveSettings() {
    const btn = document.getElementById('save-btn');
    const includeBodyweight = document.getElementById('include-bodyweight').checked;

    btn.disabled = true;
    btn.textContent = '⏳ Saving...';

    try {
        const res = await fetch('/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ include_bw: includeBodyweight })
        });

        const data = await res.json();
        if (data.success) {
            btn.textContent = '✅ Saved!';
            setTimeout(() => {
                btn.disabled = false;
                btn.textContent = 'Save Settings';
            }, 2000);
        } else {
            btn.textContent = '❌ Failed';
            setTimeout(() => {
                btn.disabled = false;
                btn.textContent = 'Save Settings';
            }, 2000);
        }
    } catch(e) {
        btn.textContent = '❌ Error';
        alert('Error: ' + e);
        setTimeout(() => {
            btn.disabled = false;
            btn.textContent = 'Save Settings';
        }, 2000);
    }
}

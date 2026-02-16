async function syncAll() {
    const btn = document.getElementById('sync-all-btn');
    btn.disabled = true;
    btn.textContent = '⏳ Syncing All...';
    try {
        const res = await fetch('/sync-all', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            btn.textContent = '✅ Synced!';
            setTimeout(() => location.reload(), 1000);
        } else {
            btn.textContent = '❌ Failed';
            alert(data.message);
            setTimeout(() => { btn.disabled = false; btn.textContent = '🔄 Sync All'; }, 2000);
        }
    } catch(e) {
        btn.textContent = '❌ Error';
        alert('Error: ' + e);
        setTimeout(() => { btn.disabled = false; btn.textContent = '🔄 Sync All'; }, 2000);
    }
}

async function syncLast() {
    const btn = document.getElementById('sync-last-btn');
    btn.disabled = true;
    btn.textContent = '⏳ Syncing...';
    try {
        const res = await fetch('/sync-last5', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            btn.textContent = '✅ Synced!';
            setTimeout(() => location.reload(), 1000);
        } else {
            btn.textContent = '❌ Failed';
            alert(data.message);
            setTimeout(() => { btn.disabled = false; btn.textContent = '🔄 Sync Last 5'; }, 2000);
        }
    } catch(e) {
        btn.textContent = '❌ Error';
        alert('Error: ' + e);
        setTimeout(() => { btn.disabled = false; btn.textContent = '🔄 Sync Last 5'; }, 2000);
    }
}

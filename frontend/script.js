document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('lead-form');
    const submitBtn = document.getElementById('submit-btn');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Update UI state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Triggering AI Call...';
        messageDiv.classList.add('hidden');

        const formData = new FormData(form);

        try {
            // Dynamically uses production URL or localhost depending on environment
            const apiBase = window.location.origin;
            const response = await fetch(`${apiBase}/api/lead`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.status === 'success') {
                showMessage('Success! Check your phone. The AI is calling now.', 'success');
                form.reset();
            } else {
                showMessage('Error: ' + result.message, 'error');
            }
        } catch (error) {
            console.error('Submission error:', error);
            showMessage('Something went wrong. Please check your connection and API keys.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Request AI Call';
        }
    });

    function showMessage(text, type) {
        messageDiv.textContent = text;
        messageDiv.className = type;
        messageDiv.classList.remove('hidden');
    }
});

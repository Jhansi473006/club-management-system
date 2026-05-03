async function loadSystemLogo() {
    try {
        const res = await fetch("http://127.0.0.1:8000/public/system-logo");
        if (res.ok) {
            const data = await res.json();
            if (data.logo_url) {
                const logoContainers = document.querySelectorAll('.logo');
                logoContainers.forEach(container => {
                    // Extract existing text structure (might have SVG or text)
                    // We will just replace it cleanly with the college logo, but keep 'ClubHub' as fallback or secondary text.
                    // Or since it's the college system, replacing the ClubHub logo SVG makes sense.
                    
                    const spanText = container.textContent.trim().replace('ADMIN HUB', '').replace('LEADER HUB', '').replace('STUDENT HUB', '').trim();
                    let extraText = '';
                    if(container.innerHTML.includes('ADMIN HUB')) extraText = '<span style="font-size: 0.8rem; color: var(--accent); margin-left:1rem;">ADMIN HUB</span>';
                    if(container.innerHTML.includes('LEADER HUB')) extraText = '<span style="font-size: 0.8rem; color: var(--accent); margin-left:1rem;">LEADER HUB</span>';
                    if(container.innerHTML.includes('STUDENT HUB')) extraText = '<span style="font-size: 0.8rem; color: var(--accent); margin-left:1rem;">STUDENT HUB</span>';

                    let imageUrl = data.logo_url;
                    if (imageUrl && imageUrl.startsWith('/')) {
                        imageUrl = 'http://127.0.0.1:8000' + imageUrl;
                    }

                    container.innerHTML = `
                        <img src="${imageUrl}" alt="College Logo" style="height: 64px; width: auto; max-width: 200px; object-fit: contain; margin-right: 1rem; border-radius: 8px;">
                        <span style="font-size: 1.25rem;">${spanText}</span> ${extraText}
                    `;
                    container.style.display = 'flex';
                    container.style.alignItems = 'center';
                });
            }
        }
    } catch (e) {
        console.error("Failed to load global logo", e);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadSystemLogo();
    injectGlobalHeader();
});

function parseJwtGlobal(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

function globalLogout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

function injectGlobalHeader() {
    const token = localStorage.getItem('token');
    
    // Look for a designated auth-buttons container, or create one in the header
    let authButtonsContainer = document.querySelector('.auth-buttons');
    if (!authButtonsContainer) {
        // Try to find the right-side div in the header to replace its content
        const header = document.querySelector('header');
        if (header) {
            const rightDiv = header.querySelector('div:last-child');
            if (rightDiv && rightDiv !== header.querySelector('.logo')) {
                rightDiv.classList.add('auth-buttons');
                authButtonsContainer = rightDiv;
            }
        }
    }

    if (token && authButtonsContainer) {
        const payload = parseJwtGlobal(token);
        const nameInitial = payload && payload.sub ? payload.sub.charAt(0).toUpperCase() : 'U';
        
        let dashboardLink = 'dashboard.html';
        if (payload && payload.role === 'admin') dashboardLink = 'admin_dashboard.html';
        else if (payload && payload.role === 'leader') dashboardLink = 'leader_dashboard.html';
        else if (payload && payload.role === 'student') dashboardLink = 'student_dashboard.html';

        const isDashboardOrProfile = window.location.pathname.includes('dashboard') || window.location.pathname.includes('profile');
        
        authButtonsContainer.innerHTML = `
            <a href="index.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500; margin-right: 1.5rem;">Home</a>
            ${!isDashboardOrProfile ? `<a href="${dashboardLink}" class="btn btn-outline" style="margin-right: 0.5rem; text-decoration: none;">Dashboard</a>` : ''}
            <div class="profile-dropdown">
                <button class="profile-btn">${nameInitial}</button>
                <div class="dropdown-menu">
                    <a href="profile.html" class="dropdown-item" style="text-decoration:none;">Edit Profile</a>
                    <button onclick="globalLogout()" class="dropdown-item" style="color: #ef4444; width:100%; text-align:left;">Logout</button>
                </div>
            </div>
        `;
        authButtonsContainer.style.display = 'flex';
        authButtonsContainer.style.alignItems = 'center';
    }
}

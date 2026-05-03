const API_BASE_URL = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', () => {
    fetchClubs();
    fetchEvents();
    fetchAnnouncements();
});

async function fetchClubs() {
    const container = document.getElementById('clubs-container');
    if (!container) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/public/clubs-slideshow`);
        const clubs = await response.json();
        
        container.innerHTML = '';
        
        if (clubs.length === 0) {
            container.innerHTML = '<div class="loading">No clubs available yet.</div>';
            return;
        }

        clubs.forEach(club => {
            let logo = club.logo_url;
            if (!logo || logo === 'null') {
                logo = `https://ui-avatars.com/api/?name=${encodeURIComponent(club.name)}&size=150&background=random`;
            } else if (logo.startsWith('/')) {
                logo = API_BASE_URL + logo;
            }
            
            const item = document.createElement('div');
            item.className = 'list-item';
            item.style.cursor = 'pointer';
            item.onclick = () => window.location.href = `club.html?id=${club.id}`;
            
            item.innerHTML = `
                <img src="${logo}" alt="${club.name}" class="item-img">
                <div class="item-content">
                    <h3 class="item-title">${club.name}</h3>
                    <p class="item-desc">${club.description || 'No description provided.'}</p>
                </div>
            `;
            container.appendChild(item);
        });
    } catch (error) {
        console.error('Error fetching clubs:', error);
        container.innerHTML = '<div class="loading" style="color: #ef4444;">Failed to load clubs.</div>';
    }
}

async function fetchEvents() {
    const container = document.getElementById('events-container');
    if (!container) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/public/events-slideshow`);
        const events = await response.json();
        
        container.innerHTML = '';

        if (events.length === 0) {
            container.innerHTML = '<div class="loading">No upcoming events.</div>';
            return;
        }

        events.forEach(event => {
            const dateObj = new Date(event.date);
            const month = dateObj.toLocaleString('default', { month: 'short' });
            const day = dateObj.getDate();
            
            const item = document.createElement('div');
            item.className = 'list-item';
            item.style.cursor = 'pointer';
            item.onclick = () => window.location.href = `event.html?id=${event.id}`;
            
            item.innerHTML = `
                <div class="date-box">
                    <span class="date-month">${month}</span>
                    <span class="date-day">${day}</span>
                </div>
                <div class="item-content">
                    <h3 class="item-title">${event.title}</h3>
                    <p class="item-desc">${event.location || 'College Campus'}</p>
                </div>
            `;
            container.appendChild(item);
        });

    } catch (error) {
        console.error('Error fetching events:', error);
        container.innerHTML = '<div class="loading" style="color: #ef4444;">Failed to load events.</div>';
    }
}

async function fetchAnnouncements() {
    const container = document.getElementById('announcements-container');
    if (!container) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/public/announcements`);
        const announcements = await response.json();
        
        container.innerHTML = '';
        if (announcements.length === 0) {
            container.innerHTML = '<div class="loading">No announcements.</div>';
            return;
        }

        announcements.forEach((ann, index) => {
            const isLatest = index === 0;
            const item = document.createElement('div');
            item.className = 'list-item';
            item.style.cursor = 'pointer';
            item.onclick = () => window.location.href = `announcement.html?id=${ann.id}`;
            
            item.innerHTML = `
                <div class="item-content">
                    <h3 class="item-title" style="display:flex; justify-content:space-between;">
                        <span>${ann.title}</span>
                        ${isLatest ? '<span style="font-size:0.7rem; background:var(--primary); color:white; padding:0.1rem 0.4rem; border-radius:12px; margin-left:0.5rem; height:fit-content;">New</span>' : ''}
                    </h3>
                    <p class="item-desc" style="margin-bottom: 0.5rem;">${ann.content}</p>
                    <small style="color: var(--primary); font-weight: 500;">${ann.club_name}</small>
                </div>
            `;
            container.appendChild(item);
        });

    } catch (error) {
        console.error('Error fetching announcements:', error);
        container.innerHTML = '<div class="loading" style="color: #ef4444;">Failed to load announcements.</div>';
    }
}

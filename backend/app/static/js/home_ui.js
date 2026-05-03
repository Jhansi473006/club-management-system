async function loadClubs() {
    let container = document.getElementById("clubsContainer")
    container.innerHTML = "<p>Loading...</p>"

    try {
        let res = await fetch("/clubs")
        let data = await res.json()

        container.innerHTML = ""

        if (data.length === 0) {
            container.innerHTML = "<p>No clubs available</p>"
            return
        }

        data.forEach(c => {
            container.innerHTML += `
            <div class="col-md-4">
                <div class="card shadow-sm">
                    <img src="/uploads/${c.logo}">
                    <div class="card-body">
                        <h5>${c.name}</h5>
                        <p>${c.description || ""}</p>
                        <button class="btn btn-primary w-100">
                            Join Club
                        </button>
                    </div>
                </div>
            </div>`
        })

    } catch (err) {
        container.innerHTML = "<p>Error loading clubs</p>"
    }
}


async function loadEvents() {
    let container = document.getElementById("eventsContainer")
    container.innerHTML = "<p>Loading...</p>"

    try {
        let res = await fetch("/events")
        let data = await res.json()

        container.innerHTML = ""

        if (data.length === 0) {
            container.innerHTML = "<p>No events available</p>"
            return
        }

        data.forEach(e => {
            container.innerHTML += `
            <div class="col-md-4">
                <div class="card shadow-sm">
                    <img src="/uploads/${e.image}">
                    <div class="card-body">
                        <h5>${e.title}</h5>
                        <p>${e.date}</p>
                        <button class="btn btn-success w-100">
                            Register
                        </button>
                    </div>
                </div>
            </div>`
        })

    } catch (err) {
        container.innerHTML = "<p>Error loading events</p>"
    }
}


loadClubs()
loadEvents()
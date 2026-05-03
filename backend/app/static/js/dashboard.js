async function loadEvents() {

    try {

        let res = await fetch("/events")

        if (!res.ok) {
            console.log("Events API error")
            return
        }

        let events = await res.json()

        let slider = document.getElementById("sliderContent")

        if (!events.length) {
            slider.innerHTML = "<p>No events available</p>"
            return
        }

        slider.innerHTML = ""

        events.forEach((event, index) => {

            let image = event.poster ? event.poster : "uploads/default.png"

            slider.innerHTML += `

<div class="carousel-item ${index == 0 ? 'active' : ''}">

<img src="http://127.0.0.1:8000/${image}" class="d-block w-100">

<div class="carousel-caption bg-dark bg-opacity-50 rounded p-2">

<h5>${event.title || "No Title"}</h5>
<p>${event.date || ""}</p>

<button class="btn btn-primary">Register</button>

</div>

</div>

`

        })

    } catch (err) {
        console.log("Event error:", err)
    }

}


async function loadClubs() {

    try {

        let res = await fetch("/clubs")

        if (!res.ok) {
            console.log("Clubs API error")
            return
        }

        let clubs = await res.json()

        let container = document.getElementById("clubList")

        if (!clubs.length) {
            container.innerHTML = "<p>No clubs available</p>"
            return
        }

        container.innerHTML = ""

        clubs.forEach(club => {

            container.innerHTML += `

<div class="col-md-4 mb-3">

<div class="card p-3 text-center">

<h5>${club.club_name || "Club"}</h5>

<p>${club.description || ""}</p>

<button class="btn btn-primary">Join</button>
<button class="btn btn-outline-dark mt-2">Coordinator</button>

</div>

</div>

`

        })

    } catch (err) {
        console.log("Club error:", err)
    }

}


loadEvents()
loadClubs()
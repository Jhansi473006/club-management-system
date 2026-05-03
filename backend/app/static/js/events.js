async function loadEvents() {

    let res = await fetch("/events")
    let events = await res.json()

    let container = document.getElementById("eventList")
    container.innerHTML = ""

    events.forEach(event => {

        container.innerHTML += `

<div class="col-md-4 mb-3">

<div class="card p-3">

<img src="http://127.0.0.1:8000/${event.poster}" 
style="height:200px;object-fit:cover;border-radius:10px">

<h5 class="mt-2">${event.title}</h5>
<p>${event.date}</p>

<button id="reg-${event.event_id}" 
onclick="registerEvent(${event.event_id})" 
class="btn btn-primary w-100">
Register
</button>

<button id="vol-${event.event_id}" 
onclick="applyVolunteer(${event.event_id})" 
class="btn btn-outline-dark w-100 mt-2">
Volunteer
</button>

</div>

</div>

`

    })

}


async function registerEvent(event_id) {

    let student_id = localStorage.getItem("user_id")
    let btn = document.getElementById(`reg-${event_id}`)

    let res = await fetch("/events/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event_id, student_id })
    })

    if (res.ok) {
        btn.innerText = "Registered"
        btn.disabled = true
    } else {
        btn.innerText = "Already Registered"
        btn.disabled = true
    }

}


async function applyVolunteer(event_id) {

    let student_id = localStorage.getItem("user_id")
    let btn = document.getElementById(`vol-${event_id}`)

    let res = await fetch("/events/volunteer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event_id, student_id })
    })

    if (res.ok) {
        btn.innerText = "Applied"
        btn.disabled = true
    } else {
        btn.innerText = "Already Applied"
        btn.disabled = true
    }

}


loadEvents()
async function loadClubs() {

    let res = await fetch("/clubs")
    let clubs = await res.json()

    let container = document.getElementById("clubList")
    container.innerHTML = ""

    clubs.forEach(club => {

        container.innerHTML += `

<div class="col-md-4 mb-3">

<div class="card p-3 text-center">

<h5>${club.club_name}</h5>
<p>${club.description}</p>

<button id="join-${club.club_id}" 
onclick="joinClub(${club.club_id})" 
class="btn btn-primary w-100">
Join
</button>

<button id="coord-${club.club_id}" 
onclick="applyCoordinator(${club.club_id})" 
class="btn btn-outline-dark w-100 mt-2">
Coordinator
</button>

</div>

</div>

`

    })

}


async function joinClub(club_id) {

    let student_id = localStorage.getItem("user_id")
    let btn = document.getElementById(`join-${club_id}`)

    let res = await fetch("/clubs/request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ club_id, student_id })
    })

    if (res.ok) {
        btn.innerText = "Requested"
        btn.disabled = true
    } else {
        btn.innerText = "Already Requested"
        btn.disabled = true
    }

}


async function applyCoordinator(club_id) {

    let student_id = localStorage.getItem("user_id")
    let btn = document.getElementById(`coord-${club_id}`)

    let res = await fetch("/clubs/coordinator/apply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ club_id, student_id })
    })

    if (res.ok) {
        btn.innerText = "Applied"
        btn.disabled = true
    } else {
        btn.innerText = "Already Applied"
        btn.disabled = true
    }

}


loadClubs()
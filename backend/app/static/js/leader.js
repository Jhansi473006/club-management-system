// ================= REQUESTS =================
async function loadRequests() {

    let container = document.getElementById("requestsList")
    if (!container) return   // ✅ prevent crash

    container.innerHTML = "<p>Loading...</p>"

    try {
        let res = await fetch("/clubs/requests")
        let requests = await res.json()

        container.innerHTML = ""

        if (!Array.isArray(requests) || requests.length === 0) {
            container.innerHTML = "<p>No pending requests</p>"
            return
        }

        requests.forEach(req => {
            container.innerHTML += `
            <div class="col-md-4 mb-3">
                <div class="card p-3">

                    <h5>Student ID: ${req.student_id}</h5>
                    <p>Club ID: ${req.club_id}</p>

                    <button onclick="approve(${req.request_id})" class="btn btn-success w-100">
                        Approve
                    </button>

                    <button onclick="reject(${req.request_id})" class="btn btn-danger w-100 mt-2">
                        Reject
                    </button>

                </div>
            </div>
            `
        })

    } catch (err) {
        container.innerHTML = "<p>Error loading requests</p>"
        console.error(err)
    }
}


async function approve(id) {
    if (!confirm("Approve this request?")) return

    await fetch(`/clubs/approve/${id}`, { method: "POST" })
    alert("Approved ✅")
    loadRequests()
}


async function reject(id) {
    if (!confirm("Reject this request?")) return

    await fetch(`/clubs/reject/${id}`, { method: "POST" })
    alert("Rejected ❌")
    loadRequests()
}


// ================= COORDINATORS =================
async function loadCoordinators() {

    let container = document.getElementById("coordinatorList")
    if (!container) return   // ✅ prevent crash

    container.innerHTML = "<p>Loading...</p>"

    try {
        let res = await fetch("/clubs/coordinator/requests")
        let data = await res.json()

        container.innerHTML = ""

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = "<p>No coordinator requests</p>"
            return
        }

        data.forEach(req => {
            container.innerHTML += `
            <div class="col-md-4 mb-3">
                <div class="card p-3">

                    <h5>Student ID: ${req.student_id}</h5>

                    <button onclick="approveCoord(${req.application_id})" class="btn btn-success w-100">
                        Approve
                    </button>

                </div>
            </div>
            `
        })

    } catch (err) {
        container.innerHTML = "<p>Error loading coordinators</p>"
        console.error(err)
    }
}


async function approveCoord(id) {
    if (!confirm("Approve coordinator?")) return

    await fetch(`/clubs/coordinator/approve/${id}`, { method: "POST" })
    alert("Coordinator Approved 🎉")
    loadCoordinators()
}


// ================= CREATE EVENT =================
async function createEvent() {
    if(!myClubId) { alert("Club info not loaded!"); return; }

    let title = document.getElementById("title")?.value
    let description = document.getElementById("eventDesc")?.value
    let date = document.getElementById("date")?.value
    let location = document.getElementById("location")?.value

    if (!title || !date) {
        alert("Title and Date are required")
        return
    }

    try {
        await fetch("/events/create", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("token")
            },
            body: JSON.stringify({
                club_id: myClubId,
                title,
                description,
                date,
                location
            })
        })

        alert("Event Created 🎉")

    } catch (err) {
        alert("Error creating event")
        console.error(err)
    }
}


// ================= SAVE CLUB =================
async function saveClub() {
    if(!myClubId) { alert("Club info not loaded!"); return; }

    let formData = new FormData()

    formData.append("club_id", myClubId)
    formData.append("club_name", document.getElementById("clubName").value)
    formData.append("description", document.getElementById("description").value)

    let logo = document.getElementById("logo").files[0]
    if (logo) formData.append("logo", logo)

    let res = await fetch("/save_club", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: formData
    })

    if(res.ok) {
        alert("Saved successfully")
    } else {
        alert("Error saving club")
    }
}


// ================= AUTO LOAD =================
let myClubId = null;

async function initLeader() {
    let leaderId = localStorage.getItem("user_id");
    if (!leaderId) {
        window.location.href = "/login";
        return;
    }
    
    try {
        let res = await fetch(`/clubs/leader/${leaderId}`);
        if(res.ok) {
            let data = await res.json();
            myClubId = data.club_id;
            document.getElementById("clubName").value = data.name || "";
            document.getElementById("description").value = data.description || "";
        }
    } catch (e) { console.error(e); }
    
    loadRequests();
    loadCoordinators();
}

initLeader();
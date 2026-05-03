async function login() {

    let email = document.getElementById("email").value
    let password = document.getElementById("password").value

    let res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })

    let data = await res.json()

    if (res.ok) {

        localStorage.setItem("token", data.access_token)
        localStorage.setItem("user_id", data.user_id)
        localStorage.setItem("role", data.role)

        if (data.role === "student") {
            window.location.href = "/student_dashboard"
        } else {
            window.location.href = "/leader_dashboard"
        }

    } else {
        alert("Invalid credentials")
    }
}
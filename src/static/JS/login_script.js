document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.forms["login-form"];
    

    loginForm.addEventListener("submit", async (event) => {
        if (!loginForm.checkValidity()) {
            return;
        }
        event.preventDefault();
        
        const formData = new FormData(loginForm);

        const fetchData = await fetch("/login", {
            method: "POST",
            body: formData
        })
        const jsonFetchData = await fetchData.json()

        if (fetchData.status == 200) {
            location.href = `${location.origin}/`;
        } else {
            alert(jsonFetchData.msg)
        }

    });
});
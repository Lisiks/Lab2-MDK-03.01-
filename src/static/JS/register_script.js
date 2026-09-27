document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.forms["register-form"];

    registerForm.addEventListener("submit", async (event) => {
        if (!registerForm.checkValidity()) {
            return;
        }
        event.preventDefault();

        const formData = new FormData(registerForm);

        const fetchData = await fetch("/register", {
            method: "POST",
            body: formData
        })
        const jsonFetchData = await fetchData.json()

        if (fetchData.status == 201) {
            location.href = `${location.origin}/`;;
        } else {
            alert(jsonFetchData.msg)
        }

    });
});
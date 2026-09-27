

document.addEventListener("DOMContentLoaded", () => {
    const pageInput = document.forms["pagination-form"].page;

    const lastPageButton = document.getElementById("last-page-button");
    const nextPageButton = document.getElementById("next-page-button");

    lastPageButton.addEventListener("click", () => {
        pageInput.value = Number(pageInput.value) > 1 ? Number(pageInput.value) - 1 : pageInput.value;
    });

    nextPageButton.addEventListener("click", () => {
        pageInput.value = Number(pageInput.value) + 1;
    });

});
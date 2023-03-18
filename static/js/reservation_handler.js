//document.getElementById("reservation_form").addEventListener("submit", handleFormValues);

function handleFormValues(event) {
    const submit_button = $("#reservation_form").querySelector('input[type="submit"]');
    console.log(submit_button.id);
    if (submit_button.id === "deleteSubmit") {
        event.preventDefault();

        const formData = new FormData();
        formData.append('id', $("#reservation_id").value);
        formData.append('teacher', $("#teacher_id").value);

        return fetch('/reservations/delete', {
            method: 'POST',
            body: formData
        })
    }
}

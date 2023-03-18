document.getElementById("search_form").addEventListener("submit", handleFormValues);
const classroom_element = document.getElementById('classroom_id');
const equipment_checkboxes = document.getElementById('equipment_id');

classroom_element.addEventListener('input', () => {
    if (classroom_element.value !== "") {
        const inputs = equipment_checkboxes.querySelectorAll('input[type="checkbox"]');
        for (const checkbox of inputs) {
            if (checkbox.checked) {
                checkbox.checked = false;
            }
        }
    }
    equipment_checkboxes.disabled = classroom_element.value !== "";
});
equipment_checkboxes.addEventListener('input', () => {
    const inputs = equipment_checkboxes.querySelectorAll('input[type="checkbox"]');
    for (const checkbox of inputs) {
        if (checkbox.checked) {
            classroom_element.value = "";
            classroom_element.disabled = true;
            return;
        }
    }
    classroom_element.disabled = false;
});


function handleFormValues(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const lesson_element = document.getElementById('lesson_id');
    //validacia ci je zadana ucebna alebo hodina
    if (classroom_element.disabled && formData.get("lesson") === "") {
        lesson_element.setCustomValidity("Nezadaná hodina!")
        lesson_element.reportValidity();
        return
    }
    if (formData.get("classroom") === "" && formData.get("lesson") === "") {
        classroom_element.setCustomValidity("Nezadaná učebňa ani hodina!")
        classroom_element.reportValidity();
        return
    }
    if (formData.get("classroom") === "") {
        formData.delete('classroom');
    }
    if (formData.get("lesson") === "") {
        formData.delete('lesson');
    }

    const params = new URLSearchParams(formData);
    window.location.href = `/search/?${params.toString()}`;

}

document.getElementById("search_form").addEventListener("submit", handleFormValues);
function createReservation(event){
    const lesson = event.target.getAttribute('lesson');
    const date = event.target.getAttribute('date');
    const classroom = event.target.getAttribute('classroom');
    const formData = new FormData();
    formData.append("date", date);
    formData.append("lesson", lesson);
    formData.append("classroom", classroom);
    const params = new URLSearchParams(formData);
    window.location.href = `/reservations/create/?${params.toString()}`;
    return false;
}
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
    const classroomInput = document.getElementById('classroom_id');
    const formData = new FormData(event.target);
    //validacia ci je zadana ucebna alebo hodina
    if (formData.get("classroom") === "" && formData.get("lesson") === "") {
        classroomInput.setCustomValidity("Nezadaná učebňa ani hodina!")
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

document.getElementById("search_form").addEventListener("submit", myF);

function myF(event) {
    console.log(event);
    const room = document.getElementById("classroom");
    const interactive_board = document.getElementById("inter_board");

    console.log(interactive_board.innerText);

    //event.preventDefault();
}

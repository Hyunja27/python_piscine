window.addEventListener("keydown", (event) => {
  if (event.key == "ArrowUp") {
    return document.getElementById("up").click();
  }
  if (event.key == "ArrowDown") {
    return document.getElementById("down").click();
  }
  if (event.key == "ArrowLeft") {
    return document.getElementById("left").click();
  }
  if (event.key == "ArrowRight") {
    return document.getElementById("right").click();
  }
  if (event.key == "A" || event.key == "a") {
    return document.getElementById("A").click();
  }
  if (event.key == "S" || event.key == "s") {
    return document.getElementById("B").click();
  }
  if (event.key == "Enter") {
    return document.getElementById("Select").click();
  }
  if (event.key == " ") {
    return document.getElementById("Start").click();
  }
});

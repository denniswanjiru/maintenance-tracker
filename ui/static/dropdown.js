const toggleDropdown = document.querySelector("#filters").classList;
const dropdownBtn = document.querySelector(".btn--dropdown");

dropdownBtn.addEventListener("click", () => {
  if (toggleDropdown.contains("hidden")) {
    toggleDropdown.replace("hidden", "dropdown__content");
  } else {
    toggleDropdown.replace("dropdown__content", "hidden");
  }
});

window.addEventListener("click", e => {
  if (!e.target.matches(".btn--dropdown")) {
    toggleDropdown.remove("dropdown__content");
    toggleDropdown.add("hidden");
  }
});

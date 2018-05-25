const chevron = document.querySelector("#filter-icon");
const filterClasses = document.querySelector("#filters").classList;
const sortClasses = document.querySelector("#sort").classList;
const sortBtn = document.querySelector("#sort-btn");
const filterBtn = document.querySelector("#filter-btn");

const toggleDropdown = searchType => {
  if (searchType.contains("hidden")) {
    searchType.replace("hidden", "dropdown__content");
  } else {
    searchType.replace("dropdown__content", "hidden");
  }
};

filterBtn.addEventListener("click", () => toggleDropdown(filterClasses));
sortBtn.addEventListener("click", () => toggleDropdown(sortClasses));

chevron.addEventListener("click", () => toggleDropdown());

window.addEventListener("click", e => {
  if (
    !e.target.matches(".btn--dropdown")
  ) {
    filterClasses.remove("dropdown__content");
    filterClasses.add("hidden");
    sortClasses.remove("dropdown__content");
    sortClasses.add("hidden");
  }
});

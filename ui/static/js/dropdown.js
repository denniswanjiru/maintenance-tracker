const signoutClasses = document.querySelector("#signout").classList;
const filterClasses = document.querySelector("#filters").classList;
const sortClasses = document.querySelector("#sort").classList;
const sortBtn = document.querySelector("#sort-btn");
const signoutBtn = document.querySelector("#signout-btn");
const filterBtn = document.querySelector("#filter-btn");

const toggleDropdown = searchType => {
  if (searchType.contains("hidden")) {
    searchType.replace("hidden", "dropdown__content");

    if (searchType === signoutClasses) {
      searchType.add("dropdown--signout");
    }
  } else {
    searchType.replace("dropdown__content", "hidden");

    if (searchType === signoutClasses) {
      searchType.remove("dropdown--signout");
    }
  }
};

filterBtn.addEventListener("click", () => toggleDropdown(filterClasses));
sortBtn.addEventListener("click", () => toggleDropdown(sortClasses));
signoutBtn.addEventListener("click", () => toggleDropdown(signoutClasses));

window.addEventListener("click", e => {
  if (!e.target.matches(".btn--dropdown")) {
    filterClasses.remove("dropdown__content");
    filterClasses.add("hidden");
    sortClasses.remove("dropdown__content");
    sortClasses.add("hidden");
  }
});

const searchBtn = document.getElementById("search-btn");
const searchInputClasses = document.getElementById("user-input-search")
  .classList;

searchBtn.addEventListener("click", () => {
  if (searchInputClasses.contains("hidden")) {
    searchInputClasses.replace("hidden", "show");
  } else {
    searchInputClasses.replace("show", "hidden");
  }
});

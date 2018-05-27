const hamburger = document.getElementById("hamburger");
const mobileNav = document.getElementById("mobile-nav").classList;
const body = document.querySelector("body").classList;

hamburger.addEventListener("click", () => {
  if (mobileNav.contains("hidden")) {
    mobileNav.replace("hidden", "show-on-mobile");
    body.add("no-overflow");
  } else {
    mobileNav.replace("show-on-mobile", "hidden");
    body.remove("no-overflow");
  }
});

const approveBtn = document.getElementById("approve");
const rejectBtn = document.getElementById("reject");
const resolveBtn = document.getElementById("resolve");

approveBtn.addEventListener("click", () => {
  approveBtn.classList.add("hidden");
  rejectBtn.classList.add("hidden");
  resolveBtn.classList.replace("hidden", "show");
});

rejectBtn.addEventListener("click", () => {
  approveBtn.classList.add("hidden");
  rejectBtn.setAttribute("disabled", "disabled");
});

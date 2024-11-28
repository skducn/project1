let follow = true;
const section = document.querySelector("section");
const form = document.querySelector("form");
const username = document.querySelector("#username");
const passwword = document.querySelector("#password");
const forgot = document.querySelector(".forgot a");
const button = document.querySelector("button");
const signup = document.querySelector(".signup a");

function disableFollow() {
  follow = false;
  section.style = "";
}

function allowFollow() {
  follow = true;
}

const interactiveElements = document.querySelectorAll("section input, section button, section a");
interactiveElements.forEach(el => {
  el.addEventListener("focus", disableFollow);
  el.addEventListener("blur", allowFollow);
});

section.addEventListener("mousemove", function(e) {
  if (follow) {
    const top = section.getBoundingClientRect().top;
    const left = section.getBoundingClientRect().left;
    const height = section.getBoundingClientRect().height;
    const width = section.getBoundingClientRect().width;
    
    
    const percentage = 
    // section.style = `--x:${35 * (-0.30 + (e.clientX - top) / height)};--y:${20 * (0.7 - (e.clientY - top) / height)};`;
    section.style = `--x:${35 * (e.clientX - left) / width};--y:${-20 * (e.clientY - top) / height};`;
  }
});
section.addEventListener("mouseleave", disableFollow);
section.addEventListener("mouseenter", allowFollow);


document.querySelector("input[type='checkbox']").addEventListener("input", function() {
  password.type = password.type === "password" ? "text" : "password";
})
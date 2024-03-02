document.addEventListener("DOMContentLoaded", function() {
    let circles = document.getElementsByClassName("circle")
    for (let i = 0; i < circles.length; i++) {
        let circle = circles[i];
        let randomRed = Math.floor(Math.random() * 256); // 0부터 255까지의 랜덤한 수
        let randomGreen = Math.floor(Math.random() * 256);
        let randomBlue = Math.floor(Math.random() * 256);
        let randomColor = "rgb(" + randomRed + ", " + randomGreen + ", " + randomBlue + ")";
        circle.style.backgroundColor = randomColor
    }
});
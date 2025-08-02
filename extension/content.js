
(function () {
    if (document.getElementById("floatingCaptions")) return;


    let captionBox = document.createElement("div");
    captionBox.id = "floatingCaptions";

    document.body.appendChild(captionBox);

    let offsetX, offsetY, isDragging = false;

    captionBox.addEventListener("mousedown", (e) => {
        isDragging = true;
        offsetX = e.clientX - captionBox.offsetLeft;
        offsetY = e.clientY - captionBox.offsetTop;
        captionBox.style.cursor = "grabbing";
    });

    document.addEventListener("mousemove", (e) => {
        if (isDragging) {
            captionBox.style.left = `${e.clientX - offsetX}px`;
            captionBox.style.top = `${e.clientY - offsetY}px`;
        }
    });

    document.addEventListener("mouseup", () => {
        isDragging = false;
        captionBox.style.cursor = "grab";
    });

    setInterval(() => {
        let captions = document.querySelector(".ytp-caption-segment");
        let text = captions ? captions.innerText.trim() : "";

        if (text !== "") {
            captionBox.innerText = text;
            captionBox.style.opacity = "1";
        }
    }, 100);
})();

let style = document.createElement("link");
style.rel = "stylesheet";
style.href = browser.runtime.getURL("styles.css");
document.head.appendChild(style);

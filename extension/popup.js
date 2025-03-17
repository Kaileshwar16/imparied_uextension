
document.addEventListener("DOMContentLoaded", () => {
    const captionDisplay = document.getElementById("captions");
    let lastCaption = "";  // Store last visible caption

    browser.runtime.onMessage.addListener((message) => {
        if (message.action === "update_captions") {
            if (message.captions.trim() !== "") {
                lastCaption = message.captions;  // Update when new text appears
            }
            captionDisplay.innerText = lastCaption;  // Always show last valid caption
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const emotions = ["happy", "calm", "sad", "worried", "frustrated", "angry"];
    const colors = {
        "happy": "#FFEEA8",
        "calm": "#D5E386",
        "sad": "#D9E8F5",
        "worried": "#D9D9D9",
        "frustrated": "#F2BDC7",
        "angry": "#ff9c78"
    };

    emotions.forEach(emotion => {
        const element = document.getElementById(`${emotion}-gif`);
        element.addEventListener('mouseenter', function() {
            document.body.style.backgroundColor = colors[emotion];
        });
        element.addEventListener('mouseleave', function() {
            document.body.style.backgroundColor = ''; // Reset to default
        });
    });
});

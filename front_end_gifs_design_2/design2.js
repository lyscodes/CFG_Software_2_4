document.addEventListener("DOMContentLoaded", function() {
    const happy = document.getElementById('happy-gif');
    const calm = document.getElementById('calm-gif');
    const sad = document.getElementById('sad-gif');
    const worried = document.getElementById('worried-gif');
    const frustrated = document.getElementById('frustrated-gif');
    const angry = document.getElementById('angry-gif');

    function changeColors(backgroundColor) {
        document.body.style.backgroundColor = backgroundColor;
    }

    function resetColors() {
        document.body.style.backgroundColor = ''; // Reset to default
    }

    happy.addEventListener('mouseenter', function() {
        changeColors('#FFEEA8');
    });
    happy.addEventListener('mouseleave', resetColors);

    calm.addEventListener('mouseenter', function() {
        changeColors('#D5E386');
    });
    calm.addEventListener('mouseleave', resetColors);

    sad.addEventListener('mouseenter', function() {
        changeColors('#D9E8F5');
    });
    sad.addEventListener('mouseleave', resetColors);

    worried.addEventListener('mouseenter', function() {
        changeColors('#D9D9D9');
    });
    worried.addEventListener('mouseleave', resetColors);

    frustrated.addEventListener('mouseenter', function() {
        changeColors('#F2BDC7');
    });
    frustrated.addEventListener('mouseleave', resetColors);

    angry.addEventListener('mouseenter', function() {
        changeColors('#ff9c78');
    });
    angry.addEventListener('mouseleave', resetColors);
});


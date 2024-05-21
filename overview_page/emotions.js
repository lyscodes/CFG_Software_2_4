
// Function to generate dummy data for average emotions
function generateDummyData() {
    return [
        { name: 'happy', value: Math.floor(Math.random() * 100) + 1 },
        { name: 'calm', value: Math.floor(Math.random() * 100) + 1 },
        { name: 'sad', value: Math.floor(Math.random() * 100) + 1 },
        { name: 'worried', value: Math.floor(Math.random() * 100) + 1 },
        { name: 'frustrated', value: Math.floor(Math.random() * 100) + 1 },
        { name: 'angry', value: Math.floor(Math.random() * 100) + 1 }
    ];
}

// Function to render the bar graph
function renderGraph(emotionsData) {
    const barsContainer = document.getElementById('bars');
    barsContainer.innerHTML = ''; // Clear any existing bars

    emotionsData.forEach(emotion => {
        const bar = document.createElement('div');
        bar.className = 'bar';
        bar.style.height = `${emotion.value * 2}px`; // Adjust height multiplier as needed

        const barValue = document.createElement('div');
        barValue.className = 'bar-value';
        barValue.innerText = emotion.value;

        bar.appendChild(barValue);
        barsContainer.appendChild(bar);
    });
}

// Generate dummy data and render the graph
const emotionsData = generateDummyData();
renderGraph(emotionsData);

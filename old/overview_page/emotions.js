
// Function to generate dummy data for average emotions
function generateDummyData() {
    return [

        { name: 'happy', {{ graph['happy']}} },
        { name: 'calm', {{ graph['happy']}} },
        { name: 'sad', {{ graph['happy']}} },
        { name: 'worried', {{ graph['happy']}} },
        { name: 'frustrated', {{ graph['happy']}} },
        { name: 'angry', {{ graph['happy']}} }
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

document.addEventListener('DOMContentLoaded', () => {
    const daysContainer = document.getElementById('days');
    const monthYearDisplay = document.getElementById('monthYear');
    const prevMonthButton = document.getElementById('prevMonth');
    const nextMonthButton = document.getElementById('nextMonth');
    const statsTitle = document.querySelector('.stats p');

    let currentDate = new Date();

    function renderCalendar() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        // Get the first day of the month and the total number of days in the month
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Set the month and year in the header
        monthYearDisplay.textContent = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

        // Update the stats title
        statsTitle.textContent = `STATS FOR ${monthYearDisplay.textContent.toUpperCase()}`;

        // Clear the previous days
        daysContainer.innerHTML = '';

        // Fill in the days of the month
        // Add empty divs for the days of the week before the start of the month
        for (let i = 0; i < firstDayOfMonth; i++) {
            const emptyDiv = document.createElement('div');
            emptyDiv.classList.add('empty');
            daysContainer.appendChild(emptyDiv);
        }

        // Add the actual days of the month
        //Fake link
        for (let day = 1; day <= daysInMonth; day++) {
            const dayDiv = document.createElement('div');
            const link = document.createElement('a');
            link.textContent = day;
            link.href = `/journal/${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            dayDiv.appendChild(link);
            daysContainer.appendChild(dayDiv);
        }
    }

    function changeMonth(delta) {
        currentDate.setMonth(currentDate.getMonth() + delta);
        renderCalendar();
    }

    prevMonthButton.addEventListener('click', () => changeMonth(-1));
    nextMonthButton.addEventListener('click', () => changeMonth(1));

    renderCalendar();
});

// Stats Calendar - changes when you move the month

document.addEventListener('DOMContentLoaded', () => {
    // Function to generate dummy data for average emotions per month
    function generateMonthlyDummyData() {
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        const monthlyData = [];

        months.forEach(month => {
            const monthData = {
                month: month,
                emotionsData: [
                    { name: 'happy', value: Math.floor(Math.random() * 100) + 1 },
                    { name: 'calm', value: Math.floor(Math.random() * 100) + 1 },
                    { name: 'sad', value: Math.floor(Math.random() * 100) + 1 },
                    { name: 'worried', value: Math.floor(Math.random() * 100) + 1 },
                    { name: 'frustrated', value: Math.floor(Math.random() * 100) + 1 },
                    { name: 'angry', value: Math.floor(Math.random() * 100) + 1 }
                ]
            };
            monthlyData.push(monthData);
        });

        return monthlyData;
    }

    // Function to render the bar graph for average emotions
    function renderMonthlyGraph(monthlyData, currentMonthIndex) {
        const barsContainer = document.getElementById('bars');
        barsContainer.innerHTML = ''; // Clear any existing bars

        // Find the data for the current month
        const currentMonthData = monthlyData[currentMonthIndex];

        // Render the graph for the current month
        currentMonthData.emotionsData.forEach(emotion => {
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

    // Generate dummy data for average emotions per month
    const monthlyData = generateMonthlyDummyData();

    // Keep track of the currently displayed month
    let currentMonthIndex = (new Date()).getMonth(); // Initialize with the current month

    // Function to show the previous month
    function showPrevMonth() {
        currentMonthIndex = (currentMonthIndex - 1 + 12) % 12; // Ensure the result is a positive number in the range [0, 11]
        renderMonthlyGraph(monthlyData, currentMonthIndex);
        updateMonthYearDisplay();
    }

    // Function to show the next month
    function showNextMonth() {
        currentMonthIndex = (currentMonthIndex + 1) % 12; // Ensure the result is in the range [0, 11]
        renderMonthlyGraph(monthlyData, currentMonthIndex);
        updateMonthYearDisplay();
    }

    // Function to update the month and year display
    function updateMonthYearDisplay() {
        document.getElementById('monthYear').textContent = monthlyData[currentMonthIndex].month + ' ' + (new Date()).getFullYear();
        // Update the stats title
        statsTitle.textContent = `STATS FOR ${monthlyData[currentMonthIndex].month.toUpperCase()} ${monthYearDisplay.textContent.split(' ')[1]}`;
    }

    // Add event listeners for navigation buttons
    document.getElementById('prevMonth').addEventListener('click', showPrevMonth);
    document.getElementById('nextMonth').addEventListener('click', showNextMonth);

    // Render the initial graph
    renderMonthlyGraph(monthlyData, currentMonthIndex);
    updateMonthYearDisplay();
});

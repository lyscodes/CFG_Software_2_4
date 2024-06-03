document.addEventListener('DOMContentLoaded', () => {
    const daysContainer = document.getElementById('days');
    const monthYearDisplay = document.getElementById('monthYear');
    const prevMonthButton = document.getElementById('prevMonth');
    const nextMonthButton = document.getElementById('nextMonth');

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
        statsTitle.textContent = `${monthYearDisplay.textContent.toUpperCase()} STATS`;

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
                year: year
            }),
            success: function(data) {
                // Update the calendar and stats based on the fetched data
                // Implement logic to update the UI with the fetched data
                console.log(data); // Just for testing, replace with actual logic
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
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

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
        for (let day = 1; day <= daysInMonth; day++) {
            const dayDiv = document.createElement('div');
            const link = document.createElement('a');
            link.textContent = day;
            link.href = `/archive/${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            dayDiv.appendChild(link);
            daysContainer.appendChild(dayDiv);
        }
    }

    function renderGraph() {
        $(document).ready(function(){
        $.ajax({
          data : {
            month : currentDate
          },
          type : 'POST',
          url : '/overview'})
        .done (function(data){
        theChart.data.datasets[0].data = data.output;
        theChart.options.title.text = data.label;
        theChart.update();
            });
        e.preventDefault();
        });
    };

    function changeMonth(delta) {
        currentDate.setMonth(currentDate.getMonth() + delta);
        renderCalendar();
        renderGraph();
    }

    prevMonthButton.addEventListener('click', () => changeMonth(-1));
    nextMonthButton.addEventListener('click', () => changeMonth(1));

    renderCalendar();

    renderGraph();

    // Initial AJAX request for the current month
    fetchDataForMonthYear(currentDate.getMonth() + 1, currentDate.getFullYear());

    // Bind form submission to fetch data
    $('#form').on('submit', function(e) {
        e.preventDefault();
        const selectedMonth = new Date($('#month').val());
        fetchDataForMonthYear(selectedMonth.getMonth() + 1, selectedMonth.getFullYear());
    });
});

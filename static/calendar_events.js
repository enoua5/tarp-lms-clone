// Function creates calendar on load.
     document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth'
        });

        // Parse the json into a Javascript object.
        let courses = JSON.parse("{{json_list|escapejs}}");

        // Loop through the lists and create event objects
        let length = courses.course_name.length;
        for (let i = 0; i < length; i++)
        {
            // Get the days that the class occurs and place in days array.
            let days = [];
            let days_string = courses.course_days[i];
            if (days_string.includes("M"))
            {
                days.push("1");
            }
            if (days_string.includes("T"))
            {
                days.push("2");
            }
            if (days_string.includes('W'))
            {
                days.push('3');
            }
            if (days_string.includes('Th'))
            {
                days.push('4');
            }
            if (days_string.includes('F'))
            {
                days.push('5');
            }

            // Create the event object. Year is hard coded for now.
            e = {
                id: 'a',
                title: courses.course_name[i],
                daysOfWeek: days,
                startRecur: "2022-09-01",
                endRecur: "2022-12-31"
            };

            // Add the event.
            calendar.addEvent(e);
        }

        // Render the calendar.
        calendar.render();
     });
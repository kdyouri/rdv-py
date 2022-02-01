var calendar = null;

$(function() {
    calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
        headerToolbar: {
            left: 'title',
            center: '',
            right: 'prev,next today'
        },
        initialView: 'timeGridWeek',
        locale: 'fr',
        timeZone: 'UTC',
        selectable: true,
        businessHours: [{
            daysOfWeek: [ 1, 2, 3, 4, 5 ],
            startTime: '09:00',
            endTime: '13:00',
        }, {
            daysOfWeek: [ 1, 2, 3, 4, 5 ],
            startTime: '14:00',
            endTime: '18:00',
        }, {
            daysOfWeek: [ 6 ],
            startTime: '09:00',
            endTime: '13:00',
        }],
        allDaySlot: false,
        nowIndicator: true,
        events: '/rendezvous/feed',
        displayEventTime: false,
        eventClick: function(info) {
            Xcrud.showDialog([], {'url' : '/rendezvous/edit/' + info.event.id})
        },
        select: function(info) {
            Xcrud.showDialog([], {'url' : '/rendezvous/add?start=' + info.start.toISOString() + '&end=' + info.end.toISOString()})
        }
    });
    calendar.render();
});

$(document).on('content.updated', '.xcrud-modal', function(){
    calendar.refetchEvents();
});
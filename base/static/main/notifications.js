(()=>{
var UPDATING_NOTIFICATIONS = true;
const NOTIFICATION_REQ_PERIOD = 10000; // 10 seconds
const NOTIF_MAX_CONSEQ_FAILS = 3;
var NOTIFICATION_FAIL_COUNT = 0;
var notification_update_timeout = undefined;
var notification_count = undefined;

function get_notifications()
{
    let REQUEST_URL = new URL('data', location.origin);
    REQUEST_URL.search = new URLSearchParams({command: 'get_mine', item_type: 'notification'});

    fetch(REQUEST_URL).then(
        resp => {
            if(resp.ok)
                return resp.json();
            else
                NOTIFICATION_FAIL_COUNT ++;
                if(NOTIFICATION_FAIL_COUNT < NOTIF_MAX_CONSEQ_FAILS)
                    setTimeout(get_notifications, NOTIFICATION_REQ_PERIOD);


                throw "Error getting notifications: server responded with code"+resp.status
        }
    )
    .then(
        data => {
            let dropdown = document.getElementById('notification-dropdown')
            dropdown.innerHTML = "";

            let prev_notif_count = notification_count;
            notification_count = data.items.length;

            let bellIcon = document.getElementById('notification-icon')
            if(prev_notif_count != undefined && notification_count > prev_notif_count)
            {
                bellIcon.classList.remove('no-notif');
                bellIcon.classList.add('yes-notif');
            }
            else
            {
                bellIcon.classList.remove('yes-notif');
                bellIcon.classList.add('no-notif');
            }

            if(notification_count == 0)
            {
                let dropdown_item =  document.createElement('div');
                dropdown_item.classList.add("dropdown-item", "alert", "alert-info");
                dropdown_item.innerText = "No notifications yet!";
                dropdown.append(dropdown_item);
            }
            else
            {

                let dropdown_item =  document.createElement('div');
                dropdown_item.classList.add("dropdown-item", "btn", "btn-danger");
                dropdown_item.onclick = (e) => {
                    clearNotif();
                }
                dropdown_item.innerText = "Clear all notifications"
                dropdown.append(dropdown_item)
            }

            for(let notice of data.items)
            {
                let dropdown_item =  document.createElement('div');
                dropdown_item.classList.add("dropdown-item");

                let div = document.createElement('div');
                div.classList.add("row");
                dropdown_item.appendChild(div)
                
                let class_name = notice.course_department + " " + notice.course_num;
                //let cn_box = document.createElement('div');
                //cn_box.innerText = class_name;
                //cn_box.classList.add("col-sm-2");
                //div.append(cn_box);

                let text_box = document.createElement('div');
                let notification_text = `Assignment "${notice.assignment_name}" ${notice.event_note}`;
                text_box.innerText = `${class_name}: ${notification_text}`;
                text_box.classList.add("col-sm-11");
                div.append(text_box);
                text_box.onclick = (e)=>{
                    navigateToAssignmentID(notice.course_id, notice.assignment_id);
                }

                let delete_button = document.createElement("a");
                delete_button.innerText = "X"
                delete_button.classList.add("col-sm-1", "btn", "btn-danger");
                delete_button.onmouseover = (e)=>{e.stopPropagation()}
                delete_button.onclick = (e)=> {
                    e.stopPropagation();
                    delete_notification(notice.id);
                }
                div.append(delete_button)
                



                dropdown.appendChild(dropdown_item);
            }

            NOTIFICATION_FAIL_COUNT = 0;

            if(UPDATING_NOTIFICATIONS)
                setTimeout(get_notifications, NOTIFICATION_REQ_PERIOD);
        }
    )
}

notification_update_timeout = setTimeout(get_notifications, 0);

function navigateToAssignmentID(course_id, assignment_id)
{
    location.replace(`/courses/${course_id}/${assignment_id}`);
}

function delete_notification(id)
{
    let REQUEST_URL = new URL('data', location.origin);
    REQUEST_URL.search = new URLSearchParams({command: 'delete', item_type: 'notification', id:id});
    fetch(REQUEST_URL).then(
        resp=>{
            if(resp.status == 202)
            {
                clearTimeout(notification_update_timeout);
                setTimeout(get_notifications, 0);
            }
        }
    );

    notification_count--;
}

function clearNotif()
{
    let REQUEST_URL = new URL('data', location.origin);
    REQUEST_URL.search = new URLSearchParams({command: 'delete_all', item_type: 'notification'});
    fetch(REQUEST_URL).then(
        resp=>{
            if(resp.status == 202)
            {
                clearTimeout(notification_update_timeout);
                setTimeout(get_notifications, 0);
            }
        }
    );

    notification_count=0;
}
})();

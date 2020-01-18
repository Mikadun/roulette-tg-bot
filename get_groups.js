
all_groups = new Set();
stop = false;

function get_all_groups() {
    let iters = 0;
    function add_current_groups() {
        if (stop) {
            
        }

        li = document.getElementsByTagName('li');
        for (let i = 0; i < li.length; i++) {
            all_groups.add(li[i]);
        }
        iters++;

        if (iters % 50 == 0) {
            console.log(unic_li);
        }
    }

    setInterval(add_current_groups, 200);
}

get_all_groups();
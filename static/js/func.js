function show_action_list(value) {
    var idList = ["action-list-1", "action-list-2", "action-list-3", "action-list-4", "action-list-5", "action-list-6"]

    for (i = 0; i < idList.length; i++) {
        if (value == idList[i]) {
            document.getElementById(idList[i]).style.display = "block";
        }
        else {
            document.getElementById(idList[i]).style.display = "none";
        }
    }
}


function select_by(target, parent_value) {
    var _target = "#" + target;
    $(_target).prop('selectedIndex', 0);
    $(_target + ">option").each(function () {
        var attr = $(this).attr('selected');
        if (typeof attr !== typeof undefined && attr !== false) {
            $(this).removeAttr('selected')
        }
        if ($(this).attr('data-parent-id') != parent_value) {
            $(this).hide()
        } else {
            $(this).show()
        }
    })
}

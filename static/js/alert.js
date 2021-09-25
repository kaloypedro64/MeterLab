
function msgAlert(header, remarks, ico)
{
    if (ico == 1) icon = 'fal fa-save fa-lg';
    if (ico == 2) icon = 'fas fa-pencil-alt fa-lg';
    if (ico == 3) icon = 'fal fa-trash-alt fa-lg';
    $(document).Toasts('create', {
        class: 'bg-white',
        title: '<span style="font-size: 12px;"> ' + header + ' </span>',
        subtitle: '<a href="" class="nav-link" id="">reserved!</a>',
        position: 'bottomRight',
        icon: icon,
        body: '<div class="col-md-9 row" style="width: 300px"><span style="font-size:13px;">' + remarks + '</span></div>',
        autohide: true,
        delay: 10000,
    });
};